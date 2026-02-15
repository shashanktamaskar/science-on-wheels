"""Regenerate specific collages with EXIF orientation fix."""
import os
import sys
import zipfile
import tempfile
import shutil
from PIL import Image, ImageOps

# Add AI-Collage-Tool to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'AI-Collage-Tool'))
from collage_generator_final import create_collage_with_header, get_best_photos

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_BASE = r"D:\OneDrive_2026-02-15\20.01.2026 to 11.02.2026"
GALLERY_DIR = os.path.join(SCRIPT_DIR, "gallery_school_collage")
LOGO_PATH = os.path.join(SCRIPT_DIR, '..', 'AI-Collage-Tool', 'plaksha_logo.png')

# Collages to regenerate
collages_to_fix = [
    {
        'name': 'GHS-KAILE-WANDER-RMSA',
        'zip': os.path.join(ZIP_BASE, '28.01.2026', 'GHS KAILE WANDER (RMSA).zip'),
        'district': 'Bathinda',
        'date': 'January 28, 2026',
    },
    {
        'name': 'GSSS-PATTI-KALA-MEHRAJ-BOYS',
        'zip': os.path.join(ZIP_BASE, '23.01.2026', 'GSSS PATTI KALA MEHRAJ BOYS.zip'),
        'district': 'Bathinda',
        'date': 'January 23, 2026',
    },
]

def extract_and_fix_orientation(zip_path, temp_dir):
    """Extract images from zip and fix EXIF orientation."""
    image_paths = []
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for name in zf.namelist():
            if name.lower().endswith(('.jpg', '.jpeg', '.png')) and not name.startswith('__MACOSX'):
                zf.extract(name, temp_dir)
                img_path = os.path.join(temp_dir, name)
                
                # Fix EXIF orientation
                try:
                    img = Image.open(img_path)
                    img = ImageOps.exif_transpose(img)
                    img.save(img_path)
                    image_paths.append(img_path)
                except Exception as e:
                    print(f"  Warning: Could not process {name}: {e}")
    
    return image_paths

def main():
    for collage in collages_to_fix:
        print(f"\nRegenerating: {collage['name']}")
        print(f"  Zip: {collage['zip']}")
        
        if not os.path.exists(collage['zip']):
            print(f"  ERROR: Zip not found!")
            continue
        
        output_path = os.path.join(GALLERY_DIR, f"{collage['name']}.jpg")
        
        # Extract to temp dir with EXIF fix
        temp_dir = tempfile.mkdtemp()
        try:
            image_paths = extract_and_fix_orientation(collage['zip'], temp_dir)
            print(f"  Found {len(image_paths)} images (EXIF-fixed)")
            
            if len(image_paths) < 6:
                print(f"  WARNING: Only {len(image_paths)} images, need at least 6")
                if len(image_paths) == 0:
                    continue
            
            logo = LOGO_PATH if os.path.exists(LOGO_PATH) else None
            
            # Select best photos using AI
            selected = get_best_photos(
                image_paths, logo,
                collage['name'], collage['district'], collage['date'],
                count=6, model_name='gemini-3-pro-image-preview'
            )
            
            # Create collage
            create_collage_with_header(
                selected, output_path,
                collage['name'], collage['district'], collage['date'],
                logo, grid_layout=(3, 2), target_size=(540, 405)
            )
            
            print(f"  OK: Saved to {output_path}")
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\nDone!")

if __name__ == '__main__':
    main()
