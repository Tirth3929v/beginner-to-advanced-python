# -*- coding: utf-8 -*-
"""
Day 59: Clean Blog Capstone Project
Phase 3: Web & Flask

Key Concepts:
Jinja2 Template Inheritance (extends, block), Bootstrap 5 Integration,
Multi-page Navigation, Dynamic JSON Data Hydration
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
from server import app, POSTS


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 59: CLEAN BLOG CAPSTONE - MULTI-PAGE SSR ENGINE")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: Jinja Template Inheritance, Responsive Headers, Article Routing\n")


def audit_blog():
    """Audits articles and template files."""
    print("🔍 Auditing Clean Blog Components & Data Store...")
    print(f"   ✅ Total Articles Indexed: {len(POSTS)}")
    for p in POSTS:
        print(f"      • [Article #{p['id']}] {p['title']}")

    base = os.path.dirname(os.path.abspath(__file__))
    templates = ["base.html", "index.html", "about.html", "contact.html", "post.html"]
    print("\n   Template checks:")
    for t in templates:
        t_path = os.path.join(base, "templates", t)
        status = "✅ Found" if os.path.exists(t_path) else "❌ Missing"
        print(f"      {status:<10} : templates/{t}")


def test_clean_blog_endpoints():
    """Validates all blog endpoints via Flask TestClient."""
    print("\n🧪 Running Automated Route Checks via Flask TestClient...")
    with app.test_client() as client:
        routes = [
            ("/", "Engineering Journal"),
            ("/about", "About Me"),
            ("/contact", "Contact Me"),
            ("/post/1", "Clean Architecture"),
            ("/static/css/clean-blog.css", "masthead"),
        ]
        for route, check in routes:
            res = client.get(route)
            print(f"   ✅ GET {route:<28} -> Status {res.status_code} ({len(res.data):,} bytes)")
            assert check.encode() in res.data, f"Failed match for '{check}' on {route}"

    print("\n✨ Clean Blog multi-page routes and template inheritance verified with 100% success!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Audit Clean Blog Articles & Template Inheritance Hierarchy")
    print(" 2) Run Automated Route & Template Verification (Flask TestClient)")
    print(" 3) Launch Live Clean Blog Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        audit_blog()
    elif choice == "2":
        test_clean_blog_endpoints()
    elif choice == "3":
        print("\n🌐 Starting Clean Blog Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
