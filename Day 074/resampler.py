"""
Day 74: Time Series Resampling & Trend Correlation Engine
Resamples high-frequency financial time series and correlates with Google search volume.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


class TrendResampler:
    def __init__(self, data_dir: str = "data"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_dir, data_dir) if not os.path.isabs(data_dir) else data_dir

        # 1. Tesla
        self.df_tesla = pd.read_csv(os.path.join(folder, "TESLA Search Trend vs Price.csv"))
        self.df_tesla["MONTH"] = pd.to_datetime(self.df_tesla["MONTH"])

        # 2. Bitcoin Search
        self.df_btc_search = pd.read_csv(os.path.join(folder, "Bitcoin Search Trend.csv"))
        self.df_btc_search["MONTH"] = pd.to_datetime(self.df_btc_search["MONTH"])

        # 3. Bitcoin Daily Price
        self.df_btc_price = pd.read_csv(os.path.join(folder, "Daily Bitcoin Price.csv"))
        self.df_btc_price["DATE"] = pd.to_datetime(self.df_btc_price["DATE"])

        # Resample daily Bitcoin to monthly average
        self.df_btc_monthly = self.df_btc_price.resample("MS", on="DATE").mean().reset_index()

        # Merge monthly BTC search with monthly BTC price
        self.df_btc_merged = pd.merge(
            self.df_btc_search,
            self.df_btc_monthly,
            left_on="MONTH",
            right_on="DATE"
        )

    def get_tesla_correlation(self) -> float:
        return float(self.df_tesla["TSLA_WEB_SEARCH"].corr(self.df_tesla["TSLA_USD_CLOSE"]))

    def get_btc_correlation(self) -> float:
        return float(self.df_btc_merged["BTC_NEWS_SEARCH"].corr(self.df_btc_merged["CLOSE"]))

    def export_tesla_chart(self, filename: str = "tesla_trend.png") -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(base_dir, filename)

        fig, ax1 = plt.subplots(figsize=(14, 7), dpi=200)
        ax2 = ax1.twinx()

        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        years_fmt = mdates.DateFormatter("%Y")

        ax1.plot(self.df_tesla["MONTH"], self.df_tesla["TSLA_USD_CLOSE"], color="#ef4444", linewidth=2.5, label="TSLA Stock Price ($)")
        ax2.plot(self.df_tesla["MONTH"], self.df_tesla["TSLA_WEB_SEARCH"], color="#3b82f6", linewidth=2, linestyle="--", label="Web Search Interest")

        ax1.xaxis.set_major_locator(years)
        ax1.xaxis.set_major_formatter(years_fmt)
        ax1.xaxis.set_minor_locator(months)

        ax1.set_title("Tesla Web Search Volume vs TSLA Stock Price", fontsize=16, fontweight="bold", pad=15)
        ax1.set_xlabel("Year", fontsize=12)
        ax1.set_ylabel("TSLA Stock Price ($USD)", color="#ef4444", fontsize=12)
        ax2.set_ylabel("Google Search Trend (0-100)", color="#3b82f6", fontsize=12)

        ax1.grid(True, linestyle=":", alpha=0.4)
        fig.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

    def export_bitcoin_chart(self, filename: str = "bitcoin_resampled_trend.png") -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(base_dir, filename)

        fig, ax1 = plt.subplots(figsize=(14, 7), dpi=200)
        ax2 = ax1.twinx()

        years = mdates.YearLocator()
        years_fmt = mdates.DateFormatter("%Y")

        ax1.plot(self.df_btc_merged["MONTH"], self.df_btc_merged["CLOSE"], color="#f59e0b", linewidth=2.5, label="BTC Monthly Avg Price ($)")
        ax2.plot(self.df_btc_merged["MONTH"], self.df_btc_merged["BTC_NEWS_SEARCH"], color="#06b6d4", linewidth=2, linestyle="--", label="BTC News Search")

        ax1.xaxis.set_major_locator(years)
        ax1.xaxis.set_major_formatter(years_fmt)

        ax1.set_title("Bitcoin Monthly Resampled Price vs Google News Search Trend", fontsize=16, fontweight="bold", pad=15)
        ax1.set_xlabel("Year", fontsize=12)
        ax1.set_ylabel("BTC Monthly Average Price ($USD)", color="#f59e0b", fontsize=12)
        ax2.set_ylabel("Google Search Trend (0-100)", color="#06b6d4", fontsize=12)

        ax1.grid(True, linestyle=":", alpha=0.4)
        fig.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path
