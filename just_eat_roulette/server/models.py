from enum import Enum

from pydantic import BaseModel


class RestaurantDTO(BaseModel):
    name: str
    url: str
    rating: float
    cuisines: list[str]
    delivery_time: float


class CountryCode(str, Enum):
    uk = "uk"
    ie = "ie"
    dk = "dk"
    es = "es"
    it = "it"
    no = "no"
    au = "au"
    nz = "nz"


class SortMethod(str, Enum):
    delivery_time = "delivery_time"
    rating = "rating"
    none = "none"
