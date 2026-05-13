# Hito 2 Leakage and Confounding Audit

## Feature audit

| Feature | Category | Use | Notes |
| --- | --- | --- | --- |
| grid_fallback | pre-race | model | grid_position with qualifying fallback |
| constructor_tier | pre-race | model | team strength proxy |
| n_stops | scenario input | model | post-race, used only for what-if |
| num_compounds | scenario input | model | derived from compound_sequence |
| circuit_type | audit slice | error analysis only | not used in training |
| wet_laps | audit slice | error analysis only | not used in training |
| finish_position / points | target only | evaluation | never used as features |

## Leakage checks
- No post-race outcome columns are used as predictors.
- Calibration uses 2022 only; the test set is untouched until final evaluation.

## Confounding note
Strategy choice correlates with driver pace, constructor strength, and race conditions.
Scenario outputs are conditional on inputs and should not be interpreted as causal effects.
This limitation applies to both targets.
