"""
Day 60: POST Requests with Flask & HTML Forms Server
Processes inbound form data from HTTP POST requests, triggers notification
pipeline, and renders dynamic submission feedback.
"""

from flask import Flask, render_template, request
from email_notifier import ContactNotifier

app = Flask(__name__)
notifier = ContactNotifier()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        record = notifier.process_submission(name, email, phone, message)
        return render_template("contact.html", msg_sent=True, form_data=record)

    return render_template("contact.html", msg_sent=False, form_data={})


if __name__ == "__main__":
    print("🌐 Starting Day 60 Flask POST Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
