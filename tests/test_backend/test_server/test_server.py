from fastapi.testclient import TestClient
from just_eat_roulette.server.server import app
from just_eat_roulette.utils.models import Restaurant


client = TestClient(app)

raw_restaurant_list = [
    {
        "Name": "test_restaurant_1",
        "Url": "http://test.url/1",
        "RatingAverage": 2.8,
        "Cuisines": [{"Name": "Pizza"}, {"Name": "Italian"}],
        "DeliveryEtaMinutes": {"RangeLower": 15, "RangeUpper": 30},
        "IsDelivery": True,
        "IsOpenNowForDelivery": True,
    },
    {
        "Name": "test_restaurant_2",
        "Url": "http://test.url/2",
        "RatingAverage": 4.3,
        "Cuisines": [{"Name": "Salad"}, {"Name": "Vegan"}],
        "DeliveryEtaMinutes": {"RangeLower": 75, "RangeUpper": 150},
        "IsDelivery": True,
        "IsOpenNowForDelivery": True,
    },
    {
        "Name": "test_restaurant_3",
        "Url": "http://test.url/3",
        "RatingAverage": 6.0,
        "Cuisines": [{"Name": "Salad"}, {"Name": "Vegan"}],
        "DeliveryEtaMinutes": {"RangeLower": 10, "RangeUpper": 25},
        "IsDelivery": True,
        "IsOpenNowForDelivery": True,
    },
    {
        "Name": "test_restaurant_4_!IsDelivery",
        "Url": "http://test.url/4",
        "RatingAverage": 0.1,
        "Cuisines": [{"Name": "Misery"}, {"Name": "Suffering"}],
        "DeliveryEtaMinutes": {"RangeLower": 1000, "RangeUpper": 10000},
        "IsDelivery": False,
        "IsOpenNowForDelivery": True,
    },
    {
        "Name": "test_restaurant_5_!IsOpenNowForDelivery",
        "Url": "http://test.url/5",
        "RatingAverage": 0.1,
        "Cuisines": [{"Name": "Misery"}, {"Name": "Suffering"}],
        "DeliveryEtaMinutes": {"RangeLower": 1000, "RangeUpper": 10000},
        "IsDelivery": True,
        "IsOpenNowForDelivery": False,
    },
]


def test_get_index_returns_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "hello world"


def test_restaurants_returns_process_list_of_restaurants(requests_mock):
    requests_mock.get(
        "/discovery/ie/restaurants/enriched", json={"Restaurants": raw_restaurant_list}
    )

    response = client.get("/restaurants?lat=0&lon=0")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "test_restaurant_1"


def test_restaurants_when_no_results_returns_404(requests_mock):
    requests_mock.get("/discovery/ie/restaurants/enriched", json={"Restaurants": []})

    response = client.get("/restaurants?lat=0&lon=0")
    assert response.status_code == 404
    assert response.json()["detail"] == "No restaurants found in your area"


def test_random_restaurant_returns_restaurant(requests_mock):
    requests_mock.get(
        "/discovery/ie/restaurants/enriched", json={"Restaurants": raw_restaurant_list}
    )
    restaurant_names = [r["Name"] for r in raw_restaurant_list]

    response = client.get("/restaurants/roulette?lat=0&lon=0")
    assert response.status_code == 200
    assert response.json()["name"] in restaurant_names
