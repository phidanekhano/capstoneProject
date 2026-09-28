# Model 1 versus Model 2

## Files and how to reproduce

The comparison uses [`performance_analysis.py`](performance_analysis.py), which reads both models' `metrics.json` and `test_predictions.csv` files, checks that the held-out labels align row for row, recalculates metrics and creates [`performance_summary.json`](performance_summary.json). Training is in [`Model1/model1.py`](Model1/model1.py) and [`Model2/model2.py`](Model2/model2.py); their separate notebooks provide interactive alternatives. From the project root, after installing [`requirements.txt`](requirements.txt):

```bash
python -m Model1.model1 --data data/bank-full.csv
python -m Model2.model2 --data data/bank-full.csv
python performance_analysis.py --results results --output performance_summary.json
```

To recalculate the supplied run directly without retraining, put `results.zip` at the project root and run `python performance_analysis.py --zip results.zip --output performance_summary.json`. The repository contains the supplied test predictions and JSON metrics with the original local source path shortened; it does not include the UCI CSV or large model binaries.

## Same held-out test segment

Both models were evaluated on **the same 9,043 ordered test rows**, including **2,856 `yes`** and **6,187 `no`** cases. The positive prevalence was **31.58%**. Each model used its own F2-maximising threshold selected on the preceding validation segment; Model 1 used **0.45**, Model 2 **0.35**. All differences below mean *Model 1 minus Model 2* and were computed before rounding the displayed values.

| Measure | Model 1: logistic | Model 2: forest | Difference | Interpretation |
|---|---:|---:|---:|---|
| ROC AUC | **0.6654** | 0.5937 | +0.0716 | Model 1 ranks positive cases better. |
| Average precision | **0.4401** | 0.3823 | +0.0578 | Model 1 has better precision–recall ranking. |
| Precision | **0.4339** | 0.3560 | +0.0778 | Model 1 wastes fewer contacts. |
| Recall | 0.6810 | **0.7616** | −0.0805 | Model 2 finds more subscribers. |
| F1 | **0.5300** | 0.4852 | +0.0448 | Model 1 has the stronger balance of precision and recall. |
| F2 | 0.6114 | **0.6203** | −0.0089 | Model 2 has a small recall-weighted edge at these thresholds. |
| Specificity | **0.5898** | 0.3642 | +0.2256 | Model 1 identifies more non-subscribers correctly. |
| Accuracy | **0.6186** | 0.4897 | +0.1289 | Both are below the always-`no` baseline (0.6842). |
| Brier score (lower is better) | 0.2380 | **0.2229** | +0.0151 | Neither beats the constant test-prevalence baseline (~0.2161). |

The forest flagged **6,109** rows versus **4,483** for logistic regression. It found **230 additional true subscribers** (2,175 versus 1,945) but produced **1,396 additional false positives** (3,934 versus 2,538). That is approximately **6.1 extra false positives per additional true positive**. If outreach capacity or contact cost matters, Model 1 is the more practical starting point. If missing a subscriber is much more costly than extra outreach, Model 2's higher recall may justify its larger contact list. This is a decision about the cost of intervention, not proof of greater business value from either model.

## Statistical comparison and limits

The analysis script used **1,000 paired bootstrap resamples** of the same test rows (fixed random seed 42) and reported percentile 95% intervals for Model 1 minus Model 2:

| Difference | Estimate | Paired bootstrap 95% interval |
|---|---:|---:|
| ROC AUC | +0.0716 | +0.0610 to +0.0817 |
| Average precision | +0.0578 | +0.0474 to +0.0685 |
| F2 | −0.0089 | −0.0237 to +0.0056 |

Within this test segment, the ranking differences consistently favour Model 1. The F2 interval includes zero, so its small forest advantage is not clear under this resampling method. **These intervals are descriptive**, because row resampling does not account for repeated customers or later campaign periods. Training, validation and test `yes` rates were **5.04%, 11.79% and 31.58%**; the large shift means precision and average precision from different periods cannot be compared without accounting for changing prevalence. A later chronological test with customer IDs and a defined intervention budget is needed before choosing a model for deployment.

Finally, the public target is **bank term-deposit subscription**. Neither model has been validated for STADIOEquities first-deposit activation, and the public dataset cannot evaluate dormancy prediction.
