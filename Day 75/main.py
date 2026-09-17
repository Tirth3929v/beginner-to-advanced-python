"""
Day 75: Beautiful Plotly Visualizations
Google Play Store App Analytics CLI
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
from app_analytics import AppStoreAnalytics


def banner():
    print(LOGO)
    print("=" * 76)
    print(" 🚀 DAY 75: BEAUTIFUL INTERACTIVE DATA VISUALIZATIONS WITH PLOTLY")
    print(" 📚 Phase 4: Data Science & Analytics | 100 Days of Code Python Bootcamp")
    print("=" * 76)
    print(" Core Plotly Concepts:")
    print("  • Interactive Bar Charts: Horizontal orientation & continuous color scaling")
    print("  • Donut / Pie Charts: Hole styling, label positioning, and percentage formatting")
    print("  • Multi-dimensional Bubble Scatter Plots: Mapping 4 dimensions (X, Y, Size, Color)")
    print("  • Web Export: Generating standalone, dependency-free interactive HTML dashboards")
    print("=" * 76 + "\n")


def display_metrics(analytics: AppStoreAnalytics):
    m = analytics.get_summary_metrics()
    print("\n📊 GOOGLE PLAY STORE MARKETPLACE KPIS")
    print("=" * 65)
    print(f"  • Total Apps Analyzed:         {m['total_apps']:,d}")
    print(f"  • Average User Rating:         \033[93m{m['avg_rating']:.2f} ★\033[0m")
    print(f"  • Total Platform Downloads:    \033[92m{m['total_installs']:,d}\033[0m")
    print(f"  • Free vs Paid Catalog:        {m['free_apps']} Free ({m['free_apps']/m['total_apps']*100:.1f}%) | {m['paid_apps']} Paid")
    print(f"  • Estimated Paid Revenue:      \033[94m${m['total_est_revenue']:,.2f}\033[0m")
    print("=" * 65 + "\n")


def display_top_installs(analytics: AppStoreAnalytics):
    top = analytics.get_top_installed_apps(8)
    print("\n⚡ TOP MOST DOWNLOADED APPS")
    print("=" * 70)
    for rank, (_, row) in enumerate(top.iterrows(), start=1):
        print(f"  {rank:2d}. {row['App']:<30} [{row['Category']}]")
        print(f"      Installs: \033[92m{int(row['Installs']):,d}\033[0m | Rating: {row['Rating']} ★ | Type: {row['Type']}")
    print("=" * 70 + "\n")


def display_top_grossing(analytics: AppStoreAnalytics):
    grossing = analytics.get_top_grossing_paid_apps(5)
    print("\n💎 HIGHEST GROSSING PAID APPLICATIONS")
    print("=" * 70)
    for rank, (_, row) in enumerate(grossing.iterrows(), start=1):
        print(f"  {rank}. {row['App']}")
        print(f"     Price: ${row['Price']:.2f} | Est. Revenue: \033[92m${row['Estimated_Revenue']:,.2f}\033[0m ({int(row['Installs']):,d} downloads)")
    print("=" * 70 + "\n")


def export_dashboard(analytics: AppStoreAnalytics):
    print("\n🎨 Building and exporting interactive Plotly HTML dashboard...")
    out_path = analytics.export_dashboard_html("play_store_dashboard.html")
    print("✅ Dashboard successfully exported!")
    print(f"   Open in browser: file:///{out_path.replace(os.sep, '/')}\n")


def run_automated_tests():
    """Verifies data cleaning, metric calculations, and Plotly figure generation."""
    print("\n🔍 Running Day 75 Automated Plotly Verification Suite...")
    print("-" * 70)
    analytics = AppStoreAnalytics()

    # 1. Row count & null verification
    metrics = analytics.get_summary_metrics()
    assert metrics["total_apps"] >= 400
    assert not analytics.df["Rating"].isna().any()
    print(f" [PASS] 1. Data cleaning verified: {metrics['total_apps']} clean apps processed.")

    # 2. Revenue calculation
    assert "Estimated_Revenue" in analytics.df.columns
    sample_paid = analytics.df[analytics.df["Type"] == "Paid"].iloc[0]
    expected_rev = sample_paid["Installs"] * sample_paid["Price"]
    assert sample_paid["Estimated_Revenue"] == expected_rev
    print(" [PASS] 2. Feature engineering: Estimated revenue math verified.")

    # 3. Top apps identification
    top_apps = analytics.get_top_installed_apps(1)
    assert top_apps.iloc[0]["Installs"] >= 500000000
    print(f" [PASS] 3. Max installs identification: '{top_apps.iloc[0]['App']}' with 1B+ downloads.")

    # 4. Plotly figure creation
    fig1 = analytics.build_category_installs_chart()
    fig2 = analytics.build_content_rating_donut()
    fig3 = analytics.build_size_vs_rating_scatter()
    assert fig1 is not None and fig2 is not None and fig3 is not None
    print(" [PASS] 4. Plotly Express figures constructed without errors.")

    # 5. Dashboard HTML export
    html_file = analytics.export_dashboard_html("test_dash.html")
    assert os.path.exists(html_file) and os.path.getsize(html_file) > 5000
    try:
        os.remove(html_file)
    except Exception:
        pass
    print(" [PASS] 5. Full HTML interactive dashboard successfully bundled.")

    print("-" * 70)
    print("✨ ALL 5 TESTS PASSED! Plotly Visualization Engine fully operational.\n")


def main():
    banner()
    analytics = AppStoreAnalytics()

    while True:
        print("Select an option:")
        print("  1) 📊 Marketplace KPIs & Overview")
        print("  2) ⚡ Top Installed Apps Leaderboard")
        print("  3) 💎 Highest Grossing Paid Applications")
        print("  4) 🎨 Export Interactive Plotly HTML Dashboard")
        print("  5) ✅ Run Automated Verification Suite (5 Unit Tests)")
        print("  6) 🚪 Exit")
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            display_metrics(analytics)
        elif choice == "2":
            display_top_installs(analytics)
        elif choice == "3":
            display_top_grossing(analytics)
        elif choice == "4":
            export_dashboard(analytics)
        elif choice == "5":
            run_automated_tests()
        elif choice in ("6", "exit", "quit", "q"):
            print("\n👋 Happy Visualizing with Plotly! Keep exploring data 🚀\n")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 75 gracefully... Goodbye!\n")
