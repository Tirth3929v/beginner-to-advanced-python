"""
Day 69: Blog Capstone Project (Part 4 - Users, Relational DBs & Admin Access)
Phase 3: Web Development & Architecture Capstone
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
from models import db, User, BlogPost, Comment
from server import create_app


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 69: RELATIONAL BLOG CAPSTONE & ROLE-BASED ACCESS CONTROL (RBAC)")
    print(" 📚 Phase 3: Advanced Web Architecture | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Architectural Pillars:")
    print("  • Bidirectional One-to-Many SQLAlchemy 2.0 ORM Relationships")
    print("  • Route Authorization Decorator (@admin_only -> HTTP 403 Barrier)")
    print("  • PBKDF2:SHA256 Password Cryptography & Flask-Login User Sessions")
    print("  • Threaded Discussion Comments linked to Authors and Blog Posts")
    print("=" * 76 + "\n")


def run_automated_tests():
    """Runs a complete test suite verifying ORM relationships, RBAC, and auth."""
    print("\n🔍 Running Day 69 Automated Architecture & RBAC Test Suite...")
    print("-" * 76)

    # Use in-memory SQLite database and disable CSRF for test client
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-key-day69"
    }

    app = create_app(test_config)
    client = app.test_client()

    with app.app_context():
        # 1. Verify Seed Users & Posts
        admin = db.session.get(User, 1)
        reader = db.session.get(User, 2)
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
        comments = db.session.execute(db.select(Comment)).scalars().all()

        assert admin is not None, "Admin user (id=1) must exist."
        assert admin.email == "admin@email.com", f"Expected admin@email.com, got {admin.email}"
        assert reader is not None, "Standard user (id=2) must exist."
        assert len(posts) >= 2, f"Expected at least 2 seeded posts, got {len(posts)}"
        assert len(comments) >= 1, f"Expected at least 1 seeded comment, got {len(comments)}"
        print(" [PASS] 1. Database initialization and initial seed data verified.")

        # 2. Verify Bidirectional Relationships
        assert len(admin.posts) == 2, "Admin should be parent to 2 posts."
        assert posts[0].author.name == admin.name, "BlogPost.author should reference Admin."
        assert comments[0].comment_author.id == reader.id, "Comment.comment_author should reference Reader."
        assert comments[0].parent_post.id == posts[0].id, "Comment.parent_post should reference Post 1."
        print(f" [PASS] 2. Bidirectional ORM relations verified:")
        print(f"         - User '{admin.name}' has authored {len(admin.posts)} articles.")
        print(f"         - Article '{posts[0].title[:35]}...' has {len(posts[0].comments)} comment(s).")
        print(f"         - Comment written by '{comments[0].comment_author.name}'.")

        # 3. Test Public Endpoints
        res_home = client.get("/")
        assert res_home.status_code == 200, f"Home route returned {res_home.status_code}"
        assert b"Clean Blog" in res_home.data
        print(" [PASS] 3. Public Home route (GET /) serves article feed (HTTP 200).")

        res_post = client.get(f"/post/{posts[0].id}")
        assert res_post.status_code == 200, f"Post route returned {res_post.status_code}"
        assert posts[0].title.encode() in res_post.data
        print(f" [PASS] 4. Article detail route (GET /post/{posts[0].id}) renders content (HTTP 200).")

        # 4. Test RBAC: Unauthenticated user attempting /new-post -> 403 Forbidden
        res_unauth_new = client.get("/new-post")
        assert res_unauth_new.status_code == 403, f"Expected 403 Forbidden for unauth user, got {res_unauth_new.status_code}"
        print(" [PASS] 5. RBAC Barrier: Anonymous user accessing /new-post correctly blocked (HTTP 403).")

        # 5. Test Login as Standard Reader & Attempt /new-post -> 403 Forbidden
        login_res = client.post("/login", data={"email": "elena@example.com", "password": "wrongpassword"}, follow_redirects=True)
        assert b"Invalid password" in login_res.data or b"danger" in login_res.data
        print(" [PASS] 6. Authentication: Invalid password rejected with flash alert.")

        # Valid login as Elena (User ID 2)
        login_elena = client.post("/login", data={"email": "elena@example.com", "password": "12345678"}, follow_redirects=True)
        assert login_elena.status_code == 200
        print(" [PASS] 7. Authentication: Reader user logged in successfully.")

        # Elena attempting /new-post -> Must still be 403 Forbidden!
        res_elena_new = client.get("/new-post")
        assert res_elena_new.status_code == 403, f"Expected 403 Forbidden for standard user, got {res_elena_new.status_code}"
        print(" [PASS] 8. RBAC Barrier: Standard user (id=2) accessing /new-post strictly rejected (HTTP 403).")

        # 6. Test Reader Adding a Comment
        comment_res = client.post(
            f"/post/{posts[0].id}",
            data={"comment_text": "This automated test comment confirms the feedback loop works!"},
            follow_redirects=True
        )
        assert comment_res.status_code == 200
        # Check comment in database
        updated_post = db.session.get(BlogPost, posts[0].id)
        assert any("automated test comment" in c.text for c in updated_post.comments), "New comment must be in DB."
        print(" [PASS] 9. Discussion Engine: Standard user submitted comment successfully.")

        # 7. Test Admin Login & Article Creation
        client.get("/logout")
        client.post("/login", data={"email": "admin@email.com", "password": "12345678"}, follow_redirects=True)

        new_post_res = client.post("/new-post", data={
            "title": "Architecting Zero Trust Microservices in Python",
            "subtitle": "Principles of least privilege and cryptographic validation.",
            "img_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1600&q=80",
            "body": "<p>A deep dive into distributed authorization with JWTs and mTLS.</p>"
        }, follow_redirects=True)
        assert new_post_res.status_code == 200
        new_post = db.session.execute(
            db.select(BlogPost).where(BlogPost.title == "Architecting Zero Trust Microservices in Python")
        ).scalar_one_or_none()
        assert new_post is not None, "Newly authored post should exist in DB."
        assert new_post.author_id == 1, "Author ID must equal 1 (Admin)."
        print(" [PASS] 10. Admin Privileges: Admin published new article with author_id=1.")

    print("-" * 76)
    print("✨ ALL 10 TESTS PASSED! Relational Blog Architecture & RBAC fully operational.\n")


def inspect_database():
    """Queries and displays live relational database records."""
    app = create_app()
    with app.app_context():
        users = db.session.execute(db.select(User)).scalars().all()
        posts = db.session.execute(db.select(BlogPost)).scalars().all()
        comments = db.session.execute(db.select(Comment)).scalars().all()

        print("\n" + "=" * 76)
        print(" 📊 RELATIONAL DATABASE INSPECTION (blog_relational.db)")
        print("=" * 76)
        print(f"\n👤 Registered Users ({len(users)}):")
        for u in users:
            role = "👑 Admin (ID=1)" if u.id == 1 else "👤 Reader"
            print(f"  • ID #{u.id}: {u.name} <{u.email}> [{role}] — Authored {len(u.posts)} post(s), {len(u.comments)} comment(s)")

        print(f"\n📰 Published Articles ({len(posts)}):")
        for p in posts:
            print(f"  • Post #{p.id}: \"{p.title}\"")
            print(f"    Author: {p.author.name} (User ID #{p.author_id}) | Date: {p.date} | Comments: {len(p.comments)}")

        print(f"\n💬 Discussion Comments ({len(comments)}):")
        for c in comments:
            print(f"  • Comment #{c.id} on Post #{c.post_id} by {c.comment_author.name} (User #{c.author_id}):")
            print(f"    \"{c.text}\" ({c.date})")
        print("=" * 76 + "\n")


def run_server():
    """Starts the Flask development server with admin credentials."""
    app = create_app()
    print("\n" + "=" * 76)
    print(" 🚀 STARTING CLEAN BLOG CAPSTONE SERVER")
    print("=" * 76)
    print(" 🌐 URL: http://127.0.0.1:5000")
    print("\n 🔑 Pre-seeded Accounts:")
    print("  • Admin Account (Can write, edit, delete articles):")
    print("      Email:    admin@email.com")
    print("      Password: 12345678")
    print("  • Reader Account (Can read and comment):")
    print("      Email:    elena@example.com")
    print("      Password: 12345678")
    print("=" * 76)
    print(" Press Ctrl+C in your terminal to shut down the server.\n")
    app.run(debug=True, port=5000)


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 🔍 Run Automated Verification Suite (ORM, RBAC & Auth tests)")
        print("  2) 📊 Inspect Relational Database Schema & Records")
        print("  3) 🌐 Launch Live Flask Web Application (http://127.0.0.1:5000)")
        print("  4) 🚪 Exit")
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            run_automated_tests()
        elif choice == "2":
            inspect_database()
        elif choice == "3":
            run_server()
            break
        elif choice in ("4", "exit", "quit", "q"):
            print("\n👋 Exiting Clean Blog Capstone. Keep building! 🚀\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 69 gracefully... Goodbye!\n")
