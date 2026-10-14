# Claim Checker

Extracts factual claims from text, searches Wikipedia for evidence, and gives a
verdict for each claim. Works with English and Hindi/Hinglish text.

Inspired by the idea behind a hackathon project on live spoken-claim verification.
This is an independent, text-first implementation.

## How it works

1. **extractor.py**: Gemini splits text into single-idea claims and labels each as
   fact, opinion or prediction. The character position is computed in Python.
2. **evidence.py**: searches English or Hindi Wikipedia for evidence.
3. **verdict.py**: Gemini writes a short search query, reads the evidence, and returns
   `supported`, `contradicted` or `insufficient_evidence` with a one-line reason.
   Responses are cached locally. Retries and model fallback handle 429/503 errors.

Only facts are verified. Opinions and predictions are skipped.

## Setup

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

Copy `.env.example` to `.env` and add your Gemini API key.

    python extractor.py
    python verdict.py

## Results on my test set

- Claim extraction: 6/6 correct on 6 hand-written test texts (`test_texts.py`).
  This is a small set written by me, not a benchmark.
- "India has over 1.4 billion people" -> supported
- Claims about an unnamed startup -> insufficient_evidence
- Hindi population claim -> insufficient_evidence (likely because the Hindi Wikipedia
  intro uses older figures)

## Limitations

- Only the intro paragraph of Wikipedia pages is used, so specific numbers are often missing.
- Search returns something even when it is irrelevant, so the verdict step must judge relevance.
- Free-tier Gemini models are sometimes busy, which slows runs.
- This is a learning project, not a replacement for professional fact-checking.

## Next steps

- Harder test cases (questions, quotes, "some people say...")
- A simple web UI
- More evidence sources
