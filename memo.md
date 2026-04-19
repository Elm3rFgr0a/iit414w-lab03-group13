# Technical Memo: Race Day Points Predictor

**To:** Head of Strategy, Formula 1 Team
**From:** Data Analytics Unit
**Date:** April 20, 2026
**Subject:** Model Deployment for Point-Scoring Probability (Binary Classification)

### What can this model do for us?
We developed a predictive model to answer a critical race-day question: *Will our driver score points today based on their qualifying position and our car's historical strength?* By turning this into a simple "Yes/No" prediction, we can better align our pit-stop models and tire preservation strategies. If the model confidently predicts we will be in the points, we can adopt a defensive strategy; if not, we can afford aggressive alternative strategies.

### The Results
When evaluating on unseen 2023 data, our recommended model (Logistic Regression) correctly identifies point-scoring finishes with high accuracy, achieving a balance score (Macro F1) of **0.79**. 
To put this into context, a simple rule of thumb ("if we start in the top 10, we finish in the top 10") achieves a score of **0.76**. Our model beats this baseline by factoring in our car's underlying pace advantage, meaning it correctly spots when a fast car starting 12th will carve through the field to score.

### Confidence and Risks
You should be highly confident in the Logistic Regression model because its performance is stable. Unlike heavier, more complex models we tested (such as the Random Forest), our simple model didn't try to memorize fluke results from 2022. It understands the fundamental rule of F1: grid position dictates race pace, and constructor strength dictates overtaking ability. 

**Limitations:**
1. We are relying entirely on pre-race data. The model cannot account for lap 1 collisions, sudden rain, or engine failures. 
2. Changes in FIA regulations (like the 2022 aerodynamic reset) temporarily disrupt the model's understanding of which teams are fastest. 

**Recommendation:** Deploy the Logistic Regression model inside the strategy dashboard as a pre-race baseline confidence metric for scoring points.
