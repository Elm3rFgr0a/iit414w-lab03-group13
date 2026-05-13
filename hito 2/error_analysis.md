# Hito 2 Error Analysis

All slices below are computed on the 2023-2024 test set using the calibrated full model
(includes scenario features). Weather slice uses wet_laps > 0 as wet.

## is_top10

### Strategy type
| strategy_type | n | brier | f1_macro |
| --- | ---: | ---: | ---: |
| no_stop | 15 | 0.174 | 0.423 |
| one_stop | 353 | 0.156 | 0.759 |
| three_plus_stop | 153 | 0.158 | 0.766 |
| two_stop | 368 | 0.126 | 0.836 |

### Circuit type
| circuit_type | n | brier | f1_macro |
| --- | ---: | ---: | ---: |
| permanent | 579 | 0.137 | 0.803 |
| semi-street | 118 | 0.185 | 0.729 |
| street | 192 | 0.140 | 0.807 |

### Weather (wet_laps > 0)
| weather_slice | n | brier | f1_macro |
| --- | ---: | ---: | ---: |
| dry | 768 | 0.145 | 0.790 |
| wet | 121 | 0.142 | 0.818 |

## is_top5

### Strategy type
| strategy_type | n | brier | f1_macro |
| --- | ---: | ---: | ---: |
| no_stop | 15 | 0.055 | 0.483 |
| one_stop | 353 | 0.102 | 0.828 |
| three_plus_stop | 153 | 0.100 | 0.777 |
| two_stop | 368 | 0.091 | 0.835 |

### Circuit type
| circuit_type | n | brier | f1_macro |
| --- | ---: | ---: | ---: |
| permanent | 579 | 0.097 | 0.821 |
| semi-street | 118 | 0.087 | 0.873 |
| street | 192 | 0.101 | 0.806 |

### Weather (wet_laps > 0)
| weather_slice | n | brier | f1_macro |
| --- | ---: | ---: | ---: |
| dry | 768 | 0.094 | 0.828 |
| wet | 121 | 0.114 | 0.796 |

## Failure-mode hypotheses
- Semi-street circuits show the highest is_top10 Brier (0.185), likely due to higher variance
  from barriers, safety cars, and track evolution that are not captured by pre-race signals.
- Wet races degrade is_top5 calibration (Brier 0.114 vs 0.094 in dry), reflecting volatility
  from changing grip and incident risk.
- no_stop strategies have very small sample size (n=15) and unstable F1, so predictions
  should be treated as low confidence.

## Implications for decisions
- For semi-street races, avoid high-confidence top10 recommendations without additional
  context checks and consider wider uncertainty bands.
- For wet races, treat top5 probabilities as stress-test outputs rather than action triggers.
- When strategy_type is no_stop, defer to human judgment or merge with one_stop for decisions.
