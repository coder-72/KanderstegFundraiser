import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime


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
    donation_element = soup.find('div', {'class': 'progress-meter_progressMeterHeading__A6Slt'})

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






def make_events_accordian():
    csv_path = "events_accordian.csv"
    html = ""
    events = []
    with open(csv_path, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter="|")
        for row in reader:
            event_date = datetime.strptime(row['date'], '%Y-%m-%d')
            events.append(
                {
                    'title': row['title'],
                    'description': row['description'],
                    'date': event_date
                }
            )

    # Filter future events
    today = datetime.now()
    future_events = [event for event in events if event['date'] > today]

    # Generate HTML for the Bootstrap accordion
    for index, event in enumerate(future_events):
        html += f'''
        <div class="accordion-item">
          <h2 class="accordion-header" id="heading{index}">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
              {event['title']}
            </button>
          </h2>
          <div id="collapse{index}" class="accordion-collapse collapse" aria-labelledby="heading{index}" data-bs-parent="#accordion">
            <div class="accordion-body">
              {event['description']}<br>
              <small class="text-muted">{event['date'].strftime('%Y-%m-%d')}</small>
            </div>
          </div>
        </div>
        '''
    return html

