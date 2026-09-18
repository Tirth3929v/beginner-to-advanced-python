# -*- coding: utf-8 -*-
"""
Day 65: Web Design Principles & UX/UI Theory
Phase 3: Web & Flask

Key Concepts:
Color Theory, Mathematical Typography (Major Third), WCAG 2.1 Contrast Ratios,
Design Token Systems, Nielsen Norman 10 Usability Heuristics
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
from server import app
from design_system import (
    CURATED_PALETTES,
    calculate_contrast_ratio,
    evaluate_wcag,
    generate_modular_scale,
)


def banner():
    """Prints the project banner and ASCII art."""
    print(LOGO)
    print("=" * 70)
    print(" 🚀 DAY 65: WEB DESIGN PRINCIPLES, DESIGN TOKENS & UX LAB")
    print(" 📚 Phase 3: Web & Flask | 100 Days of Code Python Bootcamp")
    print("=" * 70)
    print("Key Concepts: WCAG Contrast Calculus, Major Third Scale, Usability Heuristics\n")


def audit_design_tokens():
    """Calculates typography scales and color contrast metrics."""
    print("🎨 Auditing Curated Color Palettes & Contrast Accessibility...")
    for name, p in CURATED_PALETTES.items():
        contrast = calculate_contrast_ratio(p["primary"], p["bg"])
        wcag = evaluate_wcag(contrast)
        status = "✅ PASS (AA)" if wcag["AA_normal"] else "⚠️ CAUTION (<4.5:1)"
        print(f"   • {name:<18} | Primary: {p['primary']} vs Bg: {p['bg']} -> Contrast {contrast:.2f}:1 [{status}]")

    print("\n🔤 Computing Mathematical Typography Scale (Major Third - 1.25):")
    scale = generate_modular_scale(base=16.0, ratio=1.25, steps=6)
    for step in scale[::-1]:
        print(f"   • [{step['label']:<6}] {step['px']:>5.2f}px  ({step['rem']:>5.3f}rem)")


def test_design_endpoints():
    """Validates endpoints using Flask TestClient."""
    print("\n🧪 Running Automated Route Checks via Flask TestClient...")
    with app.test_client() as client:
        # GET /
        res_home = client.get("/")
        print(f"   ✅ GET /                     -> Status {res_home.status_code} ({len(res_home.data):,} bytes)")
        assert b"Web Design School" in res_home.data

        # GET /api/contrast
        res_api = client.get("/api/contrast?fg=%23ffffff&bg=%23000000")
        print(f"   ✅ GET /api/contrast         -> Status {res_api.status_code} (White/Black Contrast: 21:1)")
        data = res_api.get_json()
        assert data["contrast_ratio"] == 21.0

    print("\n✨ Design token calculators and studio web routes verified with 100% success!")


def run_project():
    banner()
    print("Choose an action:")
    print(" 1) Run Design Tokens & WCAG Contrast Ratio Audit")
    print(" 2) Run Automated Route & API Verification (Flask TestClient)")
    print(" 3) Launch Live Flask Design System Studio (http://127.0.0.1:5000)")
    print(" 4) Exit")

    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"

    if choice == "1":
        audit_design_tokens()
    elif choice == "2":
        test_design_endpoints()
    elif choice == "3":
        print("\n🌐 Starting Design Lab Studio on http://127.0.0.1:5000 ... (Press Ctrl+C to stop)")
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
