"""
Day 69: Relational Blog Capstone Application Server
Full-featured production-ready Flask server with:
- Bidirectional One-to-Many relational database (Users -> BlogPosts, Users -> Comments, BlogPosts -> Comments)
- Role-Based Access Control (RBAC) via @admin_only decorator (User ID 1 is Admin)
- Flask-Login session management with PBKDF2 password hashing
- WTForms with CSRF protection and bootstrap integration
"""

import os
import sys
from datetime import datetime
from functools import wraps
from typing import Optional

from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, BlogPost, Comment
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def create_app(test_config: Optional[dict] = None) -> Flask:
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, "instance"), exist_ok=True)

    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-day69-capstone")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'instance', 'blog_relational.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    # Role-Based Access Control Decorator
    def admin_only(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.id != 1:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function

    # Seed initial database records
    def seed_initial_data():
        with app.app_context():
            db.create_all()
            if db.session.execute(db.select(User)).first() is None:
                # 1. Admin user (id=1)
                admin_user = User(
                    name="Admin Architect",
                    email="admin@email.com",
                    password=generate_password_hash("12345678", method="pbkdf2:sha256", salt_length=8)
                )
                db.session.add(admin_user)
                db.session.commit()

                # 2. Standard user (id=2)
                reader_user = User(
                    name="Elena Rostova",
                    email="elena@example.com",
                    password=generate_password_hash("12345678", method="pbkdf2:sha256", salt_length=8)
                )
                db.session.add(reader_user)
                db.session.commit()

                # 3. Initial Blog Posts
                post_1 = BlogPost(
                    title="Mastering Relational Databases with SQLAlchemy 2.0",
                    subtitle="How bidirectional foreign keys and relationships eliminate data redundancy.",
                    date="September 17, 2026",
                    body=(
                        "<p>In modern backend engineering, organizing data into normalized relational tables "
                        "ensures integrity, consistency, and performant query execution.</p>"
                        "<p>By leveraging <code>relationship(back_populates=...)</code> and explicit foreign keys, "
                        "Python applications cleanly separate users, articles, and discussion threads into structured entities.</p>"
                    ),
                    img_url="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1600&q=80",
                    author_id=admin_user.id
                )
                post_2 = BlogPost(
                    title="Defensive Security: Role-Based Access Control",
                    subtitle="Why client-side hidden buttons are never enough for authorization.",
                    date="September 16, 2026",
                    body=(
                        "<p>Hiding an 'Edit' button in the template is good UI design, but it does not protect the endpoint. "
                        "Defensive engineering requires server-side route decorators like <code>@admin_only</code>.</p>"
                        "<p>If an unauthorized user manually calls the endpoint, the application must immediately return an HTTP 403 Forbidden status.</p>"
                    ),
                    img_url="https://images.unsplash.com/photo-1510511459019-5dda7724fd87?auto=format&fit=crop&w=1600&q=80",
                    author_id=admin_user.id
                )
                db.session.add_all([post_1, post_2])
                db.session.commit()

                # 4. Initial Sample Comment
                sample_comment = Comment(
                    text="Brilliant explanation of back_populates! This makes cascading deletes so much clearer.",
                    date="September 17, 2026",
                    author_id=reader_user.id,
                    post_id=post_1.id
                )
                db.session.add(sample_comment)
                db.session.commit()

    # Routes
    @app.route("/")
    def home():
        posts = db.session.execute(db.select(BlogPost).order_by(BlogPost.id.desc())).scalars().all()
        return render_template("index.html", posts=posts)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        form = RegisterForm()
        if form.validate_on_submit():
            existing_user = db.session.execute(
                db.select(User).where(User.email == form.email.data.strip().lower())
            ).scalar_one_or_none()
            if existing_user:
                flash("An account with that email already exists. Please log in.", "warning")
                return redirect(url_for("login"))

            hashed_pwd = generate_password_hash(
                form.password.data,
                method="pbkdf2:sha256",
                salt_length=8
            )
            new_user = User(
                name=form.name.data.strip(),
                email=form.email.data.strip().lower(),
                password=hashed_pwd
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f"Welcome to Clean Blog, {new_user.name}!", "success")
            return redirect(url_for("home"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            password = form.password.data
            user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

            if not user:
                flash("No account registered with that email address.", "danger")
                return redirect(url_for("login"))
            elif not check_password_hash(user.password, password):
                flash("Invalid password entered. Please try again.", "danger")
                return redirect(url_for("login"))
            else:
                login_user(user)
                flash(f"Logged in successfully as {user.name}.", "success")
                return redirect(url_for("home"))
        return render_template("login.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out securely.", "info")
        return redirect(url_for("home"))

    @app.route("/post/<int:post_id>", methods=["GET", "POST"])
    def show_post(post_id: int):
        post = db.session.get(BlogPost, post_id)
        if not post:
            return abort(404)
        form = CommentForm()
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                flash("You need to log in or register to submit a comment.", "warning")
                return redirect(url_for("login"))
            new_comment = Comment(
                text=form.comment_text.data.strip(),
                date=datetime.now().strftime("%B %d, %Y"),
                author_id=current_user.id,
                post_id=post.id
            )
            db.session.add(new_comment)
            db.session.commit()
            flash("Comment posted successfully!", "success")
            return redirect(url_for("show_post", post_id=post.id))
        return render_template("post.html", post=post, form=form)

    @app.route("/new-post", methods=["GET", "POST"])
    @admin_only
    def add_new_post():
        form = CreatePostForm()
        if form.validate_on_submit():
            new_post = BlogPost(
                title=form.title.data.strip(),
                subtitle=form.subtitle.data.strip(),
                body=form.body.data.strip(),
                img_url=form.img_url.data.strip(),
                author_id=current_user.id,
                date=datetime.now().strftime("%B %d, %Y")
            )
            db.session.add(new_post)
            db.session.commit()
            flash("Article published successfully!", "success")
            return redirect(url_for("home"))
        return render_template("make-post.html", form=form, is_edit=False)

    @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
    @admin_only
    def edit_post(post_id: int):
        post = db.session.get(BlogPost, post_id)
        if not post:
            return abort(404)
        form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            body=post.body
        )
        if form.validate_on_submit():
            post.title = form.title.data.strip()
            post.subtitle = form.subtitle.data.strip()
            post.img_url = form.img_url.data.strip()
            post.body = form.body.data.strip()
            db.session.commit()
            flash("Article updated successfully!", "success")
            return redirect(url_for("show_post", post_id=post.id))
        return render_template("make-post.html", form=form, is_edit=True)

    @app.route("/delete-post/<int:post_id>")
    @admin_only
    def delete_post(post_id: int):
        post = db.session.get(BlogPost, post_id)
        if not post:
            return abort(404)
        db.session.delete(post)
        db.session.commit()
        flash("Article deleted successfully.", "info")
        return redirect(url_for("home"))

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            flash("Thank you for reaching out! Your message has been received.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html")

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("base.html", heading="403 Forbidden", subheading="You do not possess the required administrative credentials to access this action."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("base.html", heading="404 Not Found", subheading="The requested article or page could not be located."), 404

    seed_initial_data()
    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Clean Blog Capstone running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
