from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import argostranslate.translate

app = FastAPI(title="Speech Translator API")

# Load installed translation packages
argostranslate.translate.load_installed_languages()

# Supported target languages (source is always English)
SUPPORTED_LANGS = {
    "fr": "French",
    "hi": "Hindi",
    "zh": "Chinese",
    "ru": "Russian",
    "es": "Spanish"
}

class TranslationRequest(BaseModel):
    text: str
    target_lang: str

@app.get("/")
def root():
    return {"message": "Welcome to the Speech Translator API!"}

@app.get("/languages")
def get_supported_languages():
    return {"supported_target_languages": SUPPORTED_LANGS}

@app.post("/translate")
def translate_text(request: TranslationRequest):
    source_lang = "en"  # Always English
    target_lang = request.target_lang.lower()

    if target_lang not in SUPPORTED_LANGS:
        raise HTTPException(status_code=400, detail="Unsupported target language code.")

    # Get installed languages
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == source_lang), None)
    to_lang = next((lang for lang in installed_languages if lang.code == target_lang), None)

    if not from_lang or not to_lang:
        raise HTTPException(status_code=400, detail="Language model not installed.")

    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(request.text)

    return {
        "translated_text": translated_text,
        "target_language": SUPPORTED_LANGS[target_lang]
    }
