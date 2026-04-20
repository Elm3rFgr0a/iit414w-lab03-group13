# AI Interaction Log - Lab 3

## 1. Data Ingestion & API Timeout Fix
* **Context**: Fetching historical F1 data (2021-2023) using the Jolpica API. The initial attempt using standard `requests.get()` hung indefinitely and threw a `ConnectTimeout` error.
* **Prompt**: "I am trying to download F1 data from api.jolpi.ca using `requests.get('http://api.jolpi.ca/ergast/f1/.../results.json')`, but I get a `ConnectTimeout: Max retries exceeded` error. How can I fix this snippet to load the data properly?"
* **Output**: The AI explained that the API might be blocking standard Python scraping attempts or dropping HTTP requests. It provided a refactored function adding `https://`, a standard `User-Agent` header, a 15-second `timeout`, and a 3-attempt retry loop using `time.sleep()`.
* **Validation**: Ran the modified code in the notebook. It successfully downloaded the data for years 2021, 2022, and 2023 without hanging.
* **Adaptations**: Modified the `User-Agent` string to identify it as our specific student project (`IIT414W-Student-Project/1.0`) and translated the console status print statements to Spanish.
* **Final Decision**: We adopted the AI's robust fetching strategy entirely because API reliability is a blocker for the rest of the lab.

## 2. Feature Engineering & Target Definition
* **Context**: We chose binary classification (Scored Points vs. No Points). We needed to transform the continuous `points` array and categorical `constructorId`.
* **Prompt**: "I am framing my F1 model as binary classification ('Will the driver finish in the Top 10 / score points?'). Given my dataframe, write the Pandas code to create a binary target `scored_points` from the `points` column, and one-hot encode the `constructor` column dropping the first category."
* **Output**: The AI provided `df['scored_points'] = (df['points'] > 0).astype(int)` and `pd.get_dummies(df, columns=['constructor'], drop_first=True)`.
* **Validation**: Checked `df.head()` and `y.value_counts()` to ensure the target distribution wasn't corrupted and dummy columns correctly replaced the categorical string.
* **Adaptations**: None, the Pandas statements were straightforward and optimal.
* **Final Decision**: Used the exact lines to cleanly define `X` and `y`.

## 3. Temporal Validation Split
* **Context**: The rubric strictly forbids `train_test_split` (random splits) and demands temporal validation.
* **Prompt**: "I have data from 2021 to 2023. Write the Pandas masking code to do a walk-forward temporal split where the training set is strictly before 2023, and the test set is exactly the 2023 season."
* **Output**: Provided masks: `train_mask = X['season'] < 2023` and `test_mask = X['season'] == 2023`, followed by applying these masks to `X` and `y`.
* **Validation**: Verified `X_train['season'].max()` to assure 2023 data did not leak into the training features.
* **Adaptations**: Added list comprehension to explicitly subset only the `feature_cols` from the X dataframe before splitting, discarding the `season` column from actual training.
* **Final Decision**: Implemented this masking approach as it directly satisfies the strict C4/C1 non-negotiable temporal split rule.

## 4. Custom Baselines (Majority Class & Domain Heuristic)
* **Context**: We needed at least two baselines, including one domain-specific heuristic, to build a credible `comparison_table`.
* **Prompt**: "Write two simple Scikit-Learn-style baseline classes for this F1 binary classification. Model 1 should be a Majority Class predictor. Model 2 should be a domain heuristic that predicts 1 (Points) only if the `grid` (starting position) is <= 10."
* **Output**: The AI generated `MajorityBaseline` and `GridHeuristicBaseline` inheriting basic `fit()` and `predict()` structures, returning `numpy.full` mode arrays and boolean masks converted to integers, respectively.
* **Validation**: Passed `X_train` and calculated train/test Macro F1. The domain baseline scored much higher (~0.74) than the naive baseline, correctly validating the F1 logic.
* **Adaptations**: Kept the core logic but explicitly structured the metric calculations outside the class using `f1_score(average='macro')` to maintain identical evaluation across all models.
* **Final Decision**: We used these custom classes to act as our explicit baseline bounds in the final dataframe comparison.

## 5. Machine Learning Models & Automated Export
* **Context**: Fitting actual models (Logistic Regression, Random Forest) and compiling the final markdown table as required by the rubric.
* **Prompt**: "Now I will train a LogisticRegression and a RandomForestClassifier (seed=414). After collecting the Macro F1 train and test scores, write the code to create a Pandas dataframe showing 'Model', 'Train Macro F1', 'Test Macro F1', and a blank string for 'WHY (Mechanistic Reasoning)'. Also include a snippet to export this dataframe automatically to `comparison_table.md`."
* **Output**: The AI provided standard `.fit()` and `.predict()` statements for Sklearn, then created the `results` dataframe structure. It appended a `to_markdown()` IO block.
* **Validation**: Ran the final cell. The `comparison_table.md` file appeared in the directory with the correct Markdown table syntax.
* **Adaptations**: We manually filled in the 'WHY' column with our own F1 domain reasoning and test-vs-train overfitting observations as this part is graded heavily in C2.
* **Final Decision**: Maintained the auto-exporting code to perfectly sync our notebook numbers with our required standalone Markdown submission.