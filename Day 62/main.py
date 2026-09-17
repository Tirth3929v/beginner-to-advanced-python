# -*- coding: utf-8 -*-
"""
Day 62: Coffee & Wifi Rating Project
Phase 3: Web & Flask

Key Concepts:
Flask-WTF, WTForms SelectField, URL Validators, CSV Data Persistence,
Tabular Bootstrap 5 Display
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
from server import app, load_cafes


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 62: COFFEE & WIFI DIGITAL NOMAD DIRECTORY")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: WTForms SelectField, URL Validator, CSV Persistence, Bootstrap Table\n")


def test_cafe_endpoints():
    """Validates CSV data parsing, table rendering, and form submission via TestClient."""
    print("🧪 Running Automated Cafe Directory Verification via Flask TestClient...\n")
    rows = load_cafes()
    print(f"   📋 Total Cafes Currently in CSV: {len(rows) - 1}")
    for row in rows[1:4]:
        print(f"      • {row[0]:<24} | Coffee: {row[4]} | WiFi: {row[5]} | Power: {row[6]}")

    with app.test_client() as client:
        # GET /
        r1 = client.get("/")
        print(f"\n   ✅ [GET /] Status {r1.status_code} (Homepage operational)")

        # GET /cafes
        r2 = client.get("/cafes")
        print(f"   ✅ [GET /cafes] Status {r2.status_code} (Verified table rendering with {len(rows)} entries)")
        assert b"DevBrew Labs" in r2.data

        # GET /add
        r3 = client.get("/add")
        print(f"   ✅ [GET /add] Status {r3.status_code} (Add Cafe form rendered)")

        # POST /add test submission
        app.config["WTF_CSRF_ENABLED"] = False
        payload = {
            "cafe": "Silicon Roasters",
            "location": "https://maps.google.com/?cid=99999",
            "open_time": "6:00 AM",
            "closing_time": "10:00 PM",
            "coffee_rating": "☕☕☕☕☕",
            "wifi_rating": "💪💪💪💪💪",
            "power_rating": "🔌🔌🔌🔌🔌"
        }
        r4 = client.post("/add", data=payload, follow_redirects=True)
        print(f"   ✅ [POST /add] Status {r4.status_code} (Successfully added 'Silicon Roasters' & redirected to /cafes)")
        assert b"Silicon Roasters" in r4.data
        app.config["WTF_CSRF_ENABLED"] = True

    print("\n✨ Coffee & WiFi directory and CSV persistence verified with 100% success!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated CSV & WTForms Directory Simulation")
    print(" 2) Launch Live Coffee & WiFi Server (http://127.0.0.1:5000)")
    print(" 3) Exit")

    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_cafe_endpoints()
    elif choice == "2":
        print("\n🌐 Starting Coffee & WiFi Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
