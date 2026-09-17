"""
Day 63: Virtual Bookshelf CRUD Server
Implements complete database lifecycle management using Flask-SQLAlchemy and SQLite.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Book

app = Flask(__name__)
# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with SQLAlchemy extension
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Read: Query all books ordered by rating descending."""
    books = db.session.execute(db.select(Book).order_by(Book.rating.desc())).scalars().all()
    return render_template("index.html", all_books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Create: Add a new book to the database."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        try:
            rating = float(request.form.get("rating", 0.0))
        except ValueError:
            rating = 5.0

        # Check if already exists
        existing = db.session.execute(db.select(Book).where(Book.title == title)).scalar()
        if not existing:
            new_book = Book(title=title, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    """Update: Modify the rating of an existing book."""
    book = db.session.get(Book, book_id)
    if not book:
        abort(404)

    if request.method == "POST":
        try:
            new_rating = float(request.form.get("rating", book.rating))
            book.rating = new_rating
            db.session.commit()
        except ValueError:
            pass
        return redirect(url_for("home"))

    return render_template("edit.html", book=book)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    """Delete: Remove a book record by primary key ID."""
    book = db.session.get(Book, book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    print("🌐 Starting Day 63 Virtual Bookshelf on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
