import requests
import requests_cache
from just_eat_roulette.utils.transforms import process_restaurant_list
from just_eat_roulette.utils.models import Restaurant
from just_eat_roulette.server.models import CountryCode

requests_cache.install_cache(
    "just_eat_cache", just_eat_roulette="sqlite", expire_after=180
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows; U; Win 9x 4.90; en-US; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)"
}


def _country_code_to_base_url_adapter(country_code: CountryCode):
    match country_code:
        case [CountryCode.uk]:
            return f"https://uk.api.just-eat.io/discovery/{country_code}/restaurants/enriched"
        case [CountryCode.au, CountryCode.nz]:
            return f"https://aus.api.just-eat.io/discovery/{country_code}/restaurants/enriched"
        case _:
            return f"https://i18n.api.just-eat.io/discovery/{country_code}/restaurants/enriched"


def get_restaurants(
    lat: float, lon: float, country_code: CountryCode = CountryCode.ie
) -> list[Restaurant]:
    BASE_URL = _country_code_to_base_url_adapter(country_code)
    url = BASE_URL + f"?Latitude={lat}&Longitude={lon}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    restaurant_list = response.json()["Restaurants"]
    if not restaurant_list:
        return []
    return process_restaurant_list(restaurant_list)
