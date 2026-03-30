Run RandomForestRegressor for finishing position

Instructions

1. Create and activate a Python venv (recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install requirements:

```bash
pip install pandas numpy scikit-learn requests
```

3. Run the script:

```bash
python run_rf_position.py
```

Behavior

- The script tries to download race results (2022–2024) from the ergast mirror API and caches them at `data/processed/results_2022_2024.csv`.
- If the download fails (no internet or API blocked), the script falls back to a synthetic dataset and still trains the model so you can reproduce the steps locally.
- Output: `rf_position_results.csv` in `labs/lab3/` with `train_MAE` and `test_MAE` and `data_source`.
