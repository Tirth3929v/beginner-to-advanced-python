"""
Day 87: Cafe & Wifi Website
Interactive Remote Work Directory CLI & Web Launcher
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
from models import db, Cafe
from server import create_app


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 87: CAFE & WIFI FULL-STACK WEB DIRECTORY")
    print(" 📚 Phase 4: Web Automation & Portfolio | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Application Architecture:")
    print("  • SQLAlchemy 2.0 ORM Database Modeling for Laptop-Friendly Spaces")
    print("  • Full-Text Search Filtering across Cities & Cafe Names")
    print("  • Responsive Bootstrap 5 Glassmorphism UI & Form Submission")
    print("  • RESTful API JSON Endpoints (/api/all)")
    print("=" * 76 + "\n")


def list_cafes():
    app = create_app()
    with app.app_context():
        cafes = db.session.execute(db.select(Cafe)).scalars().all()
        print(f"\n☕ VERIFIED LAPTOP-FRIENDLY CAFES ({len(cafes)} locations)")
        print("=" * 70)
        for c in cafes:
            wifi_str = f"WiFi: {c.wifi_rating}★" if c.has_wifi else "No WiFi"
            pwr_str = f"Sockets: {c.power_rating}★" if c.has_sockets else "No Sockets"
            print(f"  • {c.name:<26} | 📍 {c.location:<20} | {c.coffee_price}")
            print(f"    └─ {wifi_str} | {pwr_str} | Restrooms: {'Yes' if c.has_toilet else 'No'} | Calls: {'Yes' if c.can_take_calls else 'No'}")
        print("=" * 70 + "\n")


def search_cafes_cli():
    term = input("\nEnter city or name to filter (e.g. 'London' or 'Coffee'): ").strip()
    app = create_app()
    with app.app_context():
        query = db.select(Cafe).where(
            (Cafe.name.ilike(f"%{term}%")) | (Cafe.location.ilike(f"%{term}%"))
        )
        results = db.session.execute(query).scalars().all()
        print(f"\n🔍 Search Results for '{term}' ({len(results)} matches):")
        print("=" * 60)
        for c in results:
            print(f"  • \033[92m{c.name}\033[0m — {c.location} ({c.coffee_price})")
        print("=" * 60 + "\n")


def run_automated_tests():
    """Verifies database seeding, search, insertion, and REST API."""
    print("\n🔍 Running Day 87 Automated Cafe & WiFi Directory Test Suite...")
    print("-" * 70)

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-day87"
    }
    app = create_app(test_config)
    client = app.test_client()

    with app.app_context():
        # 1. Seeding check
        cafes = db.session.execute(db.select(Cafe)).scalars().all()
        assert len(cafes) >= 4, f"Expected at least 4 seeded cafes, got {len(cafes)}"
        print(f" [PASS] 1. Database seeding verified: {len(cafes)} initial spaces created.")

        # 2. GET / route check
        res_home = client.get("/")
        assert res_home.status_code == 200
        assert b"Workshop Coffee" in res_home.data
        print(" [PASS] 2. Home route (GET /) serves directory catalog (HTTP 200).")

        # 3. Search query check
        res_search = client.get("/?search=Tokyo")
        assert res_search.status_code == 200
        assert b"Fuglen Tokyo" in res_search.data
        assert b"Workshop Coffee" not in res_search.data
        print(" [PASS] 3. Search filtering verified: Filtered for 'Tokyo' successfully.")

        # 4. Insertion check (POST /add)
        res_add = client.post("/add", data={
            "name": "Dev House Cafe",
            "location": "Bangalore (Indiranagar)",
            "map_url": "https://maps.google.com/?q=Dev+House",
            "img_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb",
            "seats": "50+",
            "coffee_price": "₹250",
            "wifi_rating": 5,
            "power_rating": 5,
            "has_wifi": "on",
            "has_sockets": "on"
        }, follow_redirects=True)
        assert res_add.status_code == 200
        new_c = db.session.execute(db.select(Cafe).where(Cafe.name == "Dev House Cafe")).scalar_one_or_none()
        assert new_c is not None
        print(" [PASS] 4. Cafe insertion verified: 'Dev House Cafe' persisted into database.")

        # 5. REST API check (GET /api/all)
        res_api = client.get("/api/all")
        assert res_api.status_code == 200
        data = res_api.get_json()
        assert len(data) >= 5
        print(f" [PASS] 5. RESTful JSON endpoint (/api/all) returned {len(data)} serialized cafes.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Cafe & WiFi Directory fully operational.\n")


def run_server():
    app = create_app()
    print("\n" + "=" * 70)
    print(" 🚀 STARTING CAFE & WIFI DIRECTORY SERVER")
    print("=" * 70)
    print(" 🌐 URL: http://127.0.0.1:5000")
    print(" Press Ctrl+C in your terminal to shut down the server.\n")
    app.run(debug=True, port=5000)


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) ☕ Inspect Verified Directory Cafes (Terminal)")
        print("  2) 🔍 Search Cafes by City or Name")
        print("  3) 🌐 Launch Live Web Directory Server (http://127.0.0.1:5000)")
        print("  4) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            list_cafes()
        elif choice == "2":
            search_cafes_cli()
        elif choice == "3":
            run_server()
            break
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Happy remote working! Enjoy your coffee ☕\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 87 gracefully... Goodbye!\n")
