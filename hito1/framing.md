# Team Decision Sheet — Capstone Hito 1

### IIT414W · F1 Race Strategy Advisor · Mon May 4, 2026

**Team name:** Group 13
**Team members:** Adrean Torres, Benjamín Pinto
**GitHub repo URL:** https://github.com/Elm3rFgr0a/iit414w-lab03-group13.git

---

## 1. Decision Context

**What strategy decision is this tool supporting?**

> Whether to adopt a protective (conservative) vs aggressive pit-stop and tyre strategy for a driver on race day, based on the estimated probability that they will finish inside the top 10 and score points.

**Who makes this decision?**

> The head of strategy on the pit wall, during the race-day briefing before the formation lap.

**When in the race weekend is the decision made?**

> Race morning, after qualifying results are locked and grid positions are confirmed, before the formation lap begins.

---

## 2. Target & Metric

**Target (LOCKED for Hito 1):** `is_top10`

**Primary metric:** Brier Score (calibrated probability)

**Why this metric for this decision?** (2 sentences max)

> The strategy desk needs a calibrated probability — not just a classification — because whether to deploy a conservative or aggressive tyre strategy depends on *how confident* the model is, not just on which side of 0.5 it falls. Brier Score directly penalizes overconfident or underconfident probability estimates, which makes it the right metric for a decision that costs real pit-stop time if it is wrong.

**Secondary metric (optional but recommended):** Macro F1, ROC-AUC

**Temporal split (LOCKED for Hito 1):**

- Train: seasons 2019, 2020, 2021
- Calibration: season 2022 (used to fit calibration mapping; never for model selection)
- Test: seasons 2023, 2024 (untouched until final evaluation)

---

## 3. Baseline Plan

**Baseline approach (one sentence):**

> Calibrated logistic regression using `grid_position` when available (fallback to `qualifying_position`) plus `constructor_tier`, with Platt scaling fitted on the 2022 calibration set — the same feature set validated in Lab 3 where this model achieved Macro F1 = 0.76 on the 2023 test season.

**Why is this baseline F1-defendable?** (One sentence)

> Grid position and constructor tier are known before the race starts, require no post-race data, and reflect the two dominant physical factors in F1 point-scoring: clean-air pace from qualifying and overtaking capacity from car performance — both justifiable from domain knowledge without inspecting the 2023–2024 test data. Note: The baseline feature choice is strictly justified by this F1 domain logic; the Lab 3 test performance is only cited as a retrospective reference, not as the primary reason for selection.

**Direction check:** Higher predicted score means higher P(is_top10). No — lower `grid_position` values (e.g., 1 vs 12) correspond to higher P(is_top10); the model encodes a negative coefficient on `grid_position`, meaning position 1 yields the highest probability and position 20 the lowest.

**Observed baseline performance vs docent floor (test 2023–2024):**

- Grid-rule docent baseline: Brier = 0.208 on test
- Calibrated docent model: Brier = 0.132 on test, ROC-AUC = 0.892
- Our team's baseline achieved: Brier = **0.1431**, ROC-AUC = **0.8736**, Macro F1 = **0.8007**

---

## 4. What-If Comparison Plan

**Strategy variables we will vary:**

- [X] `n_stops`
- [X] `compound_sequence`
- [ ] `stint_lengths`
- [ ] `avg_pit_stop_duration_s`
- [ ] Other: ____________________

**Concrete scenarios to compare:**

> **Scenario A (conservative, 1-stop):** grid_position=4 (fallback to qualifying_position if missing), constructor_tier=1 (Red Bull-class), Circuit: Bahrain 2023, n_stops=1, compound_sequence=M-H, stint lengths ~28/29 laps.
>
> **Scenario B (aggressive, 2-stop):** Same driver and circuit, n_stops=2, compound_sequence=S-M-H, stint lengths ~14/20/22 laps.

**Decision metric for the comparison:**

> Difference in calibrated scenario-conditioned P(is_top10) between Scenario A and Scenario B, with bootstrap 90% confidence interval over 1,000 resamples of the 2019–2021 training set. These are **scenario-conditioned estimates**, not causal effects.

**Scenario protocol (explicit for Hito 2):**

1. Fix pre-race inputs first (use `grid_position` when available; otherwise fall back to `qualifying_position`).
2. Set user-controlled strategy inputs (`n_stops`, `compound_sequence`) explicitly.
3. Report outputs as scenario-conditioned probabilities $P(is\_top10 \mid \text{inputs})$.

---

## 5. Limitations Acknowledgment

**Limitation #1 we acknowledge:** Strategy features (`n_stops`, `compound_sequence`) are post-race observations, not pre-race decisions.

> Why it matters for our approach: In our what-if scenarios we input hypothetical future values for features the model learned from observed race outcomes — the model cannot distinguish a planned strategy from one forced by a safety car or tyre failure, so our P(is_top10) estimates for Scenario B may be contaminated by cases where 2-stop races went wrong for reasons unrelated to the strategy choice.

**Limitation #2 we acknowledge:** Strategy choice is confounded with car performance, driver skill, and weather.

> Why it matters for our approach: In Lab 3, `constructor_tier` and `qualifying_position` dominated predictions, meaning a top-grid starter's 1-stop result in the training data reflects both a good strategy and a fast car; the model cannot isolate the independent effect of `n_stops`, which inflates the predicted advantage of conservative strategies for strong constructors.

**Limitation #3 we acknowledge:** `qualifying_position` is a proxy when `grid_position` is missing.

> Why it matters for our approach: Because our decision context is pre-formation lap, the actual starting grid position is what matters. We use `grid_position` when available and fall back to `qualifying_position` otherwise, but any missing grid data can still inject error when penalties or grid drops occur.

---

## 6. Experiment Results for Hito 1

**Experiments run (test 2023–2024):**

1. Logistic regression (grid_position when available, fallback to qualifying_position + constructor_tier + n_stops): Brier = **0.1436**, ROC-AUC = **0.8728**, Macro F1 = **0.7950**.
2. Add `compound_sequence` (encoded as number of distinct compounds used): Brier = **0.1442**, ROC-AUC = **0.8721**, Macro F1 = **0.7973**.
3. Scenario A vs Scenario B (using Experiment 2): P(A) = **0.8660**, P(B) = **0.8931**, difference = **-0.0271**, 90% CI = **[-0.0558, 0.0024]** (not statistically significant).

**Fallback Conclusion:**

> If the Brier score on the test set is $\ge 0.208$, we conclude the model is unfit to inform live, time-critical pit wall decisions. In such a scenario, the model would only be kept as a pre-race explorative tool for broader what-if scenario testing, and we will state that a simple 2-feature logistic regression is insufficiently robust to replace baseline heuristics.

---

## 7. Team Workflow

**Who is doing what between now and Wednesday?**

| Member     | Owns                                                                                           | Branch / file in repo            |
| ---------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| Adrean Torres | Dataset load + temporal split, Experiment 1 (baseline logistic regression + Platt calibration) | `feature/baseline-calibration` |
| Benjamín Pinto | Experiment 2 (compound feature), Experiment 3 (what-if + bootstrap CI), framing.md updates     | `feature/whatif-scenarios`     |

**When does each member commit by?**

> Tuesday EOD: Experiment 1 notebook committed with Brier Score on test set. Wednesday 14:00: Experiments 2 and 3 committed. Wednesday 15:40: framing.md final version + Section 8 filled after pair review.

---

## 8. Critique Received in Pair Review

> *Filled during Block 5 (15:45–16:05) after the partner team reviews this sheet.*

**Reviewing team:** ____________________

**Concrete critique we received:**

> [completar durante el pair review a las 15:45]

**How we will address this critique by Wednesday:**

> [completar durante el pair review a las 15:45]

---

## Self-Check Before Committing

Before you push this to GitHub, verify:

- [X] Decision context is one sentence, not a paragraph
- [X] Target says exactly `is_top10`
- [X] Temporal split shows three blocks: 2019–2021 / 2022 / 2023–2024
- [X] Baseline is described in code-realistic terms (we could implement it)
- [X] What-if scenarios have specific feature values, not generic words
- [X] At least 2 of the 5 limitations are acknowledged with consequence
- [ ] PROMPTS.md exists in the repo (ya presente desde Lab 3 — verificar que esté poblado antes del miércoles)
