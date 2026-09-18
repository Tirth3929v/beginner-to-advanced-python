"""
Day 77: Linear Regression and Data Visualization with Seaborn
Movie Box Office Prediction & Statistical Modeling CLI
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
from regression_model import MovieRegressionModel


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 77: LINEAR REGRESSION & DATA VISUALIZATION WITH SEABORN")
    print(" 📚 Phase 4: Data Science & Machine Learning | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Core Machine Learning & Visualization Concepts:")
    print("  • Data Cleaning: Parsing currency strings & filtering unreleased films")
    print("  • Ordinary Least Squares (OLS) Linear Regression via Scikit-Learn")
    print("  • Statistical Metrics: Slope (marginal return), Intercept & R² Score")
    print("  • Seaborn Visualization: Scatter distributions & regression confidence bands")
    print("=" * 76 + "\n")


def display_model_summary(model: MovieRegressionModel):
    s = model.get_model_summary()
    print("\n📈 OLS LINEAR REGRESSION MODEL SUMMARY")
    print("=" * 65)
    print(f"  • Valid Released Movies Analyzed: {s['total_movies_analyzed']:,d}")
    print(f"  • Regression Slope (θ₁):          \033[92m{s['slope_coef']:.4f}\033[0m")
    print(f"  • Model Intercept (θ₀):           ${s['intercept']:,.2f}")
    print(f"  • Coefficient of Determ. (R²):    \033[93m{s['r2_score']:.4f} ({s['r2_score']*100:.1f}% variance explained)\033[0m")
    print(f"  • Mean Production Budget:         ${s['avg_budget']:,.2f}")
    print(f"  • Mean Worldwide Gross:           ${s['avg_worldwide_gross']:,.2f}")
    print("\n  💡 Interpretation: For every $1.00 spent in production budget,")
    print(f"     the model predicts an estimated ${s['slope_coef']:.2f} in worldwide gross.")
    print("=" * 65 + "\n")


def predict_budget(model: MovieRegressionModel):
    print("\n🔮 PREDICT WORLDWIDE BOX OFFICE REVENUE")
    print("=" * 65)
    try:
        val_str = input("Enter production budget in Millions USD (e.g. 50 or 150): ").strip()
        budget_m = float(val_str)
        budget_usd = budget_m * 1e6
        predicted_gross = model.predict_revenue(budget_usd)

        print(f"\n🎬 Prediction Results for ${budget_m:,.1f}M Production Budget:")
        print(f"  • Estimated Worldwide Gross: \033[92m${predicted_gross/1e6:,.2f} Million\033[0m (${predicted_gross:,.2f})")
        est_profit = predicted_gross - budget_usd
        print(f"  • Estimated Net Profit:      \033[94m${est_profit/1e6:,.2f} Million\033[0m")
        print(f"  • Projected ROI Multiple:    {predicted_gross / budget_usd:.2f}x\n")
    except ValueError:
        print("⚠️ Invalid numeric budget entered.\n")


def display_top_roi(model: MovieRegressionModel):
    top_roi = model.get_highest_roi_movies(5)
    print("\n💎 TOP MOVIES BY RETURN ON INVESTMENT (ROI MULTIPLE)")
    print("=" * 70)
    for rank, (_, row) in enumerate(top_roi.iterrows(), start=1):
        print(f"  {rank}. {row['Movie_Title']}")
        print(f"     Budget: ${row['USD_Production_Budget']:,.0f} -> Gross: ${row['USD_Worldwide_Gross']:,.0f} (\033[92m{row['ROI_Multiple']:,.1f}x ROI\033[0m)")
    print("=" * 70 + "\n")


def export_plot(model: MovieRegressionModel):
    print("\n🎨 Rendering Seaborn regression chart with confidence intervals...")
    out_path = model.export_seaborn_plot("box_office_regression.png")
    print("✅ Successfully exported chart to:")
    print(f"   file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies data cleaning, linear regression fit, and plot generation."""
    print("\n🔍 Running Day 77 Automated Scikit-Learn & Seaborn Test Suite...")
    print("-" * 70)
    model = MovieRegressionModel()

    # 1. Check data cleaning & unreleased film exclusion
    assert len(model.clean_df) > 100
    assert not any(model.clean_df["Movie_Title"] == "Avatar 5: The Seed Bearer"), "Future film should be filtered."
    assert not (model.clean_df["USD_Worldwide_Gross"] == 0).any(), "Zero gross films must be filtered."
    print(f" [PASS] 1. Data cleaning verified: {len(model.clean_df)} valid released films parsed.")

    # 2. Scikit-Learn Model parameters
    assert model.slope > 1.0, f"Expected positive revenue slope > 1.0, got {model.slope}"
    assert 0.0 < model.r2_score <= 1.0, f"R² must be between 0 and 1, got {model.r2_score}"
    print(f" [PASS] 2. OLS Regression fit verified: Slope = {model.slope:.4f}, R² = {model.r2_score:.4f}.")

    # 3. Revenue prediction test
    sample_pred = model.predict_revenue(100000000) # $100M budget
    assert sample_pred > 100000000, "100M budget should yield positive predicted gross."
    print(f" [PASS] 3. Inference verified: $100M budget predicts ${sample_pred/1e6:.1f}M gross.")

    # 4. Highest ROI test
    roi_df = model.get_highest_roi_movies(1)
    assert roi_df.iloc[0]["ROI_Multiple"] > 10.0
    print(f" [PASS] 4. Outlier analysis: Highest ROI film ({roi_df.iloc[0]['Movie_Title']}) verified.")

    # 5. Seaborn plot export
    test_img = model.export_seaborn_plot("test_reg.png")
    assert os.path.exists(test_img) and os.path.getsize(test_img) > 10000
    try:
        os.remove(test_img)
    except Exception:
        pass
    print(" [PASS] 5. Seaborn regression plotting pipeline rendered valid PNG.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Scikit-Learn & Seaborn Engine fully operational.\n")


def main():
    banner()
    model = MovieRegressionModel()

    while True:
        print("Select an option:")
        print("  1) 📈 View OLS Linear Regression Summary & Model Parameters")
        print("  2) 🔮 Predict Worldwide Gross for Custom Budget")
        print("  3) 💎 Top Highest ROI Movies (Low Budget Blockbusters)")
        print("  4) 🎨 Generate & Save Seaborn Regression Plot (PNG)")
        print("  5) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  6) 🚪 Exit")
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            display_model_summary(model)
        elif choice == "2":
            predict_budget(model)
        elif choice == "3":
            display_top_roi(model)
        elif choice == "4":
            export_plot(model)
        elif choice == "5":
            run_automated_tests()
        elif choice in ("6", "exit", "quit", "q"):
            print("\n👋 Happy Modeling with Scikit-Learn & Seaborn! 🎬\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 77 gracefully... Goodbye!\n")
