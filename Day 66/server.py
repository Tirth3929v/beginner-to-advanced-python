"""
Day 66: Building Your Own RESTful API Server
Implements RESTful JSON microservice with HTTP methods GET, POST, PATCH, and DELETE.
"""

import os
import random
from flask import Flask, render_template, request, jsonify
from models import db, Cafe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

API_KEY_SECRET = os.environ.get("API_KEY_SECRET", "TopSecretAPIKey")


def seed_cafes():
    count = db.session.execute(db.select(Cafe)).scalars().all()
    if not count:
        sample_cafes = [
            Cafe(
                name="Science Gallery Cafe",
                map_url="https://maps.google.com/?cid=1001",
                img_url="https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80",
                location="London",
                seats="50+",
                has_toilet=True,
                has_wifi=True,
                has_sockets=True,
                can_take_calls=True,
                coffee_price="£2.75"
            ),
            Cafe(
                name="Timberyard",
                map_url="https://maps.google.com/?cid=1002",
                img_url="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=800&q=80",
                location="London",
                seats="35+",
                has_toilet=True,
                has_wifi=True,
                has_sockets=True,
                can_take_calls=False,
                coffee_price="£3.50"
            ),
            Cafe(
                name="Coffee Collective",
                map_url="https://maps.google.com/?cid=1003",
                img_url="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80",
                location="San Francisco",
                seats="25+",
                has_toilet=True,
                has_wifi=True,
                has_sockets=False,
                can_take_calls=True,
                coffee_price="$4.50"
            )
        ]
        db.session.add_all(sample_cafes)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_cafes()


@app.route("/")
def home():
    """Renders interactive REST API documentation and live endpoint testing portal."""
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    if not cafes:
        return jsonify(error={"Not Found": "No cafes found in database."}), 404
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict()), 200


@app.route("/all")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    return jsonify(cafes=[c.to_dict() for c in cafes]), 200


@app.route("/search")
def search_cafes():
    loc = request.args.get("loc", "").strip()
    cafes = db.session.execute(db.select(Cafe).where(Cafe.location.ilike(f"%{loc}%"))).scalars().all()
    if cafes:
        return jsonify(cafes=[c.to_dict() for c in cafes]), 200
    else:
        return jsonify(error={"Not Found": f"Sorry, we don't have a cafe at '{loc}'."}), 404


@app.route("/add", methods=["POST"])
def post_new_cafe():
    data = request.get_json(silent=True) or request.form
    new_cafe = Cafe(
        name=data.get("name", "Unnamed Cafe"),
        map_url=data.get("map_url", "https://maps.google.com/"),
        img_url=data.get("img_url", "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb"),
        location=data.get("location", "Unknown"),
        seats=data.get("seats", "10+"),
        has_toilet=bool(data.get("has_toilet", True)),
        has_wifi=bool(data.get("has_wifi", True)),
        has_sockets=bool(data.get("has_sockets", True)),
        can_take_calls=bool(data.get("can_take_calls", True)),
        coffee_price=data.get("coffee_price", "£3.00")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe.", "id": new_cafe.id}), 201


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_price(cafe_id):
    new_price = request.args.get("new_price") or (request.get_json(silent=True) or {}).get("new_price")
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": f"Successfully updated the price to {new_price}."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key") or request.headers.get("api-key")
    if api_key != API_KEY_SECRET:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api-key."}), 403

    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": f"Successfully deleted cafe with id {cafe_id}."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == "__main__":
    print("🌐 Starting Day 66 RESTful API on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
