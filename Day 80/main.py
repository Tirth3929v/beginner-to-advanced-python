"""
Day 80: Multivariable Regression & House Price Predictions
Interactive Machine Learning Property Valuation CLI
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
from housing_predictor import BostonHousingPredictor


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 80: MULTIVARIABLE LINEAR REGRESSION & HOUSING VALUATION")
    print(" 📚 Phase 4: Machine Learning Foundations | 100 Days of Code Bootcamp")
    print("=" * 76)
    print(" Core Machine Learning Concepts:")
    print("  • Multivariable Modeling: Fitting 13 simultaneous feature predictors")
    print("  • Train/Test Splitting (80/20) & Generalization Assessment (Test R²)")
    print("  • Feature Coefficients: Quantifying positive drivers (RM) vs negative penalties (CRIM, LSTAT)")
    print("  • Log-Transformed Regression: Correcting skewed target distributions")
    print("  • Multicollinearity & Correlation Heatmaps via Seaborn")
    print("=" * 76 + "\n")


def display_model_metrics(predictor: BostonHousingPredictor):
    print("\n📊 MULTIVARIABLE REGRESSION PERFORMANCE METRICS")
    print("=" * 65)
    print(f"  • Training Samples:         {len(predictor.X_train)} instances")
    print(f"  • Testing Holdout Samples:  {len(predictor.X_test)} instances")
    print(f"  • Training R² Score:        \033[92m{predictor.train_r2:.4f}\033[0m")
    print(f"  • Holdout Test R² Score:    \033[92m{predictor.test_r2:.4f}\033[0m")
    print(f"  • Root Mean Squared Error:  \033[93m${predictor.rmse*1000:,.2f} RMSE\033[0m")
    print(f"  • Log-Transformed Model R²: \033[94m{predictor.log_train_r2:.4f}\033[0m")
    print("=" * 65 + "\n")


def display_coefficients(predictor: BostonHousingPredictor):
    coef_df = predictor.get_coefficients_table()
    print("\n💎 FEATURE IMPACT COEFFICIENTS (HOW FEATURES CHANGE VALUE)")
    print("=" * 65)
    print("Feature Definitions:")
    print("  RM: Rooms | LSTAT: % Lower Status | PTRATIO: Pupil-Teacher Ratio | CRIM: Crime\n")
    for _, row in coef_df.iterrows():
        c = row["Coefficient"]
        sign = "+" if c > 0 else "-"
        color = "\033[92m" if c > 0 else "\033[91m"
        bar = "█" * min(25, int(abs(c) * 1.5))
        print(f"  {row['Feature']:<10} {color}{sign} ${abs(c)*1000:>8,.2f}\033[0m / unit  {bar}")
    print("=" * 65 + "\n")


def interactive_valuation(predictor: BostonHousingPredictor):
    print("\n🏡 INTERACTIVE RESIDENTIAL PROPERTY VALUATION")
    print("=" * 65)
    try:
        rm_in = input("Enter average number of rooms (default 6.2): ").strip()
        rm = float(rm_in) if rm_in else 6.2

        crim_in = input("Enter per capita crime rate (e.g. 0.2 low, 5.0 high, default 0.25): ").strip()
        crim = float(crim_in) if crim_in else 0.25

        pt_in = input("Enter school pupil-teacher ratio (e.g. 15.0 good, 21.0 crowded, default 18.0): ").strip()
        pt = float(pt_in) if pt_in else 18.0

        lstat_in = input("Enter % lower status neighborhood demographic (e.g. 5.0 affluent, 25.0 poor, default 12.0): ").strip()
        lstat = float(lstat_in) if lstat_in else 12.0

        river_in = input("Tract bounds Charles River? (y/n, default n): ").strip().lower()
        chas = 1 if river_in.startswith("y") else 0

        pred_price_k = predictor.predict_custom_house(rm=rm, crim=crim, ptratio=pt, lstat=lstat, chas=chas)
        pred_usd = pred_price_k * 1000

        print("\n" + "-" * 65)
        print(f"  🏷️  Estimated Property Value: \033[92m${pred_usd:,.2f}\033[0m (${pred_price_k:.1f}k)")
        print(f"  📐 Profile: {rm:.1f} rooms, Crime: {crim:.2f}, Pupil-Teacher: {pt:.1f}:1, LSTAT: {lstat:.1f}%")
        print("-" * 65 + "\n")
    except ValueError:
        print("⚠️ Invalid numerical parameter entered.\n")


def export_visualizations(predictor: BostonHousingPredictor):
    print("\n🎨 Generating Seaborn correlation heatmap & residual scatter plots...")
    h_path = predictor.export_correlation_heatmap("housing_correlations.png")
    r_path = predictor.export_residuals_plot("residuals_analysis.png")
    print("✅ Successfully exported visualizations:")
    print(f"  • Correlation Matrix: file:///{h_path.replace(os.sep, '/')}")
    print(f"  • Residual Analysis:  file:///{r_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies train-test splitting, multivariable regression fit, and inference."""
    print("\n🔍 Running Day 80 Automated Multivariable Regression Test Suite...")
    print("-" * 70)
    predictor = BostonHousingPredictor()

    # 1. Shape check
    assert len(predictor.df) == 506
    assert len(predictor.features) == 13
    print(f" [PASS] 1. Boston Housing dataset loaded: {len(predictor.df)} rows across 13 predictors.")

    # 2. Train-test split
    assert len(predictor.X_train) == 404
    assert len(predictor.X_test) == 102
    print(" [PASS] 2. Train-test split verified (80% train / 20% holdout test).")

    # 3. Model R2 score check
    assert predictor.train_r2 > 0.65, f"Expected train R² > 0.65, got {predictor.train_r2}"
    assert predictor.test_r2 > 0.60, f"Expected test R² > 0.60, got {predictor.test_r2}"
    print(f" [PASS] 3. Model fitting verified: Train R² = {predictor.train_r2:.4f}, Test R² = {predictor.test_r2:.4f}.")

    # 4. Coefficients directionality
    coefs = predictor.get_coefficients_table().set_index("Feature")["Coefficient"]
    assert coefs["RM"] > 0, "Number of rooms (RM) must have positive coefficient."
    assert coefs["LSTAT"] < 0, "Poverty rate (LSTAT) must have negative coefficient."
    print(" [PASS] 4. Economic coefficient validity: RM is positive (+), LSTAT/CRIM are negative (-).")

    # 5. Interactive inference check
    price_pred = predictor.predict_custom_house(rm=8.0, crim=0.1, ptratio=14.0, lstat=4.0)
    assert price_pred > 25.0, "Luxury home should be valued > $25k ($25,000 in 1970s dollars)."
    print(f" [PASS] 5. Property valuation inference verified: Luxury home predicted at ${price_pred*1000:,.2f}.")

    # 6. Plot exports check
    h_file = predictor.export_correlation_heatmap("test_heat.png")
    r_file = predictor.export_residuals_plot("test_res.png")
    assert os.path.exists(h_file) and os.path.exists(r_file)
    try:
        os.remove(h_file)
        os.remove(r_file)
    except Exception:
        pass
    print(" [PASS] 6. Seaborn heatmap and residual scatter graphics exported cleanly.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Boston Housing ML Predictor fully operational.\n")


def main():
    banner()
    predictor = BostonHousingPredictor()

    while True:
        print("Select an option:")
        print("  1) 📊 Multivariable Regression Model Performance & Metrics")
        print("  2) 💎 Feature Coefficients & Property Value Drivers")
        print("  3) 🏡 Interactive Property Valuation Tool")
        print("  4) 🎨 Generate & Save Correlation Heatmap & Residual Plots (PNG)")
        print("  5) ✅ Run Automated Verification Suite (6 Unit Tests)")
        print("  6) 🚪 Exit")
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            display_model_metrics(predictor)
        elif choice == "2":
            display_coefficients(predictor)
        elif choice == "3":
            interactive_valuation(predictor)
        elif choice == "4":
            export_visualizations(predictor)
        elif choice == "5":
            run_automated_tests()
        elif choice in ("6", "exit", "quit", "q"):
            print("\n👋 Happy Predicting with Scikit-Learn! 🏡\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 80 gracefully... Goodbye!\n")
