"""
Day 87: Cafe & WiFi Full-Stack Web Application Server
"""

import os
import sys
from typing import Optional
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Cafe

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def create_app(test_config: Optional[dict] = None) -> Flask:
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, "instance"), exist_ok=True)

    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "cafe-wifi-secret-key-day87")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'instance', 'cafes_day87.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    def seed_cafes():
        with app.app_context():
            db.create_all()
            if db.session.execute(db.select(Cafe)).first() is None:
                samples = [
                    Cafe(
                        name="Workshop Coffee Co.",
                        location="London (Marylebone)",
                        map_url="https://maps.google.com/?q=Workshop+Coffee+London",
                        img_url="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80",
                        seats="45+",
                        has_toilet=True,
                        has_wifi=True,
                        has_sockets=True,
                        can_take_calls=True,
                        coffee_price="£3.60",
                        wifi_rating=5,
                        power_rating=4
                    ),
                    Cafe(
                        name="Sightglass Coffee",
                        location="San Francisco (SoMa)",
                        map_url="https://maps.google.com/?q=Sightglass+Coffee+SF",
                        img_url="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=800&q=80",
                        seats="60+",
                        has_toilet=True,
                        has_wifi=True,
                        has_sockets=True,
                        can_take_calls=False,
                        coffee_price="$4.50",
                        wifi_rating=5,
                        power_rating=5
                    ),
                    Cafe(
                        name="Fuglen Tokyo",
                        location="Tokyo (Shibuya)",
                        map_url="https://maps.google.com/?q=Fuglen+Tokyo",
                        img_url="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80",
                        seats="25+",
                        has_toilet=True,
                        has_wifi=True,
                        has_sockets=False,
                        can_take_calls=False,
                        coffee_price="¥550",
                        wifi_rating=4,
                        power_rating=2
                    ),
                    Cafe(
                        name="The Barn Coffee Roasters",
                        location="Berlin (Mitte)",
                        map_url="https://maps.google.com/?q=The+Barn+Berlin",
                        img_url="https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=800&q=80",
                        seats="30+",
                        has_toilet=True,
                        has_wifi=True,
                        has_sockets=True,
                        can_take_calls=True,
                        coffee_price="€3.80",
                        wifi_rating=4,
                        power_rating=4
                    )
                ]
                db.session.add_all(samples)
                db.session.commit()

    @app.route("/")
    def index():
        search = request.args.get("search", "").strip()
        if search:
            query = db.select(Cafe).where(
                (Cafe.name.ilike(f"%{search}%")) | (Cafe.location.ilike(f"%{search}%"))
            )
        else:
            query = db.select(Cafe).order_by(Cafe.id.desc())
        cafes = db.session.execute(query).scalars().all()
        return render_template("index.html", cafes=cafes, search_query=search)

    @app.route("/add", methods=["GET", "POST"])
    def add_cafe():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            location = request.form.get("location", "").strip()
            map_url = request.form.get("map_url", "").strip()
            img_url = request.form.get("img_url", "").strip()
            seats = request.form.get("seats", "30+").strip()
            coffee_price = request.form.get("coffee_price", "£3.00").strip()
            wifi_rating = int(request.form.get("wifi_rating", 4))
            power_rating = int(request.form.get("power_rating", 4))
            has_wifi = "has_wifi" in request.form
            has_sockets = "has_sockets" in request.form
            has_toilet = "has_toilet" in request.form
            can_take_calls = "can_take_calls" in request.form

            new_cafe = Cafe(
                name=name,
                location=location,
                map_url=map_url,
                img_url=img_url,
                seats=seats,
                coffee_price=coffee_price,
                wifi_rating=wifi_rating,
                power_rating=power_rating,
                has_wifi=has_wifi,
                has_sockets=has_sockets,
                has_toilet=has_toilet,
                can_take_calls=can_take_calls
            )
            db.session.add(new_cafe)
            db.session.commit()
            flash(f"'{name}' successfully added to the directory!", "success")
            return redirect(url_for("index"))
        return render_template("add.html")

    @app.route("/delete/<int:cafe_id>")
    def delete_cafe(cafe_id: int):
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            name = cafe.name
            db.session.delete(cafe)
            db.session.commit()
            flash(f"Cafe '{name}' was deleted.", "info")
        return redirect(url_for("index"))

    @app.route("/api/all")
    def api_all():
        cafes = db.session.execute(db.select(Cafe)).scalars().all()
        return jsonify([c.to_dict() for c in cafes])

    seed_cafes()
    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Cafe & WiFi directory server running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
