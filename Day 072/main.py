"""
Day 72: Data Visualization with Matplotlib
Interactive Analytics CLI & Chart Generator
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
from visualizer import TrendVisualizer


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 72: DATA VISUALIZATION WITH MATPLOTLIB & STACKOVERFLOW TRENDS")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Matplotlib Concepts:")
    print("  • Reshaping Datasets: Pivoting tables from Long to Wide format")
    print("  • Dealing with Missing Data via .fillna() and DateTime conversion")
    print("  • Smoothing volatile time series with .rolling(window=6).mean()")
    print("  • Customizing Figure dimensions, DPI, colors, legends, and gridlines")
    print("=" * 76 + "\n")


def display_totals(viz: TrendVisualizer):
    totals = viz.get_total_posts_by_language()
    print("\n📚 ALL-TIME STACKOVERFLOW POST TOTALS BY LANGUAGE")
    print("=" * 60)
    for rank, (lang, count) in enumerate(totals.items(), start=1):
        bar = "█" * int(count / (totals.max() / 30))
        print(f"  {rank:2d}. {lang.capitalize():<12} {count:>10,d} posts  \033[94m{bar}\033[0m")
    print("=" * 60 + "\n")


def display_recent(viz: TrendVisualizer):
    recent = viz.get_most_recent_rankings()
    print(f"\n⚡ MOST RECENT MONTHLY POST RANKINGS ({viz.reshaped_df.index[-1].strftime('%B %Y')})")
    print("=" * 60)
    for rank, (lang, count) in enumerate(recent.items(), start=1):
        print(f"  {rank:2d}. {lang.capitalize():<12} {int(count):>8,d} questions/month")
    print("=" * 60 + "\n")


def generate_chart(viz: TrendVisualizer):
    print("\n🎨 Rendering publication-quality multi-line chart with Matplotlib...")
    out_path = viz.export_trend_chart("programming_language_trends.png", smooth=True)
    print(f"✅ Successfully exported chart to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies pivot shaping, rolling window calculations, and chart generation."""
    print("\n🔍 Running Day 72 Automated Matplotlib & Data Reshaping Test Suite...")
    print("-" * 70)
    viz = TrendVisualizer()

    # 1. Check original and pivoted dimensions
    assert len(viz.df) > 500, f"Expected > 500 records, got {len(viz.df)}"
    assert "python" in viz.reshaped_df.columns
    assert "javascript" in viz.reshaped_df.columns
    print(f" [PASS] 1. Data loaded and successfully pivoted: {viz.reshaped_df.shape[0]} months across {viz.reshaped_df.shape[1]} languages.")

    # 2. Check no NaN after fillna
    assert not viz.reshaped_df.isna().any().any(), "Pivoted DataFrame should contain zero NaN values."
    print(" [PASS] 2. Missing value handling: 0 NaN values remaining.")

    # 3. Check rolling average calculation
    smooth_python = viz.smooth_df["python"].dropna()
    assert len(smooth_python) > 0
    print(" [PASS] 3. 6-Month rolling average calculation verified.")

    # 4. Check all-time totals
    totals = viz.get_total_posts_by_language()
    assert totals.index[0] in ["python", "javascript", "java"]
    print(f" [PASS] 4. Aggregations verified: Top language all-time is '{totals.index[0].capitalize()}'.")

    # 5. Export chart test
    test_img = viz.export_trend_chart("test_trends.png", smooth=True)
    assert os.path.exists(test_img) and os.path.getsize(test_img) > 10000
    try:
        os.remove(test_img)
    except Exception:
        pass
    print(" [PASS] 5. Matplotlib rendering pipeline: PNG output generated with valid binary size.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Matplotlib Visualizer fully operational.\n")


def main():
    banner()
    viz = TrendVisualizer()

    while True:
        print("Select an option:")
        print("  1) 📚 All-Time Historical Post Volume by Language")
        print("  2) ⚡ Latest Monthly Language Rankings")
        print("  3) 🎨 Generate & Save Multi-Line Trend Chart (PNG)")
        print("  4) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            display_totals(viz)
        elif choice == "2":
            display_recent(viz)
        elif choice == "3":
            generate_chart(viz)
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Happy Visualizing! Keep charting your progress 📈\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 72 gracefully... Goodbye!\n")
