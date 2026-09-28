# Model 2 performance — random forest

## Files and how to reproduce

Model 2 is trained by [`Model2/model2.py`](Model2/model2.py) or [`Model2/Model2.ipynb`](Model2/Model2.ipynb). The shared [`performance_analysis.py`](performance_analysis.py) independently recalculates these measures from [`results/model2/test_predictions.csv`](results/model2/test_predictions.csv) and [`results/model2/metrics.json`](results/model2/metrics.json). From the repository root:

```bash
python -m pip install -r requirements.txt
python -m Model1.model1 --data data/bank-full.csv
python -m Model2.model2 --data data/bank-full.csv
python performance_analysis.py --results results --output performance_summary.json
```

The analysis command checks both models for the paired comparison. To reproduce **only** Model 2's original test output, the Model 2 training command suffices. The numbers below were recalculated from the supplied `results.zip` test predictions, without retraining. The repository copy of `metrics.json` shortens only the source's personal computer path to `data/bank-full.csv`.

## Evaluation setup

Model 2 uses the same UCI `bank-full.csv` rows and chronological split as Model 1: 27,126 training, 9,042 validation and 9,043 test records. `y=yes` means **term-deposit subscription**, not STADIOEquities account activation or dormancy. The current call's `duration` was excluded. The random forest's threshold of **0.35** was selected on validation rows by maximising F2 and then fixed for the held-out test evaluation.

## Results

| Measure | Validation | Held-out test |
|---|---:|---:|
| `yes` prevalence | 0.1179 | 0.3158 |
| ROC AUC | 0.6137 | **0.5937** |
| Average precision (PR AUC summary) | 0.1666 | **0.3823** |
| Precision for `yes` | 0.1399 | **0.3560** |
| Recall for `yes` | 0.8171 | **0.7616** |
| F2 for `yes` | 0.4152 | **0.6203** |
| F1 for `yes` | — | 0.4852 |
| Specificity for `no` | — | 0.3642 |
| Balanced accuracy | — | 0.5629 |
| Accuracy | — | 0.4897 |
| Brier score (lower is better) | — | 0.2229 |

**Held-out confusion matrix (9,043 rows):**

| Actual / predicted | Predicted `no` | Predicted `yes` |
|---|---:|---:|
| Actual `no` | 2,253 (TN) | 3,934 (FP) |
| Actual `yes` | 681 (FN) | 2,175 (TP) |

The forest flagged **6,109** test rows as likely subscribers and found **76.16%** of the 2,856 actual subscribers. Its precision was **35.60%**: roughly 64 out of 100 flagged rows were non-subscribers. Average precision **0.3823** exceeds the test-set prevalence baseline **0.3158**, but ROC AUC **0.5937** indicates relatively weak ranking. The 95% paired-row bootstrap percentile intervals (1,000 resamples, seed 42) were **0.5805–0.6057** for ROC AUC, **0.3669–0.4004** for average precision and **0.6071–0.6337** for F2.

The lower threshold prioritises recall and yields many false positives; accuracy **0.4897** is below the always-`no` baseline **0.6842**. Brier **0.2229** is better than Model 1's score but worse than the constant test-prevalence baseline of approximately **0.2161**. The `yes` share changes sharply across training (**5.04%**), validation (**11.79%**) and test (**31.58%**) periods. This shift and the lack of customer IDs limit conclusions about future performance; the bootstrap intervals cover this observed test segment only.
