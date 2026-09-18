"""
Day 58: Web Design School - Bootstrap 5 Framework Showcase Server
Serves responsive Bootstrap 5 web application with grids, cards, carousel, and navbars.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """Renders the responsive TinDog Bootstrap 5 landing page."""
    return render_template("index.html")


if __name__ == "__main__":
    print("🌐 Starting Day 58 Bootstrap 5 Showcase on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
