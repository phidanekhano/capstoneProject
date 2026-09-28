# STADIOEquities modelling prototype

The UCI Bank Marketing `bank-full.csv` dataset supports a public **term-deposit subscription** experiment as an analogue for STADIOEquities' proposed first-deposit model. It does not contain the records needed to train a dormancy model. See the [project description](STADIOEquities_Part_B_Model_Description.md).

## Project layout

| Area | Files |
|---|---|
| Shared data preparation | [`data_preparation.py`](data_preparation.py), [Preprocessing.MD](Preprocessing.MD) |
| Shared engineered features | [`data_preparation.py`](data_preparation.py), [FeatureEngineering.MD](FeatureEngineering.MD) |
| Model 1: logistic regression | [`Model1/model1.py`](Model1/model1.py), [`Model1/Model1.ipynb`](Model1/Model1.ipynb), [Model1.MD](Model1/Model1.MD) |
| Model 2: random forest | [`Model2/model2.py`](Model2/model2.py), [`Model2/Model2.ipynb`](Model2/Model2.ipynb), [Model2.MD](Model2/Model2.MD) |
| Dependencies | [requirements.txt](requirements.txt) |

## Install and train

Run commands **from the project root**. Use Python 3.10+ and install the required packages:

```bash
python -m pip install -r requirements.txt
```

Download `bank-full.csv` from the [UCI Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing). The download contains `bank.zip`, which contains the semicolon-separated CSV. Then run either or both models independently:

```bash
python -m Model1.model1 --data bank-full.csv
python -m Model2.model2 --data bank-full.csv
```

Model 1 writes only to `results/model1/`, and Model 2 writes only to `results/model2/`. Each output directory contains `model.joblib`, `metrics.json` and `test_predictions.csv`. Omit `--data` to try downloading the official UCI archive automatically. The two notebooks provide separate interactive runs; place the CSV at the project root or edit `DATA_PATH` in the notebook.

## Score new rows

After training, provide a semicolon-separated CSV with the same UCI predictor columns. `duration` and `y` can be omitted:

```bash
python -m Model1.model1 --predict new_customers.csv
python -m Model2.model2 --predict new_customers.csv
```

Each command writes `new_predictions.csv` to its own results folder. These scores predict the public bank outcome; they are not STADIOEquities activation or dormancy probabilities.
