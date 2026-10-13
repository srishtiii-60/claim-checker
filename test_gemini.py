import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for name in ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash"]:
    try:
        r = client.models.generate_content(
            model=name,
            contents="Say hello in one short sentence.",
        )
        print(name, "->", r.text.strip())
    except Exception as e:
        print(name, "-> ERROR:", str(e)[:150])