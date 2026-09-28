from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    average_precision_score, confusion_matrix, fbeta_score, precision_score,
    recall_score, roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_bank_data(csv_path: Path | None) -> pd.DataFrame:
    if csv_path is not None:
        if not csv_path.is_file():
            raise FileNotFoundError(f"CSV not found: {csv_path}")
        frame = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")

    missing = set(ORIGINAL_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Expected bank-full.csv; missing columns: {sorted(missing)}")
    if set(frame["y"].dropna().unique()) != {"yes", "no"}:
        raise ValueError("Target y must contain both 'yes' and 'no' classes")
    return frame[ORIGINAL_COLUMNS].copy()

ORIGINAL_COLUMNS = [
    "age", "job", "marital", "education", "default", "balance", "housing",
    "loan", "contact", "day", "month", "duration", "campaign", "pdays",
    "previous", "poutcome", "y",
]
NUMERIC_COLUMNS = [
    "age", "balance", "day", "campaign", "previous", "pdays_known",
    "previously_contacted", "total_contacts", "signed_log_balance",
]
CATEGORICAL_COLUMNS = [
    "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "poutcome",
]

class BankFeatureBuilder(BaseEstimator, TransformerMixin):
    """Build features known before the current call's outcome."""

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        days = pd.to_numeric(X["pdays"], errors="coerce")
        X["previously_contacted"] = days.ge(0).astype(int)
        X["pdays_known"] = days.where(days.ge(0), np.nan)
        balance = pd.to_numeric(X["balance"], errors="coerce")
        X["signed_log_balance"] = np.sign(balance) * np.log1p(np.abs(balance))
        X["total_contacts"] = (
            pd.to_numeric(X["campaign"], errors="coerce")
            + pd.to_numeric(X["previous"], errors="coerce")
        )
        # Never pass post-call duration or target y to either model.
        return X[NUMERIC_COLUMNS + CATEGORICAL_COLUMNS]


def make_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("numeric", numeric, NUMERIC_COLUMNS),
        ("categorical", categorical, CATEGORICAL_COLUMNS),
    ])


def chronological_splits(frame: pd.DataFrame):
    first, second = int(0.60 * len(frame)), int(0.80 * len(frame))
    train, validation, test = frame.iloc[:first], frame.iloc[first:second], frame.iloc[second:]
    for label, part in (("train", train), ("validation", validation), ("test", test)):
        if part["y"].nunique() != 2:
            raise ValueError(f"{label} split contains only one target class")
    return train, validation, test


def choose_threshold(y_true: pd.Series, probabilities: np.ndarray) -> float:
    candidates = np.arange(0.10, 0.91, 0.05)
    scores = [fbeta_score(y_true, probabilities >= threshold, beta=2, zero_division=0)
              for threshold in candidates]
    return float(candidates[int(np.argmax(scores))])


def evaluate(y_true: pd.Series, probabilities: np.ndarray, threshold: float) -> dict:
    predicted = (probabilities >= threshold).astype(int)
    return {
        "threshold": round(threshold, 3),
        "roc_auc": round(float(roc_auc_score(y_true, probabilities)), 4),
        "average_precision": round(float(average_precision_score(y_true, probabilities)), 4),
        "precision_yes": round(float(precision_score(y_true, predicted, zero_division=0)), 4),
        "recall_yes": round(float(recall_score(y_true, predicted, zero_division=0)), 4),
        "f2_yes": round(float(fbeta_score(y_true, predicted, beta=2, zero_division=0)), 4),
        "confusion_matrix_no_yes": confusion_matrix(y_true, predicted, labels=[0, 1]).tolist(),
    }


def train_one(data: Path | None, output: Path, name: str, classifier) -> dict:
    """Fit only the selected classifier; never write into the other model's output."""
    frame = load_bank_data(data)
    train, validation, test = chronological_splits(frame)
    model = Pipeline([
        ("features", BankFeatureBuilder()),
        ("preprocess", make_preprocessor()),
        ("model", classifier),
    ])
    model.fit(train.drop(columns="y"), train["y"].eq("yes").astype(int))
    validation_scores = model.predict_proba(validation.drop(columns="y"))[:, 1]
    threshold = choose_threshold(validation["y"].eq("yes").astype(int), validation_scores)
    test_scores = model.predict_proba(test.drop(columns="y"))[:, 1]
    results = {
        "model": name,
        "source": str(data) if data else None,
        "rows": len(frame),
        "split_rows": {"train": len(train), "validation": len(validation), "test": len(test)},
        "positive_rate": {
            label: round(float(part["y"].eq("yes").mean()), 4)
            for label, part in (("train", train), ("validation", validation), ("test", test))
        },
        "excluded_post_outcome_column": "duration",
        "validation": evaluate(validation["y"].eq("yes").astype(int), validation_scores, threshold),
        "test": evaluate(test["y"].eq("yes").astype(int), test_scores, threshold),
    }
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output / "model.joblib")
    pd.DataFrame({
        "actual": test["y"].to_numpy(),
        "probability_yes": test_scores,
        "predicted_yes": test_scores >= threshold,
    }).to_csv(output / "test_predictions.csv", index=False)
    (output / "metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


def score_one(csv_path: Path, output: Path, name: str) -> Path:
    """Score new UCI-shaped rows with the selected fitted model."""
    model_path, metrics_path = output / "model.joblib", output / "metrics.json"
    if not model_path.is_file() or not metrics_path.is_file():
        raise FileNotFoundError(f"Missing trained model in {output}; run training first")
    frame = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    missing = set(ORIGINAL_COLUMNS) - {"duration", "y"} - set(frame.columns)
    if missing:
        raise ValueError(f"Prediction CSV is missing columns: {sorted(missing)}")
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    if metrics.get("model") != name:
        raise ValueError(f"The saved model belongs to {metrics.get('model')}, not {name}")
    model = joblib.load(model_path)
    probabilities = model.predict_proba(frame)[:, 1]
    threshold = metrics["validation"]["threshold"]
    destination = output / "new_predictions.csv"
    pd.DataFrame({
        "probability_yes": probabilities,
        "predicted_yes": probabilities >= threshold,
    }).to_csv(destination, index=False)
    print(f"Scored {len(frame)} rows with {name}; output: {destination}")
    return destination
