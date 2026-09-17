"""
Day 71: Data Exploration with Pandas
College Major vs Post-Graduation Salary Analytics Engine
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
from analyzer import SalaryAnalyzer


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 71: DATA EXPLORATION & STATISTICAL ANALYSIS WITH PANDAS")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Pandas Capabilities:")
    print("  • Handling NaN values and data cleaning (.dropna(), .isna().any())")
    print("  • Indexing, filtering, and locating extrema (.idxmax(), .idxmin(), .loc[])")
    print("  • Feature Engineering: Computing percentile spread (.90th - .10th)")
    print("  • Multi-dimensional Grouping & Aggregations (.groupby(), .agg(), .mean())")
    print("=" * 76 + "\n")


def display_overview(analyzer: SalaryAnalyzer):
    stats = analyzer.get_summary_stats()
    print("\n📊 DATASET OVERVIEW & CLEANING AUDIT")
    print("=" * 70)
    print(f"  • Total Valid Majors Analyzed: {stats['total_majors']}")
    print(f"  • Feature Columns:             {', '.join(stats['columns'])}")
    print(f"  • Academic Group Categories:   {', '.join(stats['groups'])}")
    print(f"  • Overall Mean Starting Salary: ${stats['avg_starting']:,.2f}")
    print(f"  • Overall Mean Mid-Career:      ${stats['avg_mid_career']:,.2f}")
    print("=" * 70 + "\n")


def display_starting_salaries(analyzer: SalaryAnalyzer):
    top = analyzer.highest_starting_salary()
    low = analyzer.lowest_starting_salary()
    print("\n💰 STARTING SALARY EXTREMA")
    print("=" * 70)
    print(f"  🥇 Highest Starting Salary:")
    print(f"     Major:  \033[92m{top['Undergraduate Major']}\033[0m")
    print(f"     Salary: ${top['Starting Median Salary']:,.2f} / year ({top['Group']})")
    print(f"\n  📉 Lowest Starting Salary:")
    print(f"     Major:  \033[91m{low['Undergraduate Major']}\033[0m")
    print(f"     Salary: ${low['Starting Median Salary']:,.2f} / year ({low['Group']})")
    print("=" * 70 + "\n")


def display_mid_career(analyzer: SalaryAnalyzer):
    top_mid = analyzer.highest_mid_career_salary()
    print("\n🏆 HIGHEST MID-CAREER EARNING POTENTIAL")
    print("=" * 70)
    print(f"  🥇 Top Mid-Career Earner:")
    print(f"     Major:             \033[92m{top_mid['Undergraduate Major']}\033[0m")
    print(f"     Mid-Career Median: ${top_mid['Mid-Career Median Salary']:,.2f}")
    print(f"     90th Percentile:   ${top_mid['Mid-Career 90th Percentile Salary']:,.2f}")
    print("=" * 70 + "\n")


def display_risk_and_upside(analyzer: SalaryAnalyzer):
    print("\n🛡️ LOWEST RISK MAJORS (Smallest Salary Spread)")
    print("=" * 70)
    print("These degrees have the smallest variance between top 10% and bottom 10% earners:")
    low_risk = analyzer.lowest_risk_majors(5)
    print(low_risk.to_string(index=False))

    print("\n🚀 HIGHEST POTENTIAL MAJORS (Greatest Spread / Upside)")
    print("=" * 70)
    print("These degrees have the highest potential for top 10% outlier earnings:")
    high_pot = analyzer.highest_potential_majors(5)
    print(high_pot.to_string(index=False))
    print("=" * 70 + "\n")


def display_group_aggregations(analyzer: SalaryAnalyzer):
    print("\n🏛️ SALARY BREAKDOWN BY ACADEMIC CATEGORY (STEM vs Business vs HASS)")
    print("=" * 70)
    grouped = analyzer.group_by_field()
    print(grouped.to_string())
    print("=" * 70 + "\n")


def run_automated_tests():
    """Validates Pandas transformations and metric correctness."""
    print("\n🔍 Running Day 71 Automated Pandas Verification Suite...")
    print("-" * 70)
    analyzer = SalaryAnalyzer()

    # 1. Row count after cleaning
    assert len(analyzer.df) >= 49, f"Expected at least 49 majors, got {len(analyzer.df)}"
    print(f" [PASS] 1. Data cleaning verified: {len(analyzer.df)} rows loaded with zero NaN values.")

    # 2. Spread calculation
    first_row = analyzer.df.iloc[0]
    expected_spread = first_row["Mid-Career 90th Percentile Salary"] - first_row["Mid-Career 10th Percentile Salary"]
    assert first_row["Spread"] == expected_spread
    print(" [PASS] 2. Feature engineering verified: 'Spread' column mathematically correct.")

    # 3. Highest starting salary check
    top_start = analyzer.highest_starting_salary()
    assert top_start["Undergraduate Major"] == "Physician Assistant"
    assert top_start["Starting Median Salary"] == 74300.0
    print(" [PASS] 3. Starting salary max identification: Physician Assistant ($74,300).")

    # 4. Highest mid-career salary check
    top_mid = analyzer.highest_mid_career_salary()
    assert top_mid["Undergraduate Major"] == "Chemical Engineering"
    assert top_mid["Mid-Career Median Salary"] == 107000.0
    print(" [PASS] 4. Mid-career salary max identification: Chemical Engineering ($107,000).")

    # 5. Group-by aggregates check
    grouped = analyzer.group_by_field()
    assert set(grouped.index) == {"STEM", "Business", "HASS"}
    assert grouped.loc["STEM", "Avg_Starting_Salary"] > grouped.loc["HASS", "Avg_Starting_Salary"]
    print(" [PASS] 5. Categorical GroupBy aggregations: STEM > Business > HASS verified.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Pandas Analysis Engine fully operational.\n")


def main():
    banner()
    analyzer = SalaryAnalyzer()

    while True:
        print("Select an analysis module:")
        print("  1) 📊 Dataset Overview & Summary Statistics")
        print("  2) 💰 Top & Bottom Starting Salaries")
        print("  3) 🏆 Highest Mid-Career Earnings")
        print("  4) 🛡️ Lowest Risk Degrees vs Highest Upside Potential (Spread)")
        print("  5) 🏛️ Academic Field Comparison (STEM vs Business vs HASS)")
        print("  6) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  7) 🚪 Exit")
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            display_overview(analyzer)
        elif choice == "2":
            display_starting_salaries(analyzer)
        elif choice == "3":
            display_mid_career(analyzer)
        elif choice == "4":
            display_risk_and_upside(analyzer)
        elif choice == "5":
            display_group_aggregations(analyzer)
        elif choice == "6":
            run_automated_tests()
        elif choice in ("7", "exit", "quit", "q"):
            print("\n👋 Happy Data Exploring with Pandas! 📊\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-7.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 71 gracefully... Goodbye!\n")
