"""
Day 67: RESTful Blog Capstone Server
Complete Content Management System implementing RESTful routing for articles.
"""

import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, abort
from models import db, BlogPost
from forms import CreatePostForm

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "restful_blog_secret_key_demo")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def seed_posts():
    count = db.session.execute(db.select(BlogPost)).scalars().all()
    if not count:
        sample_posts = [
            BlogPost(
                title="The Future of Distributed Systems in Python",
                subtitle="Scaling asynchronous microservices with modern messaging topologies",
                date=datetime.now().strftime("%B %d, %Y"),
                body="<p>Building high-throughput backends requires balancing fault tolerance with low operational overhead. As applications evolve from monolithic scripts into containerized services, message brokers and stateful databases form the backbone of modern cloud engineering.</p>",
                author="Tirth Patel",
                img_url="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1400&q=80"
            ),
            BlogPost(
                title="Architecting RESTful APIs with Flask & SQLAlchemy",
                subtitle="From relational models to hypermedia and predictable URI routing",
                date=datetime.now().strftime("%B %d, %Y"),
                body="<p>RESTful constraints emphasize stateless communication, uniform interfaces, and standardized HTTP response codes. Pairing Flask's flexible routing with SQLAlchemy 2.0 ORM delivers production-ready maintainability.</p>",
                author="Tirth Patel",
                img_url="https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1400&q=80"
            )
        ]
        db.session.add_all(sample_posts)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_posts()


@app.route("/")
def home():
    posts = db.session.execute(db.select(BlogPost).order_by(BlogPost.id.desc())).scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)
    return render_template("post.html", post=post)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data.strip(),
            subtitle=form.subtitle.data.strip(),
            date=datetime.now().strftime("%B %d, %Y"),
            body=form.body.data.strip(),
            author=form.author.data.strip(),
            img_url=form.img_url.data.strip()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", form=form, page_title="New Article")


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)

    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.subtitle = form.subtitle.data.strip()
        post.img_url = form.img_url.data.strip()
        post.author = form.author.data.strip()
        post.body = form.body.data.strip()
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=form, page_title="Edit Article")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    print("🌐 Starting Day 67 RESTful Blog Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
