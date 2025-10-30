import math

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return distance

# Route waypoints
waypoints = [
    (30.6310588, 76.7230178),  # Plaksha University
    (30.679443, 76.6628657),   # GHS-DAPPAR
    (30.4920036, 76.7114194),  # GSSS-LALRU
    (30.6310588, 76.7230178)   # Back to Plaksha
]

# Calculate total distance
total_distance = 0
for i in range(len(waypoints) - 1):
    lat1, lon1 = waypoints[i]
    lat2, lon2 = waypoints[i + 1]
    segment = haversine(lat1, lon1, lat2, lon2)
    print(f"Segment {i+1}: {segment:.2f} km")
    total_distance += segment

print(f"\nTotal distance: {total_distance:.2f} km")
print(f"Rounded distance: {round(total_distance)} km")
