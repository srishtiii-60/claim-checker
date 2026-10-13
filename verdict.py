import os
import json
import time
import hashlib
from pydantic import BaseModel
from google.genai import types

from extractor import client, MODELS
from evidence import search_wikipedia

CACHE_FILE = "cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}


class SearchQuery(BaseModel):
    query: str


class Verdict(BaseModel):
    verdict: str        # "supported", "contradicted" ya "insufficient_evidence"
    reason: str
    source_title: str


QUERY_PROMPT = """Write a short Wikipedia search query (2 to 6 keywords) that would find
evidence for the claim below. Use the same language as the claim.

Claim: {claim}
"""

VERDICT_PROMPT = """You are a careful fact-checker. Use ONLY the evidence below.

- "supported": the evidence clearly confirms the claim.
- "contradicted": the evidence clearly disagrees with the claim.
- "insufficient_evidence": the evidence does not directly mention the claim's specific
  facts or numbers, or is about something else. When unsure, choose this.

reason: one short sentence in the same language as the claim.
source_title: the title of the evidence you used, or an empty string.

Claim: {claim}

Evidence:
{evidence}
"""


def ask_json(prompt, schema, retries=6):
    key = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if key in cache:
        return cache[key]
    for attempt in range(retries):
        model = MODELS[attempt % len(MODELS)]
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0,
                ),
            )
            data = json.loads(response.text)
            cache[key] = data
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            return data
        except Exception as e:
            wait = 4 * (attempt + 1)
            print(f"  (retry {attempt + 1}, {model}) {str(e)[:50]} - waiting {wait}s")
            time.sleep(wait)
    return None


def check_claim(claim):
    lang = "hi" if claim["language"] == "hi" else "en"
    text = claim["normalized_claim"]

    q = ask_json(QUERY_PROMPT.format(claim=text), SearchQuery)
    query = q["query"] if q else text

    found = search_wikipedia(query, limit=3, lang=lang)
    if not found:
        return {"query": query, "verdict": "insufficient_evidence",
                "reason": "No results found.", "source_title": ""}

    evidence = "\n\n".join(f"[{r['title']}] {r['extract'][:600]}" for r in found)
    v = ask_json(VERDICT_PROMPT.format(claim=text, evidence=evidence), Verdict)
    if v is None:
        return {"query": query, "verdict": "error",
                "reason": "Model unavailable.", "source_title": ""}
    v["query"] = query
    return v


if __name__ == "__main__":
    with open("results.json", encoding="utf-8") as f:
        results = json.load(f)

    output = []
    for entry in results:
        for claim in entry["claims"]:
            if claim["statement_type"] != "fact":
                continue
            v = check_claim(claim)
            print(f"\nCLAIM: {claim['normalized_claim']}")
            print(f"  query:   {v['query']}")
            print(f"  verdict: {v['verdict']}")
            print(f"  reason:  {v['reason']}")
            output.append({"claim": claim["normalized_claim"], **v})

    with open("verdicts.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)