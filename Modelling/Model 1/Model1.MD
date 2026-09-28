# Model 1 — logistic regression

## Files and use

- **Training and inference:** [`model1.py`](model1.py), with `make_classifier()` defining Model 1 only. It imports data preparation and evaluation from [`../shared.py`](../shared.py).
- **Notebook:** [`Model1.ipynb`](Model1.ipynb), which runs only Model 1.
- **Preprocessing:** [`../Preprocessing.MD`](../Preprocessing.MD); **features:** [`../FeatureEngineering.MD`](../FeatureEngineering.MD).

Run these commands from the **project root**, after installing [`../requirements.txt`](../requirements.txt):

```bash
python -m Model1.model1 --data bank-full.csv
python -m Model1.model1 --predict new_customers.csv
```

The first command trains Model 1 and writes `results/model1/model.joblib`, `results/model1/metrics.json` and `results/model1/test_predictions.csv`. The second reads its saved pipeline and validation-selected threshold, then writes `results/model1/new_predictions.csv` with `probability_yes` and `predicted_yes`. New data must be a semicolon-separated CSV with the original UCI predictors; the `duration` and target `y` columns may be absent. An optional `--output path/to/folder` changes the Model 1 output folder for both commands.

## Technique and parameters

Logistic regression predicts `y=yes` from a linear combination of processed predictors. It uses **L2 regularisation** (solver default), `C=1.0`, `solver="lbfgs"`, `max_iter=1500`, `class_weight="balanced"` and `random_state=42`. The class weighting helps the less frequent `yes` outcome; the coefficients provide an interpretable baseline, subject to correlated predictors. These are specified starting values, not a claimed exhaustive parameter search.

Train on the earliest 60% of rows. Select the F2-maximising threshold from 0.10–0.90 in steps of 0.05 on the next 20%, then report ROC AUC, average precision, precision, recall, F2 and confusion matrix on the untouched last 20%. These results apply to the UCI term-deposit outcome, not STADIOEquities client activation.
