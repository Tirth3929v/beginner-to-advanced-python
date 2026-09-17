"""
Day 57: Templating with Jinja in Flask
Phase 3: Web & Flask

Key Concepts:
Jinja2 Syntax, Loops & Conditionals, Agify & Genderize APIs Integration
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
    print(f" 🚀 DAY 57: TEMPLATING WITH JINJA IN FLASK")
    print(f" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: Jinja2 Syntax, Loops & Conditionals, Agify & Genderize APIs Integration\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 57/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 57 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
