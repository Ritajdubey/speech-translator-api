import argostranslate.package
import argostranslate.translate
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# List of target languages (English is source)
TARGET_LANGS = ['fr', 'hi', 'zh', 'ru', 'es']

def install_language_packages():
    print("Checking and installing required language packages...")
    available_packages = argostranslate.package.get_available_packages()
    
    # Get installed packages instead of languages
    installed_packages = argostranslate.package.get_installed_packages()
    installed_pairs = {(pkg.from_code, pkg.to_code) for pkg in installed_packages}

    for to_code in TARGET_LANGS:
        if ('en', to_code) not in installed_pairs:
            package_to_install = next(
                (pkg for pkg in available_packages if pkg.from_code == 'en' and pkg.to_code == to_code),
                None
            )
            if package_to_install:
                print(f"Installing package: en → {to_code} ...")
                package_to_install.install()
            else:
                print(f"Package not found for en → {to_code}")

    print("Language packages installation complete.")

# Install language packages at startup
install_language_packages()

class TranslateRequest(BaseModel):
    text: str
    to_lang: str  # target language code

@app.post("/translate")
def translate_text(request: TranslateRequest):
    installed_languages = argostranslate.translate.load_installed_languages()
    
    from_lang = next((lang for lang in installed_languages if lang.code == "en"), None)
    to_lang = next((lang for lang in installed_languages if lang.code == request.to_lang), None)
    
    if not from_lang:
        return {"error": "Source language 'en' not installed."}
    if not to_lang:
        return {"error": f"Target language '{request.to_lang}' not installed or supported."}
    
    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(request.text)
    return {"translated_text": translated_text}

@app.get("/")
def root():
    return {"message": "Translator API is running. Source language fixed as English."}
