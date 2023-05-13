# -*- coding: utf-8 -*-
import calendar
import logging
import os
import time

import requests

from send_alert import send_email

NO_BOOKABLE_MONTH_MESSAGE = 'No bookable month was found! :-('
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


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
            logger.info(message)
            return message

    return NO_BOOKABLE_MONTH_MESSAGE


def should_message_be_send(bookable_month_message):
    if bookable_month_message is not NO_BOOKABLE_MONTH_MESSAGE or os.environ.get('ALWAYS_SEND_EMAIL') == 'true':
        return True
    return False


def email_addresses():
    return os.environ.get('MAIL_RECIPIENTS').split(',')


def is_one_day(seconds_passed):
    seconds_in_a_day = 60 * 60 * 24
    return seconds_passed > seconds_in_a_day


def call_function_every_x_seconds(func, seconds_to_wait):
    number_of_notifications = 0
    counter = 0

    while True and number_of_notifications < 10:
        if func():
            number_of_notifications += 1
        if is_one_day(seconds_to_wait * counter):
            message = find_month_with_bookable_date()
            send_email(gmail_user(), gmail_password(), email_addresses()[0], 'Health check', get_body(message))
            counter = 0
        time.sleep(seconds_to_wait)  # Delay for x seconds before the next function call
        counter += 1


def gmail_password():
    return os.environ.get('GMAIL_PASSWORD')


def gmail_user():
    return os.environ.get('GMAIL_USER')


def get_body(message):
    return f"{message} https://denieuwewinkel.com/"


def main():
    message = find_month_with_bookable_date()
    if should_message_be_send(message):
        for email_address in email_addresses():
            to = email_address
            subject = 'Mogelijk plekken beschikbaar bij de nieuwe winkel!'
            body = get_body(message)

            send_email(gmail_user(), gmail_password(), to, subject, body)
    else:
        logger.info('No email was sent')

    return True


if __name__ == '__main__':
    seconds = int(os.environ.get('INTERVAL')) if os.environ.get('INTERVAL') is not None else 300
    logger.info(f"Interval is {seconds} seconds")
    call_function_every_x_seconds(main, seconds)
