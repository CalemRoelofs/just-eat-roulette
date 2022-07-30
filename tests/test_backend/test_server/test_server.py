from fastapi.testclient import TestClient

from just_eat_roulette.server.server import app
from tests.resources.fixtures import raw_restaurant_list


client = TestClient(app)


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


def test_random_restaurant_when_no_results_returns_404(requests_mock):
    requests_mock.get("/discovery/ie/restaurants/enriched", json={"Restaurants": []})

    response = client.get("/restaurants/roulette?lat=0&lon=0")
    assert response.status_code == 404
    assert response.json()["detail"] == "No restaurants found in your area"
