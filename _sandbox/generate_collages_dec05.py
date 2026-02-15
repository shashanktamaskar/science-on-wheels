"""
Generate collages for December 5, 2025
"""
import os, sys, zipfile, tempfile, shutil, glob

sys.path.insert(0, os.path.abspath("../../AI-Collage-Tool"))
from collage_generator_final import setup_gemini, get_best_photos, create_collage_with_header, rate_collage, parse_grid_layout
from api_key import API_KEY

LOGO = os.path.abspath("../../AI-Collage-Tool/science_on_wheels_logo.png")
OUTPUT_DIR = os.path.abspath("../gallery_school_collage")
GRID = "3x2"
TARGET_SCORE = 8.0
MAX_RETRIES = 3
MODEL = "gemini-2.0-flash-exp"

SCHOOLS = [
    {
        "zip_path": r"D:\PATIALA _GSSS_TRIPURI.zip",
        "name": "GSSS TRIPURI",
        "location": "Patiala",
        "date": "December 05, 2025",
        "output": "GSSS-TRIPURI.jpg"
    },
    {
        "zip_path": r"C:\Users\lenovo\OneDrive - Plaksha University\Desktop\temp\PATIALA_GSSS_KALYAN.zip",
        "name": "GSSS KALYAN",
        "location": "Patiala",
        "date": "December 05, 2025",
        "output": "GSSS-KALYAN.jpg"
    },
    {
        "zip_path": r"D:\PATIALA_GSSS_MULTIPURPOSE.zip",
        "name": "GSSS MULTIPURPOSE",
        "location": "Patiala",
        "date": "December 05, 2025",
        "output": "GSSS-MULTIPURPOSE.jpg"
    }
]

def extract_zip(zip_path):
    temp_dir = tempfile.mkdtemp()
    print(f"📦 Extracting {os.path.basename(zip_path)}...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)
    for root, dirs, files in os.walk(temp_dir):
        if any(f.lower().endswith(('.jpg', '.jpeg', '.png')) for f in files):
            return root
    return temp_dir

def generate_collage(school):
    print(f"\n{'='*60}")
    print(f"🎨 {school['name']}")
    print(f"{'='*60}")
    
    if not os.path.exists(school['zip_path']):
        print(f"❌ Zip not found: {school['zip_path']}")
        return False
    
    images_folder = extract_zip(school['zip_path'])
    images = glob.glob(os.path.join(images_folder, "*.jpg")) + \
             glob.glob(os.path.join(images_folder, "*.JPG")) + \
             glob.glob(os.path.join(images_folder, "*.jpeg")) + \
             glob.glob(os.path.join(images_folder, "*.png"))
    
    print(f"✅ Found {len(images)} images")
    
    if len(images) < 6:
        print("❌ Need at least 6 images")
        shutil.rmtree(images_folder, ignore_errors=True)
        return False
    
    grid = parse_grid_layout(GRID)
    output_path = os.path.join(OUTPUT_DIR, school['output'])
    best_score = -1
    best_path = None
    
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n🔍 Attempt {attempt}/{MAX_RETRIES}")
        selected = get_best_photos(images, LOGO, school['name'], school['location'], 
                                   school['date'], count=6, model_name=MODEL)
        
        temp_output = output_path.replace('.jpg', f'_attempt{attempt}.jpg')
        create_collage_with_header(selected, temp_output, school['name'], school['location'],
                                   school['date'], LOGO, grid, (540, 405))
        
        rating, score = rate_collage(temp_output, LOGO, school['name'], school['location'],
                                     school['date'], MODEL)
        print(f"📊 Score: {score}/10")
        
        if score > best_score:
            best_score = score
            if best_path and os.path.exists(best_path):
                os.remove(best_path)
            best_path = temp_output
        else:
            if os.path.exists(temp_output):
                os.remove(temp_output)
        
        if score >= TARGET_SCORE:
            break
    
    if best_path:
        if os.path.exists(output_path):
            os.remove(output_path)
        os.rename(best_path, output_path)
        print(f"✅ Saved: {school['output']} (Score: {best_score}/10)")
    
    shutil.rmtree(images_folder, ignore_errors=True)
    return True

if __name__ == "__main__":
    setup_gemini(API_KEY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    success = 0
    for school in SCHOOLS:
        try:
            if generate_collage(school):
                success += 1
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print(f"✨ Generated {success}/{len(SCHOOLS)} collages")
    print(f"{'='*60}")
