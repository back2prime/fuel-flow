from enum import Enum


class FuelType(str, Enum):
    diesel = "diesel"
    e5 = "e5"
    e10 = "e10"


class SortType(str, Enum):
    price = "price"
    dist = "dist"


class ResponseKey(str, Enum):
    STATION = "station"
    STATIONS = "stations"


class CachePrefix(str, Enum):
    STATION = "station:detail"
    STATIONS = "stations:search"


class ApiMethod(str, Enum):
    STATION = "detail.php"
    STATIONS = "list.php"
