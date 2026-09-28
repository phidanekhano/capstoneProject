"""Train or use Model 2 (random forest) on UCI bank-full.csv.

Run from project root: python -m Model2.model2 --data bank-full.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier

from shared import score_one, train_one

NAME = "random_forest"


def make_classifier() -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=250, max_depth=12, min_samples_leaf=10,
        max_features="sqrt", class_weight="balanced_subsample",
        random_state=42, n_jobs=-1,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="Official UCI bank-full.csv for training")
    parser.add_argument("--output", type=Path, default=Path("results/model2"))
    parser.add_argument("--predict", type=Path, help="New semicolon-separated CSV to score")
    args = parser.parse_args()
    if args.predict:
        score_one(args.predict, args.output, NAME)
    else:
        train_one(args.data, args.output, NAME, make_classifier())


if __name__ == "__main__":
    main()
