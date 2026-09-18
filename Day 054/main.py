# -*- coding: utf-8 -*-
"""
Day 54: Introduction to Web Development with Flask
Phase 2: Intermediate

Key Concepts:
Higher-Order Functions, Decorator Syntactic Sugar, Flask Routing, Microframeworks
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
from decorator_playground import run_decorator_demo
from server import app


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 68)
    print(" 🚀 DAY 54: FLASK WEB INTRO & PYTHON DECORATOR ENGINE")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 68)
    print("Key Concepts: Closures, *args/**kwargs Wrappers, WSGI Routing\n")


def test_flask_endpoints():
    """Tests all Flask endpoints using Flask's built-in TestClient."""
    print("🧪 Running Automated Route Tests via Flask TestClient...")
    with app.test_client() as client:
        routes = ["/", "/bye", "/greet/Alice", "/status"]
        for r in routes:
            resp = client.get(r)
            status_emoji = "✅" if resp.status_code == 200 else "❌"
            print(f"   {status_emoji} GET {r:<18} -> Status {resp.status_code} ({len(resp.data)} bytes)")
    print("\n✨ All route decorators operational!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Decorator Speed Benchmark & HTML Wrapper Suite")
    print(" 2) Run Flask TestClient Automated Endpoint Check")
    print(" 3) Launch Live Flask Server (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        run_decorator_demo()
    elif choice == "2":
        test_flask_endpoints()
    elif choice == "3":
        print("\n🌐 Starting Flask Server on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
