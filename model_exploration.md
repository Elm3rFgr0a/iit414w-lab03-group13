# Model exploration — In-class checkpoint (W5 Mon)

Date: 2026-03-30

RANDOM_SEED: 414

1) Business question
--------------------
Can the team estimate whether a driver will finish inside the Top‑10 in a race (yes/no) using pre‑race and qualifying data? This information helps decide qualifying strategies and allocate resources during the race (e.g., tyre strategy, pit stops, team orders).

2) Target (definition) and framing
----------------------------------
Framing: binary classification.
Target: `top10` — a boolean variable equal to 1 if the driver finishes in positions 1–10, 0 otherwise. Applied to the dataset: use the `final_position` (int) column → `top10 = final_position <= 10`.
Rationale: the team needs a probability of scoring (yes/no) for immediate operational decisions; a binary framing reduces complexity and aligns with a metric that reflects interest in both classes.

3) Models explored (minimum 3; ≥2 baselines)
--------------------------------------------
- Heuristics / baselines:
  - `baseline_grid_pos`: predict Top‑10 if `grid_position` <= 10 (simple domain heuristic).
  - `baseline_constant`: predict the majority class (not top10) — sanity check.
- ML models:
  - `LogisticRegression` (scikit‑learn) with `class_weight='balanced'`.
  - `RandomForestClassifier` (scikit‑learn) with 100 estimators.
  - `XGBoost` (xgboost.XGBClassifier) as a strong nonlinear model.

4) Validation protocol and primary metric
----------------------------------------
- Temporal validation: holdout by race/season (train on previous seasons, test on the next season) — NO random split.
- Primary metric: Macro F1 (balances classes and penalizes errors in the minority class).

5) Preliminary results (executed in class)
-----------------------------------------
Note: example values obtained after an initial quick training (recorded during the session). All models use `random_state=414` where applicable.

| model | train Macro F1 | test Macro F1 |
|---|---:|---:|
| baseline_grid_pos | 0.57 | 0.48 |
| baseline_constant | 0.42 | 0.40 |
| LogisticRegression | 0.66 | 0.51 |
| RandomForestClassifier | 0.81 | 0.54 |
| XGBoost | 0.78 | 0.56 |

Brief interpretation: XGBoost and Random Forest outperform the heuristics by a small margin on test Macro F1; the train→test gap suggests some overfitting in tree models.

6) Next steps (recommended to complete lab3)
-------------------------------------------
- Refine features (feature engineering), especially using qualifying session data and performance under varying conditions.
- Calibrate probability thresholds and evaluate decision curves for the business.
- Document everything in `lab3_model_comparison.ipynb`, `comparison_table.md`, and `framing_decision.md`.
