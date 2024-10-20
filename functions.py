import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta




def extract_numbers(text):
    """Extracts numbers from a string and returns them as floats."""
    return [float(s.replace('$', '').replace(',', '')) for s in text.split() if s.replace('.', '', 1).isdigit()]


def within_week(today, date):
    one_week_later = today + timedelta(days=(7-today.weekday()))

    # Check if the target date is within the next week
    within_next_week = today <= date < one_week_later

    return within_next_week
def is_today(today, date):
    same_day = today.date() == date.date()
    return same_day

def is_tomorrow(today, date):
    tomorrow = date.date() + timedelta(days=1)
    same_day = today.date() == tomorrow
    return same_day

def is_next_week(today, date):
    start_of_next_week = today + timedelta(days=(7 - today.weekday()))

    end_of_next_week = start_of_next_week + timedelta(days=6)

    is_next_week = start_of_next_week <= date <= end_of_next_week

    return is_next_week

def date_sort(event):
    return event["date"].timestamp()


def time_till():
    today = datetime.now()

    date = datetime(2025, 8, 15, 0, 0)  # Replace with your target date and time

    time_difference = date - today

    # Extract days and hours from the timedelta object
    days = time_difference.days
    hours = time_difference.seconds // 3600
    return f"{days} days {hours} hrs "
