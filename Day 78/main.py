"""
Day 78: Analyzing the Nobel Prize with Seaborn
Nobel Laureates Demographics, Age Distributions & Repeat Winners CLI
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
from nobel_analyzer import NobelPrizeAnalyzer


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 78: ANALYZING NOBEL PRIZE DEMOGRAPHICS & TRENDS WITH SEABORN")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Exploratory Data Analysis Concepts:")
    print("  • Filtering & Identifying Repeat Laureates (.value_counts() > 1)")
    print("  • Demographic Feature Engineering: Age at award (Year - Birth Year)")
    print("  • Categorical Grouping: Proportions of female laureates by domain")
    print("  • Seaborn Visualization: Multi-panel subplots, boxplots & color palettes")
    print("=" * 76 + "\n")


def display_summary(analyzer: NobelPrizeAnalyzer):
    s = analyzer.get_summary()
    print("\n🏅 NOBEL PRIZE DATASET OVERVIEW (1901 - 2020)")
    print("=" * 65)
    print(f"  • Total Prizes Awarded:     {s['total_prizes']:,d}")
    print(f"  • Unique Laureates:         {s['unique_laureates']:,d}")
    print(f"  • Categories Represented:   {', '.join(s['categories'])}")
    print(f"  • Total Female Laureates:   {s['female_winners']} ({s['female_winners']/s['total_prizes']*100:.1f}%)")
    print(f"  • Overall Mean Winning Age: \033[93m{s['mean_winning_age']} years old\033[0m")
    print("=" * 65 + "\n")


def display_repeats(analyzer: NobelPrizeAnalyzer):
    repeats = analyzer.get_repeat_winners()
    print("\n⭐ MULTI-PRIZE WINNERS (REPEAT LAUREATES)")
    print("=" * 65)
    for rank, (_, row) in enumerate(repeats.iterrows(), start=1):
        print(f"  {rank}. \033[92m{row['full_name']}\033[0m — {row['prizes_won']} Nobel Prizes")
    print("=" * 65 + "\n")


def display_female_laureates(analyzer: NobelPrizeAnalyzer):
    first_w = analyzer.get_first_woman_laureate()
    print("\n👩 FEMALE NOBEL LAUREATE BREAKDOWN")
    print("=" * 65)
    print("  🥇 First Woman to Win a Nobel Prize:")
    print(f"     Name:     \033[92m{first_w['full_name']}\033[0m")
    print(f"     Category: {first_w['category']} ({first_w['year']})")
    print(f"     Country:  {first_w['birth_country']}")

    print("\n  📊 Female Laureate Share by Academic Field:")
    cat_df = analyzer.get_female_share_by_category()
    for _, row in cat_df.iterrows():
        bar = "█" * int(row['female_percentage'] / 2)
        print(f"     {row['category']:<12} {row['female_percentage']:>5.1f}%  \033[95m{bar}\033[0m ({row['total_prizes']} prizes)")
    print("=" * 65 + "\n")


def display_age_extremes(analyzer: NobelPrizeAnalyzer):
    ext = analyzer.get_youngest_and_oldest()
    y = ext["youngest"]
    o = ext["oldest"]
    print("\n⏳ LAUREATE AGE EXTREMES AT TIME OF AWARD")
    print("=" * 65)
    print("  👶 Youngest Laureate:")
    print(f"     Name:     \033[92m{y['full_name']}\033[0m")
    print(f"     Age:      \033[92m{int(y['winning_age'])} years old\033[0m ({y['year']})")
    print(f"     Category: {y['category']}")

    print("\n  👴 Oldest Laureate:")
    print(f"     Name:     \033[94m{o['full_name']}\033[0m")
    print(f"     Age:      \033[94m{int(o['winning_age'])} years old\033[0m ({o['year']})")
    print(f"     Category: {o['category']}")
    print("=" * 65 + "\n")


def display_countries(analyzer: NobelPrizeAnalyzer):
    top_c = analyzer.get_top_countries(10)
    print("\n🌍 TOP 10 LAUREATE BIRTH COUNTRIES")
    print("=" * 65)
    for rank, (country, count) in enumerate(top_c.items(), start=1):
        bar = "█" * int(count / 5)
        print(f"  {rank:2d}. {country:<20} {count:>3d} laureates  \033[96m{bar}\033[0m")
    print("=" * 65 + "\n")


def export_charts(analyzer: NobelPrizeAnalyzer):
    print("\n🎨 Rendering composite Seaborn demographics & age figures...")
    out_path = analyzer.export_nobel_charts("nobel_demographics.png")
    print("✅ Successfully exported charts to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies data parsing, repeat winner detection, age math, and Seaborn figure export."""
    print("\n🔍 Running Day 78 Automated Nobel Prize & Seaborn Test Suite...")
    print("-" * 70)
    analyzer = NobelPrizeAnalyzer()

    # 1. Row count & categories
    assert len(analyzer.df) >= 350
    assert len(analyzer.df["category"].unique()) >= 6
    print(f" [PASS] 1. Nobel prize database parsed: {len(analyzer.df)} awards across 6 domains.")

    # 2. Repeat winners detection
    repeats = analyzer.get_repeat_winners()
    assert len(repeats) >= 3
    repeat_names = set(repeats["full_name"])
    assert any("Marie Curie" in n for n in repeat_names)
    assert any("Linus Pauling" in n for n in repeat_names)
    print(f" [PASS] 2. Repeat winner identification: Marie Curie & Linus Pauling detected.")

    # 3. First female winner
    first_w = analyzer.get_first_woman_laureate()
    assert first_w["year"] == 1903
    assert "Marie Curie" in first_w["full_name"]
    print(" [PASS] 3. First woman laureate: Marie Curie (Physics, 1903) confirmed.")

    # 4. Age extremes
    ext = analyzer.get_youngest_and_oldest()
    assert ext["youngest"]["winning_age"] <= 18
    assert ext["oldest"]["winning_age"] >= 95
    print(f" [PASS] 4. Age calculations: Youngest ({int(ext['youngest']['winning_age'])}y) and Oldest ({int(ext['oldest']['winning_age'])}y) verified.")

    # 5. Seaborn plotting pipeline
    test_img = analyzer.export_nobel_charts("test_nobel.png")
    assert os.path.exists(test_img) and os.path.getsize(test_img) > 10000
    try:
        os.remove(test_img)
    except Exception:
        pass
    print(" [PASS] 5. Seaborn multi-panel demographics chart generated valid PNG.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Nobel Prize Analytics Engine fully operational.\n")


def main():
    banner()
    analyzer = NobelPrizeAnalyzer()

    while True:
        print("Select an analytical module:")
        print("  1) 🏅 Dataset Summary & Demographics Overview")
        print("  2) ⭐ Repeat Nobel Laureates (Multi-Prize Winners)")
        print("  3) 👩 Female Laureate Share & First Woman Winner")
        print("  4) ⏳ Age Extremes (Youngest vs Oldest Laureates)")
        print("  5) 🌍 Top 10 Laureate Birth Countries")
        print("  6) 🎨 Generate & Save Seaborn Demographics Chart (PNG)")
        print("  7) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  8) 🚪 Exit")
        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            display_summary(analyzer)
        elif choice == "2":
            display_repeats(analyzer)
        elif choice == "3":
            display_female_laureates(analyzer)
        elif choice == "4":
            display_age_extremes(analyzer)
        elif choice == "5":
            display_countries(analyzer)
        elif choice == "6":
            export_charts(analyzer)
        elif choice == "7":
            run_automated_tests()
        elif choice in ("8", "exit", "quit", "q"):
            print("\n👋 Happy Analyzing with Seaborn! 🏅\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-8.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 78 gracefully... Goodbye!\n")
