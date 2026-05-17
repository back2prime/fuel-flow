from app.stations.schemes import StationsGetSchemes
from app.services.utils import get_coords, edit_stations_response, edit_station_response
from core.http_helper import http_helper


async def get_stations(obj: StationsGetSchemes) -> list[dict]:
    stmt = obj.model_dump(mode="json", by_alias=True)
    stmt["lat"], stmt["lng"] = get_coords(stmt.pop("address"))
    response = await http_helper.get_response(params=stmt, api_method="list.php")
    return edit_stations_response(response["stations"])


async def get_specific_station(station_id: str) -> dict:
    stmt = {"id": station_id}
    response = await http_helper.get_response(params=stmt, api_method="detail.php")
    return edit_station_response(response["station"])
