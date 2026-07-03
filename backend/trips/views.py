# backend/trips/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from .hos_engine import simulate_truck_trip
from .log_generator import generate_daily_log_base64

def geocode_location(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    headers = {'User-Agent': 'HOS-Assessment-App/1.0'}
    try:
        response = requests.get(url, headers=headers).json()
        if len(response) > 0:
            return (float(response[0]['lon']), float(response[0]['lat']))
    except:
        pass
    return None

def get_osrm_route(start_coords, end_coords):
    coords = f"{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
    url = f"http://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson"
    try:
        data = requests.get(url).json()
        if data.get("routes"):
            route = data["routes"][0]
            return {
                "distance_miles": route["distance"] * 0.000621371,
                "duration_hours": route["duration"] / 3600.0,
                "polyline": route["geometry"]
            }
    except:
        pass
    return None

class TripAnalysisView(APIView):
    def post(self, request):
        curr_loc = request.data.get("current_location", "Los Angeles, CA")
        drop_loc = request.data.get("dropoff_location", "Phoenix, AZ")
        cycle_used = float(request.data.get("current_cycle_used", 0))
        
        start_coords = geocode_location(curr_loc)
        end_coords = geocode_location(drop_loc)
        
        if not start_coords or not end_coords:
            return Response({"error": "Geocoding failed."}, status=status.HTTP_400_BAD_REQUEST)
            
        route_info = get_osrm_route(start_coords, end_coords)
        if not route_info:
            return Response({"error": "Routing failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        simulation_days = simulate_truck_trip(route_info["distance_miles"], cycle_used)
        
        logs_base64 = []
        for day in simulation_days:
            img_str = generate_daily_log_base64(f"Day {day['day']}", day["timeline"])
            logs_base64.append(img_str)
            
        # Swap Long/Lat to Lat/Long for React Leaflet Polyline
        leaflet_coords = [[coord[1], coord[0]] for coord in route_info["polyline"]["coordinates"]]
            
        return Response({
            "route_summary": {
                "total_miles": round(route_info["distance_miles"], 1),
                "estimated_hours": round(route_info["duration_hours"], 1),
            },
            "polyline": leaflet_coords,
            "logs": logs_base64
        }, status=status.HTTP_200_OK)
    
def get_coord_at_percentage(coords, percentage):
    """Interpolates a coordinate along the polyline based on distance percentage."""
    if not coords: return None
    if percentage <= 0: return coords[0]
    if percentage >= 1: return coords[-1]
    idx = int((len(coords) - 1) * percentage)
    return coords[idx]

class TripAnalysisView(APIView):
    def post(self, request):
        curr_loc = request.data.get("current_location", "Los Angeles, CA")
        drop_loc = request.data.get("dropoff_location", "Phoenix, AZ")
        cycle_used = float(request.data.get("current_cycle_used", 0))
        
        start_coords = geocode_location(curr_loc)
        end_coords = geocode_location(drop_loc)
        
        if not start_coords or not end_coords:
            return Response({"error": "Geocoding failed."}, status=status.HTTP_400_BAD_REQUEST)
            
        route_info = get_osrm_route(start_coords, end_coords)
        if not route_info:
            return Response({"error": "Routing failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # Get logs AND stops from the updated engine
        simulation_days, stops_data = simulate_truck_trip(route_info["distance_miles"], cycle_used)
        
        logs_base64 = []
        # Inside backend/trips/views.py loop:
        for day in simulation_days:
            img_str = generate_daily_log_base64(
                log_date=f"Day {day['day']}", 
                status_intervals=day["timeline"], 
                total_trip_miles=route_info["distance_miles"],
                origin_city=curr_loc,   # Pass current location string
                dest_city=drop_loc      # Pass dropoff location string
            )   
            logs_base64.append(img_str)
            
        # Swap Long/Lat to Lat/Long for React Leaflet Polyline
        leaflet_coords = [[coord[1], coord[0]] for coord in route_info["polyline"]["coordinates"]]
        
        # Map the stops to actual physical coordinates on the route
        mapped_stops = []
        for stop in stops_data:
            percentage = min(1.0, stop["mile_mark"] / route_info["distance_miles"]) if route_info["distance_miles"] > 0 else 0
            coord = get_coord_at_percentage(leaflet_coords, percentage)
            if coord:
                mapped_stops.append({
                    "type": stop["type"],
                    "lat": coord[0],
                    "lng": coord[1],
                    "mile_mark": round(stop["mile_mark"], 1)
                })
            
        return Response({
            "route_summary": {
                "total_miles": round(route_info["distance_miles"], 1),
                "estimated_hours": round(route_info["duration_hours"], 1),
                "stops_count": len(simulation_days)
            },
            "polyline": leaflet_coords,
            "stops": mapped_stops, # Send stops to React
            "logs": logs_base64
        }, status=status.HTTP_200_OK)