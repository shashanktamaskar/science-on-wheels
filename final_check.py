import json
d = json.load(open('data.json','r',encoding='utf-8'))
schools = sum(len(u['schools']) for u in d['dailyUpdates'])
students = sum(s['studentsReached'] for u in d['dailyUpdates'] for s in u['schools'])
districts = sorted(set(s['district'] for u in d['dailyUpdates'] for s in u['schools']))
dates = sorted(set(u['date'] for u in d['dailyUpdates']))
print(f'Total schools: {schools}')
print(f'Total students: {students}')
print(f'Total districts: {len(districts)}')
print(f'Districts: {districts}')
print(f'Date range: {dates[0]} to {dates[-1]}')
print(f'Total daily updates: {len(d["dailyUpdates"])}')

# Check for missing coords
missing = []
for u in d['dailyUpdates']:
    for s in u['schools']:
        lat = s.get('location',{}).get('lat')
        if lat is None or lat == 0:
            missing.append(f"  {u['date']} - {s['name']}")
if missing:
    print(f'\nSchools with missing coordinates ({len(missing)}):')
    for m in missing:
        print(m)
else:
    print('\nAll schools have coordinates!')
