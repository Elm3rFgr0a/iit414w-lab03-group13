# Final Model Comparison Table

| Model | Train Macro F1 | Test Macro F1 | WHY (Mechanistic Reasoning & Behavior) |
|---|---|---|---|
| Baseline 1 - Majority Class | 0.33 | 0.33 | Merely outputs 0 (no points) blindly; test score reflects severe class imbalance penalty. No actual learning. |
| Baseline 2 - Grid Heuristic (<=10) | 0.77 | 0.76 | Extremely robust baseline. Since overtaking is hard, grid position heavily maps to points regardless of year. No overfitting (train ≈ test). |
| Logistic Regression | 0.81 | 0.79 | Effectively weighted the grid starting position while assigning 'boosts' to historical top constructors like Red Bull/Mercedes. |
| Random Forest | 0.88 | 0.78 | Slight overfitting is visible (train F1 > test F1). Deep trees might rely on short-term 2022 patterns that fail to generalize fully into 2023 grid shifts. |
