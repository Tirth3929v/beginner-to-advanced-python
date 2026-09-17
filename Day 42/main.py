"""
Day 42: Web Foundation - Intermediate HTML
Phase 2: Intermediate

Key Concepts:
HTML Tables, Forms, Input Types, Labels, Containers & Structuring
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
    print(f" 🚀 DAY 42: WEB FOUNDATION - INTERMEDIATE HTML")
    print(f" 📚 Phase 2: Intermediate | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: HTML Tables, Forms, Input Types, Labels, Containers & Structuring\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 42/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 42 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
