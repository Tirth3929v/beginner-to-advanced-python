"""
Day 87: Cafe & Wifi Website
Phase 5: Portfolio

Key Concepts:
Flask Full-Stack, Bootstrap 5, SQLite/SQLAlchemy Database, Search Filtering
"""

import sys

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def banner():
    """Prints the project banner."""
    print("=" * 70)
    print(f" 🚀 DAY 87: CAFE & WIFI WEBSITE")
    print(f" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Flask Full-Stack, Bootstrap 5, SQLite/SQLAlchemy Database, Search Filtering\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 87/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 87 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
