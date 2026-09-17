"""
Day 82: Portfolio Website Deployment
Interactive Developer Showcase CLI & Web Server Launcher
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
from portfolio_data import PROFILE
from server import create_app


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 82: PROFESSIONAL DEVELOPER PORTFOLIO SHOWCASE & WEB SERVER")
    print(" 📚 Phase 4: Professional Portfolio Projects | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Portfolio Architecture Highlights:")
    print("  • Modular JSON/Python Data Schema for Projects & Skills")
    print("  • Modern Dark Glassmorphic UI with Bootstrap 5 & Inter Typography")
    print("  • RESTful API Endpoints (/api/projects, /api/skills)")
    print("  • Integrated Contact Message Transmission Engine")
    print("=" * 76 + "\n")


def display_skills():
    print(f"\n👤 DEVELOPER PROFILE: {PROFILE['name']} — {PROFILE['title']}")
    print(f"📍 Location: {PROFILE['location']} | GitHub: {PROFILE['github']}")
    print(f"📝 {PROFILE['tagline']}\n")
    print("🛠️ TECHNICAL SKILLS INVENTORY:")
    print("=" * 65)
    for skill in PROFILE["skills"]:
        bar = "█" * (8 if skill["level"] == "Expert" else 6)
        print(f"  • {skill['name']:<24} [{skill['category']:<12}] \033[92m{skill['level']:<8}\033[0m {bar}")
    print("=" * 65 + "\n")


def display_projects():
    print(f"\n📂 FEATURED PROJECTS SHOWCASE ({len(PROFILE['projects'])} projects)")
    print("=" * 70)
    for p in PROFILE["projects"]:
        print(f"\n  ⭐ {p['title']} ({p['day']})")
        print(f"     Category: \033[94m{p['category']}\033[0m")
        print(f"     Summary:  {p['description']}")
        print(f"     Stack:    {', '.join(p['tech'])}")
        print(f"     Path:     \033[93m{p['github_path']}\033[0m")
    print("=" * 70 + "\n")


def run_automated_tests():
    """Verifies portfolio data integrity, Flask routes, and REST API endpoints."""
    print("\n🔍 Running Day 82 Automated Portfolio Verification Suite...")
    print("-" * 70)

    app = create_app()
    client = app.test_client()

    # 1. Profile data integrity
    assert len(PROFILE["skills"]) >= 8
    assert len(PROFILE["projects"]) >= 5
    print(f" [PASS] 1. Portfolio data models: {len(PROFILE['skills'])} skills and {len(PROFILE['projects'])} projects cataloged.")

    # 2. Test GET /
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert PROFILE["name"].encode() in res_home.data
    assert b"Featured Flagship Projects" in res_home.data
    print(" [PASS] 2. Home route (GET /) rendered portfolio showcase (HTTP 200).")

    # 3. Test POST / (Contact form submission)
    res_contact = client.post("/", data={
        "name": "Jane Recruiter",
        "email": "jane@faang.com",
        "message": "We would love to interview you for a Senior Python role."
    })
    assert res_contact.status_code == 200
    assert b"transmitted successfully" in res_contact.data
    print(" [PASS] 3. Contact inquiry transmission: Simulated form submission successful.")

    # 4. Test REST API /api/projects
    res_api_proj = client.get("/api/projects")
    assert res_api_proj.status_code == 200
    json_data = res_api_proj.get_json()
    assert len(json_data) == len(PROFILE["projects"])
    print(f" [PASS] 4. Projects REST API (/api/projects) returned {len(json_data)} JSON project objects.")

    # 5. Test REST API /api/skills
    res_api_skills = client.get("/api/skills")
    assert res_api_skills.status_code == 200
    skills_data = res_api_skills.get_json()
    assert len(skills_data) == len(PROFILE["skills"])
    print(f" [PASS] 5. Skills REST API (/api/skills) returned {len(skills_data)} JSON skill objects.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Portfolio Web Application fully operational.\n")


def run_server():
    app = create_app()
    print("\n" + "=" * 70)
    print(" 🚀 STARTING PORTFOLIO WEB SERVER")
    print("=" * 70)
    print(" 🌐 URL: http://127.0.0.1:5000")
    print(" Press Ctrl+C in your terminal to shut down the server.\n")
    app.run(debug=True, port=5000)


def main():
    banner()
    while True:
        print("Select an option:")
        print("  1) 👤 View Developer Profile & Skills Inventory")
        print("  2) 📂 Browse Featured Flagship Projects")
        print("  3) 🌐 Launch Live Portfolio Web Server (http://127.0.0.1:5000)")
        print("  4) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            display_skills()
        elif choice == "2":
            display_projects()
        elif choice == "3":
            run_server()
            break
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Keep showcasing your craft! 🚀\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 82 gracefully... Goodbye!\n")
