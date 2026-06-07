from enum import Enum


class FuelType(str, Enum):
    diesel = "diesel"
    e5 = "e5"
    e10 = "e10"


class SortType(str, Enum):
    price = "price"
    dist = "dist"
