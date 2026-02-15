import os
import re
import glob

# Schools we need (Jan 22 - Feb 9 only, Jan 21 already on website)
needed_schools = {
    '22.01.2026': ['GSSS GONIANA GIRLS', 'PM SHRI GSSS MEHMA SARJA', 'GSSS GOBINDPURA', 'GHS NATHANA GIRLS', 'GSSS SIVIAN', 'GSSS GONIANA BOYS'],
    '23.01.2026': ['GHS JEOND', 'GHS BHUNDAR', 'GSSS RAMPURA MANDI GIRLS', 'GSSS LEHRA MOHABBAT', 'GSSS PATTI KALA MEHRAJ BOYS'],
    '24.01.2026': ['GSSS BHUCHO MANDI BOYS', 'GHS BHUCHO MANDI GIRLS', 'GSSS KOT FATTA', 'GHS BHAI BAKHTAUR RMSA', 'GSSS MAUR MANDI GIRLS', 'GSSS TALWANDI SABO'],
    '28.01.2026': ['GHS KAILE WANDER (RMSA)', 'SHAHEED LABH SINGH GSSS SEKHU', 'GHS G KOTHA GURU', 'GSSS PATTI KARAMCHAND MEHRAJ GIRLS'],
    '29.01.2026': ['GSSS MUKTSAR (G) WNO.8 MKT', 'GSSS RAI KE KALAN', 'GSSS KOTLIABLU'],
    '30.01.2026': ['GSSS RUPANA (B)', 'GHS PARK', 'GSSS GIDDERBAHA (G)'],
    '31.01.2026': ['GSSS PIND MALOUT', 'GSSS MALOUT (B)', 'GSSS RUPANA (G)', 'GSSS MUKTSAR (G) WNO.8 MKT'],
    '02.02.2026': ['GSSS BALLUANA', 'GHS BRANCH ABOHAR', 'GSSS MALOUT (G) W.NO.4', 'GHS TARMALA'],
    '03.02.2026': ['GSSS NIHAL KHERA', 'GHS ASLAM WALA', 'GHS KIKKER KHERA', 'GSSS BAZID PUR KATTIAN WALI'],
    '04.02.2026': ['GSSS GIRLS SCHOOL FAZILKA', 'GSSS MAHUANA BODLA(RMSA)', 'GSSS LALO WALI'],
    '05.02.2026': ['GOVT MODEL SENIOR SECONDARY SCHOOL CHAK MOCHAN WALA', 'GSSS BALEL KE HASAL RMSA', 'GSSS DHANDHI KADIM'],
    '06.02.2026': ['GSSS GIRLS ABOHAR', 'GSSS G JAITU', 'GHS DOAD'],
    '07.02.2026': ['GHS DHILWAN KALAN', 'GSSS BARGARI', 'GHS SURGAPURI KKP', 'GSSS SANDHWAN'],
    '09.02.2026': ['GSSSG FDK', 'GSSS GOLEWALA', 'GHS TEHNA'],
}

base_path = r"D:\OneDrive_2026-02-15\20.01.2026 to 11.02.2026"

def normalize(name):
    """Normalize a name for fuzzy matching"""
    n = name.upper()
    n = re.sub(r'[^A-Z0-9]', '', n)
    return n

# Get all zip files organized by date folder
zip_by_date = {}
for date_folder in os.listdir(base_path):
    date_path = os.path.join(base_path, date_folder)
    if not os.path.isdir(date_path):
        continue
    zips = []
    # Search recursively (some dates have subfolders like "Bathinda", "Muktsar")
    for root, dirs, files in os.walk(date_path):
        for f in files:
            if f.lower().endswith('.zip'):
                full_path = os.path.join(root, f)
                zip_name = os.path.splitext(f)[0]
                zips.append((zip_name, full_path))
    zip_by_date[date_folder] = zips

# Match each needed school with a zip file
found = 0
missing = []
matched = []

for date, schools in sorted(needed_schools.items()):
    print(f"\n--- {date} ({len(schools)} schools needed) ---")
    available_zips = zip_by_date.get(date, [])
    available_norm = {normalize(z[0]): z for z in available_zips}
    
    for school in schools:
        school_norm = normalize(school)
        
        # Try exact normalized match first
        match = None
        for zip_norm, zip_info in available_norm.items():
            if school_norm == zip_norm:
                match = zip_info
                break
        
        # Try substring/fuzzy match
        if not match:
            # Extract key part of school name (remove common prefixes)
            key = re.sub(r'^(PM SHRI |GOVT MODEL SENIOR SECONDARY SCHOOL |SHAHEED LABH SINGH )', '', school.upper())
            key_norm = normalize(key)
            for zip_norm, zip_info in available_norm.items():
                if key_norm in zip_norm or zip_norm in key_norm:
                    match = zip_info
                    break
        
        # Try even more relaxed matching
        if not match:
            # Check if short school name (last word) is contained
            short_words = [w for w in school.upper().split() if len(w) > 3 and w not in ('GSSS', 'GHS', 'GSSSG', 'GOVT', 'MODEL', 'SENIOR', 'SECONDARY', 'SCHOOL', 'GIRLS', 'BOYS', 'RMSA')]
            if short_words:
                for zip_norm, zip_info in available_norm.items():
                    for w in short_words:
                        if w in zip_info[0].upper():
                            match = zip_info
                            break
                    if match:
                        break
        
        # Also search in other date folders if not found in expected date
        if not match:
            for other_date, other_zips in zip_by_date.items():
                if other_date == date:
                    continue
                other_norm = {normalize(z[0]): z for z in other_zips}
                for zip_norm, zip_info in other_norm.items():
                    if school_norm == zip_norm:
                        match = zip_info
                        print(f"  NOTE: Found in different date folder ({other_date})")
                        break
                if match:
                    break
        
        if match:
            found += 1
            matched.append((date, school, match[1]))
            print(f"  OK: {school} -> {match[0]}")
        else:
            missing.append((date, school))
            print(f"  MISSING: {school}")

print(f"\n{'='*60}")
print(f"SUMMARY:")
print(f"  Total Schools Needed: {sum(len(s) for s in needed_schools.values())}")
print(f"  Found:   {found}")
print(f"  Missing: {len(missing)}")

if missing:
    print(f"\nMISSING ZIP FILES:")
    for date, school in missing:
        print(f"  [{date}] {school}")
    
    # Show available zips in those date folders to help find them
    missing_dates = set(d for d, _ in missing)
    for d in sorted(missing_dates):
        avail = zip_by_date.get(d, [])
        print(f"\n  Available zips in {d}:")
        for name, path in avail:
            print(f"    - {name}")
