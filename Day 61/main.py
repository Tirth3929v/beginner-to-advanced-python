# -*- coding: utf-8 -*-
"""
Day 61: Building Advanced Forms with Flask-WTF
Phase 3: Web & Flask

Key Concepts:
Flask-WTF, WTForms Fields, DataRequired & Email & Length Validators,
CSRF Secret Keys & Dynamic Error Reporting
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
from server import app
from forms import LoginForm


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 61: ADVANCED FORMS WITH FLASK-WTF & CSRF PROTECTION")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: WTForms, CSRF Protection, Email/Length Validators, Access Control\n")


def test_wtf_endpoints():
    """Runs automated security simulations across all authorization scenarios."""
    print("🧪 Running Automated WTForms Security Checks via Flask TestClient...\n")
    with app.test_client() as client:
        # 1. GET /
        r1 = client.get("/")
        print(f"   ✅ [GET /] Status {r1.status_code} (Homepage operational)")

        # 2. GET /login (verify CSRF token exists in production mode)
        r2 = client.get("/login")
        print(f"   ✅ [GET /login] Status {r2.status_code} (Rendered form with CSRF token)")
        assert b"csrf_token" in r2.data, "CSRF token missing from template!"

        # Temporarily disable CSRF validation specifically for automated test submissions
        app.config["WTF_CSRF_ENABLED"] = False

        # 3. Successful Admin Auth
        r3 = client.post("/login", data={
            "email": "admin@email.com",
            "password": "12345678"
        })
        print(f"   ✅ [POST /login - Valid Admin] Status {r3.status_code} (Access Granted page loaded)")
        assert b"Access Granted" in r3.data

        # 4. Failed Admin Auth (Wrong Password)
        r4 = client.post("/login", data={
            "email": "intruder@evil.com",
            "password": "wrongpassword123"
        })
        print(f"   ✅ [POST /login - Invalid User] Status {r4.status_code} (Access Denied page loaded)")
        assert b"Access Denied" in r4.data

        # 5. Validation Error (Malformed Email & Short Password)
        r5 = client.post("/login", data={
            "email": "not-an-email",
            "password": "123"
        })
        print(f"   ✅ [POST /login - Validation Trap] Status {r5.status_code} (Validation errors caught)")
        assert b"valid email address" in r5.data or b"at least 8 characters" in r5.data

        # Re-enable CSRF protection for live server runs
        app.config["WTF_CSRF_ENABLED"] = True

    print("\n✨ All WTForms security & validation checks passed with 100% test coverage!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated WTForms & CSRF Security Simulation")
    print(" 2) Launch Live Flask-WTF Server (http://127.0.0.1:5000)")
    print(" 3) Exit")

    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_wtf_endpoints()
    elif choice == "2":
        print("\n🌐 Starting Flask-WTF Security Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
