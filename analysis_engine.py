"""
analysis_engine.py — HR Decision Support System
Accepts real-world company inputs, normalises them internally to a 0-100 scale,
computes four KPIs, and generates an organisational success/failure prediction.
"""
from __future__ import annotations

from typing import Dict, List, Mapping


# ─── helpers ──────────────────────────────────────────────────────────────────

def _to_float(form: Mapping[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(form.get(key, default))
    except (TypeError, ValueError):
        return default


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


# ─── normalisation functions (real inputs → 0-100) ───────────────────────────

def _norm_leadership_years(years: float) -> float:
    """Average C-suite / senior leadership experience in years → 0-100."""
    if years <= 0:
        return 5.0
    if years <= 3:
        return 20 + years * 6
    if years <= 8:
        return 38 + (years - 3) * 7
    if years <= 15:
        return 73 + (years - 8) * 2.7
    return min(98, 92 + (years - 15) * 0.4)


def _norm_digital(score: float) -> float:
    return _clamp((score / 10) * 100)


def _norm_retention(pct: float) -> float:
    return _clamp(pct)


def _norm_churn_risk(annual_churn_pct: float) -> float:
    """Higher churn % → higher risk score."""
    return _clamp(annual_churn_pct * 2.5)


def _norm_debt(dte_ratio: float) -> float:
    """Debt-to-equity ratio → risk score. 0 D/E = 0 risk, 2.0+ = 100 risk."""
    return _clamp(dte_ratio * 50)


def _norm_process_fragility(doc_score: float) -> float:
    """Process documentation 1-10 (10 = fully documented) → fragility risk."""
    return _clamp((10 - doc_score) * 10)


def _norm_dependency(dep_score: float) -> float:
    """Key-person / vendor dependency 1-5 (5 = highly dependent) → risk."""
    return _clamp((dep_score / 5) * 100)


def _norm_margin(margin_pct: float) -> float:
    """Operating profit margin (%) → 0-100. Handles negatives down to -20%."""
    shifted = margin_pct + 20
    return _clamp(shifted * 2)


def _norm_revenue_growth(growth_pct: float) -> float:
    """Annual revenue growth rate (%) → 0-100."""
    base = 30 + growth_pct * 1.8
    return _clamp(base)


def _norm_cash_runway(months: float) -> float:
    """Cash runway in months → 0-100."""
    if months <= 0:
        return 0.0
    if months <= 6:
        return months * 5
    if months <= 12:
        return 30 + (months - 6) * 4.17
    if months <= 24:
        return 55 + (months - 12) * 2.08
    return min(100, 80 + (months - 24) * 0.83)


# ─── band classifiers ─────────────────────────────────────────────────────────

def _band(score: float) -> str:
    if score >= 75:
        return "Strong"
    if score >= 55:
        return "Moderate"
    return "Needs Attention"


def _risk_band(score: float) -> str:
    if score >= 65:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


# ─── success / failure prediction ────────────────────────────────────────────

def _predict(ohi: float, srs: float, lrs: float, fsc: float) -> dict:
    raw_prob = (ohi * 0.55) + ((100 - srs) * 0.30) + (fsc * 0.15)
    probability = round(_clamp(raw_prob * 0.95), 1)

    if probability >= 78:
        return {
            "verdict": "High Success Probability",
            "verdict_class": "verdict-success",
            "probability": probability,
            "horizon": "Stable for 4–6 years under current trajectory",
            "summary": (
                "The company demonstrates well-rounded organisational health. Leadership capability, "
                "financial resilience, and operational stability are all above threshold. "
                "Strategic focus should shift toward sustaining growth momentum and proactive "
                "succession planning."
            ),
        }
    if probability >= 60:
        return {
            "verdict": "Moderate Success — Watchlist",
            "verdict_class": "verdict-moderate",
            "probability": probability,
            "horizon": "Stable for 2–3 years; intervention recommended within 12–18 months",
            "summary": (
                "The organisation is functional but carries identifiable risk factors that, "
                "if left unaddressed, may compound over the next 2–3 years. "
                "Targeted improvements in the weakest KPI domain will deliver the highest ROI."
            ),
        }
    if probability >= 40:
        return {
            "verdict": "Elevated Risk — Action Required",
            "verdict_class": "verdict-caution",
            "probability": probability,
            "horizon": "Critical signals expected within 1–2 years without intervention",
            "summary": (
                "Multiple risk indicators exceed acceptable thresholds. "
                "The organisation faces potential performance degradation in leadership, "
                "financial resilience, or operational stability. "
                "An urgent strategic review is strongly advised."
            ),
        }
    return {
        "verdict": "High Failure Risk — Immediate Intervention",
        "verdict_class": "verdict-danger",
        "probability": probability,
        "horizon": "Organisational distress likely within 6–18 months",
        "summary": (
            "The compound KPI profile indicates a high probability of significant operational "
            "or financial distress. Immediate management intervention, restructuring, or "
            "external advisory support is strongly recommended."
        ),
    }


# ─── insight generator ────────────────────────────────────────────────────────

def _insights(lrs: float, srs: float, fsc: float, ohi: float,
               industry: str, stage: str) -> List[str]:
    msgs = []
    if lrs < 55:
        msgs.append(
            f"Leadership Readiness is below threshold ({lrs:.0f}/100). "
            "Invest in executive development programmes, mentoring structures, and digital upskilling. "
            "Succession planning for critical roles should be formalised."
        )
    if srs > 62:
        msgs.append(
            f"Scaling Risk is elevated ({srs:.0f}/100). "
            "Key priorities: reduce single-person dependencies, document core processes, "
            "and review concentration risks in customer, supplier, and debt portfolios."
        )
    if fsc < 50:
        msgs.append(
            f"Financial Stability is fragile ({fsc:.0f}/100). "
            "Margin improvement, revenue diversification, and extending cash runway are the "
            "most impactful near-term financial levers."
        )
    if stage == "startup" and srs > 50:
        msgs.append(
            "Start-up scaling risk is a critical factor at this stage. "
            "Prioritise process documentation and team redundancy before entering the next growth phase."
        )
    if stage == "mature" and lrs < 65:
        msgs.append(
            "Mature organisations with lower leadership readiness typically face digital transformation "
            "gaps and succession risk — both should be addressed proactively."
        )
    if industry in ("technology", "saas") and fsc < 60:
        msgs.append(
            "Tech / SaaS companies are expected to maintain strong cash runway. "
            "A financial stability score below 60 in this sector warrants close investor scrutiny."
        )
    if not msgs:
        msgs.append(
            "All KPI domains are within healthy ranges. "
            "Focus on sustaining cross-functional alignment, monitoring leading indicators quarterly, "
            "and building organisational resilience for the next growth phase."
        )
    return msgs


# ─── main entry point ─────────────────────────────────────────────────────────

def run_ai_analysis(form: Mapping[str, str]) -> Dict[str, object]:
    # company profile
    company_name   = form.get("company_name", "").strip() or "Your Company"
    industry       = form.get("industry", "general").lower()
    stage          = form.get("stage", "growth").lower()
    employee_count = int(_to_float(form, "employee_count", 100))

    # real-world inputs
    leadership_years = _to_float(form, "leadership_years", 8)
    digital_score    = _clamp(_to_float(form, "digital_score", 6), 1, 10)
    retention_pct    = _clamp(_to_float(form, "retention_pct", 75), 0, 100)

    churn_pct  = _clamp(_to_float(form, "churn_pct", 15), 0, 100)
    dte_ratio  = _clamp(_to_float(form, "dte_ratio", 0.8), 0, 10)
    doc_score  = _clamp(_to_float(form, "doc_score", 6), 1, 10)
    dep_score  = _clamp(_to_float(form, "dep_score", 3), 1, 5)

    margin_pct  = _clamp(_to_float(form, "margin_pct", 8), -20, 60)
    growth_pct  = _clamp(_to_float(form, "growth_pct", 12), -30, 100)
    cash_months = _clamp(_to_float(form, "cash_months", 14), 0, 60)

    # normalise
    n_lead  = _norm_leadership_years(leadership_years)
    n_dig   = _norm_digital(digital_score)
    n_ret   = _norm_retention(retention_pct)
    n_churn = _norm_churn_risk(churn_pct)
    n_debt  = _norm_debt(dte_ratio)
    n_frag  = _norm_process_fragility(doc_score)
    n_dep   = _norm_dependency(dep_score)
    n_marg  = _norm_margin(margin_pct)
    n_grow  = _norm_revenue_growth(growth_pct)
    n_cash  = _norm_cash_runway(cash_months)

    # KPI computation
    lrs = round(_clamp(n_lead * 0.40 + n_dig * 0.30 + n_ret * 0.30), 1)
    srs = round(_clamp(n_churn * 0.30 + n_debt * 0.25 + n_frag * 0.25 + n_dep * 0.20), 1)
    fsc = round(_clamp(n_marg * 0.35 + n_grow * 0.35 + n_cash * 0.30), 1)
    ohi = round(_clamp(lrs * 0.40 + (100 - srs) * 0.35 + fsc * 0.25), 1)

    prediction   = _predict(ohi, srs, lrs, fsc)
    insight_list = _insights(lrs, srs, fsc, ohi, industry, stage)

    display_inputs = [
        ("Leadership Experience",  f"{leadership_years:.0f} years"),
        ("Digital Maturity",       f"{digital_score:.0f} / 10"),
        ("Employee Retention",     f"{retention_pct:.0f}%"),
        ("Annual Churn Rate",      f"{churn_pct:.0f}%"),
        ("Debt-to-Equity Ratio",   f"{dte_ratio:.1f}x"),
        ("Process Documentation",  f"{doc_score:.0f} / 10"),
        ("Key-Person Dependency",  f"{dep_score:.0f} / 5"),
        ("Profit Margin",          f"{margin_pct:.0f}%"),
        ("Revenue Growth",         f"{growth_pct:.0f}%"),
        ("Cash Runway",            f"{cash_months:.0f} months"),
    ]

    return {
        "company_name":   company_name,
        "industry":       industry.title(),
        "stage":          stage.title(),
        "employee_count": employee_count,
        "lrs": lrs, "srs": srs, "fsc": fsc, "ohi": ohi,
        "lrs_band":  _band(lrs),
        "srs_band":  _risk_band(srs),
        "fsc_band":  _band(fsc),
        "ohi_band":  _band(ohi),
        "prediction":      prediction,
        "insights":        insight_list,
        "display_inputs":  display_inputs,
        "explanation": (
            "Each input is normalised to a 0–100 scale using domain-calibrated functions "
            "(e.g., D/E ratio, cash runway months, retention %). "
            "KPIs are computed as weighted composites, and the success prediction combines "
            "OHI (55%), inverse Scaling Risk (30%), and Financial Stability (15%) into a "
            "transparent probability estimate."
        ),
    }
