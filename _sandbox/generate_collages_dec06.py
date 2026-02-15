"""
Generate collages for December 6, 2025 school visits.
Schools: GSSS KANGANWAL, GSSS MULTIPURPOSE (Session 2), GSSS NANDPURKESHO
"""

import os
import sys
import zipfile
import tempfile
import shutil
import glob

# Add collage tool path
COLLAGE_TOOL_PATH = r'c:\Users\lenovo\OneDrive - Plaksha University\Plaksha\Work\Research\2025\Projects\Science_on_Wheels\AI-Collage-Tool'
sys.path.insert(0, COLLAGE_TOOL_PATH)

from collage_generator_final import setup_gemini, get_best_photos, create_collage_with_header, rate_collage
from api_key import API_KEY

# Setup Gemini with API key
setup_gemini(API_KEY)

# Logo path
LOGO_PATH = os.path.join(COLLAGE_TOOL_PATH, "science_on_wheels_logo.png")

# Define schools to process
schools = [
    {
        'zip': r'D:\MALERKOTLA_GSSS_KANGANWAL.zip', 
        'name': 'GSSS-KANGANWAL',
        'location': 'Malerkotla',
        'date': 'December 6, 2025'
    },
    {
        'zip': r'D:\PATIALA_GSSS_MULTIPURPOSE.zip', 
        'name': 'GSSS-MULTIPURPOSE-SESSION-2',
        'location': 'Patiala',
        'date': 'December 6, 2025'
    },
    {
        'zip': r'D:\PATIALA_GSSS_NANDPURKESHO.zip', 
        'name': 'GSSS-NANDPURKESHO',
        'location': 'Patiala',
        'date': 'December 6, 2025'
    }
]

output_dir = r'c:\Users\lenovo\OneDrive - Plaksha University\Plaksha\Work\Research\2025\Projects\Science_on_Wheels\Website\gallery_school_collage'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

for school in schools:
    print(f"\n{'='*60}")
    print(f"Processing: {school['name']}")
    print('='*60)
    
    # Extract zip to temp folder
    temp_dir = tempfile.mkdtemp()
    try:
        print(f"Extracting {school['zip']}...")
        with zipfile.ZipFile(school['zip'], 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find all images
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        image_paths = []
        for ext in extensions:
            image_paths.extend(glob.glob(os.path.join(temp_dir, '**', ext), recursive=True))
        
        print(f'Found {len(image_paths)} images')
        
        if len(image_paths) < 6:
            print(f'ERROR: Need at least 6 images, found {len(image_paths)}')
            continue
        
        # Get best 6 photos using AI
        print('AI is selecting best 6 photos...')
        selected_photos = get_best_photos(
            image_paths,
            LOGO_PATH if os.path.exists(LOGO_PATH) else None,
            school['name'],
            school['location'],
            school['date'],
            count=6,
            model_name='gemini-2.0-flash-exp'
        )
        print(f'Selected {len(selected_photos)} photos')
        
        # Create collage
        output_path = os.path.join(output_dir, f"{school['name']}.jpg")
        print(f'Creating collage...')
        create_collage_with_header(
            selected_photos,
            output_path,
            school['name'],
            school['location'],
            school['date'],
            LOGO_PATH if os.path.exists(LOGO_PATH) else None,
            grid_layout=(3, 2),
            target_size=(540, 405)
        )
        
        # Rate collage
        print('Rating collage...')
        rating_text, score = rate_collage(
            output_path,
            LOGO_PATH if os.path.exists(LOGO_PATH) else None,
            school['name'],
            school['location'],
            school['date'],
            model_name='gemini-2.0-flash-exp'
        )
        
        print(f'\n✅ Collage saved: {output_path}')
        print(f'📊 Rating: {score}/10')
        print(f'💬 {rating_text}')
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

print('\n' + '='*60)
print('✅ All collages generated!')
print('='*60)
