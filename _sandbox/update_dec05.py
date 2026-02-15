"""
December 5, 2025 - Update Script
Vehicle 1: GSSS TRIPURI
Vehicle 2: GSSS KALYAN, GSSS MULTIPURPOSE
"""

import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# ============ VEHICLE 1 ============
v1_school = {
    "name": "GSSS TRIPURI",
    "coords": (30.3560228, 76.3899618),
    "students": 973, "girls": 489, "boys": 484,
    "district": "Patiala",
    "galleryLink": "",  # No SharePoint link provided
    "collageImage": "GSSS-TRIPURI.jpg"
}
v1_start = (30.3449167, 76.39775)
v1_end = (30.3449167, 76.39775)
v1_dist = round(haversine(v1_start[0], v1_start[1], v1_school["coords"][0], v1_school["coords"][1]) + 
                haversine(v1_school["coords"][0], v1_school["coords"][1], v1_end[0], v1_end[1]))

# ============ VEHICLE 2 ============
v2_schools = [
    {
        "name": "GSSS KALYAN",
        "coords": (30.3559951, 76.3033439),
        "students": 600, "girls": 270, "boys": 330,
        "district": "Patiala",
        "galleryLink": "",  # No SharePoint link provided
        "collageImage": "GSSS-KALYAN.jpg"
    },
    {
        "name": "GSSS MULTIPURPOSE",
        "coords": (30.3504965, 76.3843538),
        "students": 340, "girls": 90, "boys": 250,
        "district": "Patiala",
        "galleryLink": "",  # No SharePoint link provided
        "collageImage": "GSSS-MULTIPURPOSE.jpg"
    }
]
v2_start = (30.3449167, 76.39775)
v2_end = (30.3449167, 76.39775)
v2_dist = round(
    haversine(v2_start[0], v2_start[1], v2_schools[0]["coords"][0], v2_schools[0]["coords"][1]) +
    haversine(v2_schools[0]["coords"][0], v2_schools[0]["coords"][1], v2_schools[1]["coords"][0], v2_schools[1]["coords"][1]) +
    haversine(v2_schools[1]["coords"][0], v2_schools[1]["coords"][1], v2_end[0], v2_end[1])
)

print("="*60)
print("DECEMBER 5, 2025 - DATA UPDATE")
print("="*60)
print(f"\nVehicle 1:")
print(f"  {v1_school['name']}: {v1_school['students']} students ({v1_school['girls']}G/{v1_school['boys']}B)")
print(f"  Distance: {v1_dist} km")
print(f"\nVehicle 2:")
for s in v2_schools:
    print(f"  {s['name']}: {s['students']} students ({s['girls']}G/{s['boys']}B)")
print(f"  Distance: {v2_dist} km")
print("="*60)

# Load data.json
with open('../data.json', 'r') as f:
    data = json.load(f)

# Create Vehicle 1 entry
v1_entry = {
    "date": "2025-12-05",
    "vehicle": 1,
    "schools": [{
        "name": v1_school["name"],
        "location": {"lat": v1_school["coords"][0], "lng": v1_school["coords"][1]},
        "studentsReached": v1_school["students"],
        "girlsCount": v1_school["girls"],
        "boysCount": v1_school["boys"],
        "district": v1_school["district"],
        "galleryLink": v1_school["galleryLink"],
        "collageImage": v1_school["collageImage"]
    }],
    "route": {
        "startPoint": {"name": "Patiala, Punjab", "lat": v1_start[0], "lng": v1_start[1]},
        "endPoint": {"name": "Patiala, Punjab", "lat": v1_end[0], "lng": v1_end[1]},
        "distanceTravelled": v1_dist
    },
    "totalStudents": v1_school["students"],
    "schoolsVisited": 1
}

# Create Vehicle 2 entry
v2_entry = {
    "date": "2025-12-05",
    "vehicle": 2,
    "schools": [{
        "name": s["name"],
        "location": {"lat": s["coords"][0], "lng": s["coords"][1]},
        "studentsReached": s["students"],
        "girlsCount": s["girls"],
        "boysCount": s["boys"],
        "district": s["district"],
        "galleryLink": s["galleryLink"],
        "collageImage": s["collageImage"]
    } for s in v2_schools],
    "route": {
        "startPoint": {"name": "Patiala, Punjab", "lat": v2_start[0], "lng": v2_start[1]},
        "endPoint": {"name": "Patiala, Punjab", "lat": v2_end[0], "lng": v2_end[1]},
        "distanceTravelled": v2_dist
    },
    "totalStudents": sum(s["students"] for s in v2_schools),
    "schoolsVisited": 2
}

# Insert at beginning of dailyUpdates
data['dailyUpdates'].insert(0, v1_entry)
data['dailyUpdates'].insert(0, v2_entry)

# Update cumulative stats
total_schools = 1 + 2  # V1: 1 school, V2: 2 schools
total_students = v1_school["students"] + sum(s["students"] for s in v2_schools)
total_girls = v1_school["girls"] + sum(s["girls"] for s in v2_schools)
total_boys = v1_school["boys"] + sum(s["boys"] for s in v2_schools)
total_distance = v1_dist + v2_dist

data['mission']['schoolsCovered']['current'] += total_schools
data['mission']['studentsImpacted'] += total_students
data['mission']['genderBreakdown']['girls'] += total_girls
data['mission']['genderBreakdown']['boys'] += total_boys
data['mission']['distanceTravelled'] += total_distance
data['lastUpdated'] = "2025-12-05"

# Save data.json
with open('../data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("\n✅ Updated data.json")

# Update schools-gallery.json
with open('../schools-gallery.json', 'r') as f:
    gallery = json.load(f)

# Add all schools (even without gallery links for now)
all_schools = [v1_school] + v2_schools
for s in all_schools:
    gallery['schools'].append({
        "name": s["name"],
        "district": s["district"],
        "visitDate": "2025-12-05",
        "folderUrl": s["galleryLink"]
    })

with open('../schools-gallery.json', 'w') as f:
    json.dump(gallery, f, indent=4)

print("✅ Updated schools-gallery.json")

# Print summary
print("\n" + "="*60)
print("CUMULATIVE STATS")
print("="*60)
print(f"Schools Covered: {data['mission']['schoolsCovered']['current']}")
print(f"Students Impacted: {data['mission']['studentsImpacted']}")
print(f"Girls: {data['mission']['genderBreakdown']['girls']}")
print(f"Boys: {data['mission']['genderBreakdown']['boys']}")
print(f"Distance: {data['mission']['distanceTravelled']} km")
print("="*60)
