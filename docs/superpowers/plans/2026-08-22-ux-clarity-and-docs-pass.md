# UX Clarity + Documentation Pass — Claims Liability Dashboard

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task, if either is available in your environment. Otherwise, work through the numbered tasks below in order, verifying and committing after each one before moving to the next — do not batch everything into a single diff. Steps use checkbox (`- [ ]`) syntax for tracking, matching `docs/superpowers/plans/2026-05-16-ui-redesign.md`.

---

## Orientation — read this first

You're working on `app.py`, `README.md`, `tests/test_helpers.py`, and `docs/` in this repo (a Streamlit dashboard wrapping a Tweedie-GLM claims-liability model trained on the public freMTPL2 dataset, live at claims-liability-predictor.streamlit.app). I had this project reviewed ahead of a job interview, and the reviewer found one live, reproducible bug plus several polish gaps. This plan fixes all of them. Two things matter more than usual here:

1. **Precision over speed.** Several tasks below include the exact algorithm to implement, not just a description of the symptom — use it as given rather than improvising a different fix, because a superficially-plausible-but-different fix is exactly how the original bug (Task 1) was created in the first place.
2. **No model or data changes.** Don't retrain, don't touch `model/tweedie_model.pkl`, don't edit `data/`. Everything here is app-layer (`app.py`), docs-layer (`README.md`, `docs/`), or test-layer (`tests/test_helpers.py`). No new dependencies are needed — no new entries in `requirements.txt` — everything below is achievable with plain Streamlit, HTML, and CSS already in use in this codebase.

After each task: run `pytest tests/test_helpers.py -v`, then `streamlit run app.py --server.headless true &` and screenshot/visually confirm the change before moving on (same verification pattern as the prior UI-redesign plan). Commit after each task with a message describing what changed and why.

---

### Task 1 — Fix the Portfolio-Percentile vs. Percentile-Band contradiction

**Files:** `app.py` (lines ~267–296, ~392–394, ~422–429), `tests/test_helpers.py`

**The bug, exactly:** `app.py` currently has two independent functions computing two different things that get displayed together as if they were one number:

```python
def get_risk_percentile(prediction, portfolio_stats):
    thresholds = [p25, median, p75, p90, p95]
    return min(sum(1 for t in thresholds if prediction >= t) * 20, 100)   # only ever 0/20/40/60/80/100

def get_percentile_band(prediction, portfolio_stats):
    bins = sorted([p25, median, p75, p90, p95])
    return labels[min(np.searchsorted(bins, prediction, side='right'), 5)]  # a different, finer bucketing
```

Live proof this actually happens (I reproduced this on the deployed app, not just in theory): with BonusMalus=60 and everything else default, the prediction is €120.21. The **Portfolio Percentile** card shows **"40th"** while the **band sub-label directly underneath it** reads **"50th – 75th"** — two numbers describing the same prediction, disagreeing on screen at the same time. Same thing happens at BonusMalus=80 (€249.43 → "60th" shown above "75th – 90th" underneath). They only ever agree at the very top (100th / "Above 95th") and bottom (0th / "Below 25th") of the range.

**The fix — implement exactly this, don't invent a different one:**

```python
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
    if prediction >= anchor_values[-1]:
        return 100.0
    return float(np.interp(prediction, anchor_values, anchor_percentiles))


def get_percentile_band(percentile: float) -> str:
    """
    Derives the band label FROM the percentile above — never computed
    independently again. Note the changed signature: this now takes the
    percentile itself, not (prediction, portfolio_stats), so it is
    structurally impossible to call it with independently-derived data.
    """
    if percentile < 25: return 'Below 25th'
    if percentile < 50: return '25th – 50th'
    if percentile < 75: return '50th – 75th'
    if percentile < 90: return '75th – 90th'
    if percentile < 95: return '90th – 95th'
    return 'Above 95th'
```

`get_risk_tier(percentile)` is unchanged — it already just thresholds on the number it's given, and works fine fed a continuous float.

Update the call site (~line 392) to:

```python
pred_percentile = get_risk_percentile(prediction, portfolio_stats)   # float, e.g. 42.7
risk_label, risk_color, badge_class = get_risk_tier(pred_percentile)
band_label = get_percentile_band(pred_percentile)                     # derived FROM pred_percentile, not recomputed
```

And where it's rendered (~line 426, the "Portfolio Percentile" card), round only at the string-formatting step: `{round(pred_percentile)}` — do not round before computing `risk_label`/`band_label`, or you'll reintroduce a smaller version of the same class of bug at rounding boundaries (e.g. a true 74.6% rounding to "75th" for display while still correctly banding as "50th–75th" based on the unrounded value).

**Update `tests/test_helpers.py`** — the existing 6 percentile/band tests assert the *old, buggy* behavior and must be rewritten to match the new algorithm above. Using the real `PORTFOLIO` values already in that file (`p25_pure_premium: 95.52`, `median_pure_premium: 117.05`, `p75_pure_premium: 179.85`, `p90_pure_premium: 360.43`, `p95_pure_premium: 505.02`):

| prediction | expected `get_risk_percentile` | expected `get_percentile_band` |
|---|---|---|
| `0.0` | `0.0` | `'Below 25th'` |
| `95.52` (= p25) | `25.0` | `'25th – 50th'` |
| `117.05` (= median) | `50.0` | `'50th – 75th'` |
| `179.85` (= p75) | `75.0` | `'75th – 90th'` |
| `505.02` (= p95) | `95.0` | `'Above 95th'` |
| `99999.0` | `100.0` | `'Above 95th'` |

Keep the existing risk-tier tests as-is (they still pass unchanged). All 16 tests should still exist and pass — you're rewriting assertions on 6 of them, not deleting coverage.

**Optional stretch (only if time allows, skip if not):** the interpolation above assumes a straight line between each pair of the 5 known anchors, which is a reasonable approximation for a demo but not a true empirical percentile. A more rigorous version — still with zero retraining — would have the notebook's Step 7 export a finer grid of anchors (e.g. deciles p10/p20/…/p90 plus p95/p99) into `portfolio_stats.json` from the `y_pred` array it already computes, and this function would interpolate against that finer grid instead of just 5 points. Only do this if Task 1's core fix is done, verified, and there's time left.

- [ ] Implement the corrected functions and call site
- [ ] Update the 6 affected tests in `tests/test_helpers.py`
- [ ] Run `pytest tests/test_helpers.py -v` — 16 passed, 0 failed
- [ ] Run the app locally, set BonusMalus to 60, confirm the percentile number and band label now agree (should read something like "39th" / "25th – 50th", not "40th" / "50th – 75th")
- [ ] Commit: `fix: unify percentile and band into a single calculation`

---

### Task 2 — Add hover-triggered explanations throughout the app

This is the main ask: **every input and every metric on the live dashboard should have a small info affordance that explains it on hover**, so a non-technical visitor (or an interviewer clicking around cold) isn't left guessing what a number means.

**2a. Sidebar inputs — use Streamlit's native `help=` parameter.**

Every `st.slider` / `st.number_input` / `st.selectbox` / `st.radio` call in `get_user_input()` currently has its explanation as a separate, always-visible `<p class='parameter-desc'>` line above the widget. Replace that pattern: drop the separate markdown caption and instead pass the same text via each widget's built-in `help=` argument, which renders Streamlit's native small "?" icon next to the label and shows the text in a tooltip on hover — exactly the interaction being asked for, with zero custom code. Example, before:

```python
st.sidebar.markdown("<p class='param-header'>Driver Age</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='parameter-desc'>Chronological age of the policyholder; a primary factor in actuarial risk profiling.</p>", unsafe_allow_html=True)
driv_age = st.sidebar.slider("DrivAge", 18, 100, 35, label_visibility="collapsed")
```

after:

```python
st.sidebar.markdown("<p class='param-header'>Driver Age</p>", unsafe_allow_html=True)
driv_age = st.sidebar.slider(
    "DrivAge", 18, 100, 35, label_visibility="collapsed",
    help="Chronological age of the policyholder; a primary factor in actuarial risk profiling.",
)
```

Apply this to all nine inputs. Reuse each field's existing caption text as the `help=` text **except VehBrand**, whose current copy is wrong and should be corrected while you're here — the source dataset's own documentation states VehBrand's categories are anonymised/unknown, not verified manufacturer identities, so the current tooltip ("Manufacturer categorisation; proxy for parts cost and reliability.") overstates what's actually known. Replace it with:

```python
help="Anonymised vehicle brand code from the source dataset — categories are not identified manufacturers, just a proxy grouping."
```

**2b. Main-content KPI/metric cards — build a small reusable tooltip component**, since these are hand-rolled HTML `<div>` cards, not native Streamlit widgets, so `help=` doesn't apply to them. Add this CSS to the existing `<style>` block (near the other `.card-label`/`.metric-card` rules):

```css
.info-icon {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 14px;
    height: 14px;
    margin-left: 6px;
    border-radius: 50%;
    background: #1e2d45;
    color: #8899aa;
    font-size: 0.62rem;
    font-weight: 700;
    cursor: help;
    vertical-align: middle;
}
.info-icon .tooltip-text {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    bottom: 140%;
    left: 50%;
    transform: translateX(-50%);
    background: #0f1623;
    border: 1px solid #1e2d45;
    color: #cdd9e5;
    text-align: left;
    padding: 10px 12px;
    border-radius: 6px;
    font-size: 0.68rem;
    font-weight: 400;
    line-height: 1.5;
    width: 230px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    transition: opacity 0.15s ease;
    z-index: 50;
    text-transform: none;
    letter-spacing: normal;
}
.info-icon:hover .tooltip-text,
.info-icon:focus .tooltip-text {
    visibility: visible;
    opacity: 1;
}
```

Note `:focus` alongside `:hover` and `tabindex="0"` below — this makes the tooltip reachable by keyboard, not just mouse, which is a real accessibility gap the current app has nowhere at all (worth keeping consistently).

Add a small helper next to the existing `metric_card()` / `section_header()` functions:

```python
def info_icon(text: str) -> str:
    escaped = text.replace('"', '&quot;')
    return f'<span class="info-icon" tabindex="0">i<span class="tooltip-text">{escaped}</span></span>'
```

Then wire it into every card label. Use this exact copy (accurate, already fact-checked against this project's own notebook/artifacts — don't invent different explanations):

| Card | `info_icon()` text |
|---|---|
| Expected Annual Liability | "The model's best estimate of this policy's claims cost over a year, based on its risk profile — actuaries call this the 'Pure Premium'. It's before any margin, expenses, or profit loading are added to reach an actual sale price." |
| Portfolio Percentile | "How this policy's predicted cost compares to the rest of the portfolio. A percentile of 80 means this policy is predicted to cost more than 80% of policies in the reference portfolio." |
| Risk Band | "A simplified Low / Moderate / High grouping of the percentile score — Low is the bottom third of predicted costs, Moderate the middle third, High the top third." |
| Risk Spectrum (the bar) | "A visual version of the percentile score above — the further right the bar, the higher this policy's predicted cost relative to the rest of the portfolio." |
| Tweedie Deviance | "The model's primary accuracy score — lower is better. It's the standard way actuaries measure fit for claims data, where most policies cost $0 and a few cost a lot; a plain accuracy percentage doesn't work well for that shape of data." |
| MAE | "On average, how far a single prediction is from the actual claim cost. This number looks large mainly because most real policies have $0 in claims while the model always predicts a small positive number — that's expected for this kind of data, not a flaw." |
| RMSE | "Similar to MAE, but penalises big misses more heavily — it's higher mainly because of a small number of very expensive claims in the data, same as most real insurance portfolios." |
| Explained Variance | "Normally this measures how much of the outcome a model explains — but for this type of zero-inflated claims data it's expected to sit near zero even for a well-built model. It is not a sign the model is broken; Tweedie Deviance above is the right metric to judge accuracy by." |
| Feature Importance chart | "Which policy details influence the prediction most, measured by testing how much accuracy drops when each one is scrambled. Bars further right had a bigger effect on the prediction." |

Embed each by appending the icon's HTML immediately after the label text inside the relevant f-string, e.g. the "Expected Annual Liability" card's label line becomes:

```python
f'<div class="card-label">Expected Annual Liability{info_icon("The model\'s best estimate...")}</div>'
```

and give `metric_card(label, value, context, info=None)` an optional fourth argument so the four Model Performance cards can pass their tooltip text through the existing helper rather than hand-writing each card's HTML.

- [ ] Convert all 9 sidebar inputs to `help=`, remove the now-redundant `.parameter-desc` markdown lines, fix the VehBrand copy
- [ ] Add the `.info-icon`/`.tooltip-text` CSS and the `info_icon()` helper
- [ ] Wire `info_icon()` into all 8 main-content cards + the feature importance chart heading, using the copy table above verbatim
- [ ] Run the app locally, hover (and Tab-focus) each icon, confirm the tooltip appears, is readable, and doesn't clip off-screen at the sidebar's 280px width
- [ ] Commit: `feat: add hover explanations to every input and metric`

---

### Task 3 — Put the currency/dataset context on the app itself, not just the README

**File:** `app.py`, sidebar block (~line 317)

Every dollar figure on the app is in € with no explanation on-screen — the README explains this well, but a visitor to the live app never sees the README. Add one line directly under the sidebar logo block:

```python
st.sidebar.markdown(
    '<div class="sidebar-context-note">Trained on the public <strong>freMTPL2</strong> French motor '
    'dataset (EUR). Methodology transfers directly to an AUD motor book with local recalibration.</div>',
    unsafe_allow_html=True,
)
```

with a small matching CSS rule (muted, small text, consistent with `.sidebar-logo-sub`):

```css
.sidebar-context-note {
    font-size: 0.62rem;
    color: #4a6080;
    line-height: 1.5;
    padding: 10px 20px 16px;
    border-bottom: 1px solid #1e2d45;
}
```

- [ ] Add the note + CSS, confirm it renders under the logo block without crowding the "Policy Parameters" label
- [ ] Commit: `feat: surface dataset/currency context directly in the app`

---

### Task 4 — Fix the stale, contradictory PDF in `docs/`

**File:** `docs/ClaimsLiabilityPredictiveModel.pdf`

This PDF is a stale export of an earlier notebook draft. It reports **MAE €581.52** and **Mean Tweedie Deviance 155.64**, computed *without* exposure weighting. Every other source of truth in the repo — `README.md`, `model/model_metrics.json`, and the live app — agrees on **MAE €307.34** and **Deviance 84.05** (the current notebook's exposure-weighted evaluation). Anyone who opens both will see two different "official" numbers for the same model.

Simplest fix: delete `docs/ClaimsLiabilityPredictiveModel.pdf` entirely and let `README.md`'s metrics table be the single source of truth — the notebook itself (`notebooks/ClaimsLiabilityPredictiveModel.ipynb`) already is the underlying evidence and is more current than the stale PDF export.

If a PDF artifact is wanted for the docs folder, regenerate it from the *current* notebook (print-to-PDF / same export step used originally) instead — but don't just leave the old one in place.

- [ ] Delete or regenerate `docs/ClaimsLiabilityPredictiveModel.pdf` so it agrees with README/model_metrics.json
- [ ] Grep the repo for any other reference to the old €581.52 / 155.64 figures and fix them too
- [ ] Commit: `fix: remove stale, contradictory evaluation PDF`

---

### Task 5 — Soften the unsupported "collinearity" claim

**File:** `app.py`, the `.fi-context` paragraph under the feature-importance chart (~line 525)

Current text: *"Density shows a slight negative permutation score, suggesting minor collinearity with Area."* Nothing in the notebook actually tests for collinearity (no correlation matrix, no VIF) — this is a plausible-sounding but unverified claim. Two acceptable fixes, pick one:

- **(a) Soften the claim** to what the evidence actually supports:
  `"Density carries little independent predictive signal once BonusMalus, Area, and VehPower are already in the model."`
- **(b) Back the claim with real evidence** — add a quick correlation check between `Density` and `Area` (e.g. group-wise `df.groupby('Area')['Density'].describe()` or a one-hot correlation) to the notebook, and only keep the collinearity language if the number actually supports it, citing the real figure.

(a) is faster and sufficient; only do (b) if there's time and you want the stronger claim.

- [ ] Apply (a) or (b)
- [ ] Commit: `fix: don't claim collinearity the analysis never tested for`

---

### Task 6 — Rewrite `README.md` for a non-technical audience

**File:** `README.md`

The current README opens with "Predictive Claims Liability Model: Insurance Risk Oversight" and moves quickly into `ColumnTransformer`, one-hot encoding, and Tweedie deviance formulas. Restructure it so a non-technical reader (a hiring manager, a recruiter, a portfolio visitor) can understand what the project does and why it matters within the first 30 seconds, while still giving a technical reader everything they need further down. Concretely:

1. **Keep the title and dashboard screenshot at the top.**
2. **Rewrite the opening section in plain language** — lead with the real-world problem and what the tool actually does, not the modelling technique. Something in this register (adapt, don't necessarily use verbatim):

   > *"When someone lodges a car insurance claim, an insurer needs to estimate roughly how much that claim will end up costing — as early and as accurately as possible. This project is a working demo of that idea: you enter a policy's details (driver age, vehicle type, location, etc.) and it instantly estimates the expected claims cost, flags how risky that policy is relative to the rest of the portfolio, and shows how confident the underlying model is. It's built on a real, publicly available French motor insurance dataset of ~678,000 policies, using the industry-standard statistical approach for this kind of prediction (more on that below, for the technically curious)."*

3. **Add a plain-language "How it works" section** (3-4 short sentences, no code, no jargon) between the intro and the technical methodology — something like: "The model looks at a policy's risk factors and learns from hundreds of thousands of real historical policies which combinations of factors led to expensive claims. It then applies that pattern to any new policy you enter. Because most policies never make a claim at all, standard prediction accuracy measures don't work well here — the model uses actuarial-standard statistical measures suited to that reality instead."
4. **Move the deep technical detail down**, under a clearly marked heading such as `## Technical Methodology (for a technical reviewer)` — keep the Tweedie/ColumnTransformer/pipeline detail, it's good content, just don't lead with it.
5. **Rewrite the metrics table with a plain-language column added**, so it's legible without an actuarial background:

   | Metric | Value | In plain terms |
   |---|---|---|
   | Mean Tweedie Deviance | 84.0536 | The model's primary accuracy score (lower = better); the right way to score this type of claims data |
   | Mean Absolute Error | €307.34 | On average, how far a single prediction is from the real outcome |
   | Root Mean Squared Error | €8,815.60 | Similar to MAE, but weighted more heavily by rare, very expensive claims |
   | Explained Variance | −0.0002 | Expected to be near zero for this kind of data — not a sign the model is broken (explained further below) |

   Keep the existing "Why is Explained Variance near zero" callout — it's genuinely well written — just make sure it reads clearly on its own once the table above it is simplified.
6. **Simplify the "Limitations & Future Work" section's language** without losing any of the actual content — it's honest and specific (single observation year, French-market findings not directly transferable to AU without recalibration, etc.); just make sure each bullet is a plain sentence a non-technical reader could follow.
7. **Fix the live-app link** — it currently points to the ugly hash subdomain (`claims-liability-predictor-dgw3wokbgkfzrhm4yfdlrh.streamlit.app`); the clean custom subdomain `claims-liability-predictor.streamlit.app` resolves to the same app and reads far better in a portfolio piece. Swap it.
8. Keep the repo structure diagram, business-impact section, and technical-profile footer largely as-is — those aren't the parts a non-technical reader struggles with.

- [ ] Restructure per the above (plain-language lead → how-it-works → technical methodology → plain+technical metrics table → simplified limitations)
- [ ] Fix the live-app link
- [ ] Read it back top to bottom as if you'd never seen the project before — if the first two paragraphs still require knowing what a GLM is, revise again
- [ ] Commit: `docs: rewrite README for a non-technical audience`

---

### Task 7 — Re-theme the sidebar sliders (quick polish, do last)

**File:** `app.py`, CSS block

The KPI cards, badges, and buttons all use the app's teal/blue "Dark Fintech" palette, but the native Streamlit slider track and handle render in Streamlit's default red — a mismatched, unstyled component inside an otherwise custom-themed UI. Add:

```css
[data-testid="stSlider"] [role="slider"] {
    background-color: #00d4aa !important;
    border-color: #00d4aa !important;
}
[data-testid="stSlider"] > div > div > div[style*="background-color: rgb(255"] {
    background: linear-gradient(90deg, #00d4aa, #0088ff) !important;
}
```

(Streamlit's internal DOM/class names shift between versions — inspect the actual rendered slider's DOM in your environment and adjust the selectors above if they don't match; the goal is simply: slider track fill and handle should read teal/blue, not Streamlit's default red.)

- [ ] Confirm sliders now match the app's palette
- [ ] Commit: `style: re-theme slider widgets to match dashboard palette`

---

## Final verification checklist

- [ ] `pytest tests/test_helpers.py -v` — 16 passed, 0 failed
- [ ] `streamlit run app.py` locally — no console errors, no crash on any input combination
- [ ] Manually drag BonusMalus through several values and confirm the percentile number and band label always agree
- [ ] Hover (and Tab through) every sidebar input and every main-content card — tooltip text appears, is accurate, doesn't clip
- [ ] README renders cleanly on GitHub — read the first three paragraphs as a non-technical reader would
- [ ] `docs/ClaimsLiabilityPredictiveModel.pdf` (or its replacement) agrees with README/model_metrics.json
- [ ] Push and confirm Streamlit Community Cloud redeploys the live app with all of the above visible
