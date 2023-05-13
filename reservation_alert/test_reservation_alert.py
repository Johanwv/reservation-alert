# -*- coding: utf-8 -*-
import os
import unittest

from reservation_alert import get_data_from_api, is_bookable_date, NO_BOOKABLE_MONTH_MESSAGE, \
    find_month_with_bookable_date, should_message_be_send, email_addresses, call_function_every_x_seconds, \
    is_one_day


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
                "status": 3,
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

    def test_find_month_with_bookable_date(self):
        self.assertEqual(NO_BOOKABLE_MONTH_MESSAGE, find_month_with_bookable_date())

    def test_when_message_is_no_bookable_month_then_no_email_should_send(self):
        self.assertTrue(should_message_be_send(NO_BOOKABLE_MONTH_MESSAGE))

    def test_when_always_send_email_is_true_then_email_should_send(self):
        os.environ["ALWAYS_SEND_EMAIL"] = "true"

        self.assertTrue(should_message_be_send(NO_BOOKABLE_MONTH_MESSAGE))

    def test_when_multiple_email_addresses_are_passed_then_they_are_returned_by_get_email_addresses(self):
        os.environ["MAIL_RECIPIENTS"] = "test1@mail.com,test2@mail.com"

        self.assertEqual(["test1@mail.com", "test2@mail.com"], email_addresses())

    def test_when_time_is_one_hundredth_of_a_second_then_function_is_called_ten_times(self):
        counter = 0

        def increment_counter():
            nonlocal counter
            counter += 1
            return True

        call_function_every_x_seconds(increment_counter, 0.01)

        self.assertEqual(counter, 10)

    def test_when_more_than_one_day_has_passed_return_true(self):
        total_seconds = 60 * 60 * 24 + 1
        self.assertTrue(is_one_day(total_seconds))

    def test_when_less_than_one_day_has_passed_return_false(self):
        total_seconds = 60 * 60
        self.assertFalse(is_one_day(total_seconds))


if __name__ == '__main__':
    unittest.main()
