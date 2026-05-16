import streamlit as st
import pandas as pd
import joblib
import numpy as np
import json
import plotly.express as px

# 1. Page Configuration & Global Styling
st.set_page_config(page_title="Claims Liability Dashboard", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
}

[data-testid="stSidebar"] {
    min-width: 280px;
    max-width: 280px;
    background-color: #0a1220;
}

.stApp { background-color: #080c14; }

.section-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0 16px;
}
.section-divider-title {
    color: #cdd9e5;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    white-space: nowrap;
}
.section-divider-rule {
    flex: 1;
    height: 1px;
    background: #1e2d45;
}

.sidebar-logo {
    padding: 20px 20px 16px;
    border-bottom: 1px solid #1e2d45;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}
.sidebar-logo-mark {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #00d4aa, #0088ff);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #fff;
    font-weight: 900;
    flex-shrink: 0;
}
.sidebar-logo-title {
    color: #fff;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.sidebar-logo-sub {
    color: #4a6080;
    font-size: 0.62rem;
    margin-top: 2px;
}
.sidebar-section-label {
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #2a4060;
    margin-bottom: 14px;
    padding-bottom: 6px;
    border-bottom: 1px solid #12202e;
}

.param-header {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #4a6080;
    margin-bottom: 2px;
}
.parameter-desc {
    font-size: 0.62rem;
    color: #2a4060;
    margin-top: 0;
    margin-bottom: 5px;
    line-height: 1.3;
}

.kpi-accent-card {
    background: linear-gradient(135deg, #0d2137, #0a1a2e);
    border: 1px solid #00d4aa33;
    border-left: 3px solid #00d4aa;
    border-radius: 8px;
    padding: 16px 20px;
    height: 100%;
}
.kpi-card {
    background: #0f1623;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 16px 20px;
    height: 100%;
    text-align: center;
}
.card-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #4a6080;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 10px;
}
.kpi-teal { color: #00d4aa; }
.badge-low {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #00d4aa14;
    border: 1px solid #00d4aa44;
    color: #00d4aa;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.65rem;
    font-weight: 700;
}
.badge-moderate {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #f59e0b14;
    border: 1px solid #f59e0b44;
    color: #f59e0b;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.65rem;
    font-weight: 700;
}
.badge-high {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #ef444414;
    border: 1px solid #ef444444;
    color: #ef4444;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.65rem;
    font-weight: 700;
}
.kpi-stat-val {
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.5px;
    line-height: 1;
    margin: 6px 0 4px;
}
.kpi-stat-sub { color: #4a6080; font-size: 0.62rem; }
.kpi-context { color: #4a6080; font-size: 0.65rem; margin-top: 6px; }

.risk-card {
    background: #0f1623;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 14px 18px;
    margin-top: 10px;
}
.risk-bar-track {
    height: 8px;
    background: #1a2840;
    border-radius: 4px;
    overflow: hidden;
    margin: 8px 0 6px;
}

.metric-card {
    background: #0f1623;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 14px 16px;
    height: 100%;
}
.metric-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #cdd9e5;
    margin: 4px 0;
}
.metric-context {
    font-size: 0.65rem;
    color: #4a6080;
    margin-top: 4px;
    line-height: 1.4;
}

.fi-context {
    font-size: 0.7rem;
    color: #4a6080;
    line-height: 1.6;
    padding: 12px 16px;
    background: #080c14;
    border-radius: 6px;
    border: 1px solid #12202e;
    margin-top: 14px;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100vw;
    background-color: #080c14;
    color: #4a6080;
    text-align: center;
    padding: 12px 0;
    font-size: 0.65rem;
    border-top: 1px solid #1e2d45;
    z-index: 9999;
}
.main-content { margin-bottom: 80px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# 2. Load Model & Artifacts
@st.cache_resource
def load_model():
    return joblib.load('model/tweedie_model.pkl')

@st.cache_data
def load_artifacts():
    with open('model/model_metrics.json', 'r') as f:
        metrics = json.load(f)
    with open('model/portfolio_stats.json', 'r') as f:
        stats = json.load(f)
    with open('model/feature_importance.json', 'r') as f:
        feat_imp = json.load(f)
    return metrics, stats, feat_imp

model = load_model()
metrics, portfolio_stats, feat_imp = load_artifacts()


def get_risk_percentile(prediction: float, portfolio_stats: dict) -> int:
    thresholds = [
        portfolio_stats['p25_pure_premium'],
        portfolio_stats['median_pure_premium'],
        portfolio_stats['p75_pure_premium'],
        portfolio_stats['p90_pure_premium'],
        portfolio_stats['p95_pure_premium'],
    ]
    return min(sum(1 for t in thresholds if prediction >= t) * 20, 100)


def get_risk_tier(percentile: int) -> tuple:
    if percentile <= 33:
        return 'LOW', '#00d4aa', 'badge-low'
    elif percentile <= 66:
        return 'MODERATE', '#f59e0b', 'badge-moderate'
    return 'HIGH', '#ef4444', 'badge-high'


def get_percentile_band(prediction: float, portfolio_stats: dict) -> str:
    bins = sorted([
        portfolio_stats['p25_pure_premium'],
        portfolio_stats['median_pure_premium'],
        portfolio_stats['p75_pure_premium'],
        portfolio_stats['p90_pure_premium'],
        portfolio_stats['p95_pure_premium'],
    ])
    labels = ['Below 25th', '25th – 50th', '50th – 75th',
              '75th – 90th', '90th – 95th', 'Above 95th']
    return labels[min(np.searchsorted(bins, prediction, side='right'), 5)]


def section_header(title: str) -> str:
    return f"""
    <div class="section-divider">
        <span class="section-divider-title">{title}</span>
        <div class="section-divider-rule"></div>
    </div>"""


def metric_card(label: str, value: str, context: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="card-label">{label}</div>
        <div class="metric-val">{value}</div>
        <div class="metric-context">{context}</div>
    </div>"""


# 4. Sidebar
st.sidebar.markdown("""
<div class="sidebar-logo">
    <div class="sidebar-logo-mark">&#x2B21;</div>
    <div>
        <div class="sidebar-logo-title">Claims Liability</div>
        <div class="sidebar-logo-sub">Tweedie Regressor · p=1.5</div>
    </div>
</div>
<div class="sidebar-section-label">Policy Parameters</div>
""", unsafe_allow_html=True)


def get_user_input():
    st.sidebar.markdown("<p class='param-header'>Driver Age</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Chronological age of the policyholder; a primary factor in actuarial risk profiling.</p>", unsafe_allow_html=True)
    driv_age = st.sidebar.slider("DrivAge", 18, 100, 35, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Bonus / Malus (Risk Index)</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>The French CRM score: &lt;100 indicates a bonus; &gt;100 indicates a malus (high risk).</p>", unsafe_allow_html=True)
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
    st.sidebar.markdown("<p class='parameter-desc'>Zonal classification: A (rural) → F (urban core).</p>", unsafe_allow_html=True)
    area = st.sidebar.selectbox("Area", ("A", "B", "C", "D", "E", "F"), index=2, label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Vehicle Brand</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Manufacturer categorisation; proxy for parts cost and reliability.</p>", unsafe_allow_html=True)
    veh_brand = st.sidebar.selectbox("VehBrand", ("B1", "B2", "B3", "B4", "B5", "B6", "B10", "B11", "B12", "B13", "B14"), label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Fuel Type</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Diesel often correlates with high-mileage commercial usage patterns.</p>", unsafe_allow_html=True)
    veh_gas = st.sidebar.radio("VehGas", ("Regular", "Diesel"), label_visibility="collapsed")

    st.sidebar.markdown("<p class='param-header'>Administrative Region</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='parameter-desc'>Official French administrative zone classification code.</p>", unsafe_allow_html=True)
    region = st.sidebar.selectbox("Region", ("R24", "R82", "R22", "R72", "R31", "R91", "R52", "R93", "R11", "R53", "R54", "R73", "R42", "R41", "R83", "R94", "R43", "R26", "R25", "R21", "R23"), label_visibility="collapsed")

    return pd.DataFrame({
        'VehPower': veh_power, 'VehAge': veh_age, 'DrivAge': driv_age,
        'BonusMalus': bonus_malus, 'Density': density, 'Area': area,
        'VehBrand': veh_brand, 'VehGas': veh_gas, 'Region': region
    }, index=[0])


model_df = get_user_input()

st.sidebar.markdown("""
<div style="margin-top:20px;padding-top:14px;border-top:1px solid #1e2d45;
            text-align:center;font-size:0.6rem;color:#2a4060;line-height:1.7;">
    Built by
    <a href="https://aayushyagol.com" target="_blank"
       style="color:#00d4aa88;text-decoration:none;">Aayush Yagol</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/ayusyagol11/claims-liability-predictor" target="_blank"
       style="color:#4a6080;text-decoration:none;">GitHub</a><br>
    freMTPL2 · 678K policies
</div>
""", unsafe_allow_html=True)

# 5. Main content
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

prediction = model.predict(model_df)[0]
pred_percentile = get_risk_percentile(prediction, portfolio_stats)
risk_label, risk_color, badge_class = get_risk_tier(pred_percentile)
band_label = get_percentile_band(prediction, portfolio_stats)

int_part = f"{int(prediction):,}"
dec_part = f"{prediction:.2f}".split('.')[1]

# ── Section 1: Risk Assessment ────────────────────────────────────────────────
st.markdown(section_header("Risk Assessment"), unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"""
    <div class="kpi-accent-card">
        <div class="card-label">Expected Annual Liability</div>
        <div class="kpi-value">€<span class="kpi-teal">{int_part}</span>.{dec_part}</div>
        <div style="display:flex;align-items:center;gap:10px;margin-top:10px;">
            <span class="{badge_class}">
                <span style="width:6px;height:6px;border-radius:50%;background:currentColor;
                             display:inline-block;flex-shrink:0;"></span>
                {risk_label.title()} Risk
            </span>
            <span class="kpi-context">
                Portfolio median: €{portfolio_stats['median_pure_premium']:,.2f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="card-label">Portfolio Percentile</div>
        <div class="kpi-stat-val">{pred_percentile}<span style="font-size:1rem;color:#4a6080;">th</span></div>
        <div class="kpi-stat-sub">{band_label} band</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="card-label">Risk Band</div>
        <div class="kpi-stat-val" style="color:{risk_color};font-size:1.3rem;margin-top:8px;">
            {risk_label}
        </div>
        <div class="kpi-stat-sub">LOW / MODERATE / HIGH</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="risk-card">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="card-label">Risk Spectrum</span>
        <span style="font-size:0.65rem;font-weight:700;color:{risk_color};">
            {pred_percentile} / 100
        </span>
    </div>
    <div class="risk-bar-track">
        <div style="width:{pred_percentile}%;height:100%;
                    background:linear-gradient(90deg,#00d4aa,#0088ff);
                    border-radius:4px;"></div>
    </div>
    <div style="display:flex;justify-content:space-between;">
        <span style="font-size:0.6rem;color:#2a4060;">Low (&lt;p25)</span>
        <span style="font-size:0.6rem;color:#2a4060;">Moderate (p25–p75)</span>
        <span style="font-size:0.6rem;color:#2a4060;">High (&gt;p75)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Section 2: Model Performance ─────────────────────────────────────────────
st.markdown(section_header("Model Performance"), unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(metric_card(
        "Tweedie Deviance",
        f"{metrics['mean_tweedie_deviance']:.4f}",
        f"Primary metric · p={metrics['tweedie_power']}<br>"
        "Native loss for zero-inflated data"
    ), unsafe_allow_html=True)

with m2:
    st.markdown(metric_card(
        "MAE",
        f"€{metrics['mae']:,.2f}",
        f"Test set: {metrics['test_size']:,} policies<br>"
        "Zero-inflated — expected high"
    ), unsafe_allow_html=True)

with m3:
    st.markdown(metric_card(
        "RMSE",
        f"€{metrics['rmse']:,.2f}",
        "Driven by high-severity<br>tail claims (&lt;1% of policies)"
    ), unsafe_allow_html=True)

with m4:
    st.markdown(metric_card(
        "Explained Variance",
        f"{metrics['explained_variance']:.4f}",
        "Expected near-zero<br>for TPL pricing models"
    ), unsafe_allow_html=True)

fi_df = pd.DataFrame({
    'Feature': feat_imp['features'],
    'Importance': feat_imp['importance_mean']
}).sort_values('Importance', ascending=True)

fig = px.bar(
    fi_df, x='Importance', y='Feature', orientation='h',
    title='Feature Importance (Permutation Method)',
    color='Importance',
    color_continuous_scale=[[0, '#ef4444'], [0.499, '#ef4444'],
                             [0.501, '#00d4aa'], [1, '#00d4aa']],
    color_continuous_midpoint=0,
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#8899aa',
    title_font_size=14,
    title_font_color='#cdd9e5',
    height=380,
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=40, b=0),
)
fig.update_xaxes(gridcolor='#1e2d45', zerolinecolor='#1e2d45')
fig.update_yaxes(gridcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="fi-context">
    <strong style="color:#8899aa;">BonusMalus</strong> dominates with an importance score
    ~14&times; greater than the next feature (VehPower). This aligns with actuarial convention
    — the CRM score is the single strongest predictor of individual claim liability.
    Density shows a slight negative permutation score, suggesting minor collinearity with Area.
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Created by
    <a href="https://aayushyagol.com" target="_blank"
       style="color:#00d4aa88;text-decoration:none;">Aayush Yagol</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/ayusyagol11/claims-liability-predictor" target="_blank"
       style="color:#4a6080;text-decoration:none;">GitHub</a>
</div>
""", unsafe_allow_html=True)
