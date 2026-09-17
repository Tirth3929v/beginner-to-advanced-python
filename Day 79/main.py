"""
Day 79: The Tragic Discovery of Handwashing
Dr. Ignaz Semmelweis Clinical Hypothesis Testing CLI
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
from semmelweis_analyzer import SemmelweisAnalyzer


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 79: CLINICAL HYPOTHESIS TESTING & DR. SEMMELWEIS HANDWASHING")
    print(" 📚 Phase 4: Data Science & Statistics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Statistical & Clinical Concepts:")
    print("  • Observational Discrepancy: Clinic 1 (Medical Students) vs Clinic 2 (Midwives)")
    print("  • Longitudinal Time-Series Analysis of Puerperal (Childbed) Sepsis")
    print("  • Welch's Two-Sample t-test (scipy.stats.ttest_ind with unequal variances)")
    print("  • Proving Statistical Significance: Rejecting null hypothesis (p < 0.0001)")
    print("=" * 76 + "\n")


def display_clinics(analyzer: SemmelweisAnalyzer):
    comp = analyzer.get_clinic_comparison()
    print("\n🏥 VIENNA GENERAL HOSPITAL: CLINIC 1 VS CLINIC 2 (1841 - 1846)")
    print("=" * 70)
    for _, row in comp.iterrows():
        clinic_name = "Clinic 1 (Doctors / Med Students performing autopsies)" if "1" in row["clinic"] else "Clinic 2 (Midwife trainee students)"
        print(f"  • {clinic_name}:")
        print(f"      Total Births:      {row['total_births']:,d}")
        print(f"      Maternal Deaths:   {row['total_deaths']:,d}")
        color = "\033[91m" if "1" in row["clinic"] else "\033[92m"
        print(f"      Mortality Rate:    {color}{row['mortality_percentage']:.2f}%\033[0m\n")
    print("  💡 Insight: Clinic 1's mortality rate was nearly 3x higher than Clinic 2,")
    print("     driving Semmelweis to deduce 'cadaverous particles' were transferred to mothers.")
    print("=" * 70 + "\n")


def display_hypothesis_test(analyzer: SemmelweisAnalyzer):
    res = analyzer.get_handwashing_impact()
    print("\n🧪 WELCH'S TWO-SAMPLE T-TEST HYPOTHESIS TEST")
    print("=" * 70)
    print("Null Hypothesis (H₀): Chlorine handwashing had no effect on maternal mortality rates.")
    print("Alt. Hypothesis (H₁): Chlorine handwashing significantly reduced maternal mortality rates.\n")

    print(f"  • Mean Monthly Mortality BEFORE Handwashing: \033[91m{res['mean_before']*100:.2f}%\033[0m")
    print(f"  • Mean Monthly Mortality AFTER Handwashing:  \033[92m{res['mean_after']*100:.2f}%\033[0m")
    print(f"  • Absolute Mortality Reduction:             {res['absolute_drop_pct']:.2f}% points")
    print(f"  • Relative Risk Reduction:                  \033[92m{res['relative_reduction_pct']:.1f}% reduction\033[0m")
    print("-" * 70)
    print(f"  • Welch's t-statistic:                      t = {res['t_statistic']:.4f}")
    print(f"  • Two-Tailed p-value:                       p = {res['p_value']:.2e}")
    signif = "OVERWHELMINGLY SIGNIFICANT (Reject H₀)" if res["statistically_significant"] else "Not significant"
    print(f"  • Statistical Significance:                 \033[92m{signif}\033[0m")
    print("=" * 70 + "\n")


def export_plot(analyzer: SemmelweisAnalyzer):
    print("\n🎨 Generating clinical time-series chart with matplotlib...")
    out_path = analyzer.export_handwashing_chart("handwashing_impact.png")
    print("✅ Successfully exported chart to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies clinic rates, t-test results, and plot output."""
    print("\n🔍 Running Day 79 Automated Clinical Hypothesis Testing Suite...")
    print("-" * 70)
    analyzer = SemmelweisAnalyzer()

    # 1. Clinic comparison
    c_df = analyzer.get_clinic_comparison()
    c1_rate = c_df[c_df["clinic"] == "clinic 1"]["overall_mortality_rate"].iloc[0]
    c2_rate = c_df[c_df["clinic"] == "clinic 2"]["overall_mortality_rate"].iloc[0]
    assert c1_rate > c2_rate * 2.0, "Clinic 1 rate must be more than double Clinic 2."
    print(f" [PASS] 1. Observational disparity verified: Clinic 1 ({c1_rate*100:.1f}%) vs Clinic 2 ({c2_rate*100:.1f}%).")

    # 2. Before / After subsetting
    assert len(analyzer.before_df) > 50
    assert len(analyzer.after_df) > 15
    print(f" [PASS] 2. Cohort partition verified: {len(analyzer.before_df)} pre-mandate and {len(analyzer.after_df)} post-mandate months.")

    # 3. Welch's t-test verification
    impact = analyzer.get_handwashing_impact()
    assert impact["p_value"] < 0.0001, "p-value must be < 0.0001"
    assert impact["relative_reduction_pct"] > 70.0, "Handwashing must drop deaths by > 70%"
    print(f" [PASS] 3. Welch's t-test verified: p = {impact['p_value']:.2e} (< 0.0001, reject H₀).")

    # 4. Chart export verification
    test_img = analyzer.export_handwashing_chart("test_handwashing.png")
    assert os.path.exists(test_img) and os.path.getsize(test_img) > 10000
    try:
        os.remove(test_img)
    except Exception:
        pass
    print(" [PASS] 4. Clinical time-series figure exported with valid dimensions.")

    print("-" * 70)
    print("✨ ALL 4 TESTS PASSED! Clinical Hypothesis Testing Engine fully operational.\n")


def main():
    banner()
    analyzer = SemmelweisAnalyzer()

    while True:
        print("Select an analytical module:")
        print("  1) 🏥 Clinic 1 vs Clinic 2 Mortality Discrepancy")
        print("  2) 🧪 Welch's Two-Sample t-test & Hypothesis Testing")
        print("  3) 🎨 Generate & Save Clinical Mortality Time-Series Plot (PNG)")
        print("  4) ✅ Run Automated Verification Suite (4 Unit Tests)")
        print("  5) 🚪 Exit")
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            display_clinics(analyzer)
        elif choice == "2":
            display_hypothesis_test(analyzer)
        elif choice == "3":
            export_plot(analyzer)
        elif choice == "4":
            run_automated_tests()
        elif choice in ("5", "exit", "quit", "q"):
            print("\n👋 Remember to wash your hands! Keep testing hypotheses 🧼\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 79 gracefully... Goodbye!\n")
