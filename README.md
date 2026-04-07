# ml-cadd: Drug Solubility Prediction

A machine learning model that predicts the aqueous solubility (logS) of drug molecules from SMILES strings, trained on the [ESOL (Delaney) dataset](https://pubs.acs.org/doi/10.1021/ci034243x).

## Requirements

- Python 3.10+
- RDKit, scikit-learn, pandas, numpy, matplotlib, seaborn, requests

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### 1. Train the model

Downloads the ESOL dataset automatically and trains a Random Forest model.

```bash
python main.py train
```

Output:
```
Dataset size: 1128 molecules
Featurizing molecules...
Valid molecules: 1128 / 1128
Training Random Forest...

=== Results ===
Train RMSE: 0.273  R²: 0.983
Test  RMSE: 0.773  R²: 0.873  MAE: 0.531

Model saved to data/model.pkl
Parity plot saved to data/parity_plot.png
```

### 2. Predict solubility

Predict for a single SMILES:

```bash
python main.py predict "CCO"
```

Predict for multiple SMILES at once:

```bash
python main.py predict "CCO" "c1ccccc1" "CC(=O)Oc1ccccc1C(=O)O"
```

Example output:

```
SMILES                                       logS   Solubility  Category
--------------------------------------------------------------------------------
CCO                                         0.804     6.37e+00  highly soluble
c1ccccc1                                   -1.704     1.98e-02  soluble
CC(=O)Oc1ccccc1C(=O)O                      -2.291     5.12e-03  soluble
```

### 3. Use as a Python library

```python
from src.predict import predict

# Single molecule
result = predict("CCO")
print(result)
# {'smiles': 'CCO', 'logS': 0.804, 'solubility_mol_L': '6.37e+00', 'category': 'highly soluble', 'error': None}

# Multiple molecules
results = predict(["CCO", "c1ccccc1", "CC(=O)Oc1ccccc1C(=O)O"])
for r in results:
    print(r["smiles"], r["logS"], r["category"])
```

## Output fields

| Field | Description |
|-------|-------------|
| `logS` | Predicted log₁₀ molar solubility (mol/L) |
| `solubility_mol_L` | Solubility in mol/L (scientific notation) |
| `category` | Human-readable solubility class (see table below) |
| `error` | Error message if the SMILES is invalid, otherwise `null` |

**Solubility categories:**

| Category | logS range |
|----------|-----------|
| Highly soluble | logS > −1 |
| Soluble | −3 < logS ≤ −1 |
| Moderately soluble | −5 < logS ≤ −3 |
| Poorly soluble | logS ≤ −5 |

## How it works

1. **Featurization** (`src/features.py`): Each SMILES is converted to a 1034-dimensional feature vector combining:
   - 10 physicochemical descriptors (MW, LogP, HBD, HBA, TPSA, rotatable bonds, ring count, aromatic rings, Fsp³, heavy atom count)
   - 1024-bit ECFP4 Morgan fingerprints

2. **Model** (`src/train.py`): A Random Forest regressor (200 trees) trained on the ESOL dataset with an 80/20 train/test split.

3. **Prediction** (`src/predict.py`): Loads the saved model and returns logS predictions for new SMILES.

## Project structure

```
ml-cadd/
├── data/
│   ├── esol.csv          # downloaded automatically on first train
│   ├── model.pkl         # saved model (created after training)
│   └── parity_plot.png   # test set parity plot (created after training)
├── src/
│   ├── features.py       # SMILES → feature vectors
│   ├── train.py          # model training and evaluation
│   └── predict.py        # inference on new molecules
├── main.py               # CLI entry point
└── requirements.txt
```

## Model performance

Evaluated on a held-out 20% test set of the ESOL dataset (1128 molecules total):

| Metric | Value |
|--------|-------|
| Test RMSE | 0.773 logS units |
| Test R² | 0.873 |
| Test MAE | 0.531 logS units |
