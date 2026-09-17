"""
Day 59: Clean Blog Capstone Web Application Server
Serves multi-page Bootstrap 5 blog with Jinja2 template inheritance.
"""

import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)

# Load blog posts from JSON
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "posts.json")


def get_posts():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


POSTS = get_posts()


@app.route("/")
def home():
    return render_template("index.html", all_posts=POSTS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    for post in POSTS:
        if post["id"] == index:
            return render_template("post.html", post=post)
    abort(404)


if __name__ == "__main__":
    print("🌐 Starting Day 59 Clean Blog Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
