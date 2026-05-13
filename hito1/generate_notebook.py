import json

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split('\n')]
    }

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split('\n')]
    }

cells = []

# Cell 0
cells.append(create_markdown_cell("# Capstone Hito 1: F1 Race Strategy Baseline\nGroup 13: Adrean Torres, Benjamín Pinto"))
cells.append(create_code_cell("""import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, f1_score
from sklearn.calibration import calibration_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('f1_strategy_race_level.csv')
print(f"Loaded dataset with {len(df)} records.")"""))

# Cell 1
cells.append(create_markdown_cell("## 1. Temporal Split\nTrain: 2019–2021 | Calibration: 2022 | Test: 2023–2024"))
cells.append(create_code_cell("""# Define splits based on season
train_mask = df['season'].isin([2019, 2020, 2021])
calib_mask = df['season'] == 2022
test_mask = df['season'].isin([2023, 2024])

train_df = df[train_mask].copy()
calib_df = df[calib_mask].copy()
test_df = df[test_mask].copy()

# Verify no test rows in train
assert not train_df['season'].isin([2023, 2024]).any(), "Test data leaked into train!"

print(f"Train rows: {len(train_df)}")
print(f"Calibration rows: {len(calib_df)}")
print(f"Test rows: {len(test_df)}")"""))

# Cell 2
cells.append(create_markdown_cell("""## 2. Leakage Audit

| Feature | Category | Notes |
|---------|----------|-------|
| `qualifying_position` | **Pre-race available (with limits)** | *Limitation Proxy*: Explicitly used as a proxy for the actual `grid_position`. We acknowledge this ignores pre-race penalties. |
| `constructor_tier` | **Pre-race available** | Known based on team pace context heading into the race weekend. |
| `n_stops` | **Scenario Input (Post-race observed)** | Post-race observation. Only permitted for what-if scenario testing. Not a true pre-race feature. |
| `compound_sequence` | **Scenario Input (Post-race observed)** | Same as above, used specifically for scenario generation. |

*Note*: Incident features (`safety_car_periods`, `weather_actual`) are not used in these pre-race modeling pipelines to avoid target leakage."""))

# Cell 3
cells.append(create_markdown_cell("## 3. Baseline Model (2 features)\nFeatures: `qualifying_position`, `constructor_tier`\nTarget: `is_top10`"))
cells.append(create_code_cell("""from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator

features_baseline = ['qualifying_position', 'constructor_tier']
target = 'is_top10'

# Preprocessing
preprocessor_baseline = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['qualifying_position']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['constructor_tier'])
    ])

# Base Model
base_lr = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)

# Pipeline
baseline_pipe = Pipeline(steps=[('preprocessor', preprocessor_baseline),
                                ('classifier', base_lr)])

# Train on 2019-2021
baseline_pipe.fit(train_df[features_baseline], train_df[target])

# Platt Scaling on 2022 Calibration Set
calibrated_baseline = CalibratedClassifierCV(estimator=FrozenEstimator(baseline_pipe), method='sigmoid')
calibrated_baseline.fit(calib_df[features_baseline], calib_df[target])

# Evaluate on Test (2023-2024)
X_test_base = test_df[features_baseline]
y_test = test_df[target]

preds_prob_base = calibrated_baseline.predict_proba(X_test_base)[:, 1]
preds_class_base = calibrated_baseline.predict(X_test_base)

brier_base = brier_score_loss(y_test, preds_prob_base)
ll_base = log_loss(y_test, preds_prob_base)
macro_f1_base = f1_score(y_test, preds_class_base, average='macro')

print(f"--- Baseline Performance on Test ---")
print(f"Brier Score: {brier_base:.4f} (Docent calibrated reference: 0.132, Docent grid-rule reference: 0.208)")
print(f"Log Loss: {ll_base:.4f}")
print(f"Macro F1: {macro_f1_base:.4f}")

# Calibration Curve
prob_true_base, prob_pred_base = calibration_curve(y_test, preds_prob_base, n_bins=10)
plt.plot(prob_pred_base, prob_true_base, marker='o', label='Baseline')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfect Calibration')
plt.xlabel('Mean Predicted Probability')
plt.ylabel('Fraction of Positives')
plt.title('Calibration Curve - Baseline')
plt.legend()
plt.show()"""))

# Cell 4
cells.append(create_markdown_cell("## 4. Experiment 1 (3 features)\nFeatures: `qualifying_position`, `constructor_tier`, `n_stops`"))
cells.append(create_code_cell("""features_exp1 = ['qualifying_position', 'constructor_tier', 'n_stops']

preprocessor_exp1 = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['qualifying_position', 'n_stops']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['constructor_tier'])
    ])

exp1_pipe = Pipeline(steps=[('preprocessor', preprocessor_exp1),
                            ('classifier', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))])

exp1_pipe.fit(train_df[features_exp1], train_df[target])

calibrated_exp1 = CalibratedClassifierCV(estimator=FrozenEstimator(exp1_pipe), method='sigmoid')
calibrated_exp1.fit(calib_df[features_exp1], calib_df[target])

X_test_exp1 = test_df[features_exp1]
preds_prob_exp1 = calibrated_exp1.predict_proba(X_test_exp1)[:, 1]
preds_class_exp1 = calibrated_exp1.predict(X_test_exp1)

brier_exp1 = brier_score_loss(y_test, preds_prob_exp1)
macro_f1_exp1 = f1_score(y_test, preds_class_exp1, average='macro')

print(f"--- Experiment 1 Performance on Test ---")
print(f"Brier Score: {brier_exp1:.4f}")
print(f"Macro F1: {macro_f1_exp1:.4f}")
print(f"Difference vs Baseline Brier: {brier_exp1 - brier_base:.4f}")"""))

# Cell 5
cells.append(create_markdown_cell("## 5. Experiment 2 (4 features)\nFeatures: `qualifying_position`, `constructor_tier`, `n_stops`, `compound_sequence`\nEncoding compound_sequence as number of distinct compounds used."))
cells.append(create_code_cell("""# Feature engineering: encode compound_sequence as distinct count
def count_unique_compounds(seq):
    if pd.isna(seq):
        return 1 # Fallback to 1 compound if missing
    return len(set(seq.split('-')))

train_df['num_compounds'] = train_df['compound_sequence'].apply(count_unique_compounds)
calib_df['num_compounds'] = calib_df['compound_sequence'].apply(count_unique_compounds)
test_df['num_compounds'] = test_df['compound_sequence'].apply(count_unique_compounds)

features_exp2 = ['qualifying_position', 'constructor_tier', 'n_stops', 'num_compounds']

preprocessor_exp2 = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['qualifying_position', 'n_stops', 'num_compounds']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['constructor_tier'])
    ])

exp2_pipe = Pipeline(steps=[('preprocessor', preprocessor_exp2),
                            ('classifier', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000))])

exp2_pipe.fit(train_df[features_exp2], train_df[target])

calibrated_exp2 = CalibratedClassifierCV(estimator=FrozenEstimator(exp2_pipe), method='sigmoid')
calibrated_exp2.fit(calib_df[features_exp2], calib_df[target])

X_test_exp2 = test_df[features_exp2]
preds_prob_exp2 = calibrated_exp2.predict_proba(X_test_exp2)[:, 1]
preds_class_exp2 = calibrated_exp2.predict(X_test_exp2)

brier_exp2 = brier_score_loss(y_test, preds_prob_exp2)
macro_f1_exp2 = f1_score(y_test, preds_class_exp2, average='macro')

print(f"--- Experiment 2 Performance on Test ---")
print(f"Brier Score: {brier_exp2:.4f}")
print(f"Macro F1: {macro_f1_exp2:.4f}")
print(f"Difference vs Baseline Brier: {brier_exp2 - brier_base:.4f}")"""))

# Cell 6
cells.append(create_markdown_cell("""## 6. What-If Scenarios
Using **Experiment 2 (4 features)** because it incorporates both `n_stops` and `compound_sequence` (as `num_compounds`).
- **Scenario A**: qualifying_position=4, constructor_tier='front', n_stops=1, num_compounds=2 (M-H)
- **Scenario B**: qualifying_position=4, constructor_tier='front', n_stops=2, num_compounds=3 (S-M-H)"""))
cells.append(create_code_cell("""from sklearn.utils import resample

# Base scenario definitions
scenario_A = pd.DataFrame([{
    'qualifying_position': 4.0,
    'constructor_tier': 'front',
    'n_stops': 1,
    'num_compounds': 2
}])

scenario_B = pd.DataFrame([{
    'qualifying_position': 4.0,
    'constructor_tier': 'front',
    'n_stops': 2,
    'num_compounds': 3
}])

# Point estimate using the calibrated model fitted on full calib set
prob_A_point = calibrated_exp2.predict_proba(scenario_A)[0, 1]
prob_B_point = calibrated_exp2.predict_proba(scenario_B)[0, 1]
diff_point = prob_A_point - prob_B_point

print(f"Point Estimates:")
print(f"P(is_top10 | Scenario A, 1-stop M-H): {prob_A_point:.4f}")
print(f"P(is_top10 | Scenario B, 2-stop S-M-H): {prob_B_point:.4f}")
print(f"Difference (A - B): {diff_point:.4f}\\n")

# Bootstrap 90% CI
n_bootstraps = 1000
diffs = []

print("Running bootstrap resamples...")
for i in range(n_bootstraps):
    # Resample training data
    boot_train = resample(train_df, random_state=i)
    
    # Fit pipeline
    boot_pipe = Pipeline(steps=[('preprocessor', preprocessor_exp2),
                                ('classifier', LogisticRegression(class_weight='balanced', random_state=i, max_iter=1000))])
    boot_pipe.fit(boot_train[features_exp2], boot_train[target])
    
    # Calibrate on the SAME calib set
    boot_calib = CalibratedClassifierCV(estimator=FrozenEstimator(boot_pipe), method='sigmoid')
    boot_calib.fit(calib_df[features_exp2], calib_df[target])
    
    # Predict scenarios
    pA = boot_calib.predict_proba(scenario_A)[0, 1]
    pB = boot_calib.predict_proba(scenario_B)[0, 1]
    
    diffs.append(pA - pB)

# Calculate 90% CI
ci_lower = np.percentile(diffs, 5)
ci_upper = np.percentile(diffs, 95)

print(f"Bootstrap 90% CI for Difference in P(is_top10): [{ci_lower:.4f}, {ci_upper:.4f}]")
if ci_lower <= 0 <= ci_upper:
    print("Conclusion: Confidence intervals overlap zero, the advantage is NOT statistically significant.")
else:
    print("Conclusion: The advantage IS statistically significant at 90% confidence level.")"""))

# Cell 7
cells.append(create_markdown_cell("""## 7. Fallback Conclusion

```python
if brier_base < 0.132:
    print("Supera al modelo del docente. Listo para informar decisiones en pit wall.")
elif brier_base < 0.208:
    print("Supera al grid-rule baseline, pero no al docente. Usar con precaución o como explorador pre-carrera.")
else:
    print("Brier ≥ 0.208. El modelo NO se recomienda para decisiones en tiempo real en el pit wall. Se debe restringir su uso exclusivamente a simulaciones exploratorias pre-carrera (What-If), ya que no es suficientemente robusto.")
```"""))
cells.append(create_code_cell("""if brier_base < 0.132:
    conclusion = "Supera al modelo del docente. Listo para informar decisiones en pit wall."
elif brier_base < 0.208:
    conclusion = "Supera al grid-rule baseline, pero no al docente. Usar con precaución o como explorador pre-carrera."
else:
    conclusion = "Brier ≥ 0.208. El modelo NO se recomienda para decisiones en tiempo real en el pit wall. Se debe restringir su uso exclusivamente a simulaciones exploratorias pre-carrera (What-If), ya que no es suficientemente robusto."

print("Fallback Conclusion Evaluation:")
print(conclusion)"""))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('hito1_baseline.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print("Notebook generated successfully.")
