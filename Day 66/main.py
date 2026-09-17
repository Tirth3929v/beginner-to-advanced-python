"""
Day 66: Building Your Own RESTful API
Phase 3: Web & Flask

Key Concepts:
REST Architecture, GET/POST/PATCH/DELETE Endpoints, Postman, JSON Responses
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
    print(f" 🚀 DAY 66: BUILDING YOUR OWN RESTFUL API")
    print(f" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print(f"Key Concepts: REST Architecture, GET/POST/PATCH/DELETE Endpoints, Postman, JSON Responses\n")


def run_project():
    """Core demonstration and project logic."""
    banner()
    print("Project architecture and starter modules initialized.")
    print(f"To explore and extend this project, check README.md in Day 66/.\n")
    print("Happy Coding! ✨\n")


def main():
    try:
        run_project()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 66 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
