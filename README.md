# DSA210 – Exam Periods, Physical Activity & Student Burnout
**Egemen Kuş** | Spring 2025-2026 | 35224

## Research Question
Do exam periods measurably impact physical activity, and does this correlate with burnout risk in the general student population?

## Datasets
- **Burnout Dataset** — 1M student records with sleep, stress, physical activity, and burnout scores
  Source: [Kaggle – Student Mental Health and Burnout](https://www.kaggle.com/datasets/sharmajicoder/student-mental-health-and-burnout)
- **Apple Health (Personal)** — Daily step count, exercise minutes, and active calories from September 2024 onwards, with Sabancı University exam periods labeled

-> Datasets would not be included in this tag because of the size

## Plots (Exploratory Data Analysis (EDA))
* plots/01_distributions.png
* plots/02_correlation.png
* plots/03_activity_burnout.png
* plots/04_timeseries.png
* plots/05_boxplot_exam.png
* plots/06_personal_vs_population.png

## Hypotheses

**H1 — Physical Activity & Burnout (Pearson):**
Higher physical activity is negatively correlated with burnout score.
*Result: r = -0.11, p < 0.05 → REJECT H0*

**H2 — Sleep Hours & Burnout (Pearson):**
More sleep hours are negatively correlated with burnout score.
*Result: r = -0.37, p < 0.05 → REJECT H0*

**H3 — Stress Level & Burnout (Pearson):**
Higher stress is positively correlated with burnout score.
*Result: r = +0.75, p < 0.05 → REJECT H0*

**H4 — Daily Steps: Exam vs Non-Exam (Welch's t-Test):**
Step count does not significantly differ during exam periods.
*Result: p = 0.42 → FAIL TO REJECT H0*

**H5 — Exercise Minutes: Exam vs Non-Exam (Welch's t-Test):**
Exercise minutes are significantly lower during exam periods.
*Result: p = 0.016 → REJECT H0*

**H6 — Distance (km): Exam vs Non-Exam (Welch's t-Test):**
Daily walking distance does not significantly differ during exam periods.
*Result: p = 0.394 → FAIL TO REJECT H0*

## How to Run
```bash
pip install -r requirements.txt
```
and run notebooks in order: ***data_analyze.ipynb, data_visualization.ipynb, hypothesis_test.ipynb***

## Raw And Processed Data
There is a folder called ***raw+processed***. Inside, there is ***burnout_processor.py and apple_health_processor.py***. These are solely for just parsing and creating a csv of complicated and messy data. For usage, just place the downloaded files on the ***raw+processed*** folder. Then run those files. The output files should be on the "/" directory.

## AI Usage Disclosure
AI was used in the following areas:

- **Apple Health data parsing:** The raw XML export from Apple Health was too complex to process manually. Claude helped write the parsing script (`raw+processed/apple_health_processor.py`) to extract daily metrics from the XML and convert them to a structured CSV.
- **Correlation heatmap:** After seeing heatmap usage in past student projects shared via course email, I didn't know how to implement one myself. Claude provided guidance on how to use `sns.heatmap` with a correlation matrix.