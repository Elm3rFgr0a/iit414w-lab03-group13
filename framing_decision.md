# Framing Decision & Justification

**Business question**
"What are the realistic chances of our driver scoring points this weekend?" A team principal evaluating risk on race day needs to allocate resources strategically (like tire life and pit-stop timing) primarily based on whether the car can reliably break into the top 10 positions where points are awarded.

**Target variable**
`scored_points`: A binary label (1 if driver position <= 10 and scored points, else 0).

**Metric**
Macro F1. I chose this metric because we care equally about identifying when we *will* score points and when we *won't*. F1-score perfectly balances the penalty for false positives (wasting an aggressive pit strategy believing we'd score when we won't) and false negatives (abandoning a race where points were actually available). Because exactly 10 out of 20 cars score points, the classes are perfectly balanced, making Macro F1 highly interpretable.

**Rejected alternative**
I considered *Regression (Predicting exact points using MAE)* but rejected it because the points distributed in Formula 1 are heavily zero-inflated (50% of the grid scores 0 points every race). A regression model trained on MAE will continuously predict fractional points (e.g., 1.5 points) for midfield drivers, which is not actionable for a race-day binary pit decision. Furthermore, the business cost of being wrong between predicting P1 (25 pts) and P2 (18 pts) is 7 error points but changes nothing about our binary operational strategy. Conversely, the gap between P10 (1 pt) and P11 (0 pts) changes everything about how we race. Therefore, binary classification precisely mirrors the operational threshold that matters most to the team strategy.
