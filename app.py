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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
}

[data-testid="stSidebar"] {
    min-width: 300px;
    max-width: 300px;
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}

/* Sidebar is fixed open: no collapse control, no way to hide it */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp { background-color: #f5f7fa; }
[data-testid="stAppViewContainer"] { color: #101828; }

.hero {
    text-align: center;
    padding: 8px 0 6px;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    margin: 0;
}
.hero-title .hero-accent { color: #00a382; }
.page-intro {
    color: #475569;
    font-size: 1rem;
    line-height: 1.65;
    max-width: 680px;
    margin: 10px auto 4px;
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 36px 0 18px;
}
.section-divider-title {
    color: #0f172a;
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    white-space: nowrap;
}
.section-divider-rule {
    flex: 1;
    height: 1px;
    background: #dbe3ec;
}

.sidebar-section-label {
    display: flex;
    align-items: center;
    font-size: 1.05rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #0f172a;
    margin: 24px 0 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #00a38233;
}

.param-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #334155;
    margin-bottom: 4px;
}

.kpi-accent-card {
    background: linear-gradient(135deg, #ecfdf6, #eaf3ff);
    border: 1px solid #00a38233;
    border-left: 4px solid #00a382;
    border-radius: 10px;
    padding: 18px 22px;
    height: 100%;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 18px 20px;
    height: 100%;
    text-align: center;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05);
}
.card-label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2.3rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 10px;
}
.kpi-teal { color: #00a382; }
.badge-low {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #00a3821a;
    border: 1px solid #00a38255;
    color: #00785f;
    border-radius: 4px;
    padding: 4px 11px;
    font-size: 0.76rem;
    font-weight: 700;
}
.badge-moderate {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #f59e0b1a;
    border: 1px solid #f59e0b55;
    color: #92400e;
    border-radius: 4px;
    padding: 4px 11px;
    font-size: 0.76rem;
    font-weight: 700;
}
.badge-high {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #ef44441a;
    border: 1px solid #ef444455;
    color: #b91c1c;
    border-radius: 4px;
    padding: 4px 11px;
    font-size: 0.76rem;
    font-weight: 700;
}
.kpi-stat-val {
    font-size: 1.9rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    line-height: 1;
    margin: 6px 0 4px;
}
.kpi-stat-sub { color: #64748b; font-size: 0.76rem; }
.kpi-context { color: #64748b; font-size: 0.8rem; margin-top: 6px; }

.risk-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 10px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05);
}
.risk-bar-track {
    height: 9px;
    background: #e6ebf2;
    border-radius: 5px;
    overflow: hidden;
    margin: 8px 0 6px;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 16px;
    height: 100%;
    box-shadow: 0 1px 3px rgba(15,23,42,0.05);
}
.metric-val {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f172a;
    margin: 4px 0;
}
.metric-context {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 4px;
    line-height: 1.45;
}

.fi-context {
    font-size: 0.85rem;
    color: #475569;
    line-height: 1.6;
    padding: 14px 18px;
    background: #f8fafc;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    margin-top: 14px;
}

.info-icon {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 19px;
    height: 19px;
    margin-left: 6px;
    flex-shrink: 0;
    border-radius: 50%;
    background: #e2e8f0;
    color: #334155;
    font-size: 0.74rem;
    font-weight: 700;
    font-style: normal;
    cursor: help;
    vertical-align: middle;
    transition: background-color 0.12s ease, color 0.12s ease, transform 0.12s ease;
}
.info-icon:hover,
.info-icon:focus {
    background: #00a382;
    color: #ffffff;
    transform: scale(1.12);
    outline: none;
}
.info-icon .tooltip-text {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    top: 130%;
    bottom: auto;
    right: -6px;
    left: auto;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    text-align: left;
    padding: 14px 16px;
    border-radius: 10px;
    font-size: 0.82rem;
    font-weight: 400;
    line-height: 1.65;
    width: 220px;
    box-shadow: 0 12px 32px rgba(15,23,42,0.18);
    transition: opacity 0.1s ease;
    z-index: 9999;
    text-transform: none;
    letter-spacing: normal;
}
.info-icon:hover .tooltip-text,
.info-icon:focus .tooltip-text {
    visibility: visible;
    opacity: 1;
}

/* Lift the whole row containing a hovered/focused info-icon into its own
   stacking context so its tooltip always paints above later sibling rows
   (e.g. the next slider's tick-bar labels) — z-index on the tooltip alone
   isn't enough since none of Streamlit's own row wrappers set z-index, so
   z-index:auto siblings simply paint in DOM order regardless of the
   tooltip's own z-index. */
[data-testid="element-container"]:has(.info-icon) {
    position: relative;
    z-index: 10;
}
[data-testid="element-container"]:has(.info-icon:hover),
[data-testid="element-container"]:has(.info-icon:focus) {
    z-index: 9999;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100vw;
    background-color: #ffffff;
    color: #64748b;
    text-align: center;
    padding: 12px 0;
    font-size: 0.78rem;
    border-top: 1px solid #e2e8f0;
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


def get_risk_percentile(prediction: float, portfolio_stats: dict) -> float:
    """
    Single source of truth. Piecewise-linearly interpolates the prediction
    against five known portfolio percentile anchors (0th anchored at €0).
    Returns a continuous float in [0, 100] — round only when formatting
    for display, never before deriving the band label below.
    """
    anchor_percentiles = [0, 25, 50, 75, 90, 95]
    anchor_values = [
        0.0,
        portfolio_stats['p25_pure_premium'],
        portfolio_stats['median_pure_premium'],
        portfolio_stats['p75_pure_premium'],
        portfolio_stats['p90_pure_premium'],
        portfolio_stats['p95_pure_premium'],
    ]
    if prediction > anchor_values[-1]:
        return 100.0
    return float(np.interp(prediction, anchor_values, anchor_percentiles))


def get_risk_tier(percentile: float) -> tuple:
    if percentile <= 33:
        return 'LOW', '#00d4aa', 'badge-low'
    elif percentile <= 66:
        return 'MODERATE', '#f59e0b', 'badge-moderate'
    return 'HIGH', '#ef4444', 'badge-high'


def get_percentile_band(percentile: float) -> str:
    """
    Derives the band label FROM the percentile above — never computed
    independently again. Takes the percentile itself, not
    (prediction, portfolio_stats), so it is structurally impossible to
    call it with independently-derived data.
    """
    if percentile < 25: return 'Below 25th'
    if percentile < 50: return '25th – 50th'
    if percentile < 75: return '50th – 75th'
    if percentile < 90: return '75th – 90th'
    if percentile < 95: return '90th – 95th'
    return 'Above 95th'


def section_header(title: str) -> str:
    return f"""
    <div class="section-divider">
        <span class="section-divider-title">{title}</span>
        <div class="section-divider-rule"></div>
    </div>"""


def info_icon(text: str) -> str:
    escaped = text.replace('"', '&quot;')
    return f'<span class="info-icon" tabindex="0">?<span class="tooltip-text">{escaped}</span></span>'


def metric_card(label: str, value: str, context: str, info: str = None) -> str:
    label_html = f"{label}{info_icon(info)}" if info else label
    return f"""
    <div class="metric-card">
        <div class="card-label">{label_html}</div>
        <div class="metric-val">{value}</div>
        <div class="metric-context">{context}</div>
    </div>"""


# 4. Sidebar
st.sidebar.markdown("""
<div class="sidebar-section-label">Policy Parameters</div>
""", unsafe_allow_html=True)


def param_header(label: str, info: str) -> None:
    st.sidebar.markdown(
        f"<p class='param-header'>{label}{info_icon(info)}</p>",
        unsafe_allow_html=True,
    )


def get_user_input():
    param_header("Driver Age", "Chronological age of the policyholder; a primary factor in actuarial risk profiling.")
    driv_age = st.sidebar.slider("DrivAge", 18, 100, 35, label_visibility="collapsed")

    param_header("Bonus / Malus (Risk Index)", "The French CRM score: below 100 indicates a bonus; above 100 indicates a malus (high risk).")
    bonus_malus = st.sidebar.slider("BonusMalus", 50, 350, 50, label_visibility="collapsed")

    param_header("Vehicle Age (Years)", "Age of the vehicle, influencing mechanical reliability and claim severity trends.")
    veh_age = st.sidebar.slider("VehAge", 0, 50, 5, label_visibility="collapsed")

    param_header("Vehicle Power", "The engine power rating; often correlated with higher frequency in speed-related events.")
    veh_power = st.sidebar.slider("VehPower", 4, 15, 6, label_visibility="collapsed")

    param_header("Inhabitant Density", "Population density per km²; historically correlates with higher collision frequency.")
    density = st.sidebar.slider("Density", 0, 30000, 1000, label_visibility="collapsed")

    param_header("Geographic Area", "Zonal classification: A (rural) through F (urban core).")
    area = st.sidebar.selectbox("Area", ("A", "B", "C", "D", "E", "F"), index=2, label_visibility="collapsed")

    param_header("Vehicle Brand", "Anonymised vehicle brand code from the source dataset — categories are not identified manufacturers, just a proxy grouping.")
    veh_brand = st.sidebar.selectbox("VehBrand", ("B1", "B2", "B3", "B4", "B5", "B6", "B10", "B11", "B12", "B13", "B14"), label_visibility="collapsed")

    param_header("Fuel Type", "Diesel often correlates with high-mileage commercial usage patterns.")
    veh_gas = st.sidebar.radio("VehGas", ("Regular", "Diesel"), label_visibility="collapsed")

    param_header("Administrative Region", "Official French administrative zone classification code.")
    region = st.sidebar.selectbox("Region", ("R24", "R82", "R22", "R72", "R31", "R91", "R52", "R93", "R11", "R53", "R54", "R73", "R42", "R41", "R83", "R94", "R43", "R26", "R25", "R21", "R23"), label_visibility="collapsed")

    return pd.DataFrame({
        'VehPower': veh_power, 'VehAge': veh_age, 'DrivAge': driv_age,
        'BonusMalus': bonus_malus, 'Density': density, 'Area': area,
        'VehBrand': veh_brand, 'VehGas': veh_gas, 'Region': region
    }, index=[0])


model_df = get_user_input()

st.sidebar.markdown("""
<div style="margin-top:20px;padding-top:14px;border-top:1px solid #e2e8f0;
            text-align:center;font-size:0.72rem;color:#94a3b8;line-height:1.7;">
    Built by
    <a href="https://aayushyagol.com" target="_blank"
       style="color:#00a382;text-decoration:none;">Aayush Yagol</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/ayusyagol11/claims-liability-predictor" target="_blank"
       style="color:#64748b;text-decoration:none;">GitHub</a><br>
    freMTPL2 · 678K policies
</div>
""", unsafe_allow_html=True)

# 5. Main content
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

st.markdown(
    '<div class="hero">'
    '<h1 class="hero-title">Motor <span class="hero-accent">Claims Liability</span> Predictor</h1>'
    '<p class="page-intro">This dashboard estimates the expected annual claims cost '
    'for a car insurance policy, using a Tweedie regression model trained on ~678,000 '
    'real French motor insurance policies. Adjust the parameters in the sidebar to see '
    'how driver profile, vehicle, and location shape the predicted liability — and where '
    'it lands relative to the rest of the portfolio. Trained on the public '
    '<strong>freMTPL2</strong> French motor dataset (EUR) — the same methodology '
    'transfers directly to an AUD motor book with local recalibration.</p>'
    '</div>',
    unsafe_allow_html=True,
)

prediction = model.predict(model_df)[0]
pred_percentile = get_risk_percentile(prediction, portfolio_stats)   # float, e.g. 42.7
risk_label, risk_color, badge_class = get_risk_tier(pred_percentile)
band_label = get_percentile_band(pred_percentile)                     # derived FROM pred_percentile, not recomputed

int_part = f"{int(prediction):,}"
dec_part = f"{prediction:.2f}".split('.')[1]

# ── Section 1: Risk Assessment ────────────────────────────────────────────────
st.markdown(section_header("Risk Assessment"), unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"""
    <div class="kpi-accent-card">
        <div class="card-label">Expected Annual Liability{info_icon("The model's best estimate of this policy's claims cost over a year, based on its risk profile — actuaries call this the 'Pure Premium'. It's before any margin, expenses, or profit loading are added to reach an actual sale price.")}</div>
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
        <div class="card-label">Percentile{info_icon("How this policy's predicted cost compares to the rest of the portfolio. A percentile of 80 means this policy is predicted to cost more than 80% of policies in the reference portfolio.")}</div>
        <div class="kpi-stat-val">{round(pred_percentile)}<span style="font-size:1rem;color:#64748b;">th</span></div>
        <div class="kpi-stat-sub">{band_label} band</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="card-label">Risk Band{info_icon("A simplified Low / Moderate / High grouping of the percentile score — Low is the bottom third of predicted costs, Moderate the middle third, High the top third.")}</div>
        <div class="kpi-stat-val" style="color:{risk_color};font-size:1.3rem;margin-top:8px;">
            {risk_label}
        </div>
        <div class="kpi-stat-sub">LOW / MODERATE / HIGH</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="risk-card">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <span class="card-label">Risk Spectrum{info_icon("A visual version of the percentile score above — the further right the bar, the higher this policy's predicted cost relative to the rest of the portfolio.")}</span>
        <span style="font-size:0.65rem;font-weight:700;color:{risk_color};">
            {round(pred_percentile)} / 100
        </span>
    </div>
    <div class="risk-bar-track">
        <div style="width:{pred_percentile}%;height:100%;
                    background:linear-gradient(90deg,#00d4aa,#0088ff);
                    border-radius:4px;"></div>
    </div>
    <div style="display:flex;justify-content:space-between;">
        <span style="font-size:0.6rem;color:#94a3b8;">Low (&lt;p25)</span>
        <span style="font-size:0.6rem;color:#94a3b8;">Moderate (p25–p75)</span>
        <span style="font-size:0.6rem;color:#94a3b8;">High (&gt;p75)</span>
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
        f"Primary metric · p={metrics['tweedie_power']} · native loss for zero-inflated data",
        info="The model's primary accuracy score — lower is better. It's the standard way actuaries measure fit for claims data, where most policies cost $0 and a few cost a lot; a plain accuracy percentage doesn't work well for that shape of data."
    ), unsafe_allow_html=True)

with m2:
    st.markdown(metric_card(
        "MAE",
        f"€{metrics['mae']:,.2f}",
        f"Test set: {metrics['test_size']:,} policies · zero-inflated, expected high",
        info="On average, how far a single prediction is from the actual claim cost. This number looks large mainly because most real policies have $0 in claims while the model always predicts a small positive number — that's expected for this kind of data, not a flaw."
    ), unsafe_allow_html=True)

with m3:
    st.markdown(metric_card(
        "RMSE",
        f"€{metrics['rmse']:,.2f}",
        "Driven by high-severity tail claims (&lt;1% of policies)",
        info="Similar to MAE, but penalises big misses more heavily — it's higher mainly because of a small number of very expensive claims in the data, same as most real insurance portfolios."
    ), unsafe_allow_html=True)

with m4:
    st.markdown(metric_card(
        "Explained Variance",
        f"{metrics['explained_variance']:.4f}",
        "Expected near-zero for TPL pricing models",
        info="Normally this measures how much of the outcome a model explains — but for this type of zero-inflated claims data it's expected to sit near zero even for a well-built model. It is not a sign the model is broken; Tweedie Deviance above is the right metric to judge accuracy by."
    ), unsafe_allow_html=True)

fi_df = pd.DataFrame({
    'Feature': feat_imp['features'],
    'Importance': feat_imp['importance_mean']
}).sort_values('Importance', ascending=True)

fig = px.bar(
    fi_df, x='Importance', y='Feature', orientation='h',
    color='Importance',
    color_continuous_scale=[[0, '#ef4444'], [0.499, '#ef4444'],
                             [0.501, '#00d4aa'], [1, '#00d4aa']],
    color_continuous_midpoint=0,
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#64748b',
    height=380,
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=8, b=0),
)
fig.update_xaxes(gridcolor='#e2e8f0', zerolinecolor='#e2e8f0')
fig.update_yaxes(gridcolor='rgba(0,0,0,0)')

st.markdown(
    f'<div class="card-label" style="font-size:0.8rem;text-transform:none;'
    f'letter-spacing:normal;color:#0f172a;margin:20px 0 8px;">'
    f'Feature Importance (Permutation Method)'
    f'{info_icon("Which policy details influence the prediction most, measured by testing how much accuracy drops when each one is scrambled. Bars further right had a bigger effect on the prediction.")}'
    f'</div>',
    unsafe_allow_html=True,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="fi-context">
    <strong style="color:#1e293b;">BonusMalus</strong> dominates with an importance score
    ~14&times; greater than the next feature (VehPower). This aligns with actuarial convention
    — the CRM score is the single strongest predictor of individual claim liability.
    Density carries little independent predictive signal once BonusMalus, Area, and VehPower are already in the model.
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Created by
    <a href="https://aayushyagol.com" target="_blank"
       style="color:#00a382;text-decoration:none;">Aayush Yagol</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/ayusyagol11/claims-liability-predictor" target="_blank"
       style="color:#64748b;text-decoration:none;">GitHub</a>
</div>
""", unsafe_allow_html=True)
