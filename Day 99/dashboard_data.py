"""
Day 99: Public Data Analysis & Interactive Web Dashboard
Data Wrangling with Pandas and Visualizations with Plotly
"""

import os
from typing import Dict, Any, Tuple
import pandas as pd
import plotly.express as px
import plotly.io as pio

PUBLIC_GLOBAL_DATA = [
    {"country": "United States", "region": "North America", "gdp_per_capita": 76398, "internet_penetration": 93.0, "tech_exports_billions": 380.5, "developers_thousands": 4400, "clean_energy_pct": 22.5},
    {"country": "India", "region": "Asia-Pacific", "gdp_per_capita": 2612, "internet_penetration": 55.0, "tech_exports_billions": 185.0, "developers_thousands": 5200, "clean_energy_pct": 41.0},
    {"country": "Germany", "region": "Europe", "gdp_per_capita": 48718, "internet_penetration": 94.0, "tech_exports_billions": 210.2, "developers_thousands": 1100, "clean_energy_pct": 52.0},
    {"country": "United Kingdom", "region": "Europe", "gdp_per_capita": 46125, "internet_penetration": 96.0, "tech_exports_billions": 140.8, "developers_thousands": 950, "clean_energy_pct": 48.0},
    {"country": "Japan", "region": "Asia-Pacific", "gdp_per_capita": 34358, "internet_penetration": 93.0, "tech_exports_billions": 195.4, "developers_thousands": 1300, "clean_energy_pct": 24.0},
    {"country": "Canada", "region": "North America", "gdp_per_capita": 52722, "internet_penetration": 94.5, "tech_exports_billions": 68.4, "developers_thousands": 720, "clean_energy_pct": 68.0},
    {"country": "South Korea", "region": "Asia-Pacific", "gdp_per_capita": 32422, "internet_penetration": 97.0, "tech_exports_billions": 225.0, "developers_thousands": 680, "clean_energy_pct": 9.0},
    {"country": "Brazil", "region": "Latin America", "gdp_per_capita": 8917, "internet_penetration": 81.0, "tech_exports_billions": 28.5, "developers_thousands": 850, "clean_energy_pct": 84.0},
    {"country": "France", "region": "Europe", "gdp_per_capita": 40886, "internet_penetration": 92.0, "tech_exports_billions": 115.0, "developers_thousands": 780, "clean_energy_pct": 26.0},
    {"country": "Singapore", "region": "Asia-Pacific", "gdp_per_capita": 82807, "internet_penetration": 98.0, "tech_exports_billions": 160.0, "developers_thousands": 180, "clean_energy_pct": 5.0},
    {"country": "Australia", "region": "Asia-Pacific", "gdp_per_capita": 65099, "internet_penetration": 91.0, "tech_exports_billions": 32.0, "developers_thousands": 360, "clean_energy_pct": 32.0},
    {"country": "Netherlands", "region": "Europe", "gdp_per_capita": 57025, "internet_penetration": 96.5, "tech_exports_billions": 130.0, "developers_thousands": 410, "clean_energy_pct": 40.0},
    {"country": "Sweden", "region": "Europe", "gdp_per_capita": 55395, "internet_penetration": 97.0, "tech_exports_billions": 48.0, "developers_thousands": 290, "clean_energy_pct": 66.0},
    {"country": "Israel", "region": "Middle East", "gdp_per_capita": 54659, "internet_penetration": 90.0, "tech_exports_billions": 72.0, "developers_thousands": 340, "clean_energy_pct": 12.0},
    {"country": "Switzerland", "region": "Europe", "gdp_per_capita": 92434, "internet_penetration": 96.0, "tech_exports_billions": 85.0, "developers_thousands": 250, "clean_energy_pct": 62.0},
    {"country": "Mexico", "region": "Latin America", "gdp_per_capita": 11496, "internet_penetration": 76.0, "tech_exports_billions": 55.0, "developers_thousands": 450, "clean_energy_pct": 28.0},
    {"country": "Poland", "region": "Europe", "gdp_per_capita": 18321, "internet_penetration": 87.0, "tech_exports_billions": 42.0, "developers_thousands": 430, "clean_energy_pct": 21.0},
    {"country": "Spain", "region": "Europe", "gdp_per_capita": 29674, "internet_penetration": 93.0, "tech_exports_billions": 38.0, "developers_thousands": 520, "clean_energy_pct": 47.0},
    {"country": "United Arab Emirates", "region": "Middle East", "gdp_per_capita": 53707, "internet_penetration": 99.0, "tech_exports_billions": 45.0, "developers_thousands": 120, "clean_energy_pct": 15.0},
    {"country": "South Africa", "region": "Africa", "gdp_per_capita": 6776, "internet_penetration": 72.0, "tech_exports_billions": 14.0, "developers_thousands": 210, "clean_energy_pct": 11.0}
]


class PublicDataAnalytics:
    """Analytical engine for wrangling global socioeconomic and technology indicators."""

    @staticmethod
    def get_dataframe() -> pd.DataFrame:
        df = pd.DataFrame(PUBLIC_GLOBAL_DATA)
        df["devs_per_million_gdp"] = (df["developers_thousands"] * 1000) / df["gdp_per_capita"]
        return df

    @staticmethod
    def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "total_countries": int(len(df)),
            "total_developers": int(df["developers_thousands"].sum() * 1000),
            "median_gdp": round(float(df["gdp_per_capita"].median()), 2),
            "avg_internet_penetration": round(float(df["internet_penetration"].mean()), 1),
            "total_tech_exports_billions": round(float(df["tech_exports_billions"].sum()), 2),
            "avg_clean_energy": round(float(df["clean_energy_pct"].mean()), 1)
        }

    @staticmethod
    def regional_breakdown(df: pd.DataFrame) -> pd.DataFrame:
        agg = df.groupby("region").agg({
            "country": "count",
            "gdp_per_capita": "mean",
            "developers_thousands": "sum",
            "tech_exports_billions": "sum",
            "internet_penetration": "mean"
        }).reset_index()
        agg.columns = ["Region", "Countries", "Mean GDP ($)", "Total Devs (k)", "Tech Exports ($B)", "Avg Internet (%)"]
        agg["Mean GDP ($)"] = agg["Mean GDP ($)"].round(2)
        agg["Avg Internet (%)"] = agg["Avg Internet (%)"].round(1)
        return agg

    @staticmethod
    def generate_scatter_figure(df: pd.DataFrame):
        """Creates Plotly bubble chart comparing GDP per capita vs Tech Exports."""
        fig = px.scatter(
            df,
            x="gdp_per_capita",
            y="tech_exports_billions",
            size="developers_thousands",
            color="region",
            hover_name="country",
            title="Global Tech Exports vs. GDP per Capita (Bubble Size = Developer Population)",
            labels={
                "gdp_per_capita": "GDP per Capita (USD)",
                "tech_exports_billions": "Tech Exports (Billion USD)",
                "region": "World Region"
            },
            template="plotly_dark"
        )
        fig.update_layout(height=500, margin=dict(l=40, r=40, t=50, b=40))
        return fig

    @staticmethod
    def generate_top_devs_bar(df: pd.DataFrame):
        """Creates Plotly horizontal bar chart of top software developer populations."""
        top_df = df.sort_values(by="developers_thousands", ascending=True).tail(10)
        fig = px.bar(
            top_df,
            x="developers_thousands",
            y="country",
            orientation="h",
            color="region",
            title="Top 10 Nations by Software Developer Population (Thousands)",
            labels={"developers_thousands": "Developers (in 1,000s)", "country": "Country"},
            template="plotly_dark"
        )
        fig.update_layout(height=450, margin=dict(l=40, r=40, t=50, b=40))
        return fig

    @staticmethod
    def export_standalone_dashboard(output_file: str) -> str:
        """Exports an all-in-one standalone HTML dashboard file."""
        df = PublicDataAnalytics.get_dataframe()
        kpis = PublicDataAnalytics.calculate_kpis(df)
        scatter_fig = PublicDataAnalytics.generate_scatter_figure(df)
        bar_fig = PublicDataAnalytics.generate_top_devs_bar(df)

        scatter_html = pio.to_html(scatter_fig, full_html=False, include_plotlyjs="cdn")
        bar_html = pio.to_html(bar_fig, full_html=False, include_plotlyjs=False)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Global Tech & Socioeconomic Intelligence Dashboard</title>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
          <style>
            body {{ background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, system-ui, sans-serif; }}
            .kpi-card {{ background-color: #151e32; border: 1px solid #24324f; border-radius: 10px; padding: 20px; }}
            .kpi-num {{ font-size: 2.2rem; font-weight: 700; color: #38bdf8; }}
            .chart-card {{ background-color: #151e32; border: 1px solid #24324f; border-radius: 12px; padding: 15px; margin-bottom: 25px; }}
          </style>
        </head>
        <body class="py-4">
          <div class="container-fluid px-5">
            <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom border-secondary">
              <div>
                <h1 class="h2 text-white mb-1">🌐 Global Tech & Economic Dashboard</h1>
                <p class="text-secondary mb-0">Public Dataset Analytics & Interactive Plotly Engine</p>
              </div>
              <span class="badge bg-primary px-3 py-2">Day 99 Portfolio Project</span>
            </div>

            <!-- KPI Tiles -->
            <div class="row g-3 mb-4">
              <div class="col-md-3">
                <div class="kpi-card text-center">
                  <div class="text-secondary small text-uppercase">Total Software Devs</div>
                  <div class="kpi-num">{kpis['total_developers']:,}</div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="kpi-card text-center">
                  <div class="text-secondary small text-uppercase">Median GDP per Capita</div>
                  <div class="kpi-num">${kpis['median_gdp']:,.0f}</div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="kpi-card text-center">
                  <div class="text-secondary small text-uppercase">Avg Internet Penetration</div>
                  <div class="kpi-num">{kpis['avg_internet_penetration']}%</div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="kpi-card text-center">
                  <div class="text-secondary small text-uppercase">Total Tech Exports</div>
                  <div class="kpi-num">${kpis['total_tech_exports_billions']:,.1f}B</div>
                </div>
              </div>
            </div>

            <!-- Charts -->
            <div class="row">
              <div class="col-lg-7">
                <div class="chart-card shadow">
                  {scatter_html}
                </div>
              </div>
              <div class="col-lg-5">
                <div class="chart-card shadow">
                  {bar_html}
                </div>
              </div>
            </div>
          </div>
        </body>
        </html>
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_file
