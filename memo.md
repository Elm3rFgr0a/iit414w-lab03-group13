# Technical Memo: Race Day Points Predictor

**To:** Head of Strategy, Formula 1 Team
**From:** Data Analytics Unit
**Date:** April 20, 2026
**Subject:** Model Deployment for Point-Scoring Probability (Binary Classification)

### What can this model do for us?
We developed a predictive system to answer a critical race-day question: *Will our driver score points today based on their qualifying position and our car's historical strength?* By framing this as a simple "Yes/No" prediction, we can better align our pit-stop and tire preservation strategies. If the system confidently predicts we will be in the points, we can adopt a protective strategy; if not, we can afford aggressive alternative strategies to roll the dice.

### The Results
When testing our system against the unseen 2023 race season, our recommended model (Logistic Regression) correctly separated point-scoring finishes from non-scoring ones with high reliability, achieving an overall balance score of **76.0%** (0.76). 

To put this into context, a simple grid rule of thumb the paddock often uses ("if we start in the top 10, we usually finish in the top 10") achieves a score of **74.0%**. Our system beats this established heuristic by mathematically factoring in our car's underlying pace advantage and historical team form. This means it correctly spots when a fast car starting 12th will carve through the field to score, or when a slow car starting 9th will fall backward.

### Confidence and Risks
You should be confident in deploying this primary model because its performance is stable. Unlike heavier, more complex artificial intelligence we tested (such as the Random Forest, which achieved a **75.9%** score but showed early signs of simply memorizing the 2022 season instead of learning real racing rules), our simple model focuses on the fundamental laws of F1: grid position dictates clean air pace, and constructor strength dictates overtaking ability over the course of 300+ kilometers. 

**Limitations & Risks:**
1. **Unpredictable Events:** We are relying entirely on pre-race data. The system cannot probabilistically account for lap 1 collisions, sudden weather changes, or random engine failures. 
2. **Regulation Shocks:** Major changes in FIA regulations (like the 2022 aerodynamic reset) temporarily disrupt the system's understanding of which teams are fastest until enough races happen under the new rules.

**Recommendation:** 
Deploy the Logistic Regression system inside the main strategy dashboard as our pre-race baseline. We should use its "Yes/No" output to pre-load our primary and secondary racing strategies before the lights go out.
