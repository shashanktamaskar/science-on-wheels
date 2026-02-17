#!/usr/bin/env python3
"""Validate Feb 10-13 data before website update."""
import os
import re
import json

ZIP_BASE = r"D:\OneDrive_1_2-17-2026"

# Parse all school data from emails
new_days = [
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
                    ('GSSS-JANGAL', 'https://maps.app.goo.gl/aMHfNLsdAqQPCbDE8', 328, 111, 100, 'Pathankot', 'GSSS JANGAL', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSS%5FJANGAL&view=0'),
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
                    ('GSSS-GHAROTA', 'https://maps.app.goo.gl/RMuUwQxWxCVPYMV26', 450, 300, 150, 'Pathankot', 'FREEDOM FIGHTER SH. HANS RAJ GOVT. SR. SEC. SMART SCHOOL GHAROTA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FPATHANKOT%5FGSSSS%5FGHAROTA&view=0'),
                ],
            },
        ]
    },
]

print("=" * 70)
print("VALIDATION REPORT: Feb 10-13, 2026")
print("=" * 70)

# 1. Count schools per day
total_schools = 0
total_students = 0
total_girls = 0
total_boys = 0
issues = []

for day in new_days:
    day_schools = 0
    day_students = 0
    for v in day['vehicles']:
        for s in v['schools']:
            day_schools += 1
            day_students += s[2]
            total_students += s[2]
            total_girls += s[3]
            total_boys += s[4]
            # Check girls + boys = total
            if s[3] + s[4] != s[2]:
                issues.append(f"  MISMATCH: {s[0]} on {day['date']}: {s[3]}G + {s[4]}B = {s[3]+s[4]} != {s[2]} total")
    total_schools += day_schools
    print(f"\n{day['date']} ({day['date_folder']}): {day_schools} schools, {day_students} students")
    for v in day['vehicles']:
        print(f"  Vehicle {v['number']}: {len(v['schools'])} schools")
        for s in v['schools']:
            print(f"    - {s[0]} ({s[5]}) | {s[2]} students ({s[3]}G/{s[4]}B)")

print(f"\n{'=' * 70}")
print(f"TOTALS: {total_schools} new schools, {total_students} students ({total_girls}G + {total_boys}B)")

# 2. Check zip availability
print(f"\n{'=' * 70}")
print("ZIP FILE VERIFICATION")
print("=" * 70)

zip_ok = 0
zip_missing = 0
for day in new_days:
    date_folder = os.path.join(ZIP_BASE, day['date_folder'])
    if not os.path.exists(date_folder):
        print(f"\n  MISSING FOLDER: {date_folder}")
        for v in day['vehicles']:
            zip_missing += len(v['schools'])
        continue
    
    zips_in_folder = []
    for root, dirs, files in os.walk(date_folder):
        for f in files:
            if f.lower().endswith('.zip'):
                zips_in_folder.append((f, os.path.join(root, f)))
    
    print(f"\n  {day['date_folder']}: {len(zips_in_folder)} zips found")
    
    for v in day['vehicles']:
        for s in v['schools']:
            zip_search = s[6]  # zip search name
            found = False
            for zname, zpath in zips_in_folder:
                zbase = os.path.splitext(zname)[0].upper().replace('-', ' ')
                search = zip_search.upper().replace('-', ' ')
                if zbase == search or search in zbase or zbase in search:
                    found = True
                    print(f"    OK: {s[0]} -> {zname}")
                    zip_ok += 1
                    break
            if not found:
                # Try matching internal name
                school_norm = re.sub(r'[^A-Z]', '', s[0].upper())
                for zname, zpath in zips_in_folder:
                    zip_norm = re.sub(r'[^A-Z]', '', os.path.splitext(zname)[0].upper())
                    if school_norm == zip_norm or school_norm in zip_norm or zip_norm in school_norm:
                        found = True
                        print(f"    OK (fuzzy): {s[0]} -> {zname}")
                        zip_ok += 1
                        break
            if not found:
                print(f"    MISSING: {s[0]} (searched: '{zip_search}')")
                zip_missing += 1

print(f"\n  Summary: {zip_ok} found, {zip_missing} missing")

# 3. Data quality issues
print(f"\n{'=' * 70}")
print("DATA QUALITY ISSUES")
print("=" * 70)
if issues:
    for i in issues:
        print(i)
else:
    print("  No issues found!")

# 4. Duplicate maps URL check
print(f"\n{'=' * 70}")
print("DUPLICATE MAP URL CHECK")
print("=" * 70)
# Load existing data
existing_urls = set()
d = json.load(open('data.json', 'r', encoding='utf-8'))
for u in d['dailyUpdates']:
    for s in u['schools']:
        if s.get('location', {}).get('lat'):
            pass  # coords stored, not URL
# Check within new data
all_urls = {}
for day in new_days:
    for v in day['vehicles']:
        for s in v['schools']:
            url = s[1]
            if url in all_urls:
                print(f"  DUPLICATE URL: {url}")
                print(f"    Used by: {all_urls[url]} AND {s[0]}")
            all_urls[url] = s[0]

# 5. New districts
new_districts = set()
for day in new_days:
    for v in day['vehicles']:
        for s in v['schools']:
            new_districts.add(s[5])

existing_districts = set()
for u in d['dailyUpdates']:
    for s in u['schools']:
        existing_districts.add(s['district'])

truly_new = new_districts - existing_districts
print(f"\n{'=' * 70}")
print("DISTRICT SUMMARY")
print("=" * 70)
print(f"  New districts in this batch: {sorted(new_districts)}")
print(f"  Truly new (not in data.json): {sorted(truly_new)}")
print(f"  Total after update: {len(existing_districts | new_districts)}")

# 6. Post-update totals
existing_schools = sum(len(u['schools']) for u in d['dailyUpdates'])
existing_students = sum(s['studentsReached'] for u in d['dailyUpdates'] for s in u['schools'])

print(f"\n{'=' * 70}")
print("POST-UPDATE PROJECTIONS")
print("=" * 70)
print(f"  Current: {existing_schools} schools, {existing_students} students, {len(existing_districts)} districts")
print(f"  Adding:  {total_schools} schools, {total_students} students")
print(f"  After:   {existing_schools + total_schools} schools, {existing_students + total_students} students, {len(existing_districts | new_districts)} districts")
print(f"\n{'=' * 70}")
print("READY FOR UPDATE? Check issues above.")
print("=" * 70)
