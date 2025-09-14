import os
import shutil
import argostranslate.package
import argostranslate.translate

# Directory to store Argos models
MODEL_DIR = "models"

# Only allow these language pairs (en → target)
ALLOWED_TARGET_LANGS = ['fr', 'hi', 'zh', 'ru', 'es']
SOURCE_LANG = 'en'

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Clear existing models
print("Removing existing translation models...")
for filename in os.listdir(MODEL_DIR):
    file_path = os.path.join(MODEL_DIR, filename)
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)

# Get available packages
print("Fetching available Argos Translate packages...")
available_packages = argostranslate.package.get_available_packages()
selected_packages = [
    pkg for pkg in available_packages
    if pkg.from_code == SOURCE_LANG and pkg.to_code in ALLOWED_TARGET_LANGS
]

print(f"Found {len(selected_packages)} matching translation packages.")

# Download and install selected packages
for pkg in selected_packages:
    print(f"Downloading {pkg.from_code} → {pkg.to_code} package...")
    package_path = pkg.download()
    print(f"Installing {pkg.from_code} → {pkg.to_code} package...")
    argostranslate.package.install_from_path(package_path)

# Load installed packages
argostranslate.translate.load_installed_languages()

print("\n✅ Only selected translation models are now installed.")
