from just_eat_roulette.utils import transforms
from just_eat_roulette.utils.models import Restaurant
from tests.resources.fixtures import raw_restaurant_list


class TestTransforms:
    def test_process_restaurant_list_maps_results_correctly(self):
        results = transforms.process_restaurant_list(raw_restaurant_list)

        assert len(results) == 3
        assert isinstance(results[0], Restaurant)
        assert results[0].weighted_delivery_time > results[1].weighted_delivery_time

    def test_sort_by_highest_rating_returns_correctly_ordered_list(self):
        restaurant_list = transforms.process_restaurant_list(raw_restaurant_list)

        sorted_by_rating = transforms.sort_by_highest_rating(restaurant_list)

        assert sorted_by_rating[0].name == "test_restaurant_3"
        assert sorted_by_rating[-1].name == "test_restaurant_1"

    def test_sort_by_fastest_delivery_time_returns_correctly_ordered_list(self):
        restaurant_list = transforms.process_restaurant_list(raw_restaurant_list)

        sorted_by_delivery_time = transforms.sort_by_fastest_delivery_time(
            restaurant_list
        )

        assert sorted_by_delivery_time[0].name == "test_restaurant_3"
        assert sorted_by_delivery_time[-1].name == "test_restaurant_2"
