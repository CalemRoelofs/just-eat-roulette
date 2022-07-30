from tabulate import tabulate
from server.models import RestaurantDTO


class Restaurant:
    """A restaurant on Just Eat

    name (str): Name of the restaurant
    url (str): The Just Eat url for the restaurant
    rating (float): Star rating out of 6
    cuisines (list[str]): e.g. ['Turkish', 'Pizza']
    delivery_time (float): Average expected delivery time
    weighted_delivery_time (float): See `utils.set_weighted_delivery_times`
    """

    def __init__(
        self,
        name: str,
        url: str,
        rating: float,
        cuisines: list[str],
        delivery_time: float,
        weighted_delivery_time: float = 10.0,
    ):
        self.name: str = name
        self.url: str = url
        self.rating: float = rating
        self.cuisines: list[str] = cuisines
        self.delivery_time: float = delivery_time
        self.weighted_delivery_time: float = weighted_delivery_time

    def __repr__(self):
        return tabulate(
            [
                ["Restaurant", self.name],
                ["URL", self.url],
                ["Cuisines", ", ".join(self.cuisines)],
                ["Rating", self.rating],
                ["Delivery Time", f"{self.delivery_time} minutes"],
                ["Weighted Delivery Time", self.weighted_delivery_time],
            ]
        )

    def get_dto_model(self) -> RestaurantDTO:
        return RestaurantDTO(
            name=self.name,
            url=self.url,
            rating=self.rating,
            cuisines=self.cuisines,
            delivery_time=self.delivery_time,
        )
