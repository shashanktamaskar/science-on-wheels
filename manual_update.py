import json

# School 1: GSSS-DHANGERA
school1 = {
    "date": "2025-12-03",
    "name": "GSSS-DHANGERA",
    "district": "Patiala",
    "students": 527,
    "girls": 259,
    "boys": 268,
    "mapLink": "https://maps.app.goo.gl/U39v1Y3UeRBcdmdVA",
    "gallery": "https://plakshauniversity1-my.sharepoint.com/my?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FGallery%2FPATIALA%5FGSSS%5FDHANGERA&viewid=efb56dab%2D8a39%2D4d99%2Db96c%2D40fc250c7320&login_hint=scienceonwheels%40plaksha%2Eedu%2Ein&source=waffle",
    "collage": "GSSS-DHANGERA.jpg",
    "distance": 38  # Round trip
}

# School 2: GSSS-SEONA  
school2 = {
    "date": "2025-12-03",
    "name": "GSSS-SEONA",
    "district": "Patiala",
    "students": 535,
    "girls": 268,
    "boys": 267,
    "mapLink": "https://maps.app.goo.gl/AeKju2mHSQWiQRib8",
    "gallery": "https://plakshauniversity1-my.sharepoint.com/my?id=%2Fpersonal%2Fscienceonwheels%5Fplaksha%5Fedu%5Fin%2FDocuments%2FGallery%2FPATIALA%5FGSSS%5FSEONA&viewid=efb56dab%2D8a39%2D4d99%2Db96c%2D40fc250c7320&login_hint=scienceonwheels%40plaksha%2Eedu%2Ein&source=waffle",
    "collage": "GSSS-SEONA.jpg",
    "distance": 34  # Need to calculate
}

# Load data.json
with open('data.json', 'r') as f:
    data = json.load(f)

# Update cumulative stats for both schools
data['lastUpdated'] = "2025-12-03"
data['mission']['schoolsCovered']['current'] += 2
data['mission']['studentsImpacted'] += (school1['students'] + school2['students'])
data['mission']['genderBreakdown']['girls'] += (school1['girls'] + school2['girls'])
data['mission']['genderBreakdown']['boys'] += (school1['boys'] + school2['boys'])
data['mission']['distanceTravelled'] += (school1['distance'] + school2['distance'])

# Add school 1 to daily updates
entry1 = {
    "date": school1['date'],
    "schoolName": school1['name'],
    "district": school1['district'],
    "students": school1['students'],
    "girls": school1['girls'],
    "boys": school1['boys'],
    "distanceTravelled": school1['distance'],
    "mapLink": school1['mapLink'],
    "collageImage": school1['collage']
}
data['dailyUpdates'].insert(0, entry1)

# Add school 2 to daily updates
entry2 = {
    "date": school2['date'],
    "schoolName": school2['name'],
    "district": school2['district'],
    "students": school2['students'],
    "girls": school2['girls'],
    "boys": school2['boys'],
    "distanceTravelled": school2['distance'],
    "mapLink": school2['mapLink'],
    "collageImage": school2['collage']
}
data['dailyUpdates'].insert(0, entry2)

# Save updated data.json
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("✅ Updated data.json")

# Update schools-gallery.json
with open('schools-gallery.json', 'r') as f:
    gallery = json.load(f)

# Add both schools
gallery['schools'].append({
    "name": school1['name'],
    "district": school1['district'],
    "visitDate": school1['date'],
    "folderUrl": school1['gallery']
})

gallery['schools'].append({
    "name": school2['name'],
    "district": school2['district'],
    "visitDate": school2['date'],
    "folderUrl": school2['gallery']
})

# Save updated schools-gallery.json
with open('schools-gallery.json', 'w') as f:
    json.dump(gallery, f, indent=4)

print("✅ Updated schools-gallery.json")

# Print summary
print("\n=== UPDATE SUMMARY ===")
print(f"Date: {school1['date']}")
print(f"Schools added: 2 ({school1['name']}, {school2['name']})")
print(f"Total students: {school1['students'] + school2['students']}")
print(f"Total distance: {school1['distance'] + school2['distance']} km")
print(f"Collages generated:")
print(f"  - {school1['collage']}")
print(f"  - {school2['collage']}")
