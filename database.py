import libsql_experimental as libsql
from datetime import datetime
from functions import *

# Authentication and connection details
auth = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3Mjk0NDA1MTgsImlkIjoiMGM5MjE3YTYtYjIwZC00MzYyLTlhZDUtYmU3YzI5NzQyYjgxIn0.kL_ymDIAWf4FyUBnEdOhLjKrxcm-K9R_UYGdrCCNXKWr-WZLg9UKIPgBm_TkdUnFsnCbDH1pDGhPukO0pcGhAQ"
url = "libsql://database-coder-72.turso.io"

# Connect to the remote database
conn = libsql.connect("database.db", sync_interval=30, sync_url=url, auth_token=auth)


def update_stats(stat: str, value: int):
    try:
        # Execute an SQL query to update visit count
        conn.execute('''
            UPDATE visits
            SET visit_count = visit_count + ?
            WHERE endpoint = ?;
        ''', (value, stat))
        conn.sync()  # Synchronize changes to the database
    except Exception as e:
        print(f"Error updating stats: {e}")


def get_stat(stat: str):
    try:
        result = conn.execute('''
            SELECT visit_count FROM visits WHERE endpoint = ?;
        ''', (stat,)).fetchone()
        return result[0] if result else 0  # Return 0 if no result found
    except Exception as e:
        print(f"Error getting stat: {e}")
        return 0


def get_all_stats():
    try:
        result = conn.execute('''
            SELECT * FROM visits;
        ''').fetchall()
        return result
    except Exception as e:
        print(f"Error getting all stats: {e}")
        return []


def reset_stats():
    try:
        conn.execute('''
            UPDATE visits SET visit_count = 0;
        ''')
        conn.sync()  # Synchronize changes to the database
    except Exception as e:
        print(f"Error resetting stats: {e}")


def make_events_accordian():
    html = ""
    events = []

    try:
        result = conn.execute('''
            SELECT * FROM events;
        ''').fetchall()

        for row in result:
            event_date = datetime.strptime(row[2], '%Y-%m-%d')
            events.append(
                {
                    'title': row[0],
                    'description': row[1],
                    'date': event_date
                }
            )

        # Filter future events
        today = datetime.now()
        future_events = [event for event in events if event['date'].date() >= today.date()]
        future_events.sort(key=date_sort)

        # Generate HTML for the Bootstrap accordion
        for index, event in enumerate(future_events):
            badge = ""
            if is_today(today, event['date']):
                badge = '<span class="badge bg-danger">Today</span>'
            elif within_week(today, event['date']):
                badge = '<span class="badge bg-warning">This week</span>'
            elif is_next_week(today, event['date']):
                badge = '<span class="badge bg-info">Next week</span>'

            html += f'''
            <div class="accordion-item">
              <h2 class="accordion-header" id="heading{index}">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
                  {event['title']}&emsp;{badge}
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
    except Exception as e:
        print(f"Error generating events accordion: {e}")

    return html


def get_raw_events():
    try:
        result = conn.execute('''
            SELECT * FROM events;
        ''').fetchall()
        return result
    except Exception as e:
        print(f"Error getting raw events: {e}")
        return []


def close():
    try:
        conn.close()  # Close the connection
    except Exception as e:
        print(f"Error closing connection: {e}")


# Example usage
if __name__ == "__main__":
    # Your test code here
    close()  # Ensure to close the connection at the end
