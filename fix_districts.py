import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

norm = {
    'FATEHGARH Sahib': 'Fatehgarh Sahib',
    'ROOPNAGAR': 'Roopnagar',
}

changes = 0
for update in data.get('dailyUpdates', []):
    for school in update.get('schools', []):
        d = school.get('district', '')
        if d in norm:
            old = d
            school['district'] = norm[d]
            changes += 1
            print(f"  Fixed: {old} -> {norm[old]}")

print(f"\nTotal fixes: {changes}")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Saved data.json")

# Verify
with open('data.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)
districts = set()
for u in data2.get('dailyUpdates', []):
    for s in u.get('schools', []):
        districts.add(s.get('district', ''))
print(f"\nAll districts: {sorted(districts)}")
