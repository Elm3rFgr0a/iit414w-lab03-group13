# Hito 2: Midpoint Model + Error Analysis

Team: Group 13 (Adrean Torres, Benjamin Pinto)

This repository contains the Hito 2 deliverables for the F1 Race Strategy Advisor capstone.

## Runbook

### 1. Environment setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### 2. Run the notebook

1. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
2. Open `hito2_modeling.ipynb`.
3. Click Run All. The notebook is designed to execute top-to-bottom.

## Data
- Dataset: `hito1/f1_strategy_race_level.csv`
- Split: train 2019-2021, calibration 2022, test 2023-2024

## Targets
- `is_top10`
- `is_top5`

## Deliverables in this repo
- `hito2_modeling.ipynb`
- `baseline_comparison.md`
- `error_analysis.md`
- `whatif_comparison.md`
- `leakage_audit.md`
- `mitigations.md`
- `PROMPTS.md`
- `pitch_skeleton.md`

## Notes on calibration
Calibration uses the 2022 season only (manual Platt scaling) to keep the test set untouched.
