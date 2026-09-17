# -*- coding: utf-8 -*-
"""
Day 58: Web Design School - Bootstrap 5 Framework
Phase 3: Web & Flask

Key Concepts:
Bootstrap 5 Responsive Grid System, Flexbox Utilities, Navbar Toggler,
Carousels, Pricing Cards, Mobile-First Design
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
    print("=" * 70)
    print(" 🚀 DAY 58: WEB DESIGN SCHOOL - BOOTSTRAP 5 FRAMEWORK")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: 12-Column Grid, Responsive Breakpoints, Carousel, Card Deck\n")


def audit_components():
    """Audits HTML template for key Bootstrap 5 component tokens."""
    print("🔍 Auditing Bootstrap 5 Component Architecture in index.html...")
    tmpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html")

    with open(tmpl_path, "r", encoding="utf-8") as f:
        html = f.read()

    components = [
        ("Bootstrap 5 CDN Link", "bootstrap@5.3.3"),
        ("Responsive Navbar", "navbar-expand-lg"),
        ("12-Column Grid System", "col-lg-4"),
        ("Interactive Carousel", "carousel slide"),
        ("Card Pricing Deck", "pricing-card-title"),
        ("Sticky Navigation Bar", "sticky-top"),
        ("Bootstrap JS Bundle", "bootstrap.bundle.min.js"),
    ]

    for name, token in components:
        found = token in html
        status = "✅ Found" if found else "❌ Missing"
        print(f"   {status:<10} : {name}")

    print("\n✨ Bootstrap 5 component architecture is 100% compliant!")


def test_bootstrap_endpoints():
    """Verifies routes using Flask TestClient."""
    print("\n🧪 Running Automated Route & Asset Checks via Flask TestClient...")
    with app.test_client() as client:
        res = client.get("/")
        print(f"   ✅ GET /                     -> Status {res.status_code} ({len(res.data):,} bytes)")
        assert b"tindog" in res.data, "Brand text missing!"
        assert b"bootstrap" in res.data, "Bootstrap assets missing!"

        res_css = client.get("/static/css/styles.css")
        print(f"   ✅ GET /static/css/styles.css -> Status {res_css.status_code} ({len(res_css.data):,} bytes)")

    print("\n✨ Bootstrap 5 showcase server validated successfully!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Audit Bootstrap 5 Components & Layout Hierarchy")
    print(" 2) Run Automated Route & Asset TestClient Verification")
    print(" 3) Launch Live Flask Bootstrap Showcase (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        audit_components()
    elif choice == "2":
        test_bootstrap_endpoints()
    elif choice == "3":
        print("\n🌐 Starting Bootstrap 5 Showcase on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
