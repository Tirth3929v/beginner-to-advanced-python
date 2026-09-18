"""
Day 62: Coffee & Wifi Rating Project Server
Flask web application combining WTForms input validation with CSV data persistence.
"""

import os
import csv
from flask import Flask, render_template, redirect, url_for
from forms import CafeForm

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "coffee_wifi_secret_key_demo")

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cafe-data.csv")


def load_cafes():
    with open(CSV_PATH, newline="", encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        return list(csv_data)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    list_of_rows = load_cafes()
    return render_template("cafes.html", cafes=list_of_rows)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = [
            form.cafe.data.strip(),
            form.location.data.strip(),
            form.open_time.data.strip(),
            form.closing_time.data.strip(),
            form.coffee_rating.data,
            form.wifi_rating.data,
            form.power_rating.data
        ]
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(new_row)
        return redirect(url_for("cafes"))

    return render_template("add.html", form=form)


if __name__ == "__main__":
    print("🌐 Starting Day 62 Coffee & Wifi Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
