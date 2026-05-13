# Technical Memo: Race Day Points Predictor

**To:** Head of Strategy, Formula 1 Team
**From:** Data Analytics Unit
**Date:** May 13, 2026
**Subject:** Model Deployment for Point-Scoring Probability (Binary Classification)

### What can this model do for us?
We developed a predictive system to answer a critical race-day question: *Will our driver score points today based on their grid position (or qualifying position when grid is missing) and our car's historical strength?* By framing this as a calibrated probability (not just a "Yes/No" prediction), we can better align our pit-stop and tire preservation strategies. If the system confidently predicts we will be in the points, we can adopt a protective strategy; if not, we can afford aggressive alternative strategies to roll the dice.

### The Results
When testing our system against the unseen 2023–2024 seasons, our recommended model (calibrated Logistic Regression) separates point-scoring finishes from non-scoring ones with high reliability, achieving **Macro F1 = 0.8007**, **ROC-AUC = 0.8736**, and **Brier = 0.1431**. We report ROC-AUC to summarize discrimination alongside calibration metrics.

To put this into context, a simple grid rule of thumb the paddock often uses ("if we start in the top 10, we usually finish in the top 10") underperforms on calibration (docent grid baseline Brier = 0.208). Our system beats this established heuristic by mathematically factoring in our car's underlying pace advantage and historical team form. This means it correctly spots when a fast car starting 12th will carve through the field to score, or when a slow car starting 9th will fall backward.

### Confidence and Risks
You should be confident in deploying this primary model because its performance is stable. Unlike heavier, more complex artificial intelligence we tested (such as the Random Forest, which achieved a **75.9%** score but showed early signs of simply memorizing the 2022 season instead of learning real racing rules), our simple model focuses on the fundamental laws of F1: grid position dictates clean air pace, and constructor strength dictates overtaking ability over the course of 300+ kilometers.

For what-if strategy comparisons, we allow user-set inputs like `n_stops` and `compound_sequence`. These outputs are **scenario-conditioned estimates** $P(\text{points} \mid \text{inputs})$, not causal effects of strategy choice. In our two example scenarios, the model estimates 0.866 vs 0.893 for Scenario A vs B (difference -0.027), with a 90% bootstrap CI of [-0.0558, 0.0024], so the scenario difference is not statistically significant.

**Limitations & Risks:**
1. **Unpredictable Events:** We are relying entirely on pre-race data. The system cannot probabilistically account for lap 1 collisions, sudden weather changes, or random engine failures.
2. **Grid vs Qualifying:** We use `grid_position` when available and fall back to `qualifying_position`. Missing grid data can still introduce error when penalties or grid drops occur.
3. **Regulation Shocks:** Major changes in FIA regulations (like the 2022 aerodynamic reset) temporarily disrupt the system's understanding of which teams are fastest until enough races happen under the new rules.

**Recommendation:** 
Deploy the calibrated Logistic Regression system inside the main strategy dashboard as our pre-race baseline. We should use its probability output to pre-load our primary and secondary racing strategies before the lights go out.
