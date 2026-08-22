# 🛡️ Claims Liability Predictor

![Dashboard Snapshot](Dashboard.png)

## 📋 What This Is

When someone lodges a car insurance claim, an insurer needs to estimate roughly how much that claim will end up costing — as early and as accurately as possible. This project is a working demo of that idea: you enter a policy's details (driver age, vehicle type, location, etc.) and it instantly estimates the expected claims cost, flags how risky that policy is relative to the rest of the portfolio, and shows how confident the underlying model is. It's built on a real, publicly available French motor insurance dataset of ~678,000 policies, using the industry-standard statistical approach for this kind of prediction (more on that below, for the technically curious).

🔗 **[View Live Interactive Dashboard](https://claims-liability-predictor.streamlit.app/)**

---

## ⚙️ How It Works

The model looks at a policy's risk factors — driver age, vehicle power, location, claims history — and learns from hundreds of thousands of real historical policies which combinations of factors led to expensive claims. It then applies that pattern to any new policy you enter, producing an instant cost estimate. Because most policies never make a claim at all, standard prediction-accuracy measures don't work well here — the model instead uses actuarial-standard statistical measures suited to that reality, explained in the results table below.

---

## 💼 The Business Problem

Insurance organisations often face "claims leakage" and financial volatility due to reactive reserve setting. Traditional manual reviews are resource-intensive and may miss non-obvious correlations in high-volume data.

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

## 🛠️ Technical Methodology (for a technical reviewer)
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

| Metric | Value | In plain terms |
|--------|-------|-----------------|
| Mean Tweedie Deviance (p=1.5) | 84.0536 | The model's primary accuracy score (lower = better); the right way to score this type of claims data |
| Mean Absolute Error (MAE) | €307.34 | On average, how far a single prediction is from the real outcome |
| Root Mean Squared Error (RMSE) | €8,815.60 | Similar to MAE, but weighted more heavily by rare, very expensive claims |
| Explained Variance Score | -0.0002 | Expected to be near zero for this kind of data — not a sign the model is broken (explained further below) |

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
- The data covers a single year, so there's no way to validate how the model would perform over time
- It's built on the French motor insurance market — the findings would need local recalibration before applying them to an Australian (or any other) portfolio
- There's no separate, independent dataset used to double-check the results
- The Tweedie model's key setting (p=1.5) was chosen based on standard industry convention, not tuned by testing many values
- The model doesn't yet account for combinations of risk factors interacting with each other

**Future Improvements:**
- Systematically test a range of values for the Tweedie `power` setting (between 1.0 and 2.0) to find the best fit
- Validate the model using cross-validation that still respects each policy's exposure period
- Explore how risk factors interact — for example, whether driver age matters more or less depending on the Bonus/Malus score
- Group policies by geography using population density and region to spot local risk clusters
- Compare results against a Gradient Boosted Tweedie model (e.g., LightGBM with a Tweedie objective) to see if it outperforms the current approach

---

## 👤 Technical Profile
**Aayush Yagol** | 📍 Canberra, ACT
🌐 [aayushyagol.com](https://aayushyagol.com) | 🔗 [LinkedIn](https://www.linkedin.com/in/aayush-yagol-046874145/)

---
