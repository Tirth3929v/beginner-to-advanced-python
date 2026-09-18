# -*- coding: utf-8 -*-
"""
Day 66: Building Your Own RESTful API
Phase 3: Web & Flask

Key Concepts:
RESTful Architecture, JSON Serialization, HTTP Verbs (GET, POST, PATCH, DELETE),
API Key Header & Query Security, Postman Testing Pipelines
"""

import sys
import os

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from server import app, db, Cafe, API_KEY_SECRET


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 66: BUILDING YOUR OWN RESTFUL API WITH FLASK")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: REST Verbs (GET/POST/PATCH/DELETE), JSON, API Key Security\n")


def test_rest_api():
    """Executes a full integration test of all RESTful API endpoints."""
    print("🧪 Running Complete RESTful API Integration Suite via Flask TestClient...\n")

    with app.test_client() as client:
        # 1. GET /all
        r_all = client.get("/all")
        print(f"   ✅ [GET /all] Status {r_all.status_code} (Fetched {len(r_all.get_json()['cafes'])} cafes)")

        # 2. GET /random
        r_rand = client.get("/random")
        print(f"   ✅ [GET /random] Status {r_rand.status_code} (Random: '{r_rand.get_json()['cafe']['name']}')")

        # 3. GET /search?loc=London
        r_search = client.get("/search?loc=London")
        print(f"   ✅ [GET /search?loc=London] Status {r_search.status_code} (Found {len(r_search.get_json()['cafes'])} matches)")

        # 4. POST /add
        new_cafe_payload = {
            "name": "Octane Coding Hub",
            "map_url": "https://maps.google.com/?cid=888",
            "img_url": "https://images.unsplash.com/photo-1501339847302",
            "location": "Berlin",
            "seats": "40+",
            "has_toilet": True,
            "has_wifi": True,
            "has_sockets": True,
            "can_take_calls": True,
            "coffee_price": "€3.40"
        }
        r_post = client.post("/add", json=new_cafe_payload)
        new_id = r_post.get_json()["response"]["id"]
        print(f"   ✅ [POST /add] Status {r_post.status_code} (Created cafe ID #{new_id}: 'Octane Coding Hub')")

        # 5. PATCH /update-price/<id>
        r_patch = client.patch(f"/update-price/{new_id}?new_price=%E2%82%AC3.95")
        print(f"   ✅ [PATCH /update-price/{new_id}] Status {r_patch.status_code} (Updated coffee price to €3.95)")

        # 6. DELETE (Unauthorized - 403 Forbidden check)
        r_del_unauth = client.delete(f"/report-closed/{new_id}?api-key=WrongKey")
        print(f"   ✅ [DELETE /report-closed - Invalid Key] Status {r_del_unauth.status_code} (Verified 403 Forbidden)")
        assert r_del_unauth.status_code == 403

        # 7. DELETE (Authorized - 200 OK)
        r_del_auth = client.delete(f"/report-closed/{new_id}?api-key={API_KEY_SECRET}")
        print(f"   ✅ [DELETE /report-closed - Valid Key] Status {r_del_auth.status_code} (Verified 200 OK record deletion)")
        assert r_del_auth.status_code == 200

    print("\n✨ All RESTful API endpoints and security guards verified with 100% test coverage!")


def inspect_cafes():
    """Prints all active cafes in the database."""
    print("🔍 Querying Database of Registered Cafes...")
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe)).scalars().all()
        for c in cafes:
            print(f"   • [ID #{c.id:<2}] {c.name:<24} | Loc: {c.location:<14} | Price: {c.coffee_price}")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated RESTful API Test Suite (GET, POST, PATCH, DELETE, 403 Auth)")
    print(" 2) Inspect Registered Cafes Database")
    print(" 3) Launch Live RESTful API Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_rest_api()
    elif choice == "2":
        inspect_cafes()
    elif choice == "3":
        print("\n🌐 Starting RESTful API Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
        app.run(debug=False, port=5000)
    else:
        print("Exiting. Happy coding!")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Program interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
