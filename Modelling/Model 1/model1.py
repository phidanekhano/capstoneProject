"""Train or use Model 1 (logistic regression) on UCI bank-full.csv.

Run from project root: python -m Model1.model1 --data bank-full.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

from sklearn.linear_model import LogisticRegression

from shared import score_one, train_one

NAME = "logistic_regression"


def make_classifier() -> LogisticRegression:
    return LogisticRegression(
        C=1.0, solver="lbfgs", max_iter=1500,
        class_weight="balanced", random_state=42,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="Official UCI bank-full.csv for training")
    parser.add_argument("--output", type=Path, default=Path("results/model1"))
    parser.add_argument("--predict", type=Path, help="New semicolon-separated CSV to score")
    args = parser.parse_args()
    if args.predict:
        score_one(args.predict, args.output, NAME)
    else:
        train_one(args.data, args.output, NAME, make_classifier())


if __name__ == "__main__":
    main()
