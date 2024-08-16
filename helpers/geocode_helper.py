"""Helps with geocoding"""
from collections import defaultdict
from math import radians, cos, sin, sqrt, atan2
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_location():
    """Gets location with api"""
    try:
        #sends a request to the ipinfo.io API
        response = requests.get('https://ipinfo.io/json?token=7a7d575864e938')
        response.raise_for_status()
        data = response.json()
        location_data = {
            'ip': data.get('ip'),
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'latitude': data.get('loc').split(',')[0] if data.get('loc') else None,
            'longitude': data.get('loc').split(',')[1] if data.get('loc') else None
        }

        return location_data
    #exception error
    except requests.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None

#pass in address
def get_longitude_latitude(address):
    """Converts an address to longitude and latitude coordinates."""
    #uses the third geocoder in this program! nominatim is really good with long/lat converion
    geolocator = Nominatim(user_agent="Droneappdevelopement")
    #convert
    location = geolocator.geocode(address)
    if location:
        return (location.longitude, location.latitude)
    else:
        return None

"""
These two functions are not nessecary for now but here to potentially make integration easier 
"""
def count_blockages_within_radius(blockages, radius=100):
    """Counts blockages within a specified radius."""
    blockage_counter = defaultdict(int)

    #goes through dictionary and sees which ones are withi 100 feet of each other
    for i, (lon1, lat1) in enumerate(blockages):
        for j, (lon2, lat2) in enumerate(blockages):
            if i != j:
                distance = geodesic((lat1, lon1), (lat2, lon2)).feet
                if distance <= radius:
                    blockage_counter[(lon1, lat1)] += 1

    #takes central point of cluster
    for point, count in blockage_counter.items():
        central_lon, central_lat = point
        print(f"Blockage at ({central_lon}, {central_lat}) has {count} blockages within {radius} feet")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculates distance between two points while accounting for earth's shape
    """
    #radius of the Earth in kilometers
    R = 6371.0

    #convert from degrees to radians
    lon1_rad = radians(lon1)
    lat1_rad = radians(lat1)
    lon2_rad = radians(lon2)
    lat2_rad = radians(lat2)

    #difference in coordinates
    difflon = lon2_rad - lon1_rad
    difflat = lat2_rad - lat1_rad

    #haversine formula finds the distance
    a = sin(difflat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(difflon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    #distance in kilometers
    distance_kilometer = R * c

    #convert from kilometers to feet
    distance_feet = distance_kilometer * 3280.84

    return distance_feet
