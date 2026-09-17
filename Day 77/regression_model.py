"""
Day 77: Movie Box Office Linear Regression with Scikit-Learn & Seaborn
Predicts worldwide gross revenue from production budgets.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression


class MovieRegressionModel:
    def __init__(self, csv_file: str = "cost_revenue_dirty.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, csv_file) if not os.path.isabs(csv_file) else csv_file

        self.df = pd.read_csv(path)
        self.clean_data()
        self.fit_model()

    def clean_data(self):
        """Cleans currency strings, parses dates, and filters unreleased or zero-gross films."""
        # Clean currency characters
        for col in ["USD_Production_Budget", "USD_Worldwide_Gross", "USD_Domestic_Gross"]:
            self.df[col] = self.df[col].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
            self.df[col] = pd.to_numeric(self.df[col])

        self.df["Release_Date"] = pd.to_datetime(self.df["Release_Date"])

        # Filter unreleased films (after 2024-01-01) and zero revenue entries
        cutoff_date = pd.to_datetime("2024-01-01")
        self.clean_df = self.df[(self.df["Release_Date"] <= cutoff_date) & (self.df["USD_Worldwide_Gross"] > 0)].copy()

        self.clean_df["Profit"] = self.clean_df["USD_Worldwide_Gross"] - self.clean_df["USD_Production_Budget"]
        self.clean_df["ROI_Multiple"] = self.clean_df["USD_Worldwide_Gross"] / self.clean_df["USD_Production_Budget"]

    def fit_model(self):
        """Trains Scikit-Learn Ordinary Least Squares (OLS) Linear Regression model."""
        X = self.clean_df[["USD_Production_Budget"]]
        y = self.clean_df["USD_Worldwide_Gross"]

        self.model = LinearRegression()
        self.model.fit(X, y)
        self.slope = float(self.model.coef_[0])
        self.intercept = float(self.model.intercept_)
        self.r2_score = float(self.model.score(X, y))

    def get_model_summary(self) -> dict:
        return {
            "total_movies_analyzed": len(self.clean_df),
            "slope_coef": self.slope,
            "intercept": self.intercept,
            "r2_score": self.r2_score,
            "avg_budget": float(self.clean_df["USD_Production_Budget"].mean()),
            "avg_worldwide_gross": float(self.clean_df["USD_Worldwide_Gross"].mean())
        }

    def predict_revenue(self, budget_usd: float) -> float:
        """Predicts estimated worldwide box office revenue for a given production budget."""
        input_df = pd.DataFrame([[budget_usd]], columns=["USD_Production_Budget"])
        prediction = self.model.predict(input_df)[0]
        return float(max(0.0, prediction))

    def get_highest_roi_movies(self, n: int = 5) -> pd.DataFrame:
        return self.clean_df.sort_values("ROI_Multiple", ascending=False)[["Movie_Title", "USD_Production_Budget", "USD_Worldwide_Gross", "ROI_Multiple"]].head(n)

    def export_seaborn_plot(self, output_file: str = "box_office_regression.png") -> str:
        """Renders and saves a high-DPI Seaborn regression plot."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(base_dir, output_file)

        plt.figure(figsize=(12, 7), dpi=200)
        sns.set_theme(style="darkgrid")

        # Convert to Millions for readable axes
        budget_m = self.clean_df["USD_Production_Budget"] / 1e6
        revenue_m = self.clean_df["USD_Worldwide_Gross"] / 1e6

        ax = sns.regplot(
            x=budget_m,
            y=revenue_m,
            scatter_kws={"alpha": 0.5, "color": "#0284c7", "s": 40},
            line_kws={"color": "#ef4444", "linewidth": 2.5, "label": f"Fit: y = {self.slope:.2f}x + {self.intercept/1e6:.1f}M (R²={self.r2_score:.2f})"}
        )

        plt.title("Film Production Budget vs Worldwide Gross Revenue (OLS Fit)", fontsize=15, fontweight="bold", pad=15)
        plt.xlabel("Production Budget ($ Millions USD)", fontsize=12, labelpad=10)
        plt.ylabel("Worldwide Gross ($ Millions USD)", fontsize=12, labelpad=10)
        plt.xlim(0, max(budget_m) * 1.05)
        plt.ylim(0, max(revenue_m) * 1.05)
        plt.legend(loc="upper left", fontsize=11)
        plt.tight_layout()

        plt.savefig(out_path)
        plt.close()
        return out_path
