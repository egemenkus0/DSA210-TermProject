# DSA210 – Exam Periods, Physical Activity & Student Burnout
**Egemen Kuş** | Spring 2025-2026 | 35224

## Research Question
Do exam periods measurably impact physical activity, and does this correlate with burnout risk in the general student population?

## Datasets
- **Burnout Dataset** — 1M student records with sleep, stress, physical activity, and burnout scores
  Source: [Kaggle – Student Mental Health and Burnout](https://www.kaggle.com/datasets/sharmajicoder/student-mental-health-and-burnout)
- **Apple Health (Personal)** — Daily step count, exercise minutes, and active calories from September 2024 onwards, with Sabancı University exam periods labeled

-> Datasets would not be included in this tag because of the size

## Plots (Exploratory Data Analysis)
* plots/eda_distributions.png
* plots/eda_correlation.png
* plots/eda_activity_burnout.png
* plots/eda_timeseries.png
* plots/eda_boxplot_exam.png
* plots/eda_personal_vs_population.png

## Plots (ML Models)
* plots/ml_decision_tree.png
* plots/ml_confusion_matrix.png
* plots/ml_feature_importance.png
* plots/ml_kmeans_elbow.png
* plots/ml_kmeans_clusters.png
* plots/ml_personal_prediction.png

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

**H4 — Social Support & Burnout (Pearson):**
Higher social support is negatively correlated with burnout score.
*Result: r = -0.23, p < 0.05 → REJECT H0*

**H5 — Daily Steps: Exam vs Non-Exam (Welch's t-Test):**
Step count does not significantly differ during exam periods.
*Result: p = 0.42 → FAIL TO REJECT H0*

**H6 — Exercise Minutes: Exam vs Non-Exam (Welch's t-Test):**
Exercise minutes are significantly lower during exam periods.
*Result: p = 0.016 → REJECT H0*

## ML Models

Three machine learning models were applied to the burnout dataset (100k random sample from 1M rows).
Target variable: `risk_level` encoded as 0 = Low, 1 = Medium, 2 = High.
Features used: `study_hours_per_day`, `exam_pressure`, `stress_level`, `sleep_hours`, `physical_activity`, `social_support`, `screen_time`, `financial_stress`, `family_expectation`.

Data was split 70% train / 15% validation / 15% test (stratified).

**Decision Tree (max_depth=3):** Interpretable baseline model. Visualized as a tree diagram (`ml_decision_tree.png`). Evaluated on both validation and test sets.

**Random Forest (n_estimators=100):** Ensemble model for higher accuracy. Feature importances plotted (`ml_feature_importance.png`). Both models share a combined confusion matrix (`ml_confusion_matrix.png`).

**K-Means Clustering (k=3):** Unsupervised grouping of students. Optimal k chosen via elbow method (`ml_kmeans_elbow.png`). Clusters visualized in 2D via PCA (`ml_kmeans_clusters.png`).

**Personal Prediction (Side Quest):** My own Apple Health data (daily steps, exercise minutes, active calories) was fed into the trained Random Forest to predict my burnout risk across exam vs. non-exam periods (`ml_personal_prediction.png`).

## How to Run
```bash
pip install -r requirements.txt
```
and run notebooks in order: ***data_analyze.ipynb, data_visualization.ipynb, hypothesis_test.ipynb, ml_models.ipynb***

## Raw And Processed Data
There is a folder called ***raw+processed***. Inside, there is ***burnout_processor.py and apple_health_processor.py***. These are solely for just parsing and creating a csv of complicated and messy data. For usage, just place the downloaded files on the ***raw+processed*** folder. Then run those files. The output files should be on the "/" directory.

## AI Usage Disclosure
AI was used in the following areas:

- **Apple Health data parsing:** The raw XML export from Apple Health was too complex to process manually. Claude helped write the parsing script (`raw+processed/apple_health_processor.py`) to extract daily metrics from the XML and convert them to a structured CSV.
- **Correlation heatmap:** After seeing heatmap usage in past student projects shared via course email, I didn't know how to implement one myself. Claude provided guidance on how to use `sns.heatmap` with a correlation matrix.
- **ML notebook structure:** Claude helped organize the `ml_models.ipynb` notebook.