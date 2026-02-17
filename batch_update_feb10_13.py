#!/usr/bin/env python3
"""
Batch processor for Feb 10-13, 2026 daily updates.
"""
import os
import sys
import subprocess
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_BASE = r"D:\OneDrive_1_2-17-2026"

def find_zip(date_folder, school_name):
    """Find the zip file for a school."""
    date_path = os.path.join(ZIP_BASE, date_folder)
    school_norm = re.sub(r'[^A-Za-z0-9]', '', school_name.upper())
    
    for root, dirs, files in os.walk(date_path):
        for f in files:
            if f.lower().endswith('.zip'):
                zip_norm = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(f)[0].upper())
                if school_norm == zip_norm:
                    return os.path.join(root, f)
    
    # Fuzzy match
    for root, dirs, files in os.walk(date_path):
        for f in files:
            if f.lower().endswith('.zip'):
                zip_norm = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(f)[0].upper())
                if school_norm in zip_norm or zip_norm in school_norm:
                    return os.path.join(root, f)
    return None

all_days = [
    {
        'date': '2026-02-10',
        'date_folder': '10.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'end': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'schools': [
                    ('GSSS-GURU-HAR-SAHAI', 'https://maps.app.goo.gl/sf71bbupFn19EMZXA', 513, 30, 483, 'Firozpur', 'GSSS GURU HAR SAHAI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FGURU%20HAR%20SAHAI&viewid=efb56dab%2D8a39%2D4d99%2Db96c%2D40fc250c7320&view=0'),
                    ('GHS-CHHANGA-RAI-UTTAR', 'https://maps.app.goo.gl/u3YCw3tjDByPFcydA', 430, 210, 220, 'Firozpur', 'GHS CHHANGA RAI UTTAR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGHS%5FCHHANGA%20RAI%20UTTAR&view=0'),
                    ('GSSS-DONA-MATTAR', 'https://maps.app.goo.gl/HLAjCkHbt4KkKWqv9', 470, 229, 241, 'Firozpur', 'GSSS DONA MATTAR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FDONA%20MATTAR&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'end': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'schools': [
                    ('GHS-JHOK-TEHAL-SINGH', 'https://maps.app.goo.gl/ikuVNdjVb9kbQZGb8', 244, 101, 143, 'Firozpur', 'GHS JHOK TEHAL SINGH', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGHS%5FJHOK%20TEHAL%20SINGH&view=0'),
                    ('GSSS-KARIAN-PEHLWAN', 'https://maps.app.goo.gl/61QH9h7pHEkPgaqY9', 502, 256, 246, 'Firozpur', 'GSSS KARIAN PEHLWAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FKARIAN%20PEHLWAN&view=0'),
                    ('GHS-PIR-ISMAIL-KHAN', 'https://maps.app.goo.gl/qnGjXWhsMxYdjhWKA?g_st=aw', 365, 200, 165, 'Firozpur', 'GHS PIR ISMAIL KHAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGHS%5FPIR%20ISMAIL%20KHAN&view=0'),
                    ('GSSS-TALWANDI-JALE-KHAN', 'https://maps.app.goo.gl/xHVfgsAnfU6jedPz8', 380, 200, 180, 'Firozpur', 'GSSS TALWANDI JALE KHAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FTALWANDI%20JALE%20KHAN&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'end': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'schools': [
                    ('GHS-GIRLS-MAKHU', 'https://maps.app.goo.gl/Q3RikFjc7b1d8T4YA', 580, 580, 0, 'Firozpur', 'GHS GIRLS MAKHU', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGHS%5FGIRLS%20MAKHU'),
                    ('GSS-BOYS-MAKHU', 'https://maps.app.goo.gl/ExBY3pqtHthwuWSZ6', 549, 0, 549, 'Firozpur', 'GSS BOYS MAKHU', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSS%5FBOYS%20MAKHU&view=0'),
                    ('GSSS-KUSSU-WALA', 'https://maps.app.goo.gl/PfAxzrb9T5RhNZkJ8', 620, 298, 322, 'Firozpur', 'GSSS KUSSU WALA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FKUSSU%20WALA&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-11',
        'date_folder': '11.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-BOYS-FZR', 'https://maps.app.goo.gl/imL7dNi3LKCKZhPV8', 850, 0, 850, 'Firozpur', 'GSSS BOYS FZR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FBOYS%20FZR&view=0'),
                    ('GSSS-BAZIDPUR', 'https://maps.app.goo.gl/Rab8PDa53BBaL9Az6', 456, 298, 158, 'Firozpur', 'GSSS BAZIDPUR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5F%20GSSS%5FBAZIDPUR&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-BEHAK-GUJARAN', 'https://maps.app.goo.gl/V764bZk3MtRF7sRG7', 490, 197, 293, 'Firozpur', 'GSSS BEHAK GUJARAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FBEHAK%20GUJARAN&view=0'),
                    ('GHS-GHUDUWALA', 'https://maps.app.goo.gl/BKNy7U78RefCCVj77', 155, 75, 80, 'Firozpur', 'GHS GHUDUWALA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGHS%5FGHUDUWALA&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-MUDKI-BOYS', 'https://maps.app.goo.gl/Q1Yr3R3K5ceAjQSo6', 350, 0, 350, 'Firozpur', 'GSSS MUDKI BOYS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FMUDKI%20BOYS&view=0'),
                    ('GSSS-BOYS-TALWANDI-BHAI', 'https://maps.app.goo.gl/eoSz7EwnfCAhEDjy8', 360, 0, 360, 'Firozpur', 'GSSS BOYS TALWANDI BHAI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FBOYS%20TALWANDI%20BHAI&view=0'),
                    ('GSSS-GIRLS-TALWANDI-BHAI', 'https://maps.app.goo.gl/gYaEKAT1yizA36b78', 740, 740, 0, 'Firozpur', 'GSSS GIRLS TALWANDI BHAI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFIROZPUR%5FGSSS%5FGIRLS%20TALWANDI%20BHAI&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-12',
        'date_folder': '12.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-JANGAL', 'https://maps.app.goo.gl/aMHfNLsdAqQPCbDE8', 211, 111, 100, 'Pathankot', 'GSSS JANGAL', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FJANGAL&view=0'),
                    ('GSSS-TARAGARH-B', 'https://maps.app.goo.gl/3wNN4q3Bxtfz2FJc6', 105, 0, 105, 'Pathankot', 'GSSS TARAGARH (B)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FTARAGARH%20%28B%29'),
                ],
            },
            {
                'number': 2,
                'start': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-BADHANI', 'https://maps.app.goo.gl/hfM5xoYqyY8aAvka8', 750, 337, 413, 'Pathankot', 'GSSS BADHANI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FBADHANI&view=0'),
                    ('GSSS-KFC-PATHANKOT', 'https://maps.app.goo.gl/snbawPLqp7fXQTN4A', 425, 151, 274, 'Pathankot', 'GSSS KFC PATHANKOT', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FKFC%20PATHANKOT&view=0'),
                    ('GSSS-DAULATPUR-KALAN', 'https://maps.app.goo.gl/Km8Pr4ELjUXM2Ec17', 435, 245, 190, 'Pathankot', 'GSSS DAULATPUR KALAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FDAULATPUR%20KALAN&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GGSSS-SUJANPUR', 'https://maps.app.goo.gl/M7KTviQfop6km2bA6', 580, 580, 0, 'Pathankot', 'GGSSS SUJANPUR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGGSSS%5FSUJANPUR&view=0'),
                    ('GSSS-SUJANPUR-BOYS', 'https://maps.app.goo.gl/rrtrn2dr7NUEzEHL7', 540, 20, 520, 'Pathankot', 'GSSS SUJANPUR (BOYS)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FSUJANPUR%20BOYS&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-13',
        'date_folder': '13.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GGSSS-BEGOWAL', 'https://maps.app.goo.gl/7vXSaK2ro3951RLU9', 325, 325, 0, 'Pathankot', 'GGSSS BEGOWAL', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGGSSS%5FBEGOWAL&view=0'),
                    ('GHS-BANI-LODHI', 'https://maps.app.goo.gl/57ViBnUsVhTnQNFo8', 210, 90, 120, 'Pathankot', 'GHS BANI LODHI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGHS%5FBANI%20LODHI&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-FEROZEPUR-KALAN', 'https://maps.app.goo.gl/5A4mmLXKMeieMe4x5', 440, 207, 233, 'Pathankot', 'GSSS FEROZEPUR KALAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FFEROZEPUR%20KALAN&view=0'),
                    ('GSSS-MANWAL', 'https://maps.app.goo.gl/maZcgGv4ku4RBAtV7', 325, 140, 185, 'Pathankot', 'GSSS MANWAL', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FMANWAL&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'end': ('Pathankot', 'https://maps.app.goo.gl/uXCWAG9P7J9uKCoUA'),
                'schools': [
                    ('GSSS-BAMIAL', 'https://maps.app.goo.gl/q3Pjj5STg31adVbM6', 642, 302, 340, 'Pathankot', 'GSSS BAMIAL', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FBAMIAL&view=0'),
                    ('GSSS-GHAROTA', 'https://maps.app.goo.gl/RMuUwQxWxCVPYMV26', 450, 300, 150, 'Pathankot', 'GSSSS GHAROTA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSSS%5FGHAROTA&view=0'),
                ],
            },
        ]
    },
]

def generate_input_file(day_data, output_path):
    """Generate a today_update.txt file for a single day."""
    lines = [f"DATE: {day_data['date']}", ""]
    
    for vehicle in day_data['vehicles']:
        lines.append(f"VEHICLE: {vehicle['number']}")
        lines.append(f"START: {vehicle['start'][0]} | {vehicle['start'][1]}")
        
        for school in vehicle['schools']:
            name, map_url, students, girls, boys, district, zip_search_name, gallery_url = school
            
            # Find the zip file
            zip_path = find_zip(day_data['date_folder'], zip_search_name)
            if not zip_path:
                print(f"  WARNING: No zip found for {zip_search_name} ({day_data['date']})")
                zip_path = "*"
            
            lines.append(f"SCHOOL: {name} | {map_url} | {students} | {girls} | {boys} | {district} | {zip_path} | {gallery_url}")
        
        lines.append(f"END: {vehicle['end'][0]} | {vehicle['end'][1]}")
        lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return True

def main():
    print(f"Processing {len(all_days)} days of updates...")
    print(f"Zip base: {ZIP_BASE}")
    print()
    
    for i, day in enumerate(all_days):
        date = day['date']
        num_schools = sum(len(v['schools']) for v in day['vehicles'])
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(all_days)}] Processing {date} ({num_schools} schools)")
        print(f"{'='*60}")
        
        # Generate input file
        input_file = os.path.join(SCRIPT_DIR, 'today_update.txt')
        generate_input_file(day, input_file)
        
        # Run daily_update.py with --skip-push
        cmd = [sys.executable, os.path.join(SCRIPT_DIR, 'daily_update.py'), '--input', input_file, '--skip-push']
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=SCRIPT_DIR, capture_output=False)
        
        if result.returncode != 0:
            print(f"\nERROR: daily_update.py failed for {date} (exit code {result.returncode})")
            print("Stopping batch processing. Fix the issue and restart.")
            return 1
        
        print(f"Completed {date}")
    
    print(f"\n{'='*60}")
    print(f"ALL {len(all_days)} DAYS PROCESSED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"\nNow run: git add -A && git commit -m 'Batch update Feb 10-13' && git push origin main")
    return 0

if __name__ == '__main__':
    sys.exit(main())
