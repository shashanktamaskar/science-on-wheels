import json

d = json.load(open('data.json', 'r', encoding='utf-8'))

# Search for any Ferozepur/Firozpur/Firozepur variant
for u in d['dailyUpdates']:
    for s in u['schools']:
        dist = s['district'].lower()
        if 'fir' in dist or 'fer' in dist or 'fiz' in dist or 'fero' in dist:
            print(f"{u['date']} - {s['name']} - {s['district']}")

print("\n--- All unique districts ---")
districts = sorted(set(s['district'] for u in d['dailyUpdates'] for s in u['schools']))
for d_name in districts:
    print(f"  {d_name}")
