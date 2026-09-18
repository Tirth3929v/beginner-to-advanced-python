"""
Day 73: LEGO Dataset Historical Analytics
Multi-table merges, aggregations, complexity evolution, and theme metrics.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


class LegoAnalyzer:
    def __init__(self, data_dir: str = "data"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_dir, data_dir) if not os.path.isabs(data_dir) else data_dir

        self.colors_df = pd.read_csv(os.path.join(folder, "colors.csv"))
        self.themes_df = pd.read_csv(os.path.join(folder, "themes.csv"))
        self.sets_df = pd.read_csv(os.path.join(folder, "sets.csv"))

    def get_color_stats(self) -> dict:
        total_colors = self.colors_df["name"].nunique()
        trans_counts = self.colors_df["is_trans"].value_counts()
        return {
            "total_colors": int(total_colors),
            "opaque_colors": int(trans_counts.get("f", 0)),
            "transparent_colors": int(trans_counts.get("t", 0))
        }

    def get_oldest_sets(self, n: int = 5) -> pd.DataFrame:
        return self.sets_df.sort_values("year").head(n)

    def get_largest_sets(self, n: int = 5) -> pd.DataFrame:
        """Returns the largest LEGO sets ever made by part count."""
        return self.sets_df.sort_values("num_parts", ascending=False).head(n)

    def get_sets_per_year(self) -> pd.Series:
        return self.sets_df.groupby("year")["set_num"].count()

    def get_avg_parts_per_year(self) -> pd.Series:
        return self.sets_df.groupby("year")["num_parts"].mean()

    def get_top_themes(self, n: int = 10) -> pd.DataFrame:
        """Merges sets with themes to rank themes by number of published sets."""
        theme_counts = self.sets_df["theme_id"].value_counts().reset_index()
        theme_counts.columns = ["id", "set_count"]
        merged = pd.merge(theme_counts, self.themes_df, on="id")
        return merged[["name", "set_count"]].head(n)

    def export_lego_charts(self, output_path: str = "lego_evolution.png") -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, output_path)

        sets_by_year = self.get_sets_per_year()
        parts_by_year = self.get_avg_parts_per_year()

        fig, ax1 = plt.subplots(figsize=(14, 7), dpi=200)
        ax2 = ax1.twinx()

        ax1.plot(sets_by_year.index, sets_by_year.values, color="#0284c7", linewidth=2.5, label="Sets Released / Year")
        ax2.plot(parts_by_year.index, parts_by_year.values, color="#ef4444", linewidth=2.5, linestyle="--", label="Avg Parts / Set")

        ax1.set_title("The Evolution of LEGO Complexity & Set Output (1949 - 2023)", fontsize=16, fontweight="bold", pad=15)
        ax1.set_xlabel("Year", fontsize=12, labelpad=10)
        ax1.set_ylabel("Number of Sets Released", color="#0284c7", fontsize=12, labelpad=10)
        ax2.set_ylabel("Average Piece Count", color="#ef4444", fontsize=12, labelpad=10)

        ax1.tick_params(axis='y', labelcolor="#0284c7")
        ax2.tick_params(axis='y', labelcolor="#ef4444")
        ax1.grid(True, linestyle=":", alpha=0.4)

        fig.tight_layout()
        plt.savefig(full_path)
        plt.close()
        return full_path
