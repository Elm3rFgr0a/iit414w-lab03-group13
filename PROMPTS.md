# AI Documentation (Authenticity Log)

**1. Traceability & Operational Detail**
- *Model Selection Phase:* I asked the AI how to implement a temporal split accurately in pandas instead of `train_test_split`. The AI suggested `df['season'] < 2023` for training and `df['season'] == 2023` for testing (Code Cell 4). 
- *Jolpica API Refactoring:* The original Ergast API was deprecated, so I prompted the AI to transition the endpoint to `api.jolpi.ca`. The AI generated the loop and pagination parameters mapping `http://api.jolpi.ca/ergast/f1/{year}/results.json`. The AI initially forgot to handle the `position` edge case where a driver Retires and it might be string/null. I encountered a `ValueError` trying to cast "R" to int, and corrected it defensively.

**2. AI Failures & Critical Distance**
- The AI initially suggested comparing models on pure `Accuracy` instead of `Macro F1`. I pushed back, as the prompt strictly required domain reasoning. In F1, accuracy masks the true goal because predicting "no points" correctly every time for a backmarker team yields 50% accuracy. The AI hallucinated a business justification for Accuracy, demonstrating its lack of deep strategic domain knowledge of F1 scoring mechanics. 
