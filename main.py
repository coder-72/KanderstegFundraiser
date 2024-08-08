from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
@app.route("/")
def index():
    css = url_for('static', filename='style.css')
    css_general = url_for('static', filename='style_general.css')
    return render_template("index.html", css=css , css_general=css_general)


@app.route("/about")
def about():
    css = url_for('static', filename='style.css')
    css_general = url_for('static', filename='style_general.css')
    return render_template("about.html", css=css , css_general=css_general)

@app.route("/donate")
def donate():
    css = url_for('static', filename='style.css')
    css_general = url_for('static', filename='style_general.css')
    return render_template("donate.html", css=css , css_general=css_general)

@app.route("/events")
def event():
    css = url_for('static', filename='style.css')
    css_general = url_for('static', filename='style_general.css')
    return render_template("events.html", css=css , css_general=css_general)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)