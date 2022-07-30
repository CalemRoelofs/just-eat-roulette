from backend.utils import transforms
from backend.utils.models import Restaurant


class TestTransforms:
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

    def test_process_restaurant_list_maps_results_correctly(self):
        results = transforms.process_restaurant_list(self.raw_restaurant_list)

        assert len(results) == 3
        assert isinstance(results[0], Restaurant)
        assert results[0].weighted_delivery_time > results[1].weighted_delivery_time

    def test_sort_by_highest_rating_returns_correctly_ordered_list(self):
        restaurant_list = transforms.process_restaurant_list(self.raw_restaurant_list)

        sorted_by_rating = transforms.sort_by_highest_rating(restaurant_list)

        assert sorted_by_rating[0].name == "test_restaurant_3"
        assert sorted_by_rating[-1].name == "test_restaurant_1"

    def test_sort_by_fastest_delivery_time_returns_correctly_ordered_list(self):
        restaurant_list = transforms.process_restaurant_list(self.raw_restaurant_list)

        sorted_by_delivery_time = transforms.sort_by_fastest_delivery_time(
            restaurant_list
        )

        assert sorted_by_delivery_time[0].name == "test_restaurant_3"
        assert sorted_by_delivery_time[-1].name == "test_restaurant_2"
