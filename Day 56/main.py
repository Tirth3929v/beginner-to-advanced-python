# -*- coding: utf-8 -*-
"""
Day 56: Rendering HTML/Static Files & Building Personal Name Card / Portfolio Site
Phase 2: Intermediate

Key Concepts:
Flask render_template(), Serving Static CSS/Assets, Personal Brand Showcase
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


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 68)
    print(" 🚀 DAY 56: PERSONAL DIGITAL NAME CARD & PORTFOLIO SITE (FLASK)")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 68)
    print("Key Concepts: render_template(), static/ Directory Assets, Modern Vanilla CSS\n")


def audit_assets():
    """Validates presence and size of template and static CSS assets."""
    print("🔍 Auditing Project Template & Static Asset Pipeline...")
    base = os.path.dirname(os.path.abspath(__file__))
    tmpl_path = os.path.join(base, "templates", "index.html")
    css_path = os.path.join(base, "static", "css", "styles.css")

    if os.path.exists(tmpl_path):
        size = os.path.getsize(tmpl_path)
        print(f"   ✅ [Template] index.html found ({size:,} bytes)")
    else:
        print("   ❌ [Template] index.html missing!")

    if os.path.exists(css_path):
        size = os.path.getsize(css_path)
        print(f"   ✅ [Static] styles.css found ({size:,} bytes)")
    else:
        print("   ❌ [Static] styles.css missing!")


def test_portfolio_endpoints():
    """Validates endpoints using Flask TestClient."""
    print("\n🧪 Running Automated Route Checks via Flask TestClient...")
    with app.test_client() as client:
        # Check homepage HTML
        resp = client.get("/")
        print(f"   ✅ GET /                     -> Status {resp.status_code} ({len(resp.data)} bytes)")
        assert b"Tirth Patel" in resp.data, "Name card data missing!"

        # Check static CSS
        resp_css = client.get("/static/css/styles.css")
        print(f"   ✅ GET /static/css/styles.css -> Status {resp_css.status_code} ({len(resp_css.data)} bytes)")
        assert b"--card-bg" in resp_css.data, "CSS styling tokens missing!"

    print("\n✨ Portfolio app and static assets verified successfully!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Audit Template & Static File Integrity")
    print(" 2) Run Automated Route & Asset TestClient Verification")
    print(" 3) Launch Live Flask Portfolio Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        audit_assets()
    elif choice == "2":
        test_portfolio_endpoints()
    elif choice == "3":
        print("\n🌐 Starting Portfolio Card Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
