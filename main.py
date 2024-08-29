from flask import Flask, render_template, request, redirect, url_for

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
    return render_template("about.html", css=css)

@app.route("/donate")
def donate():
    css = url_for('static', filename='style.css')
    return render_template("donate.html", css=css)

@app.route("/events")
def events():
    css = url_for('static', filename='style.css')

    return render_template("events.html", css=css)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=3000, debug=True)
