"""
Day 72: Data Visualization with Matplotlib
Reshaping, Pivoting, Rolling Averages, and Multi-Line Plotting of StackOverflow Trends.
"""

import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server/script environments
import matplotlib.pyplot as plt
import pandas as pd


class TrendVisualizer:
    def __init__(self, csv_file: str = "QueryResults.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, csv_file) if not os.path.isabs(csv_file) else csv_file
        
        # Load and rename columns
        self.df = pd.read_csv(path, names=["DATE", "TAG", "POSTS"], header=0)
        self.df["DATE"] = pd.to_datetime(self.df["DATE"])
        
        # Reshape data into pivot table
        self.reshaped_df = self.df.pivot(index="DATE", columns="TAG", values="POSTS").fillna(0)
        self.smooth_df = self.reshaped_df.rolling(window=6).mean()

    def get_total_posts_by_language(self) -> pd.Series:
        """Returns total historical posts recorded per language."""
        return self.df.groupby("TAG")["POSTS"].sum().sort_values(ascending=False)

    def get_most_recent_rankings(self) -> pd.Series:
        """Returns the most recent monthly post counts sorted descending."""
        latest_row = self.reshaped_df.iloc[-1]
        return latest_row.sort_values(ascending=False)

    def export_trend_chart(self, output_filename: str = "programming_language_trends.png", smooth: bool = True) -> str:
        """Generates and saves a publication-quality Matplotlib line chart."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, output_filename)

        plot_data = self.smooth_df if smooth else self.reshaped_df

        plt.figure(figsize=(14, 8), dpi=200)
        plt.title("Popularity of Programming Languages Over Time (Stack Overflow)", fontsize=16, fontweight="bold", pad=15)
        plt.xlabel("Year", fontsize=12, labelpad=10)
        plt.ylabel("Number of Monthly Posts (6-Month Rolling Avg)", fontsize=12, labelpad=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.ylim(0, max(plot_data.max()) * 1.08)

        colors = {
            "python": "#3b82f6",
            "javascript": "#f59e0b",
            "java": "#ef4444",
            "c#": "#8b5cf6",
            "c++": "#10b981",
            "r": "#06b6d4",
            "swift": "#f97316",
            "go": "#14b8a6",
            "ruby": "#ec4899",
            "php": "#6366f1"
        }

        for column in plot_data.columns:
            line_color = colors.get(column.lower(), None)
            linewidth = 3.0 if column.lower() == "python" else 1.8
            plt.plot(plot_data.index, plot_data[column], label=column.capitalize(), color=line_color, linewidth=linewidth)

        plt.legend(fontsize=11, loc="upper left", frameon=True)
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path
