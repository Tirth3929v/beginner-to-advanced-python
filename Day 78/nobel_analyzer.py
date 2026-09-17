"""
Day 78: Nobel Prize Demographic & Historical Analytics
Analyzes repeat laureates, age distributions, country rankings, and gender ratios.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class NobelPrizeAnalyzer:
    def __init__(self, csv_file: str = "nobel_prize_data.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, csv_file) if not os.path.isabs(csv_file) else csv_file

        self.df = pd.read_csv(path)
        self.clean_data()

    def clean_data(self):
        """Converts dates and computes winning age."""
        self.df["birth_date"] = pd.to_datetime(self.df["birth_date"], errors="coerce")
        self.df["winning_age"] = self.df["year"] - self.df["birth_date"].dt.year
        self.df["is_female"] = self.df["sex"] == "Female"
        self.df["decade"] = (self.df["year"] // 10) * 10

    def get_summary(self) -> dict:
        return {
            "total_prizes": len(self.df),
            "unique_laureates": int(self.df["full_name"].nunique()),
            "categories": list(self.df["category"].unique()),
            "female_winners": int(self.df["is_female"].sum()),
            "mean_winning_age": round(float(self.df["winning_age"].mean()), 1)
        }

    def get_repeat_winners(self) -> pd.DataFrame:
        """Finds individuals or organizations who won more than once."""
        counts = self.df["full_name"].value_counts()
        repeats = counts[counts > 1].reset_index()
        repeats.columns = ["full_name", "prizes_won"]
        return repeats

    def get_first_woman_laureate(self) -> pd.Series:
        female_df = self.df[self.df["sex"] == "Female"].sort_values("year")
        return female_df.iloc[0]

    def get_youngest_and_oldest(self) -> dict:
        valid_ages = self.df.dropna(subset=["winning_age"])
        youngest = valid_ages.loc[valid_ages["winning_age"].idxmin()]
        oldest = valid_ages.loc[valid_ages["winning_age"].idxmax()]
        return {"youngest": youngest, "oldest": oldest}

    def get_top_countries(self, n: int = 10) -> pd.Series:
        return self.df["birth_country"].value_counts().head(n)

    def get_female_share_by_category(self) -> pd.DataFrame:
        cat_gender = self.df.groupby("category")["is_female"].agg(["count", "mean"]).reset_index()
        cat_gender.columns = ["category", "total_prizes", "female_proportion"]
        cat_gender["female_percentage"] = (cat_gender["female_proportion"] * 100).round(1)
        return cat_gender.sort_values("female_percentage", ascending=False)

    def export_nobel_charts(self, output_file: str = "nobel_demographics.png") -> str:
        """Generates a composite 2-panel Seaborn figure (Age distribution boxplot + Top countries)."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(base_dir, output_file)

        sns.set_theme(style="whitegrid")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=200)

        # 1. Boxplot: Age distribution across categories
        sns.boxplot(
            data=self.df.dropna(subset=["winning_age"]),
            x="category",
            y="winning_age",
            hue="category",
            legend=False,
            palette="Set2",
            ax=ax1
        )
        ax1.set_title("Laureate Age Distribution by Prize Category", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Category", fontsize=12)
        ax1.set_ylabel("Age at Award (Years)", fontsize=12)

        # 2. Barplot: Top 10 Birth Countries
        top_c = self.get_top_countries(10).reset_index()
        top_c.columns = ["Country", "Laureates"]
        sns.barplot(
            data=top_c,
            x="Laureates",
            y="Country",
            hue="Country",
            legend=False,
            palette="viridis",
            ax=ax2
        )
        ax2.set_title("Top 10 Laureate Birth Countries", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Total Nobel Prizes Won", fontsize=12)
        ax2.set_ylabel("")

        fig.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path
