"""
Day 71: College Major Salary Analysis with Pandas
Data exploration, data cleaning, spread computation, and category aggregations.
"""

import os
import pandas as pd


class SalaryAnalyzer:
    def __init__(self, csv_path: str = "salaries_by_college_major.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(base_dir, csv_path) if not os.path.isabs(csv_path) else csv_path
        
        self.df = pd.read_csv(target_path)
        self.clean_data()

    def clean_data(self):
        """Drops missing values (including metadata footer row) and sets up spread metrics."""
        self.df = self.df.dropna()
        # Compute spread between 90th and 10th percentile
        self.df["Spread"] = self.df["Mid-Career 90th Percentile Salary"] - self.df["Mid-Career 10th Percentile Salary"]

    def get_summary_stats(self) -> dict:
        return {
            "total_majors": len(self.df),
            "columns": list(self.df.columns),
            "groups": list(self.df["Group"].unique()),
            "avg_starting": float(self.df["Starting Median Salary"].mean()),
            "avg_mid_career": float(self.df["Mid-Career Median Salary"].mean())
        }

    def highest_starting_salary(self) -> pd.Series:
        idx = self.df["Starting Median Salary"].idxmax()
        return self.df.loc[idx]

    def lowest_starting_salary(self) -> pd.Series:
        idx = self.df["Starting Median Salary"].idxmin()
        return self.df.loc[idx]

    def highest_mid_career_salary(self) -> pd.Series:
        idx = self.df["Mid-Career Median Salary"].idxmax()
        return self.df.loc[idx]

    def lowest_risk_majors(self, n: int = 5) -> pd.DataFrame:
        """Majors with the lowest risk (smallest spread between 10th and 90th percentiles)."""
        low_risk = self.df.sort_values("Spread")
        return low_risk[["Undergraduate Major", "Spread", "Starting Median Salary", "Mid-Career Median Salary"]].head(n)

    def highest_potential_majors(self, n: int = 5) -> pd.DataFrame:
        """Majors with highest upside potential (largest spread)."""
        high_potential = self.df.sort_values("Spread", ascending=False)
        return high_potential[["Undergraduate Major", "Spread", "Mid-Career 90th Percentile Salary"]].head(n)

    def group_by_field(self) -> pd.DataFrame:
        """Aggregates salary statistics by academic field (STEM, Business, HASS)."""
        # Set display format for float values
        grouped = self.df.groupby("Group").agg(
            Major_Count=("Undergraduate Major", "count"),
            Avg_Starting_Salary=("Starting Median Salary", "mean"),
            Avg_Mid_Career_Salary=("Mid-Career Median Salary", "mean"),
            Avg_90th_Percentile=("Mid-Career 90th Percentile Salary", "mean")
        ).round(2)
        return grouped
