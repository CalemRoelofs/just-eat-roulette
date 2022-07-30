import random

from just_eat_roulette.utils.models import Restaurant


def _scale_between(
    unscaledNum: float, minAllowed: int, maxAllowed: int, min: float, max: float
):
    return (maxAllowed - minAllowed) * (unscaledNum - min) / (max - min) + minAllowed


def set_weighted_delivery_times(restaurant_list: list[Restaurant]) -> list[Restaurant]:
    """Sets the `weighted_delivery_time` to a value between 1 - 10.
    Weight is calculated by finding the min and max of all delivery times,
    then proportionally applying a score between 1 - 10 according to how
    close the delivery time is to the max value of the set.
    High delivery time -> closer to 1
    Low delivery time -> closer to 10

    Args:
        restaurant_list (list[Restaurant])

    Returns:
        list[Restaurant]: Restaurants with the `weighted_delivery_time` value set
    """
    all_delivery_times = [r.delivery_time for r in restaurant_list]
    dt_min = min(all_delivery_times)
    dt_max = max(all_delivery_times)

    for r in restaurant_list:
        r.weighted_delivery_time = 10 - _scale_between(
            r.delivery_time, 1, 10, dt_min, dt_max
        )
    return restaurant_list


def process_restaurant_list(raw_restaurant_list: list[dict]) -> list[Restaurant]:
    """Takes the raw response from Just Eat API and processes the list
    of restaurants into a list of `Restaurant` objects

    Args:
        raw_restaurant_list (list[dict]): List of restaurants from the Just Eat API

    Returns:
        list[Restaurant]: List of Restaurant objects
    """
    results = []
    for restaurant in raw_restaurant_list:
        if (
            restaurant["IsDelivery"] == False
            or restaurant["IsOpenNowForDelivery"] == False
        ):
            continue

        result = Restaurant(
            **{
                "name": restaurant["Name"],
                "url": restaurant["Url"],
                "rating": restaurant["RatingAverage"],
                "cuisines": [x["Name"] for x in restaurant["Cuisines"]],
                "delivery_time": restaurant["DeliveryEtaMinutes"]["RangeUpper"]
                + restaurant["DeliveryEtaMinutes"]["RangeLower"] / 2,
            }
        )

        results.append(result)

    return set_weighted_delivery_times(results)


def sort_by_fastest_delivery_time(
    restaurant_list: list[Restaurant],
) -> list[Restaurant]:
    """Returns a sorted list of Restaurants ordered by fastest delivery time"""
    return sorted(restaurant_list, key=lambda k: k.delivery_time)


def sort_by_highest_rating(restaurant_list: list[Restaurant]) -> list[Restaurant]:
    """Returns a sorted list of Restaurants ordered by highest rating"""
    return list(sorted(restaurant_list, key=lambda k: k.rating, reverse=True))


def get_weighted_random_choice(restaurant_list: list[Restaurant]) -> Restaurant:
    """Chooses a Restaurant randomly, weighted by

    Args:
        restaurant_list (list[Restaurant]): _description_

    Returns:
        Restaurant: The chosen Restaurant
    """
    weights = [
        restaurant.rating * restaurant.weighted_delivery_time
        for restaurant in restaurant_list
    ]

    return random.choices(population=restaurant_list, weights=weights, k=1)[0]
