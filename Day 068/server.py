"""
Day 68: User Authentication with Flask-Login & Werkzeug Server
Implements PBKDF2:SHA256 password hashing, user session lifecycle,
flash messaging, and authenticated file downloads.
"""

import os
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from models import db, User

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "flask_login_auth_secret_key_demo")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        name = request.form.get("name", "").strip()
        raw_password = request.form.get("password", "")

        # Check if user already registered
        existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if existing_user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        # Hash and salt password with PBKDF2:SHA256
        hashed_password = generate_password_hash(
            raw_password,
            method="pbkdf2:sha256",
            salt_length=8
        )

        new_user = User(
            email=email,
            name=name,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in newly registered user
        login_user(new_user)
        return redirect(url_for("secrets"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if not user:
            flash("That email does not exist. Please check or register a new account.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("secrets"))

    return render_template("login.html")


@app.route("/secrets")
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route("/download")
@login_required
def download():
    file_dir = os.path.join(app.root_path, "static", "files")
    return send_from_directory(
        directory=file_dir,
        path="cheat_sheet.pdf",
        as_attachment=True
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    print("🌐 Starting Day 68 Flask-Login Auth Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
