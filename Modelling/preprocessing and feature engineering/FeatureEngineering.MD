# Feature engineering

## Files and use

Feature construction lives in [`shared.py`](shared.py), class `BankFeatureBuilder`, and is reused by both [`Model1/model1.py`](Model1/model1.py) and [`Model2/model2.py`](Model2/model2.py). Both notebooks, [Model 1](Model1/Model1.ipynb) and [Model 2](Model2/Model2.ipynb), show the same transformed predictors.

From the project root, run `python -m Model1.model1 --data bank-full.csv` or `python -m Model2.model2 --data bank-full.csv`. In either case, the feature builder is part of the fitted pipeline and runs automatically during training and inference. For inspection in Python, call `BankFeatureBuilder().fit_transform(load_bank_data(Path("bank-full.csv")).drop(columns="y"))` after importing `Path` and these functions from `shared`.

| Feature | Construction | Reason |
|---|---|---|
| `previously_contacted` | 1 when `pdays >= 0`, else 0 | Distinguishes real prior contact from `-1` (none). |
| `pdays_known` | Nonnegative `pdays`, else missing | Avoids treating the sentinel as elapsed days. |
| `total_contacts` | `campaign + previous` | Captures total contact volume. |
| `signed_log_balance` | `sign(balance) × log(1 + abs(balance))` | Compresses large positive or negative balances. |

The original numeric age, balance, day, campaign and previous count also remain. Nine categorical fields (`job`, `marital`, `education`, `default`, `housing`, `loan`, `contact`, `month`, `poutcome`) are encoded by the preprocessing pipeline. Neither the outcome label nor current-call duration enters engineered predictors.
