from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from database import get_all_stats, update_stats, make_events_accordian, get_raw_events, close
from functions import *
from tabulate import tabulate

app = Flask(__name__, static_folder='static')
@app.route("/")
def index():
    css = url_for('static', filename='style.css')
    icon = url_for('static', filename='favicon.ico')
    donate = url_for('static', filename='donate-donation-svgrepo-com.svg')
    about = url_for('static', filename='about-filled-svgrepo-com.svg')
    events = url_for('static', filename='month-schedule-time-calendar-checklist-date-svgrepo-com.svg')
    update_stats("index", 1)
    return render_template("index.html", css=css, donate=donate, about=about, events=events, favicon=icon)


@app.route("/about")
def about():
    css = url_for('static', filename='style.css')
    until = time_till()
    update_stats("about", 1)
    return render_template("about.html", css=css, until=until)

@app.route("/donate")
def donate():
    css = url_for('static', filename='style.css')
    amount_raised, target_amount = get_gofundme_donation_details()
    percentage = amount_raised/target_amount *100
    update_stats("donate", 1)
    return render_template("donate.html", css=css, amount_raised=amount_raised,
                           target_amount=target_amount, percentage=percentage)

@app.route("/events")
def events():
    css = url_for('static', filename='style.css')
    html = make_events_accordian()
    update_stats("events", 1)
    return render_template("events.html", css=css, html=html)

@app.route("/donate/redirect")
def donate_redirect():
    update_stats("donate_button", 1)
    return redirect("https://www.gofundme.com/f/3rd-macclesfield-scouts-and-maasai-explorers-to-kandersteg")

@app.route("/admin/stats")
def stats():

    visits = str(tabulate(get_all_stats(), tablefmt='html'))
    events = str(tabulate(get_raw_events(), tablefmt='html'))
    table = visits + "<br>" + events
    return table

@app.route("/admin/post", methods=['POST'])
def post_ping():
    if request.method == 'POST':
        ping_info = request.get_json()['ping_info']
        get_all_stats()
    return "ping successful"

@app.route('/sitemap.xml')
@app.route('/robots.txt')
def static_from_root():
 return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=3000)
