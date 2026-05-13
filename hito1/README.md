# Capstone Hito 1: F1 Race Strategy Advisor

**Group 13**: Adrean Torres, Benjamín Pinto

This repository contains the deliverables for Hito 1 of the F1 Race Strategy Advisor Capstone project.

## 🚀 Runbook

### 1. Environment Setup

To run the Jupyter Notebook, you need a Python environment with Pandas, Numpy, Scikit-Learn, and Jupyter installed.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install required dependencies
pip install pandas numpy scikit-learn matplotlib jupyter
```

### 2. How to Run the Notebook

The primary deliverable is an end-to-end executable Jupyter Notebook.
1. Ensure the `.venv` is activated.
2. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
3. Open `hito1_baseline.ipynb`.
4. Click **"Run All"**. The notebook is designed to execute cleanly from top to bottom.

### 3. Repository Map

The files specific to Hito 1 are located in the `hito1/` folder:

- `hito1_baseline.ipynb`: The main executable notebook containing the data splits, baseline model, experiments, and what-if scenarios.
- `framing.md`: The updated Team Decision Sheet, detailing the problem framing, target definition, baseline justification, what-if plans, and recognized dataset limitations.
- `PROMPTS.md`: The AI interaction log documenting two key interactions using the mandatory 6-field standard (Context, Prompts, Output, Validation, Adaptations, Final Decision).
- `f1_strategy_race_level.csv`: The primary dataset used for the baseline model.
- `README.md`: This file, serving as the execution runbook.
