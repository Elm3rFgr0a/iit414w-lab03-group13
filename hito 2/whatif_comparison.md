# Hito 2 What-If Comparison

## Scenario setup
Race: Bahrain Grand Prix 2023
Driver: Perez (driver_id = perez)
Pre-race inputs: grid_fallback = 2, constructor_tier = front

Scenario A (conservative): n_stops = 1, num_compounds = 2 (M-H style)
Scenario B (aggressive): n_stops = 2, num_compounds = 3 (S-M-H style)

## Predictions (calibrated full model)

| Target | Scenario A | Scenario B | Diff (B - A) |
| --- | ---: | ---: | ---: |
| is_top10 | 0.906 | 0.929 | +0.023 |
| is_top5 | 0.864 | 0.911 | +0.047 |

## Decision implication
- is_top10 alone suggests both strategies are safe (difference about 2.3 pp).
- is_top5 shows higher upside for the two-stop plan (about 4.7 pp), so if the objective is
  a top5 finish, Scenario B is preferred.
- Outputs are scenario-conditioned probabilities, not causal effects of strategy choice.
