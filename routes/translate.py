from fastapi import APIRouter
import google.generativeai as genai
import os

router = APIRouter()

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")


@router.post("/translate")
def translate_text(data: dict):
    text = data.get("text")
    target_lang = data.get("target_lang", "English")

    prompt = f"Translate the following text to {target_lang}: {text}"

    response = model.generate_content(prompt)

    return {
        "translated_text": response.text
    }
