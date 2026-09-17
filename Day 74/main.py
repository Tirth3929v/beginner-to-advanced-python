"""
Day 74: Google Trends & Resampling Data
Financial Time Series Resampling & Public Interest Correlation CLI
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
from resampler import TrendResampler


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 74: GOOGLE TRENDS & FINANCIAL TIME-SERIES RESAMPLING")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Resampling & Time-Series Concepts:")
    print("  • Datetime Indexing: Converting string dates into parsed DatetimeIndex")
    print("  • Frequency Resampling: Converting high-frequency daily data to monthly (.resample('MS'))")
    print("  • Statistical Correlation: Quantifying market prices vs search interest (.corr())")
    print("  • Dual-Axis Date Formatting: Using matplotlib.dates MonthLocator & DateFormatter")
    print("=" * 76 + "\n")


def display_correlations(resampler: TrendResampler):
    tsla_corr = resampler.get_tesla_correlation()
    btc_corr = resampler.get_btc_correlation()

    print("\n📊 SEARCH VOLUME VS ASSET PRICE CORRELATIONS")
    print("=" * 65)
    print(f"  🏎️  Tesla (TSLA Search vs Stock Close):    \033[92m{tsla_corr:+.4f}\033[0m")
    print(f"  🪙  Bitcoin (BTC News Search vs Monthly Close): \033[92m{btc_corr:+.4f}\033[0m")
    print("\n  💡 Insight: High positive correlation demonstrates retail search activity")
    print("     intensely follows speculative market asset surges.")
    print("=" * 65 + "\n")


def export_charts(resampler: TrendResampler):
    print("\n🎨 Generating dual-axis financial correlation charts...")
    t_path = resampler.export_tesla_chart("tesla_trend.png")
    b_path = resampler.export_bitcoin_chart("bitcoin_resampled_trend.png")
    print(f"✅ Exported Tesla chart to:")
    print(f"   file:///{t_path.replace(os.sep, '/')}")
    print(f"✅ Exported Bitcoin chart to:")
    print(f"   file:///{b_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies resampling, merging, correlation, and figure generation."""
    print("\n🔍 Running Day 74 Automated Resampling & Time Series Test Suite...")
    print("-" * 70)
    resampler = TrendResampler()

    # 1. Tesla data shape
    assert len(resampler.df_tesla) > 50, "Tesla data should have > 50 monthly entries."
    print(f" [PASS] 1. Tesla dataset verified: {len(resampler.df_tesla)} monthly entries parsed.")

    # 2. Daily to monthly resampling
    daily_count = len(resampler.df_btc_price)
    monthly_count = len(resampler.df_btc_monthly)
    assert daily_count > 1000, f"Expected > 1000 daily prices, got {daily_count}"
    assert monthly_count < daily_count / 20, "Resampled monthly count must be ~30x smaller than daily."
    print(f" [PASS] 2. Resampling verified: {daily_count} daily entries resampled to {monthly_count} monthly averages.")

    # 3. Merged Bitcoin dataset
    assert "BTC_NEWS_SEARCH" in resampler.df_btc_merged.columns
    assert "CLOSE" in resampler.df_btc_merged.columns
    print(f" [PASS] 3. Merged financial time-series: Search volume and Price aligned on monthly date index.")

    # 4. Correlation check
    btc_corr = resampler.get_btc_correlation()
    assert btc_corr > 0.6, f"Expected strong positive correlation, got {btc_corr}"
    print(f" [PASS] 4. Correlation computation: Bitcoin correlation = {btc_corr:.4f} (Strong positive).")

    # 5. Image export check
    test_img = resampler.export_tesla_chart("test_tesla.png")
    assert os.path.exists(test_img) and os.path.getsize(test_img) > 10000
    try:
        os.remove(test_img)
    except Exception:
        pass
    print(" [PASS] 5. Matplotlib time-series dual-axis exporter rendered valid graphic.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Time Series Resampling Engine fully operational.\n")


def main():
    banner()
    resampler = TrendResampler()

    while True:
        print("Select an option:")
        print("  1) 📊 View Search Volume vs Price Correlation Metrics")
        print("  2) 📈 Generate & Save Tesla & Bitcoin Correlation Charts (PNG)")
        print("  3) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  4) 🚪 Exit")
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            display_correlations(resampler)
        elif choice == "2":
            export_charts(resampler)
        elif choice == "3":
            run_automated_tests()
        elif choice in ("4", "exit", "quit", "q"):
            print("\n👋 Happy Resampling! Keep your time-series aligned 📈\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-4.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 74 gracefully... Goodbye!\n")
