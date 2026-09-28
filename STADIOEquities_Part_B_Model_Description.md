# STADIOEquities: Part B model proposal and runnable prototype

## Scope and dataset

The business objective has two parts: predict whether a registered investor will make a first successful deposit, and predict whether an already funded investor will become dormant. The public **UCI Bank Marketing `bank-full.csv`** dataset supports a *prototype of the first part only*: its outcome `y` records whether a Portuguese bank customer subscribed to a term deposit after a marketing campaign. A term-deposit subscription is not an investment account's first deposit; the two outcomes must be described and evaluated separately. The public data contain neither STADIOEquities first-deposit records nor time-series activity needed to label future dormancy.

UCI reports **45,211 rows, 16 original predictors, and a binary `yes`/`no` target** for this particular file. The rows are ordered by campaign date. This implementation uses an earlier **60% training**, subsequent **20% validation**, and latest **20% held-out test** segment without shuffling. The file has day and month, but no unambiguous full date or anonymised customer identifier, so it cannot support a true customer-level or calendar-date grouped validation. Repeated contacts from the same person might occur across splits; this remains a limitation. [UCI dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing).

## Data preprocessing

1. Read the semicolon-separated `bank-full.csv`; check its expected column names and binary target.
2. Preserve the original row order to split before fitting any data-dependent transform. Fit imputation, scaling and categorical encoding **on the training segment only**, inside a scikit-learn pipeline.
3. Treat UCI's categorical `unknown` as an informative category; the categorical pipeline also imputes genuine missing values with the training mode. Apply one-hot encoding with `handle_unknown="ignore"` for categories not seen during training.
4. Replace the `pdays = -1` sentinel, which means no previous campaign contact, with a missing numeric value. Add a separate `previously_contacted` indicator. Impute remaining numeric missing values with the training median.
5. Standardise numeric predictors for logistic regression and use the same representation for a fair comparison with the forest. **Exclude `duration`**, the length of the last call: it is only known after the call and would compromise advance prediction.
6. Keep the less frequent `yes` outcome visible through class weighting and report recall, precision, F2, average precision (area under the precision–recall curve), ROC AUC and a confusion matrix. The code does not oversample before splitting.

## Feature engineering

| Derived feature | Formula | Reason |
|---|---|---|
| `previously_contacted` | 1 if `pdays >= 0`, else 0 | Distinguishes never previously contacted customers from those with a known interval. |
| `pdays_known` | `pdays` if nonnegative, otherwise missing | Represents recency without treating `-1` as a real elapsed time. |
| `total_contacts` | `campaign + previous` | Summarises current and prior campaign contact volume. |
| `signed_log_balance` | `sign(balance) × log(1 + abs(balance))` | Dampens the effect of very large balances while preserving negative balances. |

The original age, balance, day, campaign and previous-contact count remain available. All engineered inputs use information recorded before the current call's outcome. Any feature relying on a field not available when the score is actually produced must be removed before deployment.

## Model 1: Logistic regression

This is an interpretable binary classification baseline. It estimates the probability of `y = yes` using a linear combination of scaled numeric and one-hot categorical predictors, passed through the logistic function. The implementation uses **L2 regularisation**, `C=1.0` (inverse regularisation strength), `solver="lbfgs"`, `max_iter=1500`, `class_weight="balanced"` and `random_state=42`. Class weights increase the loss attached to mistakes on the minority class. It is straightforward to inspect coefficients, although correlated engineered variables require careful interpretation. The default parameters here are prespecified starting values, not results of a claimed tuning experiment.

## Model 2: Random forest

This classifier averages probabilities across many decision trees and can capture nonlinear effects and interactions, such as different responses to prior campaign contacts across customer segments. It uses `n_estimators=250`, `max_depth=12`, `min_samples_leaf=10`, `max_features="sqrt"`, `class_weight="balanced_subsample"`, `random_state=42` and `n_jobs=-1`. The depth and minimum leaf size restrain tree complexity. A forest is less directly interpretable than the logistic model, but permutation importance on a held-out segment can be added if explanation is required. The forest shares the same preprocessing and split as Model 1.

## Training, threshold and evaluation

The models fit **only** on the first 60% of rows. For each model, the next 20% chooses a probability threshold among 0.10, 0.15, …, 0.90 by maximising **F2**, which gives recall extra weight when identifying customers who might respond to an intervention. The final 20% is evaluated **once** with that chosen threshold; no parameter or threshold is selected on test results. Each model has its own `results/model1/` or `results/model2/` directory containing `metrics.json`, `model.joblib` and `test_predictions.csv`. Compare test average precision with the test segment's `yes` prevalence and review false negatives and false positives before recommending interventions. The resulting probabilities are for the public bank task and should not be represented as STADIOEquities client probabilities.

For the actual STADIOEquities activation model, replace the public target with **first successful deposit within a stakeholder-approved window after registration**, use only data available at the proposed prediction time, and divide customers into training/validation/test cohorts by registration date. For a separate dormancy model, begin with funded clients and define an agreed future dormancy window using qualifying account activity; keep label-window events out of predictors. Refit preprocessing and both model types on each new target; the UCI results do **not** validate the dormancy model. Where customers have multiple records, group them by anonymised client ID to avoid overlap between splits.

## Run

From the project root, install `requirements.txt`. Download the official UCI archive, extract `bank.zip` and then `bank-full.csv`, and train either or both models:

```bash
python -m pip install -r requirements.txt
python -m Model1.model1 --data /path/to/bank-full.csv
python -m Model2.model2 --data /path/to/bank-full.csv
```

For inference on a semicolon-separated CSV with the same predictor columns (the `y` and `duration` columns are optional), run:

```bash
python -m Model1.model1 --predict new_customers.csv
python -m Model2.model2 --predict new_customers.csv
```

Alternatively, omit `--data` to attempt an automatic download from UCI. The separate notebooks are `Model1/Model1.ipynb` and `Model2/Model2.ipynb`. Both use shared preprocessing from `shared.py`. The scripts check column names but cannot prove that a matching file is the original UCI data.

**Reference:** Moro, S., Cortez, P. and Rita, P. (2014) ‘A data-driven approach to predict the success of bank telemarketing’, *Decision Support Systems*, 62, pp. 22–31. Dataset: Moro, S., Rita, P. and Cortez, P. (2014) *Bank Marketing* [dataset]. UCI Machine Learning Repository. doi:10.24432/C5K306.
