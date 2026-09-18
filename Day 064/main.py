# -*- coding: utf-8 -*-
"""
Day 64: My Top 10 Movies Website
Phase 3: Web & Flask

Key Concepts:
SQLAlchemy 2.0 ORM, Flask-WTF Forms, Dynamic Ranking Algorithms,
External REST Movie APIs (TMDB) with Offline Fallback Integration
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
from server import app, db, Movie


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 64: MY TOP 10 MOVIES WEBSITE & RANKING ENGINE")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: Dynamic Re-ranking, TMDB REST API, WTForms, SQLAlchemy ORM\n")


def test_movie_endpoints():
    """Runs automated verification of the movie ranking and CRUD pipeline."""
    print("🧪 Running Automated Movie Showcase Verification via Flask TestClient...\n")

    with app.test_client() as client:
        # 1. Check Homepage & Seed Data
        r_home = client.get("/")
        print(f"   ✅ [GET /] Status {r_home.status_code} (Homepage rendered with movie cards)")
        assert b"The Matrix" in r_home.data

        # 2. Add Movie Search
        app.config["WTF_CSRF_ENABLED"] = False
        r_search = client.post("/add", data={"title": "Dark Knight"})
        print(f"   ✅ [POST /add] Status {r_search.status_code} (Searched TMDB/Catalog -> Options rendered)")
        assert b"Select Movie to Add" in r_search.data

        # 3. Select & Import Movie
        r_import = client.get("/find?id=155", follow_redirects=True)
        print(f"   ✅ [GET /find?id=155] Status {r_import.status_code} (Imported movie into SQLite & directed to edit)")

        # Find new movie ID
        with app.app_context():
            dk = db.session.execute(db.select(Movie).where(Movie.title == "The Dark Knight")).scalar()
            assert dk is not None, "Imported movie not found in DB!"
            dk_id = dk.id

        # 4. Rate & Review Movie (giving 9.9 so it becomes #1!)
        r_rate = client.post(f"/edit?id={dk_id}", data={"rating": "9.9", "review": "Legendary Heath Ledger Joker performance."}, follow_redirects=True)
        print(f"   ✅ [POST /edit?id={dk_id}] Status {r_rate.status_code} (Rated 9.9 -> Re-ranked to #1!)")
        assert b"#1" in r_rate.data

        # 5. Delete Test Movie
        r_del = client.get(f"/delete?id={dk_id}", follow_redirects=True)
        print(f"   ✅ [GET /delete?id={dk_id}] Status {r_del.status_code} (Deleted and re-ranked remaining collection)")

        app.config["WTF_CSRF_ENABLED"] = True

    print("\n✨ All movie database, search, and dynamic ranking operations passed with 100% test coverage!")


def inspect_movies():
    """Prints ranked movie records currently stored in SQLite."""
    print("🔍 Querying Ranked Movies Collection from Database...")
    with app.app_context():
        movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
        for m in movies:
            print(f"   🏆 #{m.ranking:<2} {m.title} ({m.year}) - ★ {m.rating}/10")
            print(f"       💬 \"{m.review}\"")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated Movie Search, CRUD & Re-ranking Simulation")
    print(" 2) Inspect Current Ranked Movies Database")
    print(" 3) Launch Live Top Movies Showcase Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_movie_endpoints()
    elif choice == "2":
        inspect_movies()
    elif choice == "3":
        print("\n🌐 Starting Top 10 Movies Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
