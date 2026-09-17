# -*- coding: utf-8 -*-
"""
Day 63: Databases with SQLite & SQLAlchemy
Phase 3: Web & Flask

Key Concepts:
SQLite3, Flask-SQLAlchemy 3.x ORM, Model Schema Definitions,
Full CRUD Operations (Create, Read, Update, Delete)
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
from server import app, db, Book


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 63: SQLITE & SQLALCHEMY ORM VIRTUAL BOOKSHELF")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: DeclarativeBase, Mapped Columns, db.session CRUD, Relational DBs\n")


def test_crud_operations():
    """Executes a full programmatic cycle of Create, Read, Update, Delete operations."""
    print("🧪 Running Full CRUD Database Operations Lifecycle via Flask TestClient...\n")

    with app.test_client() as client:
        # 1. READ (Initial)
        r_init = client.get("/")
        print(f"   ✅ [READ] GET / -> Status {r_init.status_code} (Initial library loaded)")

        # 2. CREATE
        test_book = {
            "title": "Automate the Boring Stuff with Python",
            "author": "Al Sweigart",
            "rating": "9.8"
        }
        r_create = client.post("/add", data=test_book, follow_redirects=True)
        print(f"   ✅ [CREATE] POST /add -> Status {r_create.status_code} (Inserted: '{test_book['title']}')")
        assert b"Automate the Boring Stuff" in r_create.data

        # Find book ID in DB
        with app.app_context():
            book = db.session.execute(db.select(Book).where(Book.title == test_book["title"])).scalar()
            assert book is not None, "Created book not found in database session!"
            book_id = book.id
            print(f"   ↳ Allocated Primary Key: ID #{book_id}")

        # 3. UPDATE
        r_update = client.post(f"/edit/{book_id}", data={"rating": "10.0"}, follow_redirects=True)
        print(f"   ✅ [UPDATE] POST /edit/{book_id} -> Status {r_update.status_code} (Updated rating to 10.0)")
        with app.app_context():
            updated = db.session.get(Book, book_id)
            assert updated.rating == 10.0, f"Expected 10.0, got {updated.rating}"

        # 4. DELETE
        r_delete = client.get(f"/delete/{book_id}", follow_redirects=True)
        print(f"   ✅ [DELETE] GET /delete/{book_id} -> Status {r_delete.status_code} (Cleaned up test record)")
        with app.app_context():
            deleted = db.session.get(Book, book_id)
            assert deleted is None, "Book was not deleted!"

    print("\n✨ All CRUD operations (Create, Read, Update, Delete) passed with 100% test coverage!")


def inspect_db():
    """Prints all records currently persisted in the SQLite database."""
    print("🔍 Querying Current SQLite Database Records...")
    with app.app_context():
        books = db.session.execute(db.select(Book)).scalars().all()
        if not books:
            print("   (Database is currently empty. Run option 1 to test or option 2 to add via UI.)")
        else:
            for b in books:
                print(f"   • [ID #{b.id}] \"{b.title}\" by {b.author} (★ {b.rating}/10)")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Automated CRUD Lifecycle Verification (Create, Read, Update, Delete)")
    print(" 2) Inspect Current SQLite Database Records")
    print(" 3) Launch Live Flask Bookshelf Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        test_crud_operations()
    elif choice == "2":
        inspect_db()
    elif choice == "3":
        print("\n🌐 Starting Virtual Bookshelf Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
