from typing import List

from fastapi import FastAPI, HTTPException

from just_eat_roulette.utils.just_eat import get_restaurants
from just_eat_roulette.utils.transforms import (
    get_weighted_random_choice,
    sort_by_fastest_delivery_time,
    sort_by_highest_rating,
)

from .models import CountryCode, RestaurantDTO, SortMethod

app = FastAPI()


@app.get("/", responses={200: {"hello": "world"}})
async def index():
    return {"message": "hello world"}


@app.get("/restaurants", response_model=List[RestaurantDTO])
async def restaurants(
    lat: float,
    lon: float,
    country_code: CountryCode = CountryCode.ie,
    sort_method: SortMethod = SortMethod.none,
):
    """Returns a list of all restaurants in a given area"""
    restaurant_list = get_restaurants(lat, lon, country_code)

    if not restaurant_list:
        raise HTTPException(status_code=404, detail="No restaurants found in your area")

    if sort_method == SortMethod.delivery_time:
        restaurant_list = sort_by_fastest_delivery_time(restaurant_list)
    elif sort_method == SortMethod.rating:
        restaurant_list = sort_by_highest_rating(restaurant_list)

    return [r.get_dto_model() for r in restaurant_list]


@app.get("/restaurants/roulette", response_model=RestaurantDTO)
async def random_restaurant(
    lat: float, lon: float, country_code: CountryCode = CountryCode.ie
):
    """Returns a semi-random restaurant, weighted on rating and delivery time"""
    restaurant_list = get_restaurants(lat, lon, country_code)

    if not restaurant_list:
        raise HTTPException(status_code=404, detail="No restaurants found in your area")

    return get_weighted_random_choice(restaurant_list).get_dto_model()
