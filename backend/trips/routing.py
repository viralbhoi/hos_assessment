import requests

def get_route_data(start_coords, end_coords):
    """
    start_coords and end_coords should be tuples: (longitude, latitude)
    OSRM expects format: {longitude},{latitude}
    """
    base_url = "http://router.project-osrm.org/route/v1/driving/"
    coords_string = f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
    
    # We request the geometry as geojson to easily draw the polyline on our Leaflet map later
    url = f"{base_url}{coords_string}?overview=full&geometries=geojson"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("routes"):
            route = data["routes"][0]
            # OSRM returns distance in meters and duration in seconds
            distance_miles = route["distance"] * 0.000621371
            duration_hours = route["duration"] / 3600.0
            geometry = route["geometry"]
            
            return {
                "distance_miles": distance_miles,
                "duration_hours": duration_hours,
                "polyline": geometry
            }
    return None