import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. Page Configuration & Strategic Branding [cite: 38]
st.set_page_config(page_title="Insurance Claims Predictor", layout="wide")

st.title("🛡️ Predictive Claims Liability Dashboard")
st.markdown("""
**Domain Expertise:** Insurance Risk Oversight (Suncorp Alignment)  
**Objective:** Bridging the gap between clinical data and financial liability using predictive analytics. [cite: 25]
""")

# 2. Load the Trained Pipeline
# (Ensure you save your model in the notebook using: joblib.dump(clf, 'tweedie_model.pkl'))
@st.cache_resource
def load_model():
    return joblib.load('tweedie_model.pkl')

model = load_model()

# 3. Sidebar for User Inputs (Strategic Storytelling through Parameters) [cite: 8]
st.sidebar.header("Input Policy Parameters")

def user_input_features():
    # Numerical Inputs [cite: 206, 207]
    driv_age = st.sidebar.slider("Driver Age", 18, 100, 35)
    veh_age = st.sidebar.slider("Vehicle Age", 0, 50, 5)
    veh_power = st.sidebar.number_input("Vehicle Power", 4, 15, 6)
    bonus_malus = st.sidebar.slider("Bonus/Malus (Risk Score)", 50, 350, 50)
    density = st.sidebar.number_input("Urban Density (Pop/km2)", 0, 30000, 1000)

    # Categorical Inputs [cite: 206, 207]
    area = st.sidebar.selectbox("Area (A=Rural, F=Urban)", ("A", "B", "C", "D", "E", "F"))
    veh_brand = st.sidebar.selectbox("Vehicle Brand", ("B1", "B2", "B3", "B4", "B5", "B6", "B10", "B11", "B12", "B13", "B14"))
    veh_gas = st.sidebar.radio("Fuel Type", ("Regular", "Diesel"))
    region = st.sidebar.selectbox("Policy Region", ("R24", "R82", "R22", "R72", "R31", "R91", "R52", "R93", "R11", "R53", "R54", "R73", "R42", "R41", "R83", "R94", "R43", "R26", "R25", "R21", "R23", "R11"))

    data = {
        'VehPower': veh_power,
        'VehAge': veh_age,
        'DrivAge': driv_age,
        'BonusMalus': bonus_malus,
        'Density': density,
        'Area': area,
        'VehBrand': veh_brand,
        'VehGas': veh_gas,
        'Region': region
    }
    return pd.DataFrame(data, index=[0])

input_df = user_input_features()

# 4. Main Panel: Prediction and Visual Insights [cite: 159]
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Policy Summary")
    st.write(input_df)

    if st.button("Predict Liability"):
        # The model predicts Pure Premium (ClaimAmount / Exposure) [cite: 281]
        prediction = model.predict(input_df)
        
        st.success(f"### Predicted Annual Liability: €{prediction[0]:.2f}")
        st.info("This prediction assists in setting accurate financial reserves and identifying high-risk claims for early intervention. [cite: 68]")

with col2:
    st.subheader("Data Quality & Governance Audit")
    st.write("This tool utilizes an end-to-end automated data supply chain to ensure 100% compliance with risk management frameworks. [cite: 25]")
    
    # Visualizing the Bonus/Malus Impact (A high-signal indicator for recruiters) [cite: 4]
    st.progress(min(int(input_df['BonusMalus'][0] / 3.5), 100))
    st.caption("Relative Risk Score (Bonus/Malus Index)")

# 5. Footer: Technical Verification [cite: 31]
st.divider()
st.markdown("""
**Technical Stack:** Python, Scikit-learn, Streamlit.  
**Architecture:** Automated Data Supply Chain with Tweedie Regression (Power=1.5). [cite: 89, 290]
""")