from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.openapi.utils import get_openapi

from just_eat_roulette.utils.just_eat import get_restaurants
from just_eat_roulette.utils.transforms import (
    get_weighted_random_choice,
    sort_by_fastest_delivery_time,
    sort_by_highest_rating,
)
from just_eat_roulette import __version__ as api_version

from .models import CountryCode, RestaurantDTO, SortMethod, Response404

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Just Eat Roulette",
        version=api_version,
        description="API for picking a random restaurant from Just Eat to order from",
        contact={
            "name": "GitHub Repository",
            "url": "https://github.com/CalemRoelofs/just-eat-roulette",
        },
        license_info={
            "name": "GNU Affero General Public License v3.0",
            "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
        },
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def redirect_to_docs():
    """Redirects to `/docs` endpoint"""
    return RedirectResponse("/docs", status_code=302)


@app.get(
    "/restaurants",
    response_model=List[RestaurantDTO],
    responses={404: {"model": Response404}},
)
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


@app.get(
    "/restaurants/roulette",
    response_model=RestaurantDTO,
    responses={404: {"model": Response404}},
)
async def random_restaurant(
    lat: float, lon: float, country_code: CountryCode = CountryCode.ie
):
    """Returns a semi-random restaurant, weighted on rating and delivery time"""
    restaurant_list = get_restaurants(lat, lon, country_code)

    if not restaurant_list:
        raise HTTPException(status_code=404, detail="No restaurants found in your area")

    return get_weighted_random_choice(restaurant_list).get_dto_model()
