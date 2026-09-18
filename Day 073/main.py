"""
Day 73: Aggregate & Merge Data with Pandas
Interactive LEGO Historical Analytics CLI
"""

import sys
import os
import pandas as pd

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO
from lego_analyzer import LegoAnalyzer


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 73: AGGREGATE & MERGE RELATIONAL DATA WITH PANDAS (LEGO DATABASE)")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Pandas Merge & Relational Concepts:")
    print("  • Database Joins: Inner joins with pd.merge(on='id', how='inner')")
    print("  • Multi-attribute aggregations: .value_counts(), .groupby('year').agg()")
    print("  • Dual-Axis Visualization: Tracking volume output vs piece complexity")
    print("  • Handling relational hierarchies (themes, parent themes, and set entities)")
    print("=" * 76 + "\n")


def display_colors(analyzer: LegoAnalyzer):
    stats = analyzer.get_color_stats()
    print("\n🎨 LEGO PALETTE & COLOR STATISTICS")
    print("=" * 60)
    print(f"  • Total Distinct Colors:      {stats['total_colors']}")
    print(f"  • Standard / Opaque Colors:   {stats['opaque_colors']}")
    print(f"  • Transparent Bricks:         {stats['transparent_colors']}")
    print("=" * 60 + "\n")


def display_largest_sets(analyzer: LegoAnalyzer):
    largest = analyzer.get_largest_sets(6)
    print("\n🏰 TOP LARGEST LEGO SETS OF ALL TIME (BY PART COUNT)")
    print("=" * 65)
    for rank, (_, row) in enumerate(largest.iterrows(), start=1):
        print(f"  {rank}. {row['name']} ({row['year']})")
        print(f"     Set #{row['set_num']} | \033[92m{int(row['num_parts']):,d} parts\033[0m")
    print("=" * 65 + "\n")


def display_top_themes(analyzer: LegoAnalyzer):
    themes = analyzer.get_top_themes(10)
    print("\n⭐ TOP 10 LEGO THEMES BY NUMBER OF RELEASED SETS")
    print("=" * 65)
    for rank, (_, row) in enumerate(themes.iterrows(), start=1):
        bar = "█" * int(row['set_count'] / 2)
        print(f"  {rank:2d}. {row['name']:<24} {row['set_count']:>3d} sets  \033[93m{bar}\033[0m")
    print("=" * 65 + "\n")


def export_charts(analyzer: LegoAnalyzer):
    print("\n🎨 Generating dual-axis evolution chart with Matplotlib...")
    out_path = analyzer.export_lego_charts("lego_evolution.png")
    print("✅ Successfully exported chart to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies relational merges, aggregations, and metrics."""
    print("\n🔍 Running Day 73 Automated LEGO Data & Merge Test Suite...")
    print("-" * 70)
    analyzer = LegoAnalyzer()

    # 1. Colors check
    colors = analyzer.get_color_stats()
    assert colors["total_colors"] >= 20
    assert colors["transparent_colors"] > 0
    print(f" [PASS] 1. Color taxonomy verified: {colors['total_colors']} colors cataloged.")

    # 2. Oldest set check
    oldest = analyzer.get_oldest_sets(1).iloc[0]
    assert oldest["year"] == 1949
    print(f" [PASS] 2. Temporal extremes: Earliest LEGO sets verified in year 1949.")

    # 3. Largest set check
    largest = analyzer.get_largest_sets(1).iloc[0]
    assert largest["num_parts"] >= 7500
    print(f" [PASS] 3. Part complexity: Largest set identified ({largest['name']} with {int(largest['num_parts']):,d} parts).")

    # 4. Relational merge check
    top_themes = analyzer.get_top_themes(5)
    assert len(top_themes) == 5
    assert "name" in top_themes.columns and "set_count" in top_themes.columns
    print(f" [PASS] 4. Relational database join: Sets merged with Themes table successfully.")

    # 5. Dual-axis plot export check
    img_path = analyzer.export_lego_charts("test_lego.png")
    assert os.path.exists(img_path) and os.path.getsize(img_path) > 10000
    try:
        os.remove(img_path)
    except Exception:
        pass
    print(" [PASS] 5. Dual-axis visualization pipeline rendered valid image file.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! LEGO Analysis Engine fully operational.\n")


def main():
    banner()
    analyzer = LegoAnalyzer()

    while True:
        print("Select an option:")
        print("  1) 🎨 Color Palette & Transparent Brick Statistics")
        print("  2) 🏰 Top Largest LEGO Sets (By Part Count)")
        print("  3) ⭐ Most Prolific Themes (Relational Merge)")
        print("  4) 📈 Generate & Save Dual-Axis Complexity Chart (PNG)")
        print("  5) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  6) 🚪 Exit")
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            display_colors(analyzer)
        elif choice == "2":
            display_largest_sets(analyzer)
        elif choice == "3":
            display_top_themes(analyzer)
        elif choice == "4":
            export_charts(analyzer)
        elif choice == "5":
            run_automated_tests()
        elif choice in ("6", "exit", "quit", "q"):
            print("\n👋 Happy Building! Keep connecting your data blocks 🧱\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 73 gracefully... Goodbye!\n")
