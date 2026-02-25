# 🛡️ Predictive Claims Liability Model: Insurance Risk Oversight

![Dashboard Snapshot](Dashboard.png)

## 📋 Project Overview
In large-scale insurance environments, accurately forecasting the ultimate cost of a claim at the point of lodgement is a critical operational hurdle. This project focuses on the development of a high-performance predictive pipeline to estimate the **Pure Premium** (Expected Annual Liability) using a dataset of over 670,000 motor insurance policies.
By synthesizing multi-dimensional risk features—including actuarial risk scores, geographic density, and vehicle specifications—the model identifies high-signal liability indicators early in the claim lifecycle. This solution serves as a technical proof-of-concept for evidence-based decision-making and proactive risk oversight within complex insurance portfolios.

🔗 **[View Live Interactive Dashboard](https://claims-liability-predictor-dgw3wokbgkfzrhm4yfdlrh.streamlit.app/)**

---

## 💼 The Business Problem
Insurance organizations often face "claims leakage" and financial volatility due to reactive reserve setting. Traditional manual reviews are resource-intensive and may miss non-obvious correlations in high-volume data.

### **Strategic Objectives:**
* **Early Intervention:** Automatically flags high-liability "outlier" claims at the point of entry for specialized management.
* **Reserve Optimization:** Provides data-driven insights to set accurate financial reserves, ensuring organizational liquidity and regulatory compliance.
* **Regulatory Adherence:** Ensures data integrity and reporting standards align with frameworks such as the **ACT Workers Compensation Act**.

---

## 📊 About the Dataset: freMTPL2
The foundation of this model is the **French Motor Third-Party Liability (TPL) Insurance Claims** dataset. It provides a comprehensive view of risk characteristics observed primarily over a one-year period.
* **Scope**: Data collected for 677,991 motor third-party liability policies.
* **Structure**: The data is partitioned into two distinct tables:
** `freMTPL2freq`: Captures policy-specific risk features (age, region, vehicle age, etc.) and the number of claims recorded.
** `freMTPL2sev`: Records the specific cost (amount) for each individual claim.
* **Integration**: Both tables are linked via a unique Policy ID `IDpol` to create a unified view of frequency and severity.

---

## 🛠️ Technical Methodology
### **Addressing Zero-Inflation with Tweedie Regression**
Insurance data is inherently "zero-inflated," meaning the vast majority of policies result in zero claims, while a small fraction result in highly skewed, positive costs.
To solve this, I implemented a **Tweedie Regressor** (), which is a compound Poisson-Gamma distribution. This approach allows for the simultaneous modeling of claim frequency and severity in a single unified framework, providing significantly higher accuracy than standard linear models for insurance pricing.

### **The "Automated Data Supply Chain"**
* **End-to-End Pipeline:** Developed a modular **Scikit-learn pipeline** to handle automated data acquisition, cleaning, and transformation.
* **Feature Engineering:** Implemented a `ColumnTransformer` for the technical verification of both numerical (Scaling) and categorical (One-Hot Encoding) risk features.
* **Exposure Weighting:** Trained the model using `Exposure` as a sample weight to ensure predictions are proportional to the policy duration.

---

## 📂 Repository Structure

```text
├── app.py                # Streamlit Dashboard (Strategic Storytelling Interface)
├── tweedie_model.pkl      # Production-ready trained pipeline (serialized)
├── requirements.txt      # Dependency manifest for automated deployment
├── README.md             # Project narrative and business impact
└── Notebooks/            # Annotated deep-dives into EDA and model validation
```

---

## 🚀 Business Impact & ROI
* **Technical Proof of Concept:** Demonstrates the ability to build "Data Apps" that allow stakeholders to explore real-time risk profiles independently.
* **Enhanced Risk Oversight:** Moves the analytical framework from retrospective reporting to proactive forecasting.
* **Actionable Insights:** Translates complex actuarial indicators (e.g., Bonus/Malus scores and Inhabitant Density) into clear, concise financial recommendations for senior stakeholders.

---

## 👤 Technical Profile
**Aayush Yagol** | 📍 Canberra, ACT 
🌐 [aayushyagol.com](https://aayushyagol.com) | 🔗 [LinkedIn](https://www.linkedin.com/in/aayush-yagol-046874145/) 

---
