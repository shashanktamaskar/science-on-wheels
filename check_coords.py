
import json

def check_coords():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        missing = []
        total_schools = 0
        valid_schools = 0
        
        for update in data.get('dailyUpdates', []):
            date = update.get('date', 'Unknown Date')
            for school in update.get('schools', []):
                total_schools += 1
                loc = school.get('location', {})
                lat = loc.get('lat')
                lng = loc.get('lng')
                
                # Check for 0, None, or empty values
                if not lat or not lng or (lat == 0 and lng == 0):
                    missing.append({
                        'date': date,
                        'name': school.get('name', 'Unknown'),
                        'map_url': school.get('mapLink', 'No Link') # Assuming mapLink might be stored or I can check input
                    })
                else:
                    valid_schools += 1

        print(f"Total Schools Processed: {total_schools}")
        print(f"Valid Coordinates: {valid_schools}")
        print(f"Missing Coordinates: {len(missing)}")
        
        if missing:
            print("\nSchools with missing coordinates:")
            for m in missing:
                print(f"  {m['date']} - {m['name']}")
                
    except Exception as e:
        print(f"Error reading or processing data.json: {e}")

if __name__ == "__main__":
    check_coords()
