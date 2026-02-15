import json

# Current website stats (as of Jan 21, 2026)
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

current_schools = data['mission']['schoolsCovered']['current']
current_students = data['mission']['studentsImpacted']
current_girls = data['mission']['genderBreakdown']['girls']
current_boys = data['mission']['genderBreakdown']['boys']
current_distance = data['mission']['distanceTravelled']
current_districts = data['mission']['districtsCovered']['current']

# Existing districts
existing_districts = set()
for update in data.get('dailyUpdates', []):
    for school in update.get('schools', []):
        existing_districts.add(school.get('district', ''))

print(f"=== CURRENT WEBSITE STATUS (as of Jan 21) ===")
print(f"Schools: {current_schools}")
print(f"Students: {current_students}")
print(f"Girls: {current_girls}")
print(f"Boys: {current_boys}")
print(f"Distance: {current_distance} km")
print(f"Districts: {current_districts} ({', '.join(sorted(existing_districts))})")

# New data from Jan 22 to Feb 9
# Note: Jan 21 data is already in the website (we processed it previously)
new_days = [
    {
        'date': '2026-01-22',
        'schools': [
            {'name': 'GSSS GONIANA GIRLS', 'students': 676, 'girls': 676, 'boys': 0, 'district': 'Bathinda'},
            {'name': 'PM SHRI GSSS MEHMA SARJA', 'students': 460, 'girls': 236, 'boys': 224, 'district': 'Bathinda'},
            {'name': 'GSSS GOBINDPURA', 'students': 355, 'girls': 197, 'boys': 158, 'district': 'Bathinda'},
            {'name': 'GHS NATHANA GIRLS', 'students': 171, 'girls': 171, 'boys': 0, 'district': 'Bathinda'},
            {'name': 'GSSS SIVIAN', 'students': 460, 'girls': 200, 'boys': 260, 'district': 'Bathinda'},
            {'name': 'GSSS GONIANA BOYS', 'students': 560, 'girls': 30, 'boys': 530, 'district': 'Bathinda'},
        ]
    },
    {
        'date': '2026-01-23',
        'schools': [
            {'name': 'GHS JEOND', 'students': 131, 'girls': 58, 'boys': 73, 'district': 'Bathinda'},
            {'name': 'GHS BHUNDAR', 'students': 105, 'girls': 65, 'boys': 40, 'district': 'Bathinda'},
            {'name': 'GSSS RAMPURA MANDI GIRLS', 'students': 762, 'girls': 762, 'boys': 0, 'district': 'Bathinda'},
            {'name': 'GSSS LEHRA MOHABBAT', 'students': 321, 'girls': 186, 'boys': 135, 'district': 'Bathinda'},
            {'name': 'GSSS PATTI KALA MEHRAJ BOYS', 'students': 320, 'girls': 0, 'boys': 320, 'district': 'Bathinda'},
        ]
    },
    {
        'date': '2026-01-24',
        'schools': [
            {'name': 'GSSS BHUCHO MANDI BOYS', 'students': 531, 'girls': 102, 'boys': 429, 'district': 'Bathinda'},
            {'name': 'GHS BHUCHO MANDI GIRLS', 'students': 339, 'girls': 339, 'boys': 0, 'district': 'Bathinda'},
            {'name': 'GSSS KOT FATTA', 'students': 280, 'girls': 160, 'boys': 120, 'district': 'Bathinda'},
            {'name': 'GHS BHAI BAKHTAUR RMSA', 'students': 159, 'girls': 79, 'boys': 80, 'district': 'Bathinda'},
            {'name': 'GSSS MAUR MANDI GIRLS', 'students': 850, 'girls': 850, 'boys': 0, 'district': 'Bathinda'},
            {'name': 'GSSS TALWANDI SABO', 'students': 600, 'girls': 308, 'boys': 292, 'district': 'Bathinda'},
        ]
    },
    {
        'date': '2026-01-28',
        'schools': [
            {'name': 'GHS KAILE WANDER (RMSA)', 'students': 207, 'girls': 125, 'boys': 82, 'district': 'Bathinda'},
            {'name': 'SHAHEED LABH SINGH GSSS SEKHU', 'students': 385, 'girls': 180, 'boys': 205, 'district': 'Bathinda'},
            {'name': 'GHS G KOTHA GURU', 'students': 174, 'girls': 174, 'boys': 0, 'district': 'Bathinda'},
            {'name': 'GSSS PATTI KARAMCHAND MEHRAJ GIRLS', 'students': 380, 'girls': 380, 'boys': 0, 'district': 'Bathinda'},
        ]
    },
    {
        'date': '2026-01-29',
        'schools': [
            {'name': 'GSSS MUKTSAR (G) WNO.8 MKT', 'students': 1290, 'girls': 1290, 'boys': 0, 'district': 'Muktsar'},
            {'name': 'GSSS RAI KE KALAN', 'students': 425, 'girls': 200, 'boys': 225, 'district': 'Bathinda'},
            {'name': 'GSSS KOTLIABLU', 'students': 382, 'girls': 187, 'boys': 195, 'district': 'Muktsar'},
        ]
    },
    {
        'date': '2026-01-30',
        'schools': [
            {'name': 'GSSS RUPANA (B)', 'students': 410, 'girls': 0, 'boys': 410, 'district': 'Muktsar'},
            {'name': 'GHS PARK', 'students': 594, 'girls': 392, 'boys': 202, 'district': 'Muktsar'},
            {'name': 'GSSS GIDDERBAHA (G)', 'students': 822, 'girls': 822, 'boys': 0, 'district': 'Muktsar'},
        ]
    },
    {
        'date': '2026-01-31',
        'schools': [
            {'name': 'GSSS PIND MALOUT', 'students': 754, 'girls': 411, 'boys': 343, 'district': 'Muktsar'},
            {'name': 'GSSS MALOUT (B)', 'students': 733, 'girls': 0, 'boys': 733, 'district': 'Muktsar'},
            {'name': 'GSSS RUPANA (G)', 'students': 635, 'girls': 601, 'boys': 34, 'district': 'Muktsar'},
            {'name': 'GSSS MUKTSAR (G) WNO.8 MKT', 'students': 806, 'girls': 806, 'boys': 0, 'district': 'Muktsar'},
        ]
    },
    {
        'date': '2026-02-02',
        'schools': [
            {'name': 'GSSS BALLUANA', 'students': 570, 'girls': 210, 'boys': 360, 'district': 'Fazilka'},
            {'name': 'GHS BRANCH ABOHAR', 'students': 324, 'girls': 154, 'boys': 170, 'district': 'Fazilka'},
            {'name': 'GSSS MALOUT (G) W.NO.4', 'students': 501, 'girls': 501, 'boys': 0, 'district': 'Muktsar'},
            {'name': 'GHS TARMALA', 'students': 234, 'girls': 100, 'boys': 134, 'district': 'Muktsar'},
        ]
    },
    {
        'date': '2026-02-03',
        'schools': [
            {'name': 'GSSS NIHAL KHERA', 'students': 872, 'girls': 492, 'boys': 380, 'district': 'Fazilka'},
            {'name': 'GHS ASLAM WALA', 'students': 159, 'girls': 85, 'boys': 74, 'district': 'Fazilka'},
            {'name': 'GHS KIKKER KHERA', 'students': 321, 'girls': 155, 'boys': 166, 'district': 'Fazilka'},
            {'name': 'GSSS BAZID PUR KATTIAN WALI', 'students': 429, 'girls': 200, 'boys': 229, 'district': 'Fazilka'},
        ]
    },
    {
        'date': '2026-02-04',
        'schools': [
            {'name': 'GSSS GIRLS SCHOOL FAZILKA', 'students': 2253, 'girls': 2253, 'boys': 0, 'district': 'Fazilka'},
            {'name': 'GSSS MAHUANA BODLA(RMSA)', 'students': 354, 'girls': 134, 'boys': 220, 'district': 'Fazilka'},
            {'name': 'GSSS LALO WALI', 'students': 390, 'girls': 220, 'boys': 170, 'district': 'Fazilka'},
        ]
    },
    {
        'date': '2026-02-05',
        'schools': [
            {'name': 'GOVT MODEL SSS CHAK MOCHAN WALA', 'students': 620, 'girls': 315, 'boys': 305, 'district': 'Fazilka'},
            {'name': 'GSSS BALEL KE HASAL RMSA', 'students': 512, 'girls': 205, 'boys': 307, 'district': 'Fazilka'},
            {'name': 'GSSS DHANDHI KADIM', 'students': 750, 'girls': 386, 'boys': 364, 'district': 'Fazilka'},
        ]
    },
    {
        'date': '2026-02-06',
        'schools': [
            {'name': 'GSSS GIRLS ABOHAR', 'students': 2022, 'girls': 2022, 'boys': 0, 'district': 'Fazilka'},
            {'name': 'GSSS G JAITU', 'students': 815, 'girls': 815, 'boys': 0, 'district': 'Faridkot'},
            {'name': 'GHS DOAD', 'students': 224, 'girls': 104, 'boys': 120, 'district': 'Faridkot'},
        ]
    },
    {
        'date': '2026-02-07',
        'schools': [
            {'name': 'GHS DHILWAN KALAN', 'students': 325, 'girls': 125, 'boys': 200, 'district': 'Faridkot'},
            {'name': 'GSSS BARGARI', 'students': 511, 'girls': 202, 'boys': 309, 'district': 'Faridkot'},
            {'name': 'GHS SURGAPURI KKP', 'students': 402, 'girls': 204, 'boys': 198, 'district': 'Faridkot'},
            {'name': 'GSSS SANDHWAN', 'students': 640, 'girls': 317, 'boys': 323, 'district': 'Faridkot'},
        ]
    },
    {
        'date': '2026-02-09',
        'schools': [
            {'name': 'GSSSG FDK', 'students': 1470, 'girls': 1470, 'boys': 0, 'district': 'Faridkot'},
            {'name': 'GSSS GOLEWALA', 'students': 468, 'girls': 236, 'boys': 232, 'district': 'Faridkot'},
            {'name': 'GHS TEHNA', 'students': 195, 'girls': 95, 'boys': 100, 'district': 'Faridkot'},
        ]
    },
]

# Check for duplicate school: GSSS MUKTSAR (G) WNO.8 MKT appears on Jan 29 AND Jan 31
# Count it as 2 visits (different sessions)

# Calculate new totals
new_schools = 0
new_students = 0
new_girls = 0
new_boys = 0
new_districts = set()
all_new_school_names = []

for day in new_days:
    for school in day['schools']:
        new_schools += 1
        new_students += school['students']
        new_girls += school['girls']
        new_boys += school['boys']
        new_districts.add(school['district'])
        all_new_school_names.append(school['name'])

# Check for duplicate school names in new data
from collections import Counter
name_counts = Counter(all_new_school_names)
duplicates = {k: v for k, v in name_counts.items() if v > 1}

# New unique districts not already in the website
truly_new_districts = new_districts - existing_districts

print(f"\n=== NEW DATA (Jan 22 - Feb 9) ===")
print(f"Days of data: {len(new_days)}")
print(f"School visits: {new_schools}")
print(f"Unique school names: {len(set(all_new_school_names))}")
print(f"New students: {new_students:,}")
print(f"New girls: {new_girls:,}")
print(f"New boys: {new_boys:,}")
print(f"Girls + Boys check: {new_girls + new_boys:,}")
print(f"Districts in new data: {', '.join(sorted(new_districts))}")
print(f"NEW districts (not on website yet): {', '.join(sorted(truly_new_districts)) if truly_new_districts else 'None'}")

if duplicates:
    print(f"\n⚠️  Duplicate school names in new data:")
    for name, count in duplicates.items():
        print(f"   - '{name}' appears {count} times")

# Calculate projected cumulative totals
# For unique schools: current + new unique (excluding duplicates already on website)
# But we can't perfectly check against existing school names without fuzzy matching, 
# so we'll report both visit count and unique count

total_schools = current_schools + len(set(all_new_school_names))  # unique new schools
total_students = current_students + new_students
total_girls = current_girls + new_girls
total_boys = current_boys + new_boys
total_districts = current_districts + len(truly_new_districts)

print(f"\n{'='*50}")
print(f"=== PROJECTED CUMULATIVE TOTALS (through Feb 9) ===")
print(f"{'='*50}")
print(f"Total Schools:    {total_schools}")
print(f"Total Students:   {total_students:,}")
print(f"  Girls:          {total_girls:,}")
print(f"  Boys:           {total_boys:,}")
print(f"Total Districts:  {total_districts}")
print(f"  All districts:  {', '.join(sorted(existing_districts | new_districts))}")

# Day-by-day breakdown
print(f"\n=== DAY-BY-DAY BREAKDOWN ===")
print(f"{'Date':<12} {'Schools':<8} {'Students':<10} {'Girls':<8} {'Boys':<8} {'District'}")
print("-" * 70)
for day in new_days:
    day_students = sum(s['students'] for s in day['schools'])
    day_girls = sum(s['girls'] for s in day['schools'])
    day_boys = sum(s['boys'] for s in day['schools'])
    day_districts = ', '.join(sorted(set(s['district'] for s in day['schools'])))
    print(f"{day['date']:<12} {len(day['schools']):<8} {day_students:<10,} {day_girls:<8,} {day_boys:<8,} {day_districts}")

total_new = sum(sum(s['students'] for s in day['schools']) for day in new_days)
print("-" * 70)
print(f"{'TOTAL':<12} {new_schools:<8} {total_new:<10,} {new_girls:<8,} {new_boys:<8,}")
