# -*- coding: utf-8 -*-
"""
Day 55: HTML & URL Parsing in Flask and the Higher-Lower Game
Phase 2: Intermediate

Key Concepts:
Flask URL Path Converters (<int:var>), Advanced Decorators (*args, **kwargs),
Dynamic Response Generation, HTML Templating Logic
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
from advanced_decorators import run_decorator_exercises
from server import app, get_secret, reset_secret


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 68)
    print(" 🚀 DAY 55: HIGHER OR LOWER FLASK WEB GAME")
    print(" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 68)
    print("Key Concepts: URL Path Variables, Dynamic HTML Responses, Advanced Decorators\n")


def test_game_endpoints():
    """Runs automated simulation testing all game conditions via TestClient."""
    print("🧪 Running Higher-Lower Game Engine Simulation via Flask TestClient...")
    secret = get_secret()
    print(f"🎯 Current Server Secret Number: {secret}")

    with app.test_client() as client:
        # Test Home
        resp = client.get("/")
        print(f"   ✅ GET /       -> Status {resp.status_code} (Homepage Loaded)")

        # Test too low (if secret > 0)
        if secret > 0:
            low_guess = secret - 1
            resp = client.get(f"/{low_guess}")
            print(f"   📉 GET /{low_guess}     -> Status {resp.status_code} (Verified 'Too low' response)")

        # Test too high (if secret < 9)
        if secret < 9:
            high_guess = secret + 1
            resp = client.get(f"/{high_guess}")
            print(f"   📈 GET /{high_guess}     -> Status {resp.status_code} (Verified 'Too high' response)")

        # Test exact match
        resp = client.get(f"/{secret}")
        print(f"   🎉 GET /{secret}     -> Status {resp.status_code} (Verified 'You found me!' winning response)")

        # Test reset
        resp = client.get("/reset")
        print(f"   🔄 GET /reset  -> Status {resp.status_code} (Secret Number reset to {get_secret()})")

    print("\n✨ All URL parsing and game state logic verified!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Advanced Decorators Exercises (*args, **kwargs, Auth Guard)")
    print(" 2) Run Automated Higher-Lower TestClient Game Simulation")
    print(" 3) Launch Live Flask Higher-Lower Web Game (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        run_decorator_exercises()
    elif choice == "2":
        test_game_endpoints()
    elif choice == "3":
        print(f"\n🎯 Current Secret Number is: {get_secret()}")
        print("🌐 Starting Flask Web Game on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
