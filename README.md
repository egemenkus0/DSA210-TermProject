# DSA210 — Exam Periods, Physical Activity & Student Burnout

**Egemen Kuş** | Spring 2025–2026 | Student ID: 35224 | Sabancı University

---

## Research Question

Do exam periods measurably reduce physical activity, and does this correlate with burnout risk in the general student population?

---

## 1. Motivation

Every student who has ever crammed for finals knows the feeling: the gym visits stop, the late-night study sessions begin, and somewhere between the third coffee and the fourth practice exam, you stop moving altogether. I wanted to know whether this intuition holds up under data.

As a Sabancı University student, I wore my Apple Watch through two full academic years and collected daily step counts, exercise minutes, and calorie data. The question I kept asking myself was:

> *Do exam periods actually reduce my physical activity — and if so, does that reduction matter for burnout risk?*

To answer this, I combined two sources: my own Apple Health export (personal, longitudinal) and a publicly available dataset of 1,000,000 student records with burnout scores (population-level). The combination lets me ground personal observations in statistical evidence, and then turn the lens back on myself with a machine learning model trained on the population data.

---

## 2. Datasets

- **Burnout Dataset** — 1M synthetic student records with sleep, stress, physical activity, exam pressure, social support, and burnout scores.
  Source: [Kaggle – Student Mental Health and Burnout](https://www.kaggle.com/datasets/sharmajicoder/student-mental-health-and-burnout)

- **Apple Health (Personal)** — Daily step count, exercise minutes, active calories, and heart rate from September 2024 onwards. Exam periods labelled from the official Sabancı University academic calendar. 577 days total.

> Datasets are not included in this repository due to size. See **Raw and Processed Data** section for instructions.

---

## 3. Exploratory Data Analysis

EDA was performed on both datasets to understand distributions, spot anomalies, and identify features worth investigating.

| Plot | Description |
|------|-------------|
| `plots/eda_distributions.png` | Distributions of key burnout dataset variables |
| `plots/eda_correlation.png` | Pearson correlation heatmap — stress level dominates (r ≈ 0.75) |
| `plots/eda_activity_burnout.png` | Physical activity vs. burnout score |
| `plots/eda_timeseries.png` | My daily step count over time with exam periods highlighted |
| `plots/eda_boxplot_exam.png` | Exercise minutes during exam vs. non-exam days |
| `plots/eda_personal_vs_population.png` | My normalised activity score vs. the population distribution |

---

## 4. Hypotheses

Six hypotheses were tested. Pearson correlation for population-level variables; Welch's t-test for personal exam vs. non-exam comparisons. Significance threshold: **α = 0.05**.

| # | Hypothesis | Test | Statistic | p-value | Result |
|---|-----------|------|-----------|---------|--------|
| H1 | Physical Activity & Burnout | Pearson r | −0.1101 | < 0.001 | **REJECT H0** ✓ |
| H2 | Sleep Hours & Burnout | Pearson r | −0.3714 | < 0.001 | **REJECT H0** ✓ |
| H3 | Stress Level & Burnout | Pearson r | +0.7531 | < 0.001 | **REJECT H0** ✓ |
| H4 | Social Support & Burnout | Pearson r | −0.2298 | < 0.001 | **REJECT H0** ✓ |
| H5 | Daily Steps: Exam vs Non-Exam | Welch t | t = 0.82 | 0.415 | FAIL TO REJECT ✗ |
| H6 | Exercise Minutes: Exam vs Non-Exam | Welch t | t = −2.42 | 0.016 | **REJECT H0** ✓ |

**Key insight:** Step count does not drop during exams (H5 not significant), but exercise minutes fall to zero on average (H6 significant, p = 0.016 — exam mean: 0 min vs. non-exam mean: 1.02 min). I stay incidentally active but drop structured workouts entirely.

---

## 5. ML Models

Three machine learning approaches on the burnout dataset (100k stratified sample from 1M rows).

**Target:** `risk_level` → 0 = Low, 1 = Medium, 2 = High
**Features:** `study_hours_per_day`, `exam_pressure`, `stress_level`, `sleep_hours`, `physical_activity`, `social_support`, `screen_time`, `financial_stress`, `family_expectation`
**Split:** 70% train / 15% validation / 15% test (stratified)

### Results

| Model | Val. Accuracy | Test Accuracy | Weighted F1 | High-Risk Recall |
|-------|--------------|---------------|-------------|-----------------|
| Decision Tree (max_depth=3) | 84.16% | 84.01% | 83% | 0% |
| Random Forest (n=100) | 85.55% | 85.53% | 85% | 22% |

The Random Forest gains 1.5 pp in accuracy. More importantly, the Decision Tree fails to identify any High-risk students (the class is only 1.5% of the data), while the Random Forest achieves 22% recall on that minority class.

### Plots

| Plot | Description |
|------|-------------|
| `plots/ml_decision_tree.png` | Decision tree — first split is on stress_level |
| `plots/ml_confusion_matrix.png` | Confusion matrices for DT (Blues) and RF (Oranges) |
| `plots/ml_feature_importance.png` | RF feature importances — stress_level accounts for ~40% |
| `plots/ml_kmeans_elbow.png` | Elbow plot — inertia flattens after k = 3 |
| `plots/ml_kmeans_clusters.png` | PCA scatter coloured by cluster vs. actual risk level |
| `plots/ml_personal_prediction.png` | My personal burnout risk probabilities: exam vs. non-exam |

### K-Means Clustering (k=3)

Unsupervised grouping of students without using the risk label. Optimal k chosen via elbow method. Clusters visualised in 2D via PCA. The three clusters broadly align with Low / Medium / High risk, validating that the lifestyle features encode meaningful groupings.

### Personal Prediction (Side Quest)

I used the trained Random Forest to predict my own burnout risk, combining my real `physical_activity` values (normalised Apple Watch step count) with personal estimates for the other eight features.

| Period | Model | Predicted Risk | P(Low) | P(Medium) | P(High) |
|--------|-------|---------------|--------|-----------|---------|
| Exam Period | Decision Tree | **Medium** | 0.24 | 0.70 | 0.06 |
| Exam Period | Random Forest | **Medium** | 0.10 | 0.85 | 0.05 |
| Non-Exam Period | Decision Tree | **Low** | 0.92 | 0.08 | 0.00 |
| Non-Exam Period | Random Forest | **Low** | 0.99 | 0.01 | 0.00 |

Both models agree: Low risk during normal periods → Medium risk during exam periods. The shift is driven by the combined increase in stress and exam pressure, not by the physical activity drop alone.

---

## 6. Key Findings

- **Stress dominates burnout.** r = +0.75 with burnout score; ~40% of Random Forest feature importance. No other variable comes close.
- **Sleep is the most important protective factor** (r = −0.37). Losing sleep during exams carries more burnout risk than losing exercise time.
- **Physical activity has a small but real protective effect** (r = −0.11). Significant across 1M records, but secondary to stress and sleep.
- **Social support matters** (r = −0.23). Students with stronger social networks show consistently lower burnout.
- **Personally, I maintain step count during exams but stop deliberate exercise entirely** — confirming the pattern quantitatively (H6, p = 0.016).
- **The ML models predict I shift from Low to Medium burnout risk during exam periods**, driven by the combined effect of higher stress, less sleep, and reduced exercise.

---

## 7. Limitations and Future Work

**Limitations:**
- The burnout dataset is synthetic. Results cannot be directly generalised to a real student population without validation on genuine survey data.
- Personal data covers one person over two academic years — illustrative, not clinically conclusive.
- Class imbalance is severe (Low: 76.7%, High: 1.5%). Models still struggle to recall High-risk students.
- The physical_activity scale mapping (steps → 1–7) is an approximation.

**Future work:**
- Collect real survey data from multiple students to replace the synthetic dataset.
- Add Apple Health sleep duration to the personal ML prediction.
- Apply SMOTE or class-weight adjustment to improve High-risk recall.
- Use time-series models (LSTM, Prophet) to predict burnout trajectory over time.

---

## 8. How to Run

```bash
pip install -r requirements.txt
```

Run notebooks in order:

1. `data_analyze.ipynb`
2. `data_visualization.ipynb`
3. `hypothesis_test.ipynb`
4. `ml_models.ipynb`

---

## 9. Raw and Processed Data

There is a folder called `raw+processed`. Inside, there is `burnout_processor.py` and `apple_health_processor.py`. These scripts parse the raw data and produce structured CSVs. For usage, place the downloaded files in the `raw+processed` folder and run the scripts. The output CSVs will be saved to the root `/` directory.

---

## 10. AI Usage Disclosure

AI assistance (Claude) was used in the following specific areas:

- **Apple Health data parsing:** The raw XML export from Apple Health is complex and undocumented. Claude helped write the parsing script (`raw+processed/apple_health_processor.py`) to extract daily metrics and convert them to a structured CSV.
- **Correlation heatmap:** After seeing heatmap usage in other student projects shared via course email, I asked Claude for guidance on implementing `sns.heatmap` with a correlation matrix.
- **ML notebook structure:** Claude helped organise `ml_models.ipynb`, including the 70/15/15 train/validation/test split, combining the two confusion matrices into a single figure, and applying a colorblind-safe colour palette.

All analysis decisions, hypothesis formulations, data interpretations, and written content are my own. AI was not used to generate, fabricate, or alter any data.
