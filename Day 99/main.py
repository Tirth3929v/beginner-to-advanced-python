"""
Day 99: Public Data Analysis & Interactive Web Dashboard
Phase 5: Portfolio

Key Concepts:
Streamlit / Dash Framework, Pandas Data Wrangling, Interactive Visualizations
"""

import os
import sys
import tempfile

# Ensure UTF-8 output encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from art import LOGO, DASHBOARD_ICON
from dashboard_data import PublicDataAnalytics
from server import app


def banner():
    """Prints the project banner and ASCII art."""
    print("=" * 72)
    print(LOGO)
    print(DASHBOARD_ICON)
    print("=" * 72)
    print(" 🚀 DAY 99: PUBLIC DATA ANALYSIS & INTERACTIVE WEB DASHBOARD")
    print(" 📚 Phase 5: Portfolio | 100 Days of Code Python Bootcamp")
    print(" Key Concepts: Pandas Data Wrangling, Plotly Visualizations, Flask Dashboard")
    print("=" * 72 + "\n")


def run_automated_tests():
    """Validates data wrangling, KPI computations, Plotly figures, and dashboard exports."""
    print("\n🔍 Running Day 99 Automated Public Data & Dashboard Test Suite...")
    print("-" * 70)

    # 1. DataFrame ingestion & feature engineering
    df = PublicDataAnalytics.get_dataframe()
    assert len(df) == 20
    assert "devs_per_million_gdp" in df.columns
    assert "gdp_per_capita" in df.columns
    print(" [PASS] 1. Pandas DataFrame ingestion & derived ratio features verified.")

    # 2. KPI metrics calculation
    kpis = PublicDataAnalytics.calculate_kpis(df)
    assert kpis["total_countries"] == 20
    assert kpis["total_developers"] > 15_000_000
    assert kpis["median_gdp"] > 30_000
    assert 50 < kpis["avg_internet_penetration"] < 100
    print(f" [PASS] 2. Macroeconomic KPI aggregation verified ({kpis['total_developers']:,} devs, ${kpis['median_gdp']:,.0f} median GDP).")

    # 3. Regional aggregation breakdown
    regional_df = PublicDataAnalytics.regional_breakdown(df)
    assert len(regional_df) >= 5
    assert "Region" in regional_df.columns
    assert "Mean GDP ($)" in regional_df.columns
    print(" [PASS] 3. Regional multi-column groupby aggregation verified.")

    # 4. Plotly figure generation
    scatter_fig = PublicDataAnalytics.generate_scatter_figure(df)
    bar_fig = PublicDataAnalytics.generate_top_devs_bar(df)
    assert scatter_fig is not None
    assert bar_fig is not None
    assert len(scatter_fig.data) > 0
    assert len(bar_fig.data) > 0
    print(" [PASS] 4. Plotly Express scatter bubble & horizontal bar figure compilation verified.")

    # 5. Standalone HTML dashboard export
    temp_dir = tempfile.mkdtemp()
    out_file = os.path.join(temp_dir, "dashboard.html")
    exported = PublicDataAnalytics.export_standalone_dashboard(out_file)
    assert os.path.exists(exported)
    with open(exported, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Global Tech & Economic Dashboard" in content
        assert "plotly" in content.lower()
    print(" [PASS] 5. Standalone responsive HTML dashboard compilation verified.")

    # 6. Flask test client KPI endpoint
    client = app.test_client()
    resp = client.get("/api/kpis")
    assert resp.status_code == 200
    assert resp.get_json()["total_countries"] == 20
    print(" [PASS] 6. Live Flask REST KPI endpoint verified.")

    print("-" * 70)
    print("✨ ALL 6 TESTS PASSED! Public Data Analysis & Web Dashboard fully operational.\n")


def interactive_cli():
    """Interactive command-line interface."""
    banner()
    df = PublicDataAnalytics.get_dataframe()

    while True:
        print("\n" + "=" * 55)
        print("  PUBLIC DATA & DASHBOARD COMMAND CENTER")
        print("=" * 55)
        print("  [1] View Global Tech & Economic KPIs")
        print("  [2] View Regional Socioeconomic Aggregations")
        print("  [3] View Top 10 Developer Populations")
        print("  [4] Export Standalone Interactive HTML Dashboard")
        print("  [5] Launch Live Web Dashboard Server (Port 5050)")
        print("  [6] Run Automated Test Suite")
        print("  [7] Exit")
        print("=" * 55)

        choice = input("Enter option (1-7): ").strip()

        if choice == "1":
            kpis = PublicDataAnalytics.calculate_kpis(df)
            print("\n  📊 GLOBAL TECHNOLOGY & SOCIOECONOMIC KPIS:")
            print("  " + "-" * 50)
            print(f"  Total Countries Tracked   : {kpis['total_countries']}")
            print(f"  Total Software Developers : {kpis['total_developers']:,}")
            print(f"  Median GDP per Capita     : ${kpis['median_gdp']:,.2f}")
            print(f"  Avg Internet Penetration  : {kpis['avg_internet_penetration']}%")
            print(f"  Total Tech Exports        : ${kpis['total_tech_exports_billions']:,.2f} Billion")
            print(f"  Avg Clean Energy Adoption : {kpis['avg_clean_energy']}%")

        elif choice == "2":
            reg = PublicDataAnalytics.regional_breakdown(df)
            print("\n  🌐 REGIONAL AGGREGATION BREAKDOWN:")
            print("  " + "-" * 75)
            print(reg.to_string(index=False))

        elif choice == "3":
            top10 = df.sort_values(by="developers_thousands", ascending=False).head(10)
            print("\n  🏆 TOP 10 SOFTWARE DEVELOPER POPULATIONS:")
            print("  " + "-" * 65)
            for idx, (_, row) in enumerate(top10.iterrows(), 1):
                print(f"  {idx:>2}. {row['country']:<18} ({row['region']:<14}) : {row['developers_thousands'] * 1000:,} devs")

        elif choice == "4":
            out = os.path.join(os.path.dirname(__file__), "global_tech_dashboard.html")
            PublicDataAnalytics.export_standalone_dashboard(out)
            print(f"\n  [✓] Interactive dashboard successfully exported to:")
            print(f"      {out}")
            print("  Open this HTML file in any browser to explore dynamic charts!")

        elif choice == "5":
            print("\n  🚀 Starting Interactive Dashboard Server on http://127.0.0.1:5050 ...")
            print("  Press Ctrl+C to return to CLI menu.")
            try:
                app.run(port=5050, debug=False)
            except (KeyboardInterrupt, SystemExit):
                print("\n  [✓] Dashboard server halted.")

        elif choice == "6":
            run_automated_tests()

        elif choice == "7":
            print("\n👋 Exiting Public Data Dashboard. Happy Analyzing!\n")
            break
        else:
            print("  [!] Invalid option. Please choose 1-7.")


def main():
    try:
        interactive_cli()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Exiting Day 99 gracefully... Goodbye!\n")


if __name__ == "__main__":
    main()
