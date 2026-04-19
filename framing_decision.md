# Framing Decision & Justification

**Business question**
"What are the realistic chances of our driver scoring points this weekend?" A team principal evaluating risk on race day needs to allocate resources strategically (like tire life and pit-stop timing) primarily based on whether the car can reliably break into the top 10 positions where points are awarded.

**Target variable**
`scored_points`: A binary label (1 if driver position <= 10 and scored points, else 0).

**Metric**
Macro F1. It is appropriate because it perfectly balances the penalty for false positives (wasting pit strategy believing we'd score) and false negatives (abandoning a race where points were available), given the slight imbalance (only 10 out of 20 cars score points). 

**Rejected alternative**
I considered *Regression (Predicting exact points using MAE)* but rejected it because the points distributed are heavily zero-inflated (half the grid scores 0). A model trained on MAE will continuously predict fractional points (e.g., 1.5 points) for midfield drivers, which isn't actionable for race-day binary pit decisions. The cost of being wrong between P1 and P2 is high on paper but strategically less volatile than the gap between P10 and P11.
