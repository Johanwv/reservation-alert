import unittest

from src.reservation_alert import get_data_from_api, is_bookable_date


class TestGetDataFromAPI(unittest.TestCase):
    def test_get_data_from_api(self):
        api_endpoint = 'https://widget-api.formitable.com/api/availability/bb6b9cdd/monthWeeks/9/2023/2/nl'
        actual_data = get_data_from_api(api_endpoint)

        expected_number_of_days = 35
        self.assertEqual(expected_number_of_days, len(actual_data))

    def test_check_status_returns_true(self):
        reservation_days = [
            {
                "date": "2023-08-27T22:00:00Z",
                "status": 1,
            },
            {
                "date": "2023-08-28T22:00:00Z",
                "status": 2,
            },
        ]

        result = is_bookable_date(reservation_days)
        self.assertEqual(result, True)

    def test_check_status_returns_false(self):
        reservation_days = [
            {
                "date": "2023-08-27T22:00:00Z",
                "status": 1,
            },
            {
                "date": "2023-08-28T22:00:00Z",
                "status": 6,
            },
        ]

        result = is_bookable_date(reservation_days)
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
