# -*- coding: utf-8 -*-
"""
Day 60: Make POST Requests with Flask & HTML Forms
Phase 3: Web & Flask

Key Concepts:
HTTP Request Methods (GET vs POST), request.form Extraction,
Contact Message Ingestion, Email / Ledger Notification Pipelines
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
from server import app, notifier


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 60: POST REQUESTS & HTML CONTACT FORM SUBMISSION")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: methods=['GET', 'POST'], request.form, Dispatch Pipelines\n")


def test_post_endpoints():
    """Validates GET and POST endpoints using Flask TestClient."""
    print("🧪 Running Automated Form Processing via Flask TestClient...")
    with app.test_client() as client:
        # Test GET /
        res_home = client.get("/")
        print(f"   ✅ GET  /        -> Status {res_home.status_code} (Homepage Loaded)")

        # Test GET /contact
        res_get_contact = client.get("/contact")
        print(f"   ✅ GET  /contact -> Status {res_get_contact.status_code} (Empty Form Rendered)")
        assert b"Send a Message" in res_get_contact.data

        # Test POST /contact
        payload = {
            "name": "Sarah Connor",
            "email": "sarah@cyberdyne.org",
            "phone": "555-0199",
            "message": "Need advice on protecting our Python microservices against autonomous AI agents!"
        }
        res_post_contact = client.post("/contact", data=payload)
        print(f"   ✅ POST /contact -> Status {res_post_contact.status_code} (Form Data Ingested)")
        assert b"Successfully Sent Your Message" in res_post_contact.data
        assert b"Sarah Connor" in res_post_contact.data

    print(f"\n📊 Total Inquiries Logged in Ledger: {len(notifier.submissions)}")
    print("✨ Form processing and notification pipeline verified with 100% success!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated GET & POST TestClient Simulation")
    print(" 2) View Contact Inquiries Ledger")
    print(" 3) Launch Live Flask Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_post_endpoints()
    elif choice == "2":
        print("\n📋 Recent Inbound Inquiries:")
        if not notifier.submissions:
            print("   (No inquiries recorded yet. Run option 1 to simulate a submission!)")
        else:
            for s in notifier.submissions:
                print(f"   • [{s['timestamp']}] {s['name']} <{s['email']}>: \"{s['message']}\"")
    elif choice == "3":
        print("\n🌐 Starting Flask POST Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
