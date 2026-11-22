import os, mimetypes, time, requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema import Receipt

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_prompt(version="v1"):
    with open(f"prompts/{version}.txt", encoding="utf-8") as f:
        return f.read()

def load_image(source):
    if source.startswith("http"):
        r = requests.get(source, timeout=30)
        r.raise_for_status()
        mime = r.headers.get("Content-Type", "image/jpeg").split(";")[0]
        return r.content, mime
    mime = mimetypes.guess_type(source)[0] or "image/jpeg"
    with open(source, "rb") as f:
        return f.read(), mime

def extract(source, user_prompt="", version="v1", retries=5):
    data, mime = load_image(source)
    prompt = load_prompt(version)
    if user_prompt:
        prompt += "\nExtra instruction from user: " + user_prompt
    for attempt in range(retries):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=[types.Part.from_bytes(data=data, mime_type=mime), prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Receipt,
                    temperature=0,
                ),
            )
            return resp.parsed
        except Exception as e:
            if attempt == retries - 1:
                raise
            # Exponential backoff with multiplier to handle transient 503 / 429 rate limit errors
            time.sleep(2 ** attempt * 2)

if __name__ == "__main__":
    import sys
    result = extract(sys.argv[1])
    print(result.model_dump_json(indent=2))
