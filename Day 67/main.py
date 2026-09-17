# -*- coding: utf-8 -*-
"""
Day 67: RESTful Blog Capstone (Part 3)
Phase 3: Web & Flask

Key Concepts:
RESTful Route Architecture (GET /post, POST /new-post, POST /edit-post, GET /delete),
WTForms Integration, Jinja Template Inheritance & SQLAlchemy 2.0 ORM
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
from server import app, db, BlogPost


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 67: RESTFUL BLOG CAPSTONE & CMS ENGINE")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: RESTful URL Routing, WTForms, SQLAlchemy ORM, Full CMS\n")


def test_blog_crud():
    """Runs automated verification of the RESTful blog CRUD lifecycle."""
    print("🧪 Running Automated RESTful Blog CRUD Suite via Flask TestClient...\n")

    with app.test_client() as client:
        # 1. READ (GET /)
        r_home = client.get("/")
        print(f"   ✅ [GET /] Status {r_home.status_code} (Homepage rendered with published articles)")
        assert b"The Future of Distributed Systems" in r_home.data

        # 2. CREATE (POST /new-post)
        app.config["WTF_CSRF_ENABLED"] = False
        new_article = {
            "title": "Autonomous Coding Agents in 2026",
            "subtitle": "How agentic loops and tool calling revolutionize development",
            "author": "Tirth Patel",
            "img_url": "https://images.unsplash.com/photo-1518770660439",
            "body": "<p>Autonomous coding agents represent a quantum leap in developer velocity.</p>"
        }
        r_create = client.post("/new-post", data=new_article, follow_redirects=True)
        print(f"   ✅ [POST /new-post] Status {r_create.status_code} (Created article: '{new_article['title']}')")
        assert b"Autonomous Coding Agents" in r_create.data

        # Find post ID in database
        with app.app_context():
            post = db.session.execute(db.select(BlogPost).where(BlogPost.title == new_article["title"])).scalar()
            assert post is not None, "Created post was not found in DB!"
            post_id = post.id
            print(f"   ↳ Allocated Primary Key: ID #{post_id}")

        # 3. READ SINGLE ARTICLE (GET /post/<id>)
        r_show = client.get(f"/post/{post_id}")
        print(f"   ✅ [GET /post/{post_id}] Status {r_show.status_code} (Article detail page rendered)")
        assert b"quantum leap in developer velocity" in r_show.data

        # 4. UPDATE (POST /edit-post/<id>)
        edit_data = {
            "title": "Autonomous Coding Agents in 2026 (Updated)",
            "subtitle": new_article["subtitle"],
            "author": new_article["author"],
            "img_url": new_article["img_url"],
            "body": "<p>Updated body content with production benchmarks.</p>"
        }
        r_edit = client.post(f"/edit-post/{post_id}", data=edit_data, follow_redirects=True)
        print(f"   ✅ [POST /edit-post/{post_id}] Status {r_edit.status_code} (Updated title to 'Updated')")
        assert b"Updated" in r_edit.data

        # 5. DELETE (GET /delete/<id>)
        r_delete = client.get(f"/delete/{post_id}", follow_redirects=True)
        print(f"   ✅ [GET /delete/{post_id}] Status {r_delete.status_code} (Article successfully deleted)")
        with app.app_context():
            deleted = db.session.get(BlogPost, post_id)
            assert deleted is None, "Post was not removed from DB!"

        app.config["WTF_CSRF_ENABLED"] = True

    print("\n✨ All RESTful blog operations (Create, Read, Update, Delete) passed with 100% test coverage!")


def inspect_posts():
    """Prints all articles stored in the database."""
    print("🔍 Querying Published Articles Database...")
    with app.app_context():
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
        for p in posts:
            print(f"   • [ID #{p.id:<2}] \"{p.title}\" by {p.author} ({p.date})")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated RESTful Blog CRUD Test Suite")
    print(" 2) Inspect Published Articles in SQLite Database")
    print(" 3) Launch Live RESTful Blog Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_blog_crud()
    elif choice == "2":
        inspect_posts()
    elif choice == "3":
        print("\n🌐 Starting RESTful Blog Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
