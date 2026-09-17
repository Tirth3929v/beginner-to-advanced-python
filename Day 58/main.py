"""
Day 58: Web Design School - Bootstrap 5
Phase 3: Web & Flask

Key Concepts:
Bootstrap 5 Grid System, Components, Cards, Responsive Navbar, Utilities
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
    print(f" 🚀 DAY 58: WEB DESIGN SCHOOL - BOOTSTRAP 5")
    print(f" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Bootstrap 5 Grid System, Components, Cards, Responsive Navbar, Utilities\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 58/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 58 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
