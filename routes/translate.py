from fastapi import APIRouter
import google.generativeai as genai
import os

router = APIRouter()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


@router.post("/translate")
def translate_text(data: dict):
    texts = data.get("texts")   # list of texts
    target_lang = data.get("target_lang", "English")

    if not texts:
        return {"translated": []}

    prompt = f"""
You are a strict translator.

Translate each sentence into {target_lang}.
Rules:
- Return ONLY translated text
- Do NOT add explanations
- Keep same order
- Output as plain list

Texts:
{texts}
"""

    response = model.generate_content(prompt)

    # Split output into list safely
    output = response.text.strip().split("\n")

    # Clean numbering if model adds (1., 2., etc.)
    cleaned = [line.split(".", 1)[-1].strip() for line in output]

    return {"translated": cleaned}
