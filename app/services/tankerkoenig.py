from app.stations.schemes import StationsGetSchemes
from app.services.utils import get_coords, edit_response
from core.http_helper import http_helper


async def get_stations(obj: StationsGetSchemes) -> list:
    stmt = obj.model_dump(mode="json", by_alias=True)
    stmt["lat"], stmt["lng"] = get_coords(stmt.pop("address"))
    response = await http_helper.get_response(params=stmt, api_method="list.php")
    return edit_response(response["stations"])
