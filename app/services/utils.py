from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app")


def get_coords(address: str) -> tuple:
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


def edit_response(response: list) -> list:
    result = []
    for station in response:
        if station["isOpen"] and station["price"]:
            address = (
                f"{station.pop('postCode', '')} {station.pop('place', '')} "
                f"{station.pop('street', '')} {station.pop('houseNumber', '')}"
            )
            station["address"] = address
            result.append(station)
    return result
