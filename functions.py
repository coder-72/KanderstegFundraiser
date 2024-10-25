import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta




def extract_numbers(text):
    # Remove commas from the text
    text = text.replace(',', '')
    # Find all numbers in the text and return them as integers
    numbers = re.findall(r'\d+', text)
    return [int(num) for num in numbers]


def get_gofundme_donation_details():
    url = 'https://www.gofundme.com/f/3rd-macclesfield-scouts-and-maasai-explorers-to-kandersteg'

    # Send a GET request to the GoFundMe page
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific div containing the donation details
    donation_element = soup.find('div', {'class': 'progress-meter_progressMeterHeading__A6Slt hrt-text-body-sm'})

    if donation_element:
        # Extract the amount raised and the target amount
        spans = donation_element.find_all('span')
        if len(spans) >= 2:
            amount_raised_text = spans[0].text.strip()
            target_amount_text = spans[1].text.strip()

            # Extract numbers from the text
            amount_raised_numbers = extract_numbers(amount_raised_text)
            target_amount_numbers = extract_numbers(target_amount_text)

            # Assuming the first number found is the relevant amount
            amount_raised = amount_raised_numbers[0] if amount_raised_numbers else None
            target_amount = target_amount_numbers[0] if target_amount_numbers else None
        else:
            amount_raised = None
            target_amount = None
    else:
        amount_raised = None
        target_amount = None

    return amount_raised, target_amount


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

