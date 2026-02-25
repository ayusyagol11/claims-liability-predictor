import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. Page Configuration & Global Styling
st.set_page_config(page_title="Insurance Claims Predictor", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Open Sans', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        min-width: 480px;
        max-width: 480px;
        z-index: 100; /* Lower than the footer */
    }
    
    .param-header {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 2px;
        color: white;
    }
    
    .parameter-desc {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 0px;
        margin-bottom: 15px;
        line-height: 1.2;
    }

    /* Green Predict Button */
    div.stButton > button:first-child {
        width: 100%;
        height: 3.5em;
        font-size: 1.4rem !important;
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        font-weight: 700;
        margin-top: 20px;
        border: none;
    }

    /* Fixed Footer - High Z-Index to stay on top of Sidebar */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw; /* Spans full viewport width */
        background-color: #0e1117;
        color: #888;
        text-align: center;
        padding: 15px 0;
        font-size: 0.85rem;
        border-top: 1px solid #333;
        z-index: 9999; /* Higher than any other element */
    }
    
    /* Pushing content up so it's not hidden behind footer */
    .main-content {
        margin-bottom: 80px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Precise Strategic Narrative
st.title("🛡️ Predictive Claims Liability Dashboard")
st.markdown("""
    This analytical tool utilizes a **Tweedie Regressor** to estimate the **Pure Premium** (Expected Annual Liability) 
    at the individual policy level. By synthesizing multi-dimensional risk features—including 
    actuarial risk scores, geographic density, and vehicle specifications—this dashboard identifies high-signal 
    liability indicators early in the claim lifecycle.
""")

# 3. Load Model
@st.cache_resource
def load_model():
    return joblib.load('tweedie_model.pkl')

model = load_model()

# 4. Input Policy Parameters
st.sidebar.header("Input Policy Parameters")

def get_user_input():
    # Sequence of parameters
    st.sidebar.markdown("<p class='param-header'>Driver Age</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Chronological age of the policyholder; a primary factor in actuarial risk profiling.</p>", unsafe_allow_html=True)
    driv_age = st.sidebar.slider("DrivAge", 18, 100, 35, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Bonus/Malus (Risk Index)</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>The French CRM score: <100 indicates a bonus; >100 indicates a malus (high risk).</p>", unsafe_allow_html=True)
    bonus_malus = st.sidebar.slider("BonusMalus", 50, 350, 50, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Vehicle Age (Years)</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Age of the vehicle, influencing mechanical reliability and claim severity trends.</p>", unsafe_allow_html=True)
    veh_age = st.sidebar.slider("VehAge", 0, 50, 5, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Vehicle Power</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>The engine power rating; often correlated with higher frequency in speed-related events.</p>", unsafe_allow_html=True)
    veh_power = st.sidebar.number_input("VehPower", 4, 15, 6, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Inhabitant Density</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Population density per km²; historically correlates with higher collision frequency.</p>", unsafe_allow_html=True)
    density = st.sidebar.number_input("Density", 0, 30000, 1000, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Geographic Area</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Zonal classification ranging from 'A' (rural) to 'F' (urban core).</p>", unsafe_allow_html=True)
    area = st.sidebar.selectbox("Area", ("A", "B", "C", "D", "E", "F"), index=2, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Vehicle Brand</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Manufacturer categorization; proxy for parts replacement cost and reliability.</p>", unsafe_allow_html=True)
    veh_brand = st.sidebar.selectbox("VehBrand", ("B1", "B2", "B3", "B4", "B5", "B6", "B10", "B11", "B12", "B13", "B14"), label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Fuel Type</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>The energy source; Diesel often correlates with high-mileage commercial usage.</p>", unsafe_allow_html=True)
    veh_gas = st.sidebar.radio("VehGas", ("Regular", "Diesel"), label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Administrative Region</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>The regional classification code based on official French administrative zones.</p>", unsafe_allow_html=True)
    region = st.sidebar.selectbox("Region", ("R24", "R82", "R22", "R72", "R31", "R91", "R52", "R93", "R11", "R53", "R54", "R73", "R42", "R41", "R83", "R94", "R43", "R26", "R25", "R21", "R23"), label_visibility="collapsed")

    # Maintain sequence for Display
    display_data = {
        'Driver Age (year)': driv_age,
        'Bonus/Malus (Risk Index)': bonus_malus,
        'Vehicle Age (Years)': veh_age,
        'Vehicle Power': veh_power,
        'Inhabitant Density': density,
        'Geographic Area': area,
        'Vehicle Brand': veh_brand,
        'Fuel Type': veh_gas,
        'Administrative Region': region
    }
    
    # Feature names must match training columns
    model_data = {
        'VehPower': veh_power, 'VehAge': veh_age, 'DrivAge': driv_age, 
        'BonusMalus': bonus_malus, 'Density': density, 'Area': area, 
        'VehBrand': veh_brand, 'VehGas': veh_gas, 'Region': region
    }
    
    return pd.DataFrame(display_data, index=[0]), pd.DataFrame(model_data, index=[0])

display_df, model_df = get_user_input()

# 5. Main Content Wrapper
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# 5a. Analytical Policy Summary Table
st.subheader("📊 Analytical Policy Summary")
styled_table = display_df.style.set_properties(**{
    'background-color': 'black',
    'color': 'white',
    'border-color': '#444',
    'font-size': '1.1rem',
    'text-align': 'center'
}).hide(axis='index')

st.table(styled_table)

# 5b. Fixed Gradient Risk Profile
st.markdown("### **Relative Risk Profile**")
risk_val = model_df['BonusMalus'][0]
risk_percent = min(max((risk_val - 50) / 300 * 100, 0), 100)

st.markdown(f"""
    <div style="width: 100%; background-color: #333; border-radius: 10px; height: 35px; margin: 10px 0; overflow: hidden;">
        <div style="width: {risk_percent}%; height: 100%; 
             background: linear-gradient(90deg, #28a745 0%, #ffc107 50%, #dc3545 100%); 
             background-attachment: fixed;
             border-right: 4px solid white;">
        </div>
    </div>
    <p style="text-align: right; font-weight: bold; color: white;">Risk Score Intensity: {int(risk_percent)}%</p>
    """, unsafe_allow_html=True)

# 5c. Prediction Execution
if st.button("Predict Annual Liability"):
    prediction = model.predict(model_df)[0]
    st.markdown("<h2 style='text-align: center; color: #28a745; margin-top: 30px;'>Calculated Expected Claim Liability</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 5rem; color: white;'>€{prediction:,.2f}</h1>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 6. Global Fixed Footer (Floating over Sidebar)
st.markdown(f"""
    <div class="footer">
        Created by Aayush Yagol
    </div>
    """, unsafe_allow_html=True)