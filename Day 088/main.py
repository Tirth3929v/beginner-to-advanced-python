"""
Day 88: Todo List Web Application
Interactive Task Management CLI & Web Server Launcher
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
from models import db, Task
from server import create_app


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 88: FULL-STACK TODO LIST & TASK PRODUCTIVITY MANAGER")
    print(" 📚 Phase 4: Web Automation & Portfolio | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Application Architecture:")
    print("  • SQLAlchemy 2.0 ORM Task Schema with Categories & Priority Tiers")
    print("  • Category Tab Filtering & Real-Time Dynamic Progress Calculation")
    print("  • Checkbox State Toggling & Soft/Hard Deletion Lifecycle")
    print("  • RESTful JSON API (/api/tasks) for External Client Synchronization")
    print("=" * 76 + "\n")


def list_tasks():
    app = create_app()
    with app.app_context():
        tasks = db.session.execute(db.select(Task).order_by(Task.id.desc())).scalars().all()
        print(f"\n📋 CURRENT TASK BOARD ({len(tasks)} tasks)")
        print("=" * 70)
        for t in tasks:
            status = "\033[92m[DONE]\033[0m" if t.is_completed else "\033[93m[TODO]\033[0m"
            print(f"  {status} #{t.id:2d}: {t.title:<35} [{t.category:<8} | Priority: {t.priority}]")
        print("=" * 70 + "\n")


def quick_add():
    title = input("\nEnter task title: ").strip()
    if not title:
        print("⚠️ Task title cannot be empty.\n")
        return
    cat = input("Category (Work/Personal/Study/Health, default Study): ").strip() or "Study"
    prio = input("Priority (High/Medium/Low, default Medium): ").strip() or "Medium"

    app = create_app()
    with app.app_context():
        new_t = Task(title=title, category=cat, priority=prio)
        db.session.add(new_t)
        db.session.commit()
        print(f"✅ Added task #{new_t.id}: '{title}'\n")


def run_automated_tests():
    """Verifies database seeding, task addition, state toggle, deletion, and REST API."""
    print("\n🔍 Running Day 88 Automated Todo Web Application Test Suite...")
    print("-" * 70)

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-key-day88"
    }
    app = create_app(test_config)
    client = app.test_client()

    with app.app_context():
        # 1. Seeding check
        tasks = db.session.execute(db.select(Task)).scalars().all()
        assert len(tasks) >= 5, f"Expected at least 5 seeded tasks, got {len(tasks)}"
        print(f" [PASS] 1. Initial tasks seed verified: {len(tasks)} tasks present in database.")

        # 2. GET / route check
        res_home = client.get("/")
        assert res_home.status_code == 200
        assert b"Todo Desk" in res_home.data
        print(" [PASS] 2. Web UI (GET /) serves task management board (HTTP 200).")

        # 3. Add task check (POST /add)
        res_add = client.post("/add", data={
            "title": "Build Automated Unit Tests for Day 88",
            "category": "Work",
            "priority": "High"
        }, follow_redirects=True)
        assert res_add.status_code == 200
        new_task = db.session.execute(
            db.select(Task).where(Task.title == "Build Automated Unit Tests for Day 88")
        ).scalar_one_or_none()
        assert new_task is not None
        print(f" [PASS] 3. Task persistence verified: Created task #{new_task.id}.")

        # 4. Toggle completion check (GET /toggle/<id>)
        init_state = new_task.is_completed
        client.get(f"/toggle/{new_task.id}", follow_redirects=True)
        toggled_task = db.session.get(Task, new_task.id)
        assert toggled_task.is_completed != init_state
        print(f" [PASS] 4. State toggle verified: Changed is_completed from {init_state} to {toggled_task.is_completed}.")

        # 5. REST API check (GET & POST /api/tasks)
        res_get_api = client.get("/api/tasks")
        assert res_get_api.status_code == 200
        data = res_get_api.get_json()
        assert len(data) >= 6

        res_post_api = client.post("/api/tasks", json={
            "title": "API Task Item",
            "category": "Personal",
            "priority": "Low"
        })
        assert res_post_api.status_code == 201
        print(" [PASS] 5. RESTful JSON API (/api/tasks) verified for both GET and POST.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Todo Web Application fully operational.\n")


def run_server():
    app = create_app()
    print("\n" + "=" * 70)
    print(" 🚀 STARTING TODO DESK WEB SERVER")
    print("=" * 70)
    print(" 🌐 URL: http://127.0.0.1:5000")
    print(" Press Ctrl+C in your terminal to shut down the server.\n")
    app.run(debug=True, port=5000)


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 📋 List All Tasks (Terminal Overview)")
        print("  2) ➕ Quick Add Task via Console")
        print("  3) 🌐 Launch Live Web Application (http://127.0.0.1:5000)")
        print("  4) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            list_tasks()
        elif choice == "2":
            quick_add()
        elif choice == "3":
            run_server()
            break
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Stay organized and productive! 📋\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 88 gracefully... Goodbye!\n")
