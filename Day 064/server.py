"""
Day 64: My Top 10 Movies Website Server
Combines Flask-SQLAlchemy with WTForms and TMDB Movie Services.
Features automated ranking calculation based on user rating scores.
"""

import os
from flask import Flask, render_template, redirect, url_for, request, abort
from models import db, Movie
from forms import RateMovieForm, FindMovieForm
from movie_service import search_movies, get_movie_details

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "top_movies_secret_key_demo")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def update_rankings():
    """Recalculates dynamic rankings: #1 is the highest rated movie."""
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars().all()
    for rank, movie in enumerate(movies, start=1):
        movie.ranking = rank
    db.session.commit()


def seed_database():
    """Seeds initial demonstration movies if database is unpopulated."""
    count = db.session.execute(db.select(Movie)).scalars().all()
    if not count:
        sample_movies = [
            Movie(
                title="The Matrix",
                year=1999,
                description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                rating=9.5,
                ranking=1,
                review="Revolutionary sci-fi and cyberpunk action philosophy. Truly iconic.",
                img_url="https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
            ),
            Movie(
                title="Interstellar",
                year=2014,
                description="The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel.",
                rating=9.3,
                ranking=2,
                review="Emotional score and stunning cosmological visuals. Zimmer at his best.",
                img_url="https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
            ),
            Movie(
                title="Inception",
                year=2010,
                description="Cobb steals information from his targets by entering their dreams. He is wanted for his alleged role in his wife's murder.",
                rating=9.0,
                ranking=3,
                review="A masterclass in tension, dream layers, and non-linear storytelling.",
                img_url="https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"
            )
        ]
        db.session.add_all(sample_movies)
        db.session.commit()
        update_rankings()


with app.app_context():
    db.create_all()
    seed_database()


@app.route("/")
def home():
    update_rankings()
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", all_movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    movie_id = request.args.get("id")
    movie = db.session.get(Movie, movie_id)
    if not movie:
        abort(404)

    form = RateMovieForm()
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data.strip()
        db.session.commit()
        return redirect(url_for("home"))

    form.rating.data = movie.rating
    form.review.data = movie.review
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.session.get(Movie, movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        update_rankings()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        title = form.title.data.strip()
        results = search_movies(title)
        return render_template("select.html", options=results)

    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    movie_id = request.args.get("id", type=int)
    details = get_movie_details(movie_id)

    # Check if movie already in DB
    existing = db.session.execute(db.select(Movie).where(Movie.title == details["title"])).scalar()
    if not existing:
        new_movie = Movie(
            title=details["title"],
            year=details["year"],
            description=details["description"],
            rating=0.0,
            ranking=10,
            review="",
            img_url=details["img_url"]
        )
        db.session.add(new_movie)
        db.session.commit()
        target_id = new_movie.id
    else:
        target_id = existing.id

    return redirect(url_for("edit_movie", id=target_id))


if __name__ == "__main__":
    print("🌐 Starting Day 64 Top 10 Movies Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
