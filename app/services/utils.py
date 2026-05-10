from geopy.geocoders import Nominatim

from app.schemes import StationsGetSchemes

geolocator = Nominatim(user_agent="my_app")

def get_coords(obj: StationsGetSchemes) -> tuple:
    location = geolocator.geocode(obj.address)
    return location.latitude, location.longitude

def edit_response(response: list) -> list:
    for station in response:
        address = (f"{station.pop('postCode', '')} {station.pop('place', '')} "
                   f"{station.pop('street', '')} {station.pop('houseNumber', '')}")
        station["address"] = address
    return response