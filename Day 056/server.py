"""
Day 56: Personal Digital Name Card & Portfolio Web App
Demonstrates static asset serving (CSS/images) and Jinja/HTML template rendering.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """Renders the digital CV / Name Card template."""
    return render_template("index.html")


if __name__ == "__main__":
    print("🌐 Launching Day 56 Portfolio Card on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
