# tests/test_helpers.py
import numpy as np

PORTFOLIO = {
    'p25_pure_premium': 95.52,
    'median_pure_premium': 117.05,
    'p75_pure_premium': 179.85,
    'p90_pure_premium': 360.43,
    'p95_pure_premium': 505.02,
}


def get_risk_percentile(prediction, portfolio_stats):
    thresholds = [
        portfolio_stats['p25_pure_premium'],
        portfolio_stats['median_pure_premium'],
        portfolio_stats['p75_pure_premium'],
        portfolio_stats['p90_pure_premium'],
        portfolio_stats['p95_pure_premium'],
    ]
    return min(sum(1 for t in thresholds if prediction >= t) * 20, 100)


def get_risk_tier(percentile):
    if percentile <= 33:
        return 'LOW', '#00d4aa', 'badge-low'
    elif percentile <= 66:
        return 'MODERATE', '#f59e0b', 'badge-moderate'
    return 'HIGH', '#ef4444', 'badge-high'


def get_percentile_band(prediction, portfolio_stats):
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


def section_header(title):
    return f'<div class="section-divider"><span class="section-divider-title">{title}</span><div class="section-divider-rule"></div></div>'


def metric_card(label, value, context):
    return f'<div class="metric-card"><div class="card-label">{label}</div><div class="metric-val">{value}</div><div class="metric-context">{context}</div></div>'


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_risk_percentile_below_p25():
    assert get_risk_percentile(50.0, PORTFOLIO) == 0

def test_risk_percentile_at_p25():
    assert get_risk_percentile(95.52, PORTFOLIO) == 20

def test_risk_percentile_at_median():
    assert get_risk_percentile(117.05, PORTFOLIO) == 40

def test_risk_percentile_at_p95():
    assert get_risk_percentile(505.02, PORTFOLIO) == 100

def test_risk_percentile_above_p95_capped():
    assert get_risk_percentile(99999.0, PORTFOLIO) == 100

def test_risk_tier_low():
    label, color, badge = get_risk_tier(0)
    assert label == 'LOW' and color == '#00d4aa' and badge == 'badge-low'

def test_risk_tier_low_at_boundary():
    label, _, _ = get_risk_tier(33)
    assert label == 'LOW'

def test_risk_tier_moderate():
    label, color, badge = get_risk_tier(40)
    assert label == 'MODERATE' and color == '#f59e0b' and badge == 'badge-moderate'

def test_risk_tier_moderate_at_boundary():
    label, _, _ = get_risk_tier(66)
    assert label == 'MODERATE'

def test_risk_tier_high():
    label, color, badge = get_risk_tier(80)
    assert label == 'HIGH' and color == '#ef4444' and badge == 'badge-high'

def test_percentile_band_below_p25():
    assert get_percentile_band(50.0, PORTFOLIO) == 'Below 25th'

def test_percentile_band_between_p25_and_median():
    assert get_percentile_band(100.0, PORTFOLIO) == '25th – 50th'

def test_percentile_band_between_median_and_p75():
    assert get_percentile_band(150.0, PORTFOLIO) == '50th – 75th'

def test_percentile_band_above_p95():
    assert get_percentile_band(9999.0, PORTFOLIO) == 'Above 95th'

def test_section_header_contains_title_and_class():
    html = section_header('Risk Assessment')
    assert 'Risk Assessment' in html
    assert 'section-divider' in html

def test_metric_card_contains_all_parts():
    html = metric_card('MAE', '€307.34', 'some context note')
    assert 'MAE' in html
    assert '€307.34' in html
    assert 'some context note' in html
