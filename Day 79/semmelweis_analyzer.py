"""
Day 79: Dr. Ignaz Semmelweis Handwashing & Childbed Fever Statistical Analysis
Clinical time series analysis, clinic comparison, and Welch's t-test hypothesis testing.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


class SemmelweisAnalyzer:
    HANDWASHING_START = pd.to_datetime("1847-06-01")

    def __init__(self, base_path: str = "."):
        folder = os.path.dirname(os.path.abspath(__file__))

        self.annual_df = pd.read_csv(os.path.join(folder, "annual_deaths_by_clinic.csv"))
        self.annual_df["pct_deaths"] = self.annual_df["deaths"] / self.annual_df["births"]

        self.monthly_df = pd.read_csv(os.path.join(folder, "monthly_deaths.csv"))
        self.monthly_df["date"] = pd.to_datetime(self.monthly_df["date"])
        self.monthly_df["pct_deaths"] = self.monthly_df["deaths"] / self.monthly_df["births"]

        # Split into before and after chlorine disinfection policy
        self.before_df = self.monthly_df[self.monthly_df["date"] < self.HANDWASHING_START]
        self.after_df = self.monthly_df[self.monthly_df["date"] >= self.HANDWASHING_START]

    def get_clinic_comparison(self) -> pd.DataFrame:
        """Compares total births, deaths, and average mortality rate across clinics."""
        grouped = self.annual_df.groupby("clinic").agg(
            total_births=("births", "sum"),
            total_deaths=("deaths", "sum"),
            overall_mortality_rate=("deaths", lambda d: d.sum() / self.annual_df.loc[d.index, "births"].sum())
        ).reset_index()
        grouped["mortality_percentage"] = (grouped["overall_mortality_rate"] * 100).round(2)
        return grouped

    def get_handwashing_impact(self) -> dict:
        """Calculates statistical shift and Welch's t-test hypothesis test."""
        before_rates = self.before_df["pct_deaths"]
        after_rates = self.after_df["pct_deaths"]

        t_stat, p_value = stats.ttest_ind(before_rates, after_rates, equal_var=False)

        mean_before = float(before_rates.mean())
        mean_after = float(after_rates.mean())
        absolute_drop = mean_before - mean_after
        relative_reduction = (absolute_drop / mean_before) * 100

        return {
            "mean_before": mean_before,
            "mean_after": mean_after,
            "absolute_drop_pct": absolute_drop * 100,
            "relative_reduction_pct": relative_reduction,
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "statistically_significant": bool(p_value < 0.001)
        }

    def export_handwashing_chart(self, output_file: str = "handwashing_impact.png") -> str:
        """Renders time-series chart highlighting the dramatic plunge in maternal mortality."""
        folder = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(folder, output_file)

        plt.figure(figsize=(14, 7), dpi=200)
        
        # Plot Before and After curves
        plt.plot(self.before_df["date"], self.before_df["pct_deaths"] * 100, color="#ef4444", linewidth=2.2, label="Before Handwashing Policy")
        plt.plot(self.after_df["date"], self.after_df["pct_deaths"] * 100, color="#10b981", linewidth=2.5, label="After Chlorine Washing Mandate")

        # Vertical line for mandate
        plt.axvline(x=self.HANDWASHING_START, color="#3b82f6", linestyle="--", linewidth=2, label="Handwashing Introduced (June 1847)")

        # Annotations
        plt.annotate(
            "Chlorine Handwashing Mandated\nMortality plummets from ~10.5% to ~2.1%",
            xy=(self.HANDWASHING_START, 12),
            xytext=(pd.to_datetime("1845-01-01"), 15),
            arrowprops=dict(facecolor="#3b82f6", shrink=0.08, width=1.5, headwidth=8),
            fontsize=11,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#3b82f6", alpha=0.9)
        )

        plt.title("Vienna General Hospital: Monthly Maternal Mortality Rate (1841 - 1849)", fontsize=15, fontweight="bold", pad=15)
        plt.xlabel("Year", fontsize=12, labelpad=10)
        plt.ylabel("Percentage of Maternal Deaths (%)", fontsize=12, labelpad=10)
        plt.ylim(0, max(self.monthly_df["pct_deaths"] * 100) * 1.15)
        plt.grid(True, linestyle=":", alpha=0.5)
        plt.legend(loc="upper right", fontsize=11)
        plt.tight_layout()

        plt.savefig(out_path)
        plt.close()
        return out_path
