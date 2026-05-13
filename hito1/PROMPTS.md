# AI Interaction Log - Capstone Hito 1

## 1. What-If Scenarios Using the Wrong Model (Rejected Suggestion)
* **Context**: We needed to implement the What-If scenarios in Cell 6. The instructions asked to compare Scenario A (1 stop, M-H) with Scenario B (2 stops, S-M-H).
* **Prompt**: "Write the code for Cell 6 to run the What-If scenarios comparing Scenario A and Scenario B. Use the model with the best Brier score from Experiments 1 and 2."
* **Output**: The AI suggested using the model from Experiment 1 (which only included `qualifying_position`, `constructor_tier`, and `n_stops`) because it assumed that the simplest model with the lowest Brier score should be preferred. It generated the code to compare both scenarios using the `exp1_pipe`.
* **Validation**: When we reviewed the logic, we realized that changing the `compound_sequence` from "M-H" to "S-M-H" had absolutely no effect on the predicted probabilities because Experiment 1 does not use that feature.
* **Adaptations**: We rejected the AI's logic to "use the best model" based purely on metrics. We overrode the suggestion and explicitly instructed the code to use the Experiment 2 model (which includes `num_compounds`) because without it, the What-If scenario variable for tyre compounds is completely ignored, rendering the comparison useless.
* **Final Decision**: We implemented the What-If scenarios exclusively using the 4-feature model from Experiment 2, prioritizing domain logic and scenario validity over marginal Brier score differences.

## 2. Encoding the Compound Sequence Feature
* **Context**: The `compound_sequence` feature comes as strings like "S-M", "M-H", or "S-M-H". We needed to encode this for our Logistic Regression model in Experiment 2.
* **Prompt**: "How should I encode the `compound_sequence` string (e.g., 'S-M-H') as a feature for a logistic regression model in Scikit-Learn? Should I use One-Hot Encoding?"
* **Output**: The AI suggested that using One-Hot Encoding on the exact sequences would result in very high dimensionality and sparse features because "S-M-H" and "M-H-S" would be treated entirely differently. It recommended a simpler heuristic: count the number of distinct compounds used (e.g., "S-M-H" -> 3 distinct compounds) and treat it as a numerical feature.
* **Validation**: We validated this by checking the F1 domain logic: the number of distinct compounds captures the essence of degradation strategy and regulatory requirements without exploding the feature space.
* **Adaptations**: We implemented a custom Pandas `.apply()` function to compute `len(set(seq.split('-')))` with a fallback to `1` for missing values, exactly as the AI suggested.
* **Final Decision**: We used the distinct compound count as our `num_compounds` feature for Experiment 2.
