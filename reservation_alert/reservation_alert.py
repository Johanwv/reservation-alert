# -*- coding: utf-8 -*-
import calendar
import os
import time

import requests

from send_alert import send_email

NO_BOOKABLE_MONTH_MESSAGE = 'No bookable month was found! :-('


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


def find_month_with_bookable_date():
    for month_number in range(8, 13):
        api_endpoint = f"https://widget-api.formitable.com/api/availability/bb6b9cdd/monthWeeks/{month_number}/2023/2/nl"
        data = get_data_from_api(api_endpoint)

        month_name = calendar.month_name[month_number]

        if is_bookable_date(data):
            message = f"In {month_name} there is a bookable date"
            print(message)
            return message

    return NO_BOOKABLE_MONTH_MESSAGE


def should_message_be_send(bookable_month_message):
    if bookable_month_message is not NO_BOOKABLE_MONTH_MESSAGE or os.environ.get('ALWAYS_SEND_EMAIL') == 'true':
        return True
    return False


def email_addresses():
    return os.environ.get('MAIL_RECIPIENTS').split(',')


def call_function_every_x_seconds(func, seconds):
    number_of_notifications = 0

    while True and number_of_notifications < 10:
        if func():
            number_of_notifications += 1
        time.sleep(seconds)  # Delay for x seconds before the next function call


def main():
    message = find_month_with_bookable_date()
    if should_message_be_send(message):
        for email_address in email_addresses():
            gmail_user = os.environ.get('GMAIL_USER')
            gmail_password = os.environ.get('GMAIL_PASSWORD')
            to = email_address
            subject = 'Mogelijk plekken beschikbaar bij de nieuwe winkel!'
            body = f"{message} https://denieuwewinkel.com/"

            send_email(gmail_user, gmail_password, to, subject, body)
    else:
        print('No email was sent')

    return True


if __name__ == '__main__':
    seconds = int(os.environ.get('INTERVAL')) if os.environ.get('INTERVAL') is not None else 300
    print(f"Interval is {seconds} seconds")
    call_function_every_x_seconds(main, seconds)
