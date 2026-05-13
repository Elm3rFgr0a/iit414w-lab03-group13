# Hito 2 Risks and Mitigations

- Risk: Strategy confounding (n_stops and num_compounds reflect incidents or pace rather than choice).
  Mitigation: report scenario-conditioned probabilities; in future, add driver/constructor fixed effects
  or causal designs (instrumental variables, safety car controls).
- Risk: Semi-street circuits show higher error for is_top10.
  Mitigation: add circuit-specific features and calibrate per circuit_type.
- Risk: Wet races degrade is_top5 calibration.
  Mitigation: train a weather-aware calibration layer or separate wet-model.
- Risk: no_stop sample is tiny, leading to unstable metrics.
  Mitigation: treat as out-of-scope for decisions or merge with one_stop.
- Risk: Dataset starts in 2019 only; regulation shifts can break patterns.
  Mitigation: retrain each season and monitor calibration drift.
