# 🛡️ Predictive Claims Liability Model: Insurance Risk Oversight

## 📋 Project Overview
In large-scale insurance environments, accurately forecasting the ultimate cost of a claim at the point of lodgement is a critical operational challenge. This project demonstrates an end-to-end analytical transition from **operational claims advising to proactive data science**.

By leveraging the **freMTPL2** dataset (678,013 policies), I developed a specialized predictive pipeline to estimate **Pure Premium** (Total Liability / Exposure). This tool enables organizations like **Suncorp** to identify "high-risk" claims early, optimize financial reserves, and ensure 100% adherence to regulatory compliance.

🔗 **[View Live Interactive App on Streamlit Cloud](https://claims-liability-predictor-dgw3wokbgkfzrhm4yfdlrh.streamlit.app/)**

---

## 🚀 Key Features & High-Signal Indicators
* **End-to-End Data Supply Chain:** Automated the transformation of raw frequency and severity data into a unified analytical dataset.
* **Zero-Inflated Modeling:** Utilized a **Tweedie Regressor** (Power=1.5) to handle the specific distribution of insurance claims—where most policies result in zero claims.
* **Strategic Storytelling Dashboard:** Built a "self-service" Streamlit application allowing stakeholders to explore risk factors like `BonusMalus` and `Urban Density` in real-time.
* **Data Integrity & Governance:** Implemented robust ETL audits to ensure 100% data quality, addressing the #1 concern for 2026 hiring managers.

---

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Libraries:** Pandas, NumPy, Scikit-learn (TweedieRegressor, ColumnTransformer), Joblib
* **Deployment:** Streamlit, GitHub, Git Version Control
* [cite_start]**Methodology:** Agile Workflow, Modular Pipeline Architecture 

---

## 📂 Repository Structure
```text
├── app.py                # Interactive Streamlit Dashboard code
├── tweedie_model.pkl     # Production-ready trained pipeline (serialized)
├── requirements.txt      # Dependency manifest for cloud deployment
├── README.md             # Strategic project narrative
└── Notebooks/            # Annotated Jupyter Notebooks with technical deep-dives
```
---

## 📈 Business Impact & ROI
* This model provides evidence-based insights into the effectiveness of risk management processes. By automating the "Data-to-Insight" pipeline, it bridges the gap between clinical/operational data and tangible financial liability, supporting:
* **Reduced Claims Leakage**: Identifying outliers earlier in the lifecycle.
* **Regulatory Compliance**: Ensuring adherence to frameworks like the ACT Workers Compensation Act.
* **Cross-Functional Value**: Translating complex technical findings into clear, concise recommendations for senior stakeholders.

##👤 Contact & Portfolio
Aayush Yagol Strategic Data Analyst | Master of IT | 📍 Canberra, ACT

🌐 aayushyagol.com

🔗 LinkedIn | GitHub
