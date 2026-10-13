import os
import json
import time
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

from test_texts import TEST_TEXTS, EXPECTED

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),
)
MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash"]


class ExtractedClaim(BaseModel):
    original_text: str
    normalized_claim: str
    statement_type: str  # "fact", "opinion" ya "prediction"
    language: str        # "en", "hi" ya "hinglish"


PROMPT = """You extract claims from text.

Rules:
- Split compound sentences into separate, single-idea claims.
- original_text must be copied EXACTLY from the input, word for word.
- normalized_claim is a short, clear, standalone version (same language as the input).
- statement_type is one of:
  - "fact": a checkable statement about the world (numbers, events, states)
  - "opinion": a personal judgement or feeling
  - "prediction": a statement about the future
- language is "en", "hi" or "hinglish".
- Do not add claims that are not in the text.

Text:
{text}
"""


def extract_claims(text, retries=6):
    raw = None
    for attempt in range(retries):
        model = MODELS[attempt % len(MODELS)]
        try:
            response = client.models.generate_content(
                model=model,
                contents=PROMPT.format(text=text),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=list[ExtractedClaim],
                    temperature=0,
                ),
            )
            raw = json.loads(response.text)
            break
        except Exception as e:
            wait = 4 * (attempt + 1)
            print(f"  (retry {attempt + 1}, {model}) {str(e)[:50]} - waiting {wait}s")
            time.sleep(wait)

    if raw is None:
        return []

    claims = []
    for i, item in enumerate(raw, start=1):
        claims.append({
            "id": f"c{i}",
            "original_text": item["original_text"],
            "normalized_claim": item["normalized_claim"],
            "statement_type": item["statement_type"].lower(),
            "position": text.find(item["original_text"]),
            "context": text,
            "language": item["language"],
        })
    return claims


if __name__ == "__main__":
    results = []
    passed = 0
    for i, text in enumerate(TEST_TEXTS):
        claims = extract_claims(text)
        got = [c["statement_type"].upper() for c in claims]
        expected = [t for t, _ in EXPECTED[i]]
        ok = got == expected
        passed += ok
        print(f"Text {i + 1}: {'PASS' if ok else 'FAIL'}  expected={expected} got={got}")
        results.append({"text": text, "expected": expected, "got": got, "claims": claims, "pass": ok})

    print(f"\n{passed}/{len(TEST_TEXTS)} passed")
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)