# Hito 2 Baseline Comparison

This file compares baselines and models for both targets using the locked split:
train 2019-2021, calibration 2022, test 2023-2024. Split counts: train n=1132, cal n=426, test n=889.

## Targets
- is_top10 (binary)
- is_top5 (binary)

## Model definitions
- Baseline: calibrated logistic regression using grid_fallback + constructor_tier
- Full: baseline + n_stops + num_compounds (scenario inputs)
- Docent reference: calibrated model for is_top10 with Brier 0.132 on test

## Test metrics (2023-2024)

| Target | Model | Brier | ROC-AUC | Macro F1 | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| is_top10 | Docent baseline | 0.132 | n/a | n/a | External reference from course baseline |
| is_top10 | Baseline | 0.1429 | 0.8736 | 0.8007 | grid_fallback + constructor_tier |
| is_top10 | Full | 0.1443 | 0.8718 | 0.7939 | adds n_stops + num_compounds |
| is_top5 | Baseline | 0.0952 | 0.9235 | 0.8225 | grid_fallback + constructor_tier |
| is_top5 | Full | 0.0965 | 0.9207 | 0.8243 | adds n_stops + num_compounds |

## Takeaways
- The baseline slightly outperforms the full model on Brier for both targets.
- The full model is still used for scenario comparisons because it includes strategy inputs.
