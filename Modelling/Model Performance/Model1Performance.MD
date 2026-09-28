# Model 1 performance — logistic regression

## Files and how to reproduce

Model 1 is trained by [`Model1/model1.py`](Model1/model1.py) or [`Model1/Model1.ipynb`](Model1/Model1.ipynb). The shared [`performance_analysis.py`](performance_analysis.py) independently recalculates this report's metrics from [`results/model1/test_predictions.csv`](results/model1/test_predictions.csv) and [`results/model1/metrics.json`](results/model1/metrics.json); it never loads the saved model object. From the repository root:

```bash
python -m pip install -r requirements.txt
python -m Model1.model1 --data data/bank-full.csv
python -m Model2.model2 --data data/bank-full.csv
python performance_analysis.py --results results --output performance_summary.json
```

The analysis command checks both models because it also produces the paired comparison. To reproduce **only** Model 1's original test output, the Model 1 training command suffices. The numbers below were recalculated from the supplied `results.zip` test predictions; this report did not retrain the model. In the repository copy of `metrics.json`, only the source's personal computer path has been shortened to `data/bank-full.csv`.

## Evaluation setup

The UCI `bank-full.csv` file contains 45,211 records. The original date-ordered rows were split into 27,126 training, 9,042 validation and 9,043 test rows (60/20/20). The outcome `y=yes` means **term-deposit subscription**. The current call's `duration` was excluded because it would not be available before the call. The Model 1 threshold of **0.45** was selected on validation rows by maximising F2; the test rows were then evaluated once at that threshold. This is an analogue for STADIOEquities activation, not an actual first-deposit or dormancy model.

## Results

| Measure | Validation | Held-out test |
|---|---:|---:|
| `yes` prevalence | 0.1179 | 0.3158 |
| ROC AUC | 0.6248 | **0.6654** |
| Average precision (PR AUC summary) | 0.1634 | **0.4401** |
| Precision for `yes` | 0.1474 | **0.4339** |
| Recall for `yes` | 0.8068 | **0.6810** |
| F2 for `yes` | 0.4257 | **0.6114** |
| F1 for `yes` | — | 0.5300 |
| Specificity for `no` | — | 0.5898 |
| Balanced accuracy | — | 0.6354 |
| Accuracy | — | 0.6186 |
| Brier score (lower is better) | — | 0.2380 |

**Held-out confusion matrix (9,043 rows):**

| Actual / predicted | Predicted `no` | Predicted `yes` |
|---|---:|---:|
| Actual `no` | 3,649 (TN) | 2,538 (FP) |
| Actual `yes` | 911 (FN) | 1,945 (TP) |

The model flagged **4,483** test rows as likely subscribers. Of those, 1,945 actually subscribed: precision **43.39%**. It found **68.10%** of the 2,856 actual subscribers. ROC AUC **0.6654** and average precision **0.4401** indicate useful but limited ranking; average precision exceeds the test-set prevalence baseline **0.3158**. The 95% paired-row bootstrap percentile intervals (1,000 resamples, seed 42) were **0.6547–0.6775** for ROC AUC, **0.4236–0.4582** for average precision and **0.5977–0.6261** for F2.

Accuracy **0.6186** is below the always-`no` test baseline **0.6842** because the validation-selected F2 threshold favours finding subscribers and creates false positives. Brier **0.2380** is also worse than a constant test-prevalence probability baseline of approximately **0.2161**; probability calibration needs assessment before acting on the probabilities as absolute risk estimates. The positive rate changed from **5.04%** in training to **11.79%** in validation and **31.58%** in testing. This substantial temporal shift limits claims about future campaigns. The row bootstrap intervals describe uncertainty within this test segment and do not account for later periods or repeated customers.
