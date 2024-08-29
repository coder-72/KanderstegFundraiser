from flask import Flask, render_template, request, redirect, url_for
from functions import *

app = Flask(__name__)
@app.route("/")
def index():
    css = url_for('static', filename='style.css')
    icon = url_for('static', filename='favicon.ico')
    donate = url_for('static', filename='donate-donation-svgrepo-com.svg')
    about = url_for('static', filename='about-filled-svgrepo-com.svg')
    events = url_for('static', filename='month-schedule-time-calendar-checklist-date-svgrepo-com.svg')
    return render_template("index.html", css=css, donate=donate, about=about, events=events, favicon=icon)


@app.route("/about")
def about():
    css = url_for('static', filename='style.css')
    until = time_till()
    return render_template("about.html", css=css, until=until)

@app.route("/donate")
def donate():
    css = url_for('static', filename='style.css')
    amount_raised, target_amount = get_gofundme_donation_details()
    percentage = amount_raised/target_amount *100
    return render_template("donate.html", css=css, amount_raised=amount_raised,
                           target_amount=target_amount, percentage=percentage)

@app.route("/events")
def events():
    css = url_for('static', filename='style.css')
    html = make_events_accordian()
    return render_template("events.html", css=css, html=html)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=3000, debug=True)
