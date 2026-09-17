"""
Day 96: Custom API-Powered E-Commerce Store
Flask REST API and Stripe-Mock Payment Processor
"""

import os
import secrets
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from models import StoreRepository

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "devstore.db")


def create_app(db_path: str = DEFAULT_DB) -> Flask:
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-ecommerce-stripe-insecure-key-96")
    repo = StoreRepository(db_path)

    @app.before_request
    def ensure_session():
        if "user_id" not in session:
            session["user_id"] = secrets.token_hex(8)

    # --- HTML Page Routes ---

    @app.route("/")
    def index():
        products = repo.get_all_products()
        cart = repo.get_cart(session["user_id"])
        cart_count = sum(i["quantity"] for i in cart)
        return render_template("index.html", products=products, cart_count=cart_count)

    @app.route("/cart")
    def view_cart():
        items = repo.get_cart(session["user_id"])
        subtotal = sum(i["price"] * i["quantity"] for i in items)
        return render_template("cart.html", items=items, subtotal=subtotal)

    @app.route("/cart/remove", methods=["POST"])
    def remove_cart_item():
        prod_id = int(request.form.get("product_id", 0))
        repo.remove_from_cart(session["user_id"], prod_id)
        return redirect(url_for("view_cart"))

    @app.route("/checkout", methods=["POST"])
    def checkout_page():
        email = request.form.get("email", "").strip()
        promo = request.form.get("promo_code", "").strip()
        order_res = repo.checkout(session["user_id"], email=email, promo_code=promo)
        if order_res.get("success"):
            return render_template("success.html", order=order_res)
        return render_template("cart.html", items=repo.get_cart(session["user_id"]), subtotal=0, error=order_res.get("error"))

    # --- REST API Endpoints ---

    @app.route("/api/products", methods=["GET"])
    def api_get_products():
        return jsonify({"products": repo.get_all_products(), "count": len(repo.get_all_products())})

    @app.route("/api/products/<int:prod_id>", methods=["GET"])
    def api_get_single_product(prod_id: int):
        p = repo.get_product(prod_id)
        if p:
            return jsonify({"success": True, "product": p})
        return jsonify({"success": False, "error": "Product not found"}), 404

    @app.route("/api/cart", methods=["GET"])
    def api_get_cart():
        user = request.args.get("session_id", session["user_id"])
        items = repo.get_cart(user)
        subtotal = sum(i["price"] * i["quantity"] for i in items)
        return jsonify({"cart": items, "subtotal": round(subtotal, 2), "item_count": sum(i["quantity"] for i in items)})

    @app.route("/api/cart/add", methods=["POST"])
    def api_add_to_cart():
        data = request.get_json() or {}
        prod_id = int(data.get("product_id", 0))
        qty = int(data.get("quantity", 1))
        user = data.get("session_id", session["user_id"])

        success = repo.add_to_cart(user, prod_id, qty)
        if success:
            items = repo.get_cart(user)
            return jsonify({"success": True, "cart_count": sum(i["quantity"] for i in items)})
        return jsonify({"success": False, "error": "Insufficient stock or invalid product"}), 400

    @app.route("/api/cart/remove", methods=["POST"])
    def api_remove_from_cart():
        data = request.get_json() or {}
        prod_id = int(data.get("product_id", 0))
        user = data.get("session_id", session["user_id"])
        repo.remove_from_cart(user, prod_id)
        return jsonify({"success": True})

    @app.route("/api/checkout", methods=["POST"])
    def api_checkout():
        data = request.get_json() or {}
        email = data.get("email", "api_customer@example.com")
        promo = data.get("promo_code")
        user = data.get("session_id", session["user_id"])

        result = repo.checkout(user, email=email, promo_code=promo)
        if result.get("success"):
            return jsonify(result), 201
        return jsonify(result), 400

    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 DevStore running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
