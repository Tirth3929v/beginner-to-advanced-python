"""
Day 80: Multivariable Linear Regression House Price Predictor
Feature engineering, train-test splitting, log-transformation, and correlation heatmaps.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


class BostonHousingPredictor:
    def __init__(self, csv_file: str = "boston.csv"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, csv_file) if not os.path.isabs(csv_file) else csv_file

        self.df = pd.read_csv(path)
        self.features = [c for c in self.df.columns if c != "PRICE"]
        self.prepare_and_fit()

    def prepare_and_fit(self):
        """Splits train/test datasets and fits standard + log-transformed regression models."""
        X = self.df[self.features]
        y = self.df["PRICE"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # 1. Standard Linear Regression
        self.linear_model = LinearRegression()
        self.linear_model.fit(self.X_train, self.y_train)

        self.train_r2 = float(self.linear_model.score(self.X_train, self.y_train))
        self.test_r2 = float(self.linear_model.score(self.X_test, self.y_test))
        self.y_pred = self.linear_model.predict(self.X_test)
        self.rmse = float(np.sqrt(mean_squared_error(self.y_test, self.y_pred)))

        # 2. Log-Transformed Model (ln(PRICE))
        y_train_log = np.log(self.y_train)
        self.log_model = LinearRegression()
        self.log_model.fit(self.X_train, y_train_log)
        self.log_train_r2 = float(self.log_model.score(self.X_train, y_train_log))

    def get_coefficients_table(self) -> pd.DataFrame:
        """Returns sorted feature impact coefficients."""
        coef_df = pd.DataFrame({
            "Feature": self.features,
            "Coefficient": self.linear_model.coef_
        })
        coef_df["Abs_Impact"] = coef_df["Coefficient"].abs()
        return coef_df.sort_values("Abs_Impact", ascending=False).drop(columns=["Abs_Impact"])

    def predict_custom_house(self, rm: float = 6.0, crim: float = 0.2, ptratio: float = 18.0, lstat: float = 12.0, chas: int = 0) -> float:
        """Predicts estimated median house price ($1000s) given core user inputs."""
        # Use median values for other features
        sample = self.df[self.features].median().to_dict()
        sample["RM"] = rm
        sample["CRIM"] = crim
        sample["PTRATIO"] = ptratio
        sample["LSTAT"] = lstat
        sample["CHAS"] = chas

        sample_df = pd.DataFrame([sample])
        pred_k = float(self.linear_model.predict(sample_df)[0])
        return float(np.clip(pred_k, 5.0, 60.0))

    def export_correlation_heatmap(self, output_file: str = "housing_correlations.png") -> str:
        """Renders correlation matrix heatmap using Seaborn."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(base_dir, output_file)

        plt.figure(figsize=(12, 10), dpi=200)
        corr_matrix = self.df.corr().round(2)
        sns.heatmap(
            corr_matrix,
            cmap="coolwarm",
            annot=True,
            fmt=".2f",
            linewidths=0.5,
            cbar_kws={"label": "Pearson Correlation"}
        )
        plt.title("Boston Housing: Multivariable Feature Correlation Matrix", fontsize=15, fontweight="bold", pad=15)
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        return out_path

    def export_residuals_plot(self, output_file: str = "residuals_analysis.png") -> str:
        """Renders Actual vs Predicted scatter plot."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(base_dir, output_file)

        plt.figure(figsize=(10, 6), dpi=200)
        sns.set_theme(style="whitegrid")

        plt.scatter(self.y_test, self.y_pred, color="#0284c7", alpha=0.7, edgecolors="none", s=50)
        plt.plot([self.y_test.min(), self.y_test.max()], [self.y_test.min(), self.y_test.max()], color="#ef4444", linestyle="--", linewidth=2, label="Perfect 1:1 Line")

        plt.title(f"Actual vs Predicted Housing Prices (Test R² = {self.test_r2:.3f})", fontsize=14, fontweight="bold", pad=12)
        plt.xlabel("Actual Median Home Price ($1000s)", fontsize=11)
        plt.ylabel("Model Predicted Price ($1000s)", fontsize=11)
        plt.legend(loc="upper left")
        plt.tight_layout()

        plt.savefig(out_path)
        plt.close()
        return out_path
