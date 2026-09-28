# Model 2 — random forest

## Files and use

- **Training and inference:** [`model2.py`](model2.py), with `make_classifier()` defining Model 2 only. It imports shared data preparation and evaluation from [`../shared.py`](../shared.py).
- **Notebook:** [`Model2.ipynb`](Model2.ipynb), which runs only Model 2.
- **Preprocessing:** [`../Preprocessing.MD`](../Preprocessing.MD); **features:** [`../FeatureEngineering.MD`](../FeatureEngineering.MD).

Run these commands from the **project root**, after installing [`../requirements.txt`](../requirements.txt):

```bash
python -m Model2.model2 --data bank-full.csv
python -m Model2.model2 --predict new_customers.csv
```

The first command trains Model 2 and writes `results/model2/model.joblib`, `results/model2/metrics.json` and `results/model2/test_predictions.csv`. The second loads its saved pipeline and validation-selected threshold, then writes `results/model2/new_predictions.csv` with `probability_yes` and `predicted_yes`. New data must be a semicolon-separated CSV with the original UCI predictors; `duration` and target `y` may be absent. An optional `--output path/to/folder` changes the Model 2 output folder for both commands.

## Technique and parameters

A random forest averages probability estimates from multiple trees, capturing nonlinear effects and interactions. Its settings are `n_estimators=250`, `max_depth=12`, `min_samples_leaf=10`, `max_features="sqrt"`, `class_weight="balanced_subsample"`, `random_state=42` and `n_jobs=-1`. The depth and minimum leaf size restrain complexity. It uses the same predictors and chronological split as Model 1; these values are specified starting parameters, not a claimed exhaustive search.

Train on the earliest 60% of rows. Select its own F2-maximising threshold from 0.10–0.90 on the next 20%, then report ROC AUC, average precision, precision, recall, F2 and confusion matrix on the untouched last 20%. The public dataset does not establish performance for STADIOEquities dormancy prediction.
