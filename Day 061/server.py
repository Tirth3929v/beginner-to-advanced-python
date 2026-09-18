"""
Day 61: Advanced Forms with Flask-WTF Server
Enforces client & server-side validation and CSRF protection via FlaskForm.
"""

import os
from flask import Flask, render_template, request
from forms import LoginForm

app = Flask(__name__)
# Secret key for CSRF token generation
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "flask_wtf_secret_key_demo_only")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        password = form.password.data.strip()

        # Check against authorized admin credentials
        if email == "admin@email.com" and password == "12345678":
            return render_template("success.html", email=email)
        else:
            return render_template("denied.html", email=email)

    return render_template("login.html", form=form)


if __name__ == "__main__":
    print("🌐 Starting Day 61 Flask-WTF Security Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
