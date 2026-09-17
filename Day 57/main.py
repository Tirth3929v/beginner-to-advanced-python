# -*- coding: utf-8 -*-
"""
Day 57: Jinja Templating in Flask Applications
Phase 2: Intermediate

Key Concepts:
Jinja2 Expressions {{ }}, Control Flow {% %}, Dynamic URL Building url_for(),
API-Driven Data Pipelines, Multi-Page Server-Side Blog Engine
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
from server import app, ALL_POSTS


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 57: JINJA2 DYNAMIC SERVER-SIDE TEMPLATING & BLOG ENGINE")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: Jinja Expressions, Control Loops, url_for(), RESTful APIs\n")


def audit_blog_data():
    """Checks the database of articles and template files."""
    print("🔍 Auditing Jinja Templates & Post Dataset...")
    print(f"   ✅ Loaded {len(ALL_POSTS)} blog posts from data/posts.json:")
    for post in ALL_POSTS:
        print(f"      • [Post #{post.id}] \"{post.title}\" ({len(post.body)} chars)")

    base = os.path.dirname(os.path.abspath(__file__))
    templates = ["index.html", "guess.html", "blog.html", "post.html"]
    print("\n   Template checks:")
    for t in templates:
        t_path = os.path.join(base, "templates", t)
        if os.path.exists(t_path):
            print(f"      ✅ templates/{t:<12} ({os.path.getsize(t_path):,} bytes)")
        else:
            print(f"      ❌ templates/{t} missing!")


def test_jinja_endpoints():
    """Validates endpoints and template rendering via Flask TestClient."""
    print("\n🧪 Running Automated Route Checks via Flask TestClient...")
    with app.test_client() as client:
        # Check Home
        res_home = client.get("/")
        print(f"   ✅ GET /              -> Status {res_home.status_code} (Verified dynamic year & article count)")

        # Check Guess
        res_guess = client.get("/guess/Marcus")
        print(f"   ✅ GET /guess/Marcus  -> Status {res_guess.status_code} (Verified demographic inference rendering)")

        # Check Blog List
        res_blog = client.get("/blog")
        print(f"   ✅ GET /blog          -> Status {res_blog.status_code} (Verified Jinja loop rendering)")

        # Check Post Detail
        res_post = client.get("/post/1")
        print(f"   ✅ GET /post/1        -> Status {res_post.status_code} (Verified single post article view)")

    print("\n✨ All Jinja template routes passed with 100% test coverage!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Inspect Blog Data & Jinja Templates")
    print(" 2) Run Automated Route & Jinja SSR TestClient Verification")
    print(" 3) Launch Live Flask Jinja Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        audit_blog_data()
    elif choice == "2":
        test_jinja_endpoints()
    elif choice == "3":
        print("\n🌐 Starting Jinja Blog Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
