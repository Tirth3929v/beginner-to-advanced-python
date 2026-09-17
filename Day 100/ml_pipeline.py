"""
Day 100: Predict Titanic Survival / Machine Learning Capstone
Scikit-Learn End-to-End Pipeline: Feature Engineering, Model Training, and Inference
"""

import os
import re
from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split

TITLE_MAP = {
    "mr": 0,
    "miss": 1,
    "mrs": 2,
    "master": 3,
    "rare": 4
}


def extract_title(name: str) -> int:
    """Extracts and normalizes social title from passenger name string."""
    match = re.search(r",\s*([A-Za-z]+)\.", name)
    if match:
        title = match.group(1).lower()
        if title in ["mr"]:
            return 0
        elif title in ["miss", "ms", "mme"]:
            return 1
        elif title in ["mrs", "mlle"]:
            return 2
        elif title in ["master"]:
            return 3
        else:
            return 4  # Dr, Rev, Col, Major, Don, etc.
    return 0


class TitanicMLPipeline:
    """Comprehensive ML pipeline for Titanic passenger survival prediction."""

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or os.path.join(os.path.dirname(__file__), "titanic_data.csv")
        self.rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        self.lr_model = LogisticRegression(max_iter=1000, random_state=42)
        self.feature_names = [
            "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare",
            "Embarked", "FamilySize", "IsAlone", "Title"
        ]
        self.is_trained = False
        self.metrics: Dict[str, Any] = {}

    def preprocess_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms raw Titanic records with imputation and feature engineering."""
        data = df.copy()

        # 1. Feature extraction: Title
        if "Name" in data.columns:
            data["Title"] = data["Name"].apply(extract_title)
        else:
            data["Title"] = 0

        # 2. Imputation: Age (median fallback)
        median_age = data["Age"].median() if not data["Age"].dropna().empty else 28.0
        data["Age"] = data["Age"].fillna(median_age)

        # 3. Imputation: Fare
        median_fare = data["Fare"].median() if not data["Fare"].dropna().empty else 14.45
        data["Fare"] = data["Fare"].fillna(median_fare)

        # 4. Encoding: Sex (male=0, female=1)
        data["Sex"] = data["Sex"].map({"male": 0, "female": 1}).fillna(0).astype(int)

        # 5. Encoding: Embarked (S=0, C=1, Q=2)
        data["Embarked"] = data["Embarked"].map({"S": 0, "C": 1, "Q": 2}).fillna(0).astype(int)

        # 6. Feature engineering: Family dynamics
        data["SibSp"] = data["SibSp"].fillna(0).astype(int)
        data["Parch"] = data["Parch"].fillna(0).astype(int)
        data["FamilySize"] = data["SibSp"] + data["Parch"] + 1
        data["IsAlone"] = (data["FamilySize"] == 1).astype(int)

        return data

    def load_and_prepare(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Loads dataset and prepares feature matrix X and target y."""
        raw_df = pd.read_csv(self.data_path)
        processed = self.preprocess_raw_data(raw_df)
        X = processed[self.feature_names]
        y = processed["Survived"]
        return X, y

    def train_and_evaluate(self, test_size: float = 0.2) -> Dict[str, Any]:
        """Trains Random Forest and Logistic Regression models, returning metrics."""
        X, y = self.load_and_prepare()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Train models
        self.rf_model.fit(X_train, y_train)
        self.lr_model.fit(X_train, y_train)
        self.is_trained = True

        # Predictions
        rf_preds = self.rf_model.predict(X_test)
        rf_probs = self.rf_model.predict_proba(X_test)[:, 1]

        lr_preds = self.lr_model.predict(X_test)
        lr_probs = self.lr_model.predict_proba(X_test)[:, 1]

        # Feature importances
        importances = sorted(
            zip(self.feature_names, self.rf_model.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )

        self.metrics = {
            "test_samples": len(y_test),
            "rf_accuracy": round(float(accuracy_score(y_test, rf_preds)), 4),
            "rf_precision": round(float(precision_score(y_test, rf_preds, zero_division=0)), 4),
            "rf_recall": round(float(recall_score(y_test, rf_preds, zero_division=0)), 4),
            "rf_f1": round(float(f1_score(y_test, rf_preds, zero_division=0)), 4),
            "rf_roc_auc": round(float(roc_auc_score(y_test, rf_probs)), 4),
            "rf_confusion_matrix": confusion_matrix(y_test, rf_preds).tolist(),
            "lr_accuracy": round(float(accuracy_score(y_test, lr_preds)), 4),
            "lr_f1": round(float(f1_score(y_test, lr_preds, zero_division=0)), 4),
            "feature_importances": importances
        }

        return self.metrics

    def predict_passenger(
        self,
        pclass: int,
        sex: str,
        age: float,
        sibsp: int = 0,
        parch: int = 0,
        fare: float = 30.0,
        embarked: str = "S",
        title: str = "mr"
    ) -> Dict[str, Any]:
        """Predicts survival outcome and probability for an individual passenger."""
        if not self.is_trained:
            self.train_and_evaluate()

        family_size = sibsp + parch + 1
        is_alone = 1 if family_size == 1 else 0
        sex_num = 1 if sex.lower() == "female" else 0
        emb_map = {"s": 0, "c": 1, "q": 2}
        emb_num = emb_map.get(embarked.lower(), 0)
        title_num = TITLE_MAP.get(title.lower(), 0)

        feature_vector = pd.DataFrame([{
            "Pclass": pclass,
            "Sex": sex_num,
            "Age": age,
            "SibSp": sibsp,
            "Parch": parch,
            "Fare": fare,
            "Embarked": emb_num,
            "FamilySize": family_size,
            "IsAlone": is_alone,
            "Title": title_num
        }])[self.feature_names]

        prob = float(self.rf_model.predict_proba(feature_vector)[0][1])
        survived = bool(prob >= 0.5)

        return {
            "survived": survived,
            "survival_probability": round(prob * 100, 2),
            "fatality_probability": round((1.0 - prob) * 100, 2),
            "input_summary": {
                "class": f"{pclass}st/nd/rd Class",
                "sex": sex.capitalize(),
                "age": age,
                "family_size": family_size,
                "fare_usd": fare
            }
        }
