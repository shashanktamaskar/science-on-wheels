import zipfile
import os

zip_path = r"C:\Users\lenovo\OneDrive - Plaksha University\Desktop\temp\Ludhiana_GSSS-KASABAAD.zip"
extract_to = "temp_images_retry"

os.makedirs(extract_to, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print(f"✅ Extracted to: {extract_to}")
print(f"Files: {len(os.listdir(extract_to))}")
