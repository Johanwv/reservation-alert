import calendar
import os

import requests

from send_alert import send_email


def get_data_from_api(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ValueError(f"Error getting data from API. Status code: {response.status_code}")


def is_bookable_date(json_array):
    for obj in json_array:
        if obj["status"] != 1 and obj["status"] != 2 and obj["status"] != 6:
            return True
    return False


if __name__ == '__main__':
    for month_number in range(1, 2):
        api_endpoint = f"https://widget-api.formitable.com/api/availability/bb6b9cdd/monthWeeks/{month_number}/2023/2/nl"
        data = get_data_from_api(api_endpoint)

        month_name = calendar.month_name[month_number]

        message = f"In {month_name} there is {'a' if is_bookable_date(data) else 'no'} bookable date"
        print(message)

        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_PASSWORD')
        to = os.environ.get('MAIL_RECIPIENT')
        subject = 'Mogelijk plekken beschikbaar bij de nieuwe winkel!'
        body = f"{message}! https://denieuwewinkel.com/"

        send_email(gmail_user, gmail_password, to, subject, body)
