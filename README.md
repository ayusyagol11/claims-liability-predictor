# 🛡️ Predictive Claims Liability Model: Insurance Risk Oversight

![Dashboard Snapshot](Dashboard.png)

## 📋 Project Overview
In large-scale insurance environments, accurately forecasting the ultimate cost of a claim at the point of lodgement is a critical operational challenge. This project demonstrates an end-to-end analytical transition from **operational claims advising to proactive data science**.

By leveraging the **freMTPL2** dataset (678,013 policies), I developed a specialized predictive pipeline to estimate **Pure Premium** (Total Liability / Exposure). This tool enables insurers to identify "high-risk" claims early, optimize financial reserves, and ensure adherence to regulatory compliance.

🔗 **[View Live Interactive Dashboard](https://claims-liability-predictor-dgw3wokbgkfzrhm4yfdlrh.streamlit.app/)**

---

## 🚀 Quick Start

```bash
git clone https://github.com/ayusyagol11/claims-liability-predictor.git
cd claims-liability-predictor
pip install -r requirements.txt
streamlit run app.py
```

---

## 💼 The Business Problem
Insurance organizations often face "claims leakage" and financial volatility due to reactive reserve setting. Traditional manual reviews are resource-intensive and may miss non-obvious correlations in high-volume data.

### **Strategic Objectives:**
* **Early Intervention:** Automatically flags high-liability "outlier" claims at the point of entry for specialized management.
* **Reserve Optimization:** Provides data-driven insights to set accurate financial reserves, ensuring organizational liquidity and regulatory compliance.
* **Regulatory Adherence:** Ensures data integrity and reporting standards align with French motor insurance governance frameworks.

---

## 📊 About the Dataset: freMTPL2
The foundation of this model is the **French Motor Third-Party Liability (TPL) Insurance Claims** dataset. It provides a comprehensive view of risk characteristics observed primarily over a one-year period.
* **Scope**: Data collected for 677,991 motor third-party liability policies.
* **Structure**: The data is partitioned into two distinct tables:
  * `freMTPL2freq`: Captures policy-specific risk features (age, region, vehicle age, etc.) and the number of claims recorded.
  * `freMTPL2sev`: Records the specific cost (amount) for each individual claim.
* **Integration**: Both tables are linked via a unique Policy ID `IDpol` to create a unified view of frequency and severity.

---

## 🛠️ Technical Methodology
### **Addressing Zero-Inflation with Tweedie Regression**
Insurance data is inherently "zero-inflated," meaning the vast majority of policies result in zero claims, while a small fraction result in highly skewed, positive costs.
To solve this, I implemented a **Tweedie Regressor** (p=1.5), which is a compound Poisson-Gamma distribution. This approach allows for the simultaneous modeling of claim frequency and severity in a single unified framework, providing significantly higher accuracy than standard linear models for insurance pricing.

### **ML Preprocessing Pipeline**
* **End-to-End Pipeline:** Developed a modular **Scikit-learn pipeline** to handle automated data acquisition, cleaning, and transformation.
* **Feature Engineering:** Implemented a `ColumnTransformer` for the technical verification of both numerical (Scaling) and categorical (One-Hot Encoding) risk features.
* **Exposure Weighting:** Trained the model using `Exposure` as a sample weight to ensure predictions are proportional to the policy duration.

---

## 📈 Model Evaluation Results

Evaluated on a 20% holdout test set (~135,000 policies):

| Metric | Value |
|--------|-------|
| Mean Tweedie Deviance (p=1.5) | 84.0536 |
| Mean Absolute Error (MAE) | €307.34 |
| Root Mean Squared Error (RMSE) | €8,815.60 |
| Explained Variance Score | -0.0002 |

> **Note:** Mean Tweedie Deviance is the primary evaluation metric as it is the native loss
> function for the Tweedie distribution family. Standard R² can be misleading for
> zero-inflated insurance data where most policies have zero claims.
>
> **Why is Explained Variance near zero and MAE high?** Over 93% of policies have zero claims,
> making the actual Pure Premium distribution extremely zero-inflated. The model predicts
> *expected* liability (a small positive value for every policy), not whether a specific claim
> will occur. This means the MAE (€307) is large relative to the median predicted premium
> (€117) because most actuals are €0 while predictions are always positive — this is by design
> in actuarial pricing models, not a deficiency. The Tweedie Deviance (84.05) is the
> appropriate measure of fit for this distribution.

---

## 📂 Repository Structure

```
├── app.py                          # Streamlit dashboard (entry point)
├── requirements.txt                # Python dependencies
├── README.md
├── Dashboard.png                   # Dashboard screenshot
│
├── model/                          # Trained model & evaluation artifacts
│   ├── tweedie_model.pkl           # Serialised Tweedie pipeline (joblib)
│   ├── model_metrics.json          # Evaluation metrics for dashboard
│   ├── portfolio_stats.json        # Portfolio distribution stats
│   └── feature_importance.json     # Permutation importance results
│
├── notebooks/                      # Training & analysis
│   └── ClaimsLiabilityPredictiveModel.ipynb
│
├── data/                           # Source datasets
│   ├── freMTPL2freq.csv
│   └── freMTPL2sev.csv
│
├── assets/                         # Generated charts
│   ├── pred_vs_actual.png
│   ├── residuals_distribution.png
│   └── feature_importance.png
│
└── docs/                           # Reference documents
    ├── ClaimsLiabilityPredictiveModel.pdf
    └── freMTPL2 French Motor Third-Part Liability dataset.pdf
```

---

## 🚀 Business Impact & ROI
* **Technical Proof of Concept:** Demonstrates the ability to build "Data Apps" that allow stakeholders to explore real-time risk profiles independently.
* **Enhanced Risk Oversight:** Moves the analytical framework from retrospective reporting to proactive forecasting.
* **Actionable Insights:** Translates complex actuarial indicators (e.g., Bonus/Malus scores and Inhabitant Density) into clear, concise financial recommendations for senior stakeholders.

---

## ⚠️ Limitations & Future Work

**Current Limitations:**
- Single observation year — no temporal validation possible
- French Motor TPL market — findings are not directly transferable to Australian portfolios without recalibration
- No external validation dataset
- Tweedie power parameter (p=1.5) was set based on domain convention, not optimised via grid search
- No feature interaction terms explored

**Future Improvements:**
- Grid search on Tweedie `power` parameter (1.0 < p < 2.0)
- Cross-validation with exposure-weighted folds
- Feature interaction terms (e.g., DrivAge × BonusMalus)
- Geographic risk clustering using Inhabitant Density and Region
- Comparison with Gradient Boosted Tweedie (e.g., LightGBM with Tweedie objective)

---

## 👤 Technical Profile
**Aayush Yagol** | 📍 Canberra, ACT
🌐 [aayushyagol.com](https://aayushyagol.com) | 🔗 [LinkedIn](https://www.linkedin.com/in/aayush-yagol-046874145/)

---
