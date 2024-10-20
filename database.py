import libsql_experimental as libsql
from functions import *
import os

auth = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3Mjk0NDA1MTgsImlkIjoiMGM5MjE3YTYtYjIwZC00MzYyLTlhZDUtYmU3YzI5NzQyYjgxIn0.kL_ymDIAWf4FyUBnEdOhLjKrxcm-K9R_UYGdrCCNXKWr-WZLg9UKIPgBm_TkdUnFsnCbDH1pDGhPukO0pcGhAQ"
url = "libsql://database-coder-72.turso.io"

conn = libsql.connect("database.db",sync_interval=30, sync_url=url,
                      auth_token=auth)
conn.sync()

def update_stats(stat:str, value:int):


    # Execute an SQL query (example: creating a table)
    conn.execute(f'''
        UPDATE visits
        SET visit_count = {get_stat(stat) + value}
        WHERE endpoint = '{stat}';
    ''')

    # Commit changes to the database
    conn.commit()

def get_stat(stat:str):
    result = conn.execute(f'''
        SELECT visit_count FROM visits WHERE endpoint = '{stat}';
    ''').fetchone()
    conn.commit()
    return result[0]

def get_all_stats():
    result = conn.execute(f'''
            SELECT * FROM visits;
        ''').fetchall()
    conn.commit()
    return result

def reset_stats():
    conn.execute(f'''
                UPDATE visits SET visit_count = 0;
            ''')
    conn.commit()

def make_events_accordian():
    html = ""
    events = []

    result = conn.execute(f'''
                SELECT * FROM events;
''').fetchall()
    for row in result:
        event_date = datetime.strptime(row[2], '%Y-%m-%d')
        events.append(
            {
                'title': row[0],
                'description': row[1],
                'date': event_date
            })

    # Filter future events
    today = datetime.now()
    future_events = [event for event in events if event['date'].date() >= today.date()]
    future_events.sort(key=date_sort)

    # Generate HTML for the Bootstrap accordion
    for index, event in enumerate(future_events):
        if is_today(today, event['date']):
            html += f'''
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{index}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
                  {event['title']}&emsp;
                  <span class="badge bg-danger">Today</span>
                </button>
              </h2>
              <div id="collapse{index}" class="accordion-collapse collapse" aria-labelledby="heading{index}" data-bs-parent="#accordion">
                <div class="accordion-body">
                  <strong>Description:</strong> {event['description']}<br>
                  <small class="text-muted">{event['date'].strftime('%Y-%m-%d')}</small>
                </div>
              </div>
            </div>
            '''
        elif within_week(today, event['date']):
            html += f'''
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{index}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
                  {event['title']}&emsp;
                  <span class="badge bg-warning">This week</span>
                </button>
              </h2>
              <div id="collapse{index}" class="accordion-collapse collapse" aria-labelledby="heading{index}" data-bs-parent="#accordion">
                <div class="accordion-body">
                  <strong>Description:</strong> {event['description']}<br>
                  <small class="text-muted">{event['date'].strftime('%Y-%m-%d')}</small>
                </div>
              </div>
            </div>
            '''
        elif is_next_week(today, event['date']):
            html += f'''
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{index}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
                  {event['title']}&emsp;
                  <span class="badge bg-info">Next week</span>
                </button>
              </h2>
              <div id="collapse{index}" class="accordion-collapse collapse" aria-labelledby="heading{index}" data-bs-parent="#accordion">
                <div class="accordion-body">
                  <strong>Description:</strong> {event['description']}<br>
                  <small class="text-muted">{event['date'].strftime('%Y-%m-%d')}</small>
                </div>
              </div>
            </div>
            '''
        else:
            html += f'''
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{index}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
                  {event['title']}
                </button>
              </h2>
              <div id="collapse{index}" class="accordion-collapse collapse" aria-labelledby="heading{index}" data-bs-parent="#accordion">
                <div class="accordion-body">
                  <strong>Description:</strong> {event['description']}<br>
                  <small class="text-muted">{event['date'].strftime('%Y-%m-%d')}</small>
                </div>
              </div>
            </div>
            '''
    return html

def get_raw_events():
    result = conn.execute(f'''
                    SELECT * FROM events;
    ''').fetchall()
    return result

def close():
    # Close the cursor and connection
    conn.close()
