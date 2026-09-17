"""
Day 75: Google Play Store Analytics with Plotly
Interactive Donut charts, Bar charts, Scatter plots, and HTML Dashboard export.
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class AppStoreAnalytics:
    def __init__(self, csv_file: str = "apps.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, csv_file) if not os.path.isabs(csv_file) else csv_file
        
        self.df = pd.read_csv(path)
        self.clean_data()

    def clean_data(self):
        """Deduplicates and ensures proper numerical data types."""
        self.df = self.df.drop_duplicates(subset=["App"]).dropna(subset=["Rating"])
        self.df["Installs"] = pd.to_numeric(self.df["Installs"])
        self.df["Price"] = pd.to_numeric(self.df["Price"])
        self.df["Estimated_Revenue"] = self.df["Installs"] * self.df["Price"]

    def get_summary_metrics(self) -> dict:
        return {
            "total_apps": len(self.df),
            "avg_rating": round(float(self.df["Rating"].mean()), 2),
            "total_installs": int(self.df["Installs"].sum()),
            "free_apps": int((self.df["Type"] == "Free").sum()),
            "paid_apps": int((self.df["Type"] == "Paid").sum()),
            "total_est_revenue": float(self.df["Estimated_Revenue"].sum())
        }

    def get_top_installed_apps(self, n: int = 5) -> pd.DataFrame:
        return self.df.sort_values("Installs", ascending=False)[["App", "Category", "Installs", "Rating", "Type"]].head(n)

    def get_top_grossing_paid_apps(self, n: int = 5) -> pd.DataFrame:
        paid_df = self.df[self.df["Type"] == "Paid"]
        return paid_df.sort_values("Estimated_Revenue", ascending=False)[["App", "Category", "Price", "Installs", "Estimated_Revenue"]].head(n)

    def build_category_installs_chart(self) -> go.Figure:
        cat_installs = self.df.groupby("Category")["Installs"].sum().reset_index().sort_values("Installs", ascending=True)
        fig = px.bar(
            cat_installs,
            x="Installs",
            y="Category",
            orientation="h",
            title="Total App Installs by Category",
            color="Installs",
            color_continuous_scale="Viridis",
            labels={"Installs": "Cumulative Installs"}
        )
        fig.update_layout(height=500, margin=dict(l=120, r=40, t=50, b=40))
        return fig

    def build_content_rating_donut(self) -> go.Figure:
        cr_counts = self.df["Content_Rating"].value_counts().reset_index()
        cr_counts.columns = ["Content_Rating", "Count"]
        fig = px.pie(
            cr_counts,
            values="Count",
            names="Content_Rating",
            title="Content Rating Distribution (Target Demographics)",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(height=450)
        return fig

    def build_size_vs_rating_scatter(self) -> go.Figure:
        fig = px.scatter(
            self.df,
            x="Size_MBs",
            y="Rating",
            color="Category",
            size="Installs",
            hover_name="App",
            title="App Size (MB) vs User Rating (Bubble Size = Installs)",
            labels={"Size_MBs": "App Size in MB", "Rating": "Star Rating (1-5)"},
            opacity=0.75
        )
        fig.update_layout(height=550)
        return fig

    def export_dashboard_html(self, output_file: str = "play_store_dashboard.html") -> str:
        """Exports a unified HTML dashboard with all interactive Plotly charts."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, output_file)

        fig1 = self.build_category_installs_chart()
        fig2 = self.build_content_rating_donut()
        fig3 = self.build_size_vs_rating_scatter()

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Google Play Store Interactive Analytics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; }}
        .metric-card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; }}
        .chart-box {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1rem; margin-bottom: 2rem; }}
    </style>
</head>
<body class="py-5">
    <div class="container">
        <header class="text-center mb-5">
            <h1 class="display-5 fw-bold text-info">📱 Google Play Store Analytics Dashboard</h1>
            <p class="text-secondary">Day 75 Capstone • Interactive Data Science with Plotly</p>
        </header>

        <!-- KPI Metrics -->
        <div class="row g-4 mb-5">
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <h5 class="text-secondary small text-uppercase">Total Apps Cataloged</h5>
                    <h2 class="fw-bold text-white">{len(self.df):,d}</h2>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <h5 class="text-secondary small text-uppercase">Average User Rating</h5>
                    <h2 class="fw-bold text-warning">{self.df['Rating'].mean():.2f} ★</h2>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <h5 class="text-secondary small text-uppercase">Total Downloads Tracked</h5>
                    <h2 class="fw-bold text-success">{self.df['Installs'].sum():,d}</h2>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <h5 class="text-secondary small text-uppercase">Est. Paid App Revenue</h5>
                    <h2 class="fw-bold text-info">${self.df['Estimated_Revenue'].sum():,.2f}</h2>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="chart-box">
            {fig1.to_html(full_html=False, include_plotlyjs=False)}
        </div>

        <div class="row g-4 mb-4">
            <div class="col-lg-6">
                <div class="chart-box h-100">
                    {fig2.to_html(full_html=False, include_plotlyjs=False)}
                </div>
            </div>
            <div class="col-lg-6">
                <div class="chart-box h-100">
                    {fig3.to_html(full_html=False, include_plotlyjs=False)}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return full_path
