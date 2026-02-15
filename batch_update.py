#!/usr/bin/env python3
"""
Batch processor for Science on Wheels daily updates.
Processes multiple days sequentially using daily_update.py
"""
import os
import sys
import subprocess
import json
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_BASE = r"D:\OneDrive_2026-02-15\20.01.2026 to 11.02.2026"

def find_zip(date_folder, school_name):
    """Find the zip file for a school, searching in the date folder and subfolders."""
    date_path = os.path.join(ZIP_BASE, date_folder)
    
    # Normalize for matching
    school_norm = re.sub(r'[^A-Za-z0-9]', '', school_name.upper())
    
    # Search recursively for zip files
    for root, dirs, files in os.walk(date_path):
        for f in files:
            if f.lower().endswith('.zip'):
                zip_norm = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(f)[0].upper())
                if school_norm == zip_norm:
                    return os.path.join(root, f)
    
    # Fuzzy: try substring match
    for root, dirs, files in os.walk(date_path):
        for f in files:
            if f.lower().endswith('.zip'):
                zip_norm = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(f)[0].upper())
                # Remove common prefixes for comparison
                school_key = school_norm
                for prefix in ['PMSHRI', 'GOVTMODELSENIORSECONDARYSCOOL', 'GOVTMODELSENIORSECONDARYSCBOOL', 'GOVTMODELSENIORSECONDARYSCHOOL', 'SHAHEEDLABHSINGH']:
                    school_key = school_key.replace(prefix, '')
                if school_key in zip_norm or zip_norm in school_key:
                    return os.path.join(root, f)
    
    # Search ALL date folders as fallback
    for other_folder in os.listdir(ZIP_BASE):
        other_path = os.path.join(ZIP_BASE, other_folder)
        if not os.path.isdir(other_path) or other_folder == date_folder:
            continue
        for root, dirs, files in os.walk(other_path):
            for f in files:
                if f.lower().endswith('.zip'):
                    zip_norm = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(f)[0].upper())
                    if school_norm == zip_norm:
                        return os.path.join(root, f)
    
    return None

# All days to process (Jan 22 - Feb 9)
all_days = [
    {
        'date': '2026-01-22',
        'date_folder': '22.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-GONIANA-GIRLS', 'https://maps.app.goo.gl/snYotWyCBZeGog457', 676, 676, 0, 'Bathinda', 'GSSS GONIANA GIRLS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FGONIANA%20GIRLS&view=0'),
                    ('GSSS-MEHMA-SARJA', 'https://maps.app.goo.gl/wXQdtQjPMh9FMHL79', 460, 236, 224, 'Bathinda', 'GSSS MEHMA SARJA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FMEHMA%20SARJA&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-GOBINDPURA', 'https://maps.app.goo.gl/tS2EoxKHynEVPerPA', 355, 197, 158, 'Bathinda', 'GSSS GOBINDPURA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FGOBINDPURA&view=0'),
                    ('GHS-NATHANA-GIRLS', 'https://maps.app.goo.gl/5ekwFuyHdGkUrFEW6', 171, 171, 0, 'Bathinda', 'GHS NATHANA GIRLS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGHS%5FNATHANA%20GIRLS&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-SIVIAN', 'https://maps.app.goo.gl/sgowQZKcywG4KMrg6', 460, 200, 260, 'Bathinda', 'GSSS SIVIAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FSIVIAN&view=0'),
                    ('GSSS-GONIANA-BOYS', 'https://maps.app.goo.gl/kc6KChGobVybHrn47', 560, 30, 530, 'Bathinda', 'GSSS GONIANA BOYS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FGONIANA%20BOYS&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-01-23',
        'date_folder': '23.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GHS-JEOND', 'https://maps.app.goo.gl/yPDjaAAaMifAqVCE9', 131, 58, 73, 'Bathinda', 'GHS JEOND', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGHS%5FJEOND&view=0'),
                    ('GHS-BHUNDAR', 'https://maps.app.goo.gl/pZw2vCDsiSpafz9P9', 105, 65, 40, 'Bathinda', 'GHS BHUNDAR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGHS%5FBHUNDAR&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-RAMPURA-MANDI-GIRLS', 'https://maps.app.goo.gl/uSwuG8ySZjnKB4f36', 762, 762, 0, 'Bathinda', 'GSSS RAMPURA MANDI GIRLS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FRAMPURA%20MANDI%20GIRLS&view=0'),
                    ('GSSS-LEHRA-MOHABBAT', 'https://maps.app.goo.gl/1KgfuckyNxXJBJUM8', 321, 186, 135, 'Bathinda', 'GSSS LEHRA MOHABBAT', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FLEHRA%20MOHABBAT&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-PATTI-KALA-MEHRAJ-BOYS', 'https://maps.app.goo.gl/shF2RQLyoS33gU8G9', 320, 0, 320, 'Bathinda', 'GSSS PATTI KALA MEHRAJ BOYS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FPATTI%20KALA%20MEHRAJ%20BOYS&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-01-24',
        'date_folder': '24.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-BHUCHO-MANDI-BOYS', 'https://maps.app.goo.gl/ZfWX4QNMmACPbcxF8', 531, 102, 429, 'Bathinda', 'GSSS BHUCHO MANDI BOYS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FBHUCHO%20MANDI%20BOYS&view=0'),
                    ('GHS-BHUCHO-MANDI-GIRLS', 'https://maps.app.goo.gl/s1YaTzPF1jcfwgR78', 339, 339, 0, 'Bathinda', 'GHS BHUCHO MANDI GIRLS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FBHUCHO%20MANDI%20GIRLS&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-KOT-FATTA', 'https://maps.app.goo.gl/UNtLVPAPmdFDUTX67', 280, 160, 120, 'Bathinda', 'GSSS KOT FATTA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FKOT%20FATTA&view=0'),
                    ('GHS-BHAI-BAKHTAUR-RMSA', 'https://maps.app.goo.gl/8p8FmHe1zWLgaJRB9', 159, 79, 80, 'Bathinda', 'GHS BHAI BAKHTAUR RMSA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGHS%5FBHAI%20BAKHTAUR%20RMSA&view=0'),
                ],
            },
            {
                'number': 3,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GSSS-MAUR-MANDI-GIRLS', 'https://maps.app.goo.gl/VTifL3jCFJXdZbuS9', 850, 850, 0, 'Bathinda', 'GSSS MAUR MANDI GIRLS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FMAUR%20MANDI%20GIRLS&view=0'),
                    ('GSSS-TALWANDI-SABO', 'https://maps.app.goo.gl/ptKfScUnLJsriSPd8', 600, 308, 292, 'Bathinda', 'GSSS TALWANDI SABO', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FTALWANDI%20SABO&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-01-28',
        'date_folder': '28.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GHS-KAILE-WANDER-RMSA', 'https://maps.app.goo.gl/A36gXwakLna88Bvq9', 207, 125, 82, 'Bathinda', 'GHS KAILE WANDER (RMSA)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGHS%5FKAILE%20WANDER%20RMSA&view=0'),
                    ('GSSS-SEKHU', 'https://maps.app.goo.gl/e9aRgT9mfJV6DeC59', 385, 180, 205, 'Bathinda', 'SHAHEED LABH SINGH GSSS SEKHU', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FSEKHU&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'schools': [
                    ('GHS-G-KOTHA-GURU', 'https://maps.app.goo.gl/Yzipw2N391756XLY8', 174, 174, 0, 'Bathinda', 'GHS G KOTHA GURU', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGHS%5FKOTHA%20GURU%20G&view=0'),
                    ('GSSS-PATTI-KARAMCHAND-MEHRAJ-GIRLS', 'https://maps.app.goo.gl/Ygy9SwZhYGCrPFM26', 380, 380, 0, 'Bathinda', 'GSSS PATTI KARAMCHAND MEHRAJ GIRLS', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FPATTI%20KARAMCHAND%20MEHRAJ%20GIRLS&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-01-29',
        'date_folder': '29.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'schools': [
                    ('GSSS-MUKTSAR-G-WNO8-MKT', 'https://maps.app.goo.gl/d7d1dvi8yGky5Jb18', 1290, 1290, 0, 'Muktsar', 'GSSS MUKTSAR (G) WNO.8 MKT', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FMUKTSAR%20%28G%29&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Bathinda', 'https://maps.app.goo.gl/iJafYdsGoK74rbMS8'),
                'end': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'schools': [
                    ('GSSS-RAI-KE-KALAN', 'https://maps.app.goo.gl/TtcQos63srzhtrgm7', 425, 200, 225, 'Bathinda', 'GSSS RAI KE KALAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FBATHINDA%5FGSSS%5FRAI%20KE%20KALAN&view=0'),
                    ('GSSS-KOTLIABLU', 'https://maps.app.goo.gl/jpM8NuEdeUcy7X7DA', 382, 187, 195, 'Muktsar', 'GSSS KOTLIABLU', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FKOTLIABLU&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-01-30',
        'date_folder': '30.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'end': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'schools': [
                    ('GSSS-RUPANA-B', 'https://maps.app.goo.gl/vmJpCXcRXTwZ62VC9', 410, 0, 410, 'Muktsar', 'GSSS RUPANA (B)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FRUPANA%20%28B%29&view=0'),
                    ('GHS-PARK', 'https://maps.app.goo.gl/z6ngQq1jKAbXqQ2YA', 594, 392, 202, 'Muktsar', 'GHS PARK', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGHS%5FPARK&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'end': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'schools': [
                    ('GSSS-GIDDERBAHA-G', 'https://maps.app.goo.gl/KZgyWVpCTDaGCaxm8', 822, 822, 0, 'Muktsar', 'GSSS GIDDERBAHA (G)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FGIDDERBAHA%20%28G%29&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-01-31',
        'date_folder': '31.01.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'end': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'schools': [
                    ('GSSS-PIND-MALOUT', 'https://maps.app.goo.gl/xzJS77FtwaX2zJMf9', 754, 411, 343, 'Muktsar', 'GSSS PIND MALOUT', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FPIND%20MALOUT&view=0'),
                    ('GSSS-MALOUT-B', 'https://maps.app.goo.gl/XMB3X6v1oo6BnKsP7', 733, 0, 733, 'Muktsar', 'GSSS MALOUT (B)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FMALOUT%20%28B%29&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'end': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'schools': [
                    ('GSSS-RUPANA-G', 'https://maps.app.goo.gl/gofDRXsMGT2xXY4N9', 635, 601, 34, 'Muktsar', 'GSSS RUPANA (G)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FRUPANA%20%28G%29&view=0'),
                    ('GSSS-MUKTSAR-G-WNO8-MKT-S2', 'https://maps.app.goo.gl/sMSgahJAKsrFMkEs7', 806, 806, 0, 'Muktsar', 'GSSS MUKTSAR (G) WNO.8 MKT', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FMUKTSAR%20%28G%29&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-02',
        'date_folder': '02.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/NzW2BVJd2eoTLWHDA'),
                'schools': [
                    ('GSSS-BALLUANA', 'https://maps.app.goo.gl/iKEwGBZfU878nGU5A', 570, 210, 360, 'Fazilka', 'GSSS BALLUANA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FBALLUANA&view=0'),
                    ('GHS-BRANCH-ABOHAR', 'https://maps.app.goo.gl/cmjHK5nYaYgN7BR48', 324, 154, 170, 'Fazilka', 'GHS BRANCH ABOHAR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGHS%5FBRANCH%20ABOHAR&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Muktsar', 'https://maps.app.goo.gl/pe1TejDLZtm1BjHo6'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/NzW2BVJd2eoTLWHDA'),
                'schools': [
                    ('GSSS-MALOUT-G-WNO4', 'https://maps.app.goo.gl/qg2XDrbgXHwhFwZ58', 501, 501, 0, 'Muktsar', 'GSSS MALOUT (G) W.NO.4', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGSSS%5FMALOUT%20%28G%29&view=0'),
                    ('GHS-TARMALA', 'https://maps.app.goo.gl/Vq2AzZ6cugDwkaNY6', 234, 100, 134, 'Muktsar', 'GHS TARMALA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FMUKTSAR%5FGHS%5FTARMALA&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-03',
        'date_folder': '03.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'schools': [
                    ('GSSS-NIHAL-KHERA', 'https://maps.app.goo.gl/LLa11WhU97kjXNgz9', 872, 492, 380, 'Fazilka', 'GSSS NIHAL KHERA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FNIHAL%20KHERA&view=0'),
                    ('GHS-ASLAM-WALA', 'https://maps.app.goo.gl/cXbHz582HyhWiQto9', 159, 85, 74, 'Fazilka', 'GHS ASLAM WALA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGHS%5FASLAM%20WALA&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'schools': [
                    ('GHS-KIKKER-KHERA', 'https://maps.app.goo.gl/5fqBWnz14H8pRV3z6', 321, 155, 166, 'Fazilka', 'GHS KIKKER KHERA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGHS%5FKIKKER%20KHERA&view=0'),
                    ('GSSS-BAZID-PUR-KATTIAN-WALI', 'https://maps.app.goo.gl/9QgEcoRD2yT4k5sz8', 429, 200, 229, 'Fazilka', 'GSSS BAZID PUR KATTIAN WALI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FBAZID%20PUR%20KATTIAN%20WALI&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-04',
        'date_folder': '04.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'schools': [
                    ('GSSS-GIRLS-SCHOOL-FAZILKA', 'https://maps.app.goo.gl/bZ8W1XgKNV9Cyu7L6', 2253, 2253, 0, 'Fazilka', 'GSSS GIRLS SCHOOL FAZILKA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FGIRLS%20SCHOOL%20FAZILKA&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'schools': [
                    ('GSSS-MAHUANA-BODLA-RMSA', 'https://maps.app.goo.gl/dpbk4G54N9THaaaEA', 354, 134, 220, 'Fazilka', 'GSSS MAHUANA BODLA(RMSA)', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FMAHUANA%20BODLA%28RMSA%29&view=0'),
                    ('GSSS-LALO-WALI', 'https://maps.app.goo.gl/ivcXC4AL92TJCeFB7', 390, 220, 170, 'Fazilka', 'GSSS LALO WALI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FLALO%20WALI&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-05',
        'date_folder': '05.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/sxgRJw16c9AijEAp7'),
                'schools': [
                    ('GSSS-CHAK-MOCHAN-WALA', 'https://maps.app.goo.gl/12xQ9Q9Y8rSx2G7z9', 620, 315, 305, 'Fazilka', 'GOVT MODEL SENIOR SECONDARY SCHOOL CHAK MOCHAN WALA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FCHAK%20MOCHAN%20WALA&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'schools': [
                    ('GSSS-BALEL-KE-HASAL-RMSA', 'https://maps.app.goo.gl/Yd1KqhCdt8yW9FCE8', 512, 205, 307, 'Fazilka', 'GSSS BALEL KE HASAL RMSA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FBALEL%20KE%20HASAL%20RMSA&view=0'),
                    ('GSSS-DHANDHI-KADIM', 'https://maps.app.goo.gl/3Gdo6dhkVWq6i9SNA', 750, 386, 364, 'Fazilka', 'GSSS DHANDHI KADIM', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FDHANDHI%20KADIM&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-06',
        'date_folder': '06.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Fazilka', 'https://maps.app.goo.gl/sxgRJw16c9AijEAp7'),
                'end': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'schools': [
                    ('GSSS-GIRLS-ABOHAR', 'https://maps.app.goo.gl/AdVNDEcEy6L8SNha7', 2022, 2022, 0, 'Fazilka', 'GSSS GIRLS ABOHAR', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFAZILKA%5FGSSS%5FGIRLS%20ABOHAR&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Fazilka', 'https://maps.app.goo.gl/nZ8BPhr4JTPxQgARA'),
                'end': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'schools': [
                    ('GSSS-G-JAITU', 'https://maps.app.goo.gl/1ydCWmxxdSGk32Cz9', 815, 815, 0, 'Faridkot', 'GSSS G JAITU', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGSSS%5FG%20JAITU&view=0'),
                    ('GHS-DOAD', 'https://maps.app.goo.gl/83BMSqqmFE8JZHS58', 224, 104, 120, 'Faridkot', 'GHS DOAD', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGHS%5FDOAD&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-07',
        'date_folder': '07.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'end': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'schools': [
                    ('GHS-DHILWAN-KALAN', 'https://maps.app.goo.gl/r2WucoL1ttPouV8o8', 325, 125, 200, 'Faridkot', 'GHS DHILWAN KALAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGHS%5FDHILWAN%20KALAN&view=0'),
                    ('GSSS-BARGARI', 'https://maps.app.goo.gl/jkXijeF4k5GkHPsm8', 511, 202, 309, 'Faridkot', 'GSSS BARGARI', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGSSS%5FBARGARI&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'end': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'schools': [
                    ('GHS-SURGAPURI-KKP', 'https://maps.app.goo.gl/2VqdPTmm1Pk7QXUJ9', 402, 204, 198, 'Faridkot', 'GHS SURGAPURI KKP', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGHS%5FSURGAPURI%20KKP&view=0'),
                    ('GSSS-SANDHWAN', 'https://maps.app.goo.gl/PfAxzrb9T5RhNZkJ8', 640, 317, 323, 'Faridkot', 'GSSS SANDHWAN', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGSSS%5FSANDHWAN&view=0'),
                ],
            },
        ]
    },
    {
        'date': '2026-02-09',
        'date_folder': '09.02.2026',
        'vehicles': [
            {
                'number': 1,
                'start': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'end': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'schools': [
                    ('GSSSG-FDK', 'https://maps.app.goo.gl/gCXbpvzGX2E5LEQB8', 1470, 1470, 0, 'Faridkot', 'GSSSG FDK', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGSSSG%5FFDK&view=0'),
                    ('GSSS-GOLEWALA', 'https://maps.app.goo.gl/samCWp9PGPuSaAEQ7', 468, 236, 232, 'Faridkot', 'GSSS GOLEWALA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGSSS%5FGOLEWALA&view=0'),
                ],
            },
            {
                'number': 2,
                'start': ('Faridkot', 'https://maps.app.goo.gl/cywdeSqjNpCoo2kb6'),
                'end': ('Firozpur', 'https://maps.app.goo.gl/xCjuVeufmvpeFRa78'),
                'schools': [
                    ('GHS-TEHNA', 'https://maps.app.goo.gl/hZSgSVhBpqQ3s5fB6', 195, 95, 100, 'Faridkot', 'GHS TEHNA', 'https://plakshauniversity1-my.sharepoint.com/personal/scienceonwheels_plaksha_edu_in/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FDocuments%2FGallery%2FFARIDKOT%5FGHS%5FTEHNA&view=0'),
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
                zip_path = "*"  # Will skip collage generation
            
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
        
        # Run daily_update.py
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
    print(f"\nNow run: git add . && git commit -m 'Batch update Jan 22 - Feb 9' && git push origin main")
    return 0

if __name__ == '__main__':
    sys.exit(main())
