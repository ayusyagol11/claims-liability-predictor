# UI Redesign — Claims Liability Predictive Dashboard

**Date:** 2026-05-16  
**Status:** Approved  
**Scope:** Full visual redesign of `app.py` (Streamlit). No model, data, or logic changes.

---

## 1. Design Direction

**Dark Fintech** — deep navy base with teal/blue gradient accents, inspired by Robinhood/Revolut.

| Token | Value |
|---|---|
| Page background | `#080c14` |
| Sidebar background | `#0a1220` |
| Card background | `#0f1623` |
| Border | `#1e2d45` |
| Primary accent (teal) | `#00d4aa` |
| Secondary accent (blue) | `#0088ff` |
| Accent gradient | `linear-gradient(90deg, #00d4aa, #0088ff)` |
| Text — primary | `#cdd9e5` |
| Text — secondary | `#8899aa` |
| Text — muted | `#4a6080` |
| Text — faint | `#2a4060` |
| Font | `'Inter', 'Segoe UI', -apple-system, sans-serif` |

Risk badge colours:
- Low risk: `#00d4aa` (teal), background `#00d4aa14`, border `#00d4aa44`
- Moderate risk: `#f59e0b` (amber)
- High risk: `#ef4444` (red)

---

## 2. Layout

**Slim sidebar + main content area.** No full-width header.

- Sidebar: `280px` fixed width (down from 480px). Replaces current `min-width/max-width: 480px` CSS.
- Main area: fills remaining viewport width, `padding: 24px 28px`, scrollable.
- Footer: fixed, full-width, `z-index: 9999`, same as current but restyled.
- Page config: `layout="wide"` retained.

### Sidebar structure (top to bottom)

1. **Logo block** — teal gradient icon mark + "Claims Liability" title + "Tweedie Regressor · p=1.5" subtitle. Separated from inputs by a bottom border.
2. **"Policy Parameters" section label** — small uppercase muted label.
3. **9 input controls** — each has a `param-label` (uppercase, small) and a `param-desc` (one-line explanation, very muted). Controls use collapsed `label_visibility="collapsed"` as now.
4. **Footer block** — "Built by Aayush Yagol · freMTPL2 · 678K policies" with GitHub and portfolio links. Pinned to the bottom of the sidebar via flex layout.

---

## 3. Main Content — Sections

Main content is divided into two named sections, each with a section header: a small uppercase title on the left, a horizontal rule filling the remaining width.

### Section 1: Risk Assessment

**KPI Strip** — three cards in a `3-column grid (2fr 1fr 1fr)`:

1. **Primary card** (accent-styled: teal left-border, gradient background):
   - Label: `EXPECTED ANNUAL LIABILITY`
   - Value: `€247.80` — large (`~2.2rem`, bold, white), euro sign white, digits teal
   - Below: Low Risk badge (teal pill with dot indicator) + muted context text "Portfolio median: €117.05"

2. **Percentile card** (standard card):
   - Label: `PORTFOLIO PERCENTILE`
   - Large number (e.g. `35th`) centred, with ordinal suffix muted
   - Sub-label: percentile band (e.g. `25th – 50th band`)

3. **Risk Band card** (standard card):
   - Label: `RISK BAND`
   - Tier name coloured teal/amber/red depending on risk: `LOW` (≤33rd pct), `MODERATE` (34–66th), `HIGH` (≥67th)
   - Sub-label: `LOW / MODERATE / HIGH` — matches the same 3-tier threshold logic currently used for `bar_color`

**Risk Spectrum bar** — full-width card below the KPI strip:
- Label: `RISK SPECTRUM` on the left, numeric score `35 / 100` in teal on the right
- Track: `8px` height, `#1a2840` background, gradient fill (`#00d4aa → #0088ff`), rounded
- Below track: three labels — `Low (<p25)` / `Moderate (p25–p75)` / `High (>p75)`

Risk percentile calculation: unchanged from current logic (5 portfolio thresholds mapped to 0–100).

---

### Section 2: Model Performance

**4-column metrics row** — one card per metric, always visible (no expander):

| Card | Primary value | Context note |
|---|---|---|
| Tweedie Deviance | `84.0536` | "Primary metric · p=1.5 · Native loss for zero-inflated data" |
| MAE | `€307.34` | "Test set: 135,603 policies · Zero-inflated — expected high" |
| RMSE | `€8,815.60` | "Driven by high-severity tail claims (<1% of policies)" |
| Explained Variance | `−0.0002` | "Expected near-zero for TPL pricing models" |

Each card has: small uppercase label, bold metric value (`~1rem`, `#cdd9e5`), then a two-line muted context note (`0.65rem`, `#4a6080`).

**Feature Importance chart** — full-width card below the metrics row:
- Label: `FEATURE IMPORTANCE — PERMUTATION METHOD`
- Rendered as a Plotly horizontal bar chart (retained from current implementation)
- Plotly layout overrides:
  - `plot_bgcolor='rgba(0,0,0,0)'`
  - `paper_bgcolor='rgba(0,0,0,0)'`
  - `font_color='#8899aa'`
  - Bar colour: `#00d4aa` (positive), `#ef4444` (negative — Density)
  - Height: `380px`
- Below the chart: a single paragraph of portfolio context text (static, pre-written):
  > *BonusMalus dominates with an importance score ~14× greater than the next feature (VehPower). This aligns with actuarial convention — the CRM score is the single strongest predictor of individual claim liability. Density shows a slight negative permutation score, suggesting minor collinearity with Area.*

---

## 4. Removed from Current App

| Element | Reason |
|---|---|
| "Analytical Policy Summary" table (`st.table`) | Redundant — sidebar already shows all 9 inputs |
| Intro paragraph (`st.markdown` narrative block) | Replaced by sidebar logo sub-label + section headers |
| `st.expander("Model Performance & Evaluation")` wrapper | Metrics are now always visible in Section 2 |
| `st.title(...)` and `st.subheader(...)` calls | Replaced by section headers and sidebar branding |

---

## 5. CSS Changes

All custom CSS is injected via a single `st.markdown(..., unsafe_allow_html=True)` block at the top.

Key rules to add/update:

```css
/* Sidebar width */
[data-testid="stSidebar"] {
    min-width: 280px;
    max-width: 280px;
}

/* Page background */
.stApp { background-color: #080c14; }

/* Section header divider */
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

/* Sidebar logo block */
.sidebar-logo {
    padding: 20px 20px 16px;
    border-bottom: 1px solid #1e2d45;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sidebar-logo-mark {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #00d4aa, #0088ff);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: #fff; font-weight: 900;
}

/* KPI accent card */
.kpi-accent-card {
    background: linear-gradient(135deg, #0d2137, #0a1a2e);
    border: 1px solid #00d4aa33;
    border-left: 3px solid #00d4aa;
    border-radius: 8px;
    padding: 16px 20px;
}

/* Risk badge */
.badge-low { background: #00d4aa14; border: 1px solid #00d4aa44; color: #00d4aa; }
.badge-moderate { background: #f59e0b14; border: 1px solid #f59e0b44; color: #f59e0b; }
.badge-high { background: #ef444414; border: 1px solid #ef444444; color: #ef4444; }

/* Metric context note */
.metric-context { font-size: 0.65rem; color: #4a6080; margin-top: 4px; line-height: 1.4; }

/* Feature importance context */
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

/* Footer */
.footer {
    position: fixed; left: 0; bottom: 0;
    width: 100vw;
    background: #080c14;
    border-top: 1px solid #1e2d45;
    color: #4a6080;
    text-align: center;
    padding: 12px 0;
    font-size: 0.65rem;
    z-index: 9999;
}
```

Streamlit metric widgets (`st.metric`) are replaced by raw `st.markdown` HTML cards for full styling control.

---

## 6. Streamlit Structure (post-redesign `app.py`)

```
st.set_page_config(...)
st.markdown(CSS_BLOCK, unsafe_allow_html=True)

[sidebar]
  logo block (HTML)
  section label (HTML)
  9 × input controls

[main]
  section_header("Risk Assessment")
  kpi_strip(prediction, percentile, risk_band)   ← 3-col HTML columns
  risk_bar(pred_percentile, bar_color)            ← HTML card
  
  section_header("Model Performance")
  metrics_row(metrics)                            ← 4 × st.columns HTML cards
  feature_importance_chart(fi_df)                 ← st.plotly_chart
  fi_context_note()                               ← HTML paragraph

footer (HTML)
```

Helper functions replace the current inline `st.markdown` blocks for each repeated pattern (section header, KPI card, metric card).

---

## 7. Out of Scope

- No changes to model loading, prediction logic, or data pipeline
- No new Streamlit pages or multi-page structure
- No changes to `requirements.txt` (no new packages)
- No mobile-specific breakpoints (Streamlit's responsive behaviour is unchanged)
