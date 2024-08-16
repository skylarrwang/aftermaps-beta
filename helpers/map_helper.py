"""Helps with map output"""
import requests
API_KEY = "AIzaSyBBXtjSysC3I-B05t05wMs6UVfsHpfEzAU"

def get_placeid(lat, long):
    """gets placee's id"""
    # Define the latitude and longitude coordinates
    latlng = f"{lat},{long}"

    # Google Nearest Roads API
    base_url = "https://roads.googleapis.com/v1/nearestRoads"

    # Define the parameters for the API request
    params = {
        "points": latlng,
        "key": API_KEY
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if "snappedPoints" in data:
            snappedPoint = data["snappedPoints"][0]
            return snappedPoint['placeId']
        else:
            return None
    else:
        return response.status_code

def get_address(place_id):
    """get address location"""
    # Google Places API Place Details endpoint
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    # Define the parameters for the API request
    params = {
        "place_id": place_id,
        "fields": "formatted_address",
        "key": API_KEY
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the result is valid and contains a formatted address
        if "result" in data and "formatted_address" in data["result"]:
            formatted_address = data["result"]["formatted_address"]
            return formatted_address
        else:
            return None
    else:
        return response.status_code

def location_details(place_id):
    """gets location details"""
    # Google Places API Place Details endpoint
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    # Define the parameters for the API request
    params = {
        "place_id": place_id,
        "fields": "address_components",
        "key": API_KEY
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the result is valid and contains a formatted address
        if "result" in data and "address_components" in data["result"]:
            address_components = data["result"]["address_components"]
            for component in address_components:
                if "route" in component["types"]:
                    street = component["long_name"]
                elif "postal_code" in component["types"]:
                    zipcode = component["long_name"]
                elif "administrative_area_level_1" in component["types"]:
                    state = component["long_name"]
            return street, zipcode, state
        else:
            return None
    else:
        return response.status_code

def lat_long_validation(curr_lat, curr_long, rep_lat, rep_long):
    """error messages"""
    ## Check location is enabled
    if curr_long == "" or curr_lat == "":
        return "Error: Please enable location tracking."
    if rep_long == "" or rep_lat == "":
        return "Error: Please select a point on the map."
    return None
