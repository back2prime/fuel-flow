from geopy.geocoders import Nominatim

from app.stations.schemes import StationsGetSchemes

geolocator = Nominatim(user_agent="my_app")


def get_coords(address: str) -> tuple:
    location = geolocator.geocode(address)
    return round(location.latitude, 3), round(location.longitude, 3)


def edit_address(response: dict) -> dict:
    address = (
        f"{response.pop('postCode', '')} {response.pop('place', '')}"
        f" {response.pop('street', '')} {response.pop('houseNumber','')}"
    )
    response["address"] = address
    return response


def edit_stations_response(response: list[dict]) -> list[dict]:
    result = []
    for station in response:
        if station["isOpen"] and station["price"]:
            edit_address(station)
            result.append(station)
    return result


def edit_station_response(response: dict) -> dict:
    return edit_address(response)


def create_redis_key(obj: StationsGetSchemes, lat: float, lng: float) -> str:
    return f"stations:{str(lat)}:{str(lng)}:{str(obj.radius)}:{obj.fuel_type.value}:{obj.sort_type.value}"
