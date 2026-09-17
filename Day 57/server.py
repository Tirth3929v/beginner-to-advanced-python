"""
Day 57: Jinja Templating & Blog Engine Server
Demonstrates dynamic server-side template rendering, url_for generation,
external API integration (Agify & Genderize), and dynamic URL parameters.
"""

import os
import json
import datetime
import requests
from flask import Flask, render_template, abort
from post import Post

app = Flask(__name__)

# Load blog posts data
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "posts.json")


def load_all_posts():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Post.from_dict(item) for item in data]
    except Exception:
        return []


ALL_POSTS = load_all_posts()


@app.route("/")
def home():
    current_year = datetime.datetime.now().year
    return render_template("index.html", year=current_year, num_posts=len(ALL_POSTS))


@app.route("/guess/<name>")
def guess_demographics(name):
    # Fetch predicted age from Agify
    try:
        agify_res = requests.get(f"https://api.agify.io?name={name}", timeout=4)
        age = agify_res.json().get("age", 25) if agify_res.status_code == 200 else 25
    except Exception:
        age = 28

    # Fetch predicted gender from Genderize
    try:
        gender_res = requests.get(f"https://api.genderize.io?name={name}", timeout=4)
        gender = gender_res.json().get("gender", "neutral") if gender_res.status_code == 200 else "neutral"
    except Exception:
        gender = "ambassador"

    return render_template("guess.html", name=name, gender=gender or "neutral", age=age or 25)


@app.route("/blog")
def get_blog():
    return render_template("blog.html", all_posts=ALL_POSTS)


@app.route("/post/<int:index>")
def get_post(index):
    for post in ALL_POSTS:
        if post.id == index:
            return render_template("post.html", post=post)
    abort(404)


if __name__ == "__main__":
    print("🌐 Starting Day 57 Jinja Blog & Demographic Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
