# AI Interaction Log - Hito 2

## 1. Manual Platt scaling for fixed calibration set

- Context: We needed calibrated probabilities using the locked 2022 calibration set, but the
  current scikit-learn version did not accept cv='prefit' for CalibratedClassifierCV.
- Prompt: "How can we calibrate a prefit model using a fixed holdout set (2022) without
  leaking test data?"
- Output: Use manual Platt scaling by fitting a logistic regression on the base model decision
  scores from the calibration set and then applying that mapping to the test set.
- Validation: Verified that only 2022 data was used for the calibration fit and that test data
  was never used during fitting.
- Adaptations: Implemented a small helper that uses decision_function scores with a very large
  C value to mimic near-unregularized Platt scaling.
- Final Decision: Use manual Platt scaling on the 2022 calibration split for both targets.

## 2. Error analysis slices and what-if scenario design

- Context: The rubric requires error analysis by strategy type, circuit type, and one additional
  context, plus a what-if comparison that reveals a trade-off between targets.
- Prompt: "Propose the required slices and a what-if setup that can show disagreement between
  is_top10 and is_top5 in a realistic race scenario."
- Output: Slice by strategy_type, circuit_type, and weather (wet vs dry); compare a 1-stop
  vs 2-stop plan with fixed pre-race inputs and use both targets to show differing upsides.
- Validation: Ran the notebook to compute slice tables and a Bahrain 2023 example with
  a front-tier car; confirmed that is_top5 differences are larger than is_top10.
- Adaptations: Used wet_laps > 0 to define wet races and anchored the scenario on an actual
  test-set row to keep inputs realistic.
- Final Decision: Include the three slices in error_analysis.md and the Bahrain 2023 scenario
  in whatif_comparison.md, with a clear non-causal disclaimer.
