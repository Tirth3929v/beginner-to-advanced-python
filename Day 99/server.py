"""
Day 99: Public Data Analysis & Interactive Web Dashboard
Flask Web Server Hosting Live Interactive Plotly Dashboard
"""

import os
from flask import Flask, render_template_string, jsonify, request
from dashboard_data import PublicDataAnalytics
import plotly.io as pio

app = Flask(__name__)


@app.route("/")
def index():
    region = request.args.get("region")
    df = PublicDataAnalytics.get_dataframe()
    if region and region != "All":
        df = df[df["region"] == region]

    kpis = PublicDataAnalytics.calculate_kpis(df)
    scatter_fig = PublicDataAnalytics.generate_scatter_figure(df)
    bar_fig = PublicDataAnalytics.generate_top_devs_bar(df)

    scatter_html = pio.to_html(scatter_fig, full_html=False, include_plotlyjs="cdn")
    bar_html = pio.to_html(bar_fig, full_html=False, include_plotlyjs=False)

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Global Tech & Socioeconomic Intelligence Dashboard</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
      <style>
        body { background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, system-ui, sans-serif; }
        .kpi-card { background-color: #151e32; border: 1px solid #24324f; border-radius: 10px; padding: 20px; }
        .kpi-num { font-size: 2.2rem; font-weight: 700; color: #38bdf8; }
        .chart-card { background-color: #151e32; border: 1px solid #24324f; border-radius: 12px; padding: 15px; margin-bottom: 25px; }
      </style>
    </head>
    <body class="py-4">
      <div class="container-fluid px-5">
        <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom border-secondary">
          <div>
            <h1 class="h2 text-white mb-1">🌐 Global Tech & Economic Dashboard</h1>
            <p class="text-secondary mb-0">Public Dataset Analytics & Interactive Plotly Engine</p>
          </div>
          <form class="d-flex gap-2 align-items-center" method="GET" action="/">
            <label class="text-secondary small">Filter Region:</label>
            <select name="region" class="form-select form-select-sm bg-dark text-white border-secondary" onchange="this.form.submit()">
              <option value="All" {% if selected_region == 'All' %}selected{% endif %}>All Regions</option>
              <option value="Europe" {% if selected_region == 'Europe' %}selected{% endif %}>Europe</option>
              <option value="Asia-Pacific" {% if selected_region == 'Asia-Pacific' %}selected{% endif %}>Asia-Pacific</option>
              <option value="North America" {% if selected_region == 'North America' %}selected{% endif %}>North America</option>
              <option value="Latin America" {% if selected_region == 'Latin America' %}selected{% endif %}>Latin America</option>
              <option value="Middle East" {% if selected_region == 'Middle East' %}selected{% endif %}>Middle East</option>
              <option value="Africa" {% if selected_region == 'Africa' %}selected{% endif %}>Africa</option>
            </select>
          </form>
        </div>

        <!-- KPI Tiles -->
        <div class="row g-3 mb-4">
          <div class="col-md-3">
            <div class="kpi-card text-center">
              <div class="text-secondary small text-uppercase">Total Software Devs</div>
              <div class="kpi-num">{{ "{:,}".format(kpis['total_developers']) }}</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="kpi-card text-center">
              <div class="text-secondary small text-uppercase">Median GDP per Capita</div>
              <div class="kpi-num">${{ "{:,.0f}".format(kpis['median_gdp']) }}</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="kpi-card text-center">
              <div class="text-secondary small text-uppercase">Avg Internet Penetration</div>
              <div class="kpi-num">{{ kpis['avg_internet_penetration'] }}%</div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="kpi-card text-center">
              <div class="text-secondary small text-uppercase">Total Tech Exports</div>
              <div class="kpi-num">${{ "{:,.1f}".format(kpis['total_tech_exports_billions']) }}B</div>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="row">
          <div class="col-lg-7">
            <div class="chart-card shadow">
              {{ scatter_html|safe }}
            </div>
          </div>
          <div class="col-lg-5">
            <div class="chart-card shadow">
              {{ bar_html|safe }}
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    return render_template_string(
        template,
        kpis=kpis,
        scatter_html=scatter_html,
        bar_html=bar_html,
        selected_region=region or "All"
    )


@app.route("/api/kpis")
def api_kpis():
    df = PublicDataAnalytics.get_dataframe()
    return jsonify(PublicDataAnalytics.calculate_kpis(df))


if __name__ == "__main__":
    print("🚀 Public Data Dashboard running at http://127.0.0.1:5050")
    app.run(port=5050, debug=True)
