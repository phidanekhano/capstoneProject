# Preprocessing

## Files and use

The shared implementation is [`shared.py`](shared.py): `load_bank_data`, `chronological_splits`, `make_preprocessor` and `train_one`. It is imported by **both** [`Model1/model1.py`](Model1/model1.py) and [`Model2/model2.py`](Model2/model2.py). The separate [Model 1](Model1/Model1.ipynb) and [Model 2](Model2/Model2.ipynb) notebooks show their own training runs.

From the project root, run `python -m Model1.model1 --data bank-full.csv` for logistic regression or `python -m Model2.model2 --data bank-full.csv` for random forest. Both commands require the semicolon-separated UCI `bank-full.csv` and use the **same** preprocessing rules.

## Procedure

1. Read the UCI CSV with `sep=";"`; validate all 17 original columns and `y` values (`yes`/`no`). Keep original row order, which UCI reports is ordered by campaign date.
2. Split into the earliest 60% for training, next 20% for validation and latest 20% for test. Do not shuffle.
3. Inside each pipeline, impute numeric missing values with the training median, and genuine categorical missing values with the training mode. Retain the literal category `unknown` where it is present in the original data.
4. Standardise numeric columns and one-hot encode categorical columns with `handle_unknown="ignore"`. All fitted transforms use **training rows only**; validation, test and inference rows use the already fitted pipeline.
5. Exclude `duration` because the last call's duration is unknown before that call, and exclude the target `y` from all predictors. Convert the `pdays=-1` sentinel with the rules in [FeatureEngineering.MD](FeatureEngineering.MD).

There is no oversampling across the splits. Each classifier has its own class weights. The public CSV contains no client ID, so it cannot guarantee that repeated contacts from one person stay in one partition; a STADIOEquities implementation would need client-level grouping.
