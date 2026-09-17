"""
Day 96: Custom API-Powered E-Commerce Store
Phase 5: Portfolio

Key Concepts:
Flask Web Framework, Stripe Checkout API Integration, Product Cart State
"""

import os
import sys
import tempfile

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, CART_ICON
from models import StoreRepository
from server import create_app


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(CART_ICON)
    print("=" * 72)
    print(" 🚀 DAY 96: CUSTOM API-POWERED E-COMMERCE STORE")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: Flask, Stripe Checkout API, Cart State Machine, REST Endpoints")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates the e-commerce catalog, cart operations, REST endpoints, and checkout."""
    print("\n🔍 Running Day 96 Automated E-Commerce API & Store Test Suite...")
    print("-" * 70)

    # Use isolated temp database for tests
    temp_dir = tempfile.mkdtemp()
    test_db = os.path.join(temp_dir, "test_store.db")
    app = create_app(db_path=test_db)
    client = app.test_client()

    # 1. Product catalog retrieval
    resp = client.get("/api/products")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] >= 6
    assert any("Keyboard" in p["name"] for p in data["products"])
    print(" [PASS] 1. Catalog REST API endpoint verified (products populated & mapped).")

    # 2. Add to cart
    session_id = "test_user_session_123"
    add_resp = client.post(
        "/api/cart/add",
        json={"product_id": 1, "quantity": 2, "session_id": session_id}
    )
    assert add_resp.status_code == 200
    assert add_resp.get_json()["cart_count"] == 2
    print(" [PASS] 2. Shopping cart addition & quantity tracking verified.")

    # 3. View cart & subtotal
    cart_resp = client.get(f"/api/cart?session_id={session_id}")
    assert cart_resp.status_code == 200
    cart_data = cart_resp.get_json()
    assert cart_data["subtotal"] == 299.98  # 149.99 * 2
    print(" [PASS] 3. Cart subtotal arithmetic verified ($299.98).")

    # 4. Promo code application & checkout
    checkout_resp = client.post(
        "/api/checkout",
        json={
            "session_id": session_id,
            "email": "tester@example.com",
            "promo_code": "PYTHON100"
        }
    )
    assert checkout_resp.status_code == 201
    order = checkout_resp.get_json()
    assert order["success"] is True
    assert order["subtotal"] == 299.98
    assert order["discount"] == 60.0  # 20% discount on 299.98 = 59.996 -> 60.0
    assert order["order_id"].startswith("ORD-")
    print(" [PASS] 4. Stripe-mock checkout session & 20% promo code coupon verified.")

    # 5. Cart emptied post-checkout
    cleared_cart = client.get(f"/api/cart?session_id={session_id}").get_json()
    assert cleared_cart["item_count"] == 0
    print(" [PASS] 5. Post-order cart state transition (cleared) verified.")

    # 6. HTML page status code checks
    assert client.get("/").status_code == 200
    assert client.get("/cart").status_code == 200
    print(" [PASS] 6. Frontend store and cart Jinja2 templates verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Custom API-Powered E-Commerce Store fully operational.\n")


def interactive_cli():
    """Interactive command-line store client."""
    banner()
    repo = StoreRepository(os.path.join(os.path.dirname(__file__), "devstore.db"))
    user_session = "cli_shopper"

    while True:
        print("\n" + "=" * 55)
        print("  DEVSTORE PRO - COMMAND CENTER")
        print("=" * 55)
        print("  [1] Browse Catalog & Hardware Inventory")
        print("  [2] View Shopping Cart")
        print("  [3] Add Item to Cart")
        print("  [4] Checkout & Pay with Stripe Mock")
        print("  [5] Launch Live Web Store (Flask Server)")
        print("  [6] Run Automated Test Suite")
        print("  [7] Exit")
        print("=" * 55)

        choice = input("Enter option (1-7): ").strip()

        if choice == "1":
            products = repo.get_all_products()
            print("\n  📦 CURRENT HARDWARE CATALOG:")
            print("  " + "-" * 75)
            for p in products:
                print(f"  [{p['id']}] {p['image_emoji']} {p['name']:<45} | ${p['price']:<7.2f} (Stock: {p['stock']})")
            print("  " + "-" * 75)

        elif choice == "2":
            cart = repo.get_cart(user_session)
            if not cart:
                print("\n  [i] Your cart is currently empty.")
            else:
                subtotal = sum(i["price"] * i["quantity"] for i in cart)
                print("\n  🛍️ YOUR CART:")
                print("  " + "-" * 60)
                for item in cart:
                    print(f"  • {item['image_emoji']} {item['name']} x{item['quantity']} = ${item['price'] * item['quantity']:.2f}")
                print("  " + "-" * 60)
                print(f"  Subtotal: ${subtotal:.2f}")

        elif choice == "3":
            pid_str = input("  Enter product ID to add: ").strip()
            qty_str = input("  Enter quantity (default: 1): ").strip()
            qty = int(qty_str) if qty_str.isdigit() else 1
            if pid_str.isdigit():
                ok = repo.add_to_cart(user_session, int(pid_str), qty)
                if ok:
                    print("  [✓] Item successfully added to cart!")
                else:
                    print("  [!] Failed to add (insufficient stock or invalid ID).")

        elif choice == "4":
            cart = repo.get_cart(user_session)
            if not cart:
                print("  [!] Cart is empty! Add products first.")
                continue
            email = input("  Enter customer email: ").strip() or "customer@example.com"
            promo = input("  Enter promo code (e.g., 'PYTHON100' or press Enter): ").strip()
            res = repo.checkout(user_session, email, promo_code=promo)
            if res.get("success"):
                print("\n  🎉 CHECKOUT SUCCESSFUL!")
                print(f"     Order ID : {res['order_id']}")
                print(f"     Subtotal : ${res['subtotal']:.2f}")
                print(f"     Discount : -${res['discount']:.2f}")
                print(f"     Tax (8%) : ${res['tax']:.2f}")
                print(f"     TOTAL    : ${res['total']:.2f}")
                print(f"     Gateway  : {res['payment_gateway']}")
            else:
                print(f"  [!] Checkout error: {res.get('error')}")

        elif choice == "5":
            print("\n  🚀 Starting DevStore Web Server on http://127.0.0.1:5000 ...")
            print("  Press Ctrl+C to return to CLI menu.")
            app = create_app()
            try:
                app.run(port=5000, debug=False)
            except (KeyboardInterrupt, SystemExit):
                print("\n  [✓] Web server stopped.")

        elif choice == "6":
            run_automated_tests()

        elif choice == "7":
            print("\n👋 Exiting DevStore. Happy Coding!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-7.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 96 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
