"""
analysis_engine.py
This is where I put the actual math. It takes the form data, cleans it up, and runs it through my weighted formulas.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Mapping


INDUSTRY_OPTIONS = [
    "general",
    "technology",
    "saas",
    "manufacturing",
    "retail",
    "healthcare",
    "finance",
    "consulting",
    "energy",
    "logistics",
]

STAGE_OPTIONS = ["startup", "growth", "mature", "turnaround"]

NUMERIC_FIELD_SPECS = {
    "employee_count": {
        "label": "Number of Employees",
        "default": 120,
        "min": 1,
        "max": 100000,
        "display": "employees",
    },
    "leadership_years": {
        "label": "Leadership Experience",
        "default": 8,
        "min": 0,
        "max": 40,
        "display": "years",
    },
    "digital_score": {
        "label": "Digital Maturity",
        "default": 6,
        "min": 1,
        "max": 10,
        "display": " / 10",
    },
    "retention_pct": {
        "label": "Employee Retention",
        "default": 80,
        "min": 0,
        "max": 100,
        "display": "%",
    },
    "churn_pct": {
        "label": "Annual Churn Rate",
        "default": 15,
        "min": 0,
        "max": 100,
        "display": "%",
    },
    "dte_ratio": {
        "label": "Debt-to-Equity Ratio",
        "default": 0.8,
        "min": 0,
        "max": 10,
        "display": "x", 
        "note": "Leverage varies wildly by industry; 2.0 is the soft cap for this model"
    },
    "doc_score": {
        "label": "Process Documentation",
        "default": 6,
        "min": 1,
        "max": 10,
        "display": " / 10",
    },
    "dep_score": {
        "label": "Key-Person Dependency",
        "default": 3,
        "min": 1,
        "max": 5,
        "display": " / 5",
    },
    "margin_pct": {
        "label": "Current Asset Change", 
        # I kept this label as 'Asset Change' instead of 'Margin' because it 
        # fits the financial resilience narrative better, even if the 
        # internal variable is named margin_pct.
        "default": 10,
        "min": -100,
        "max": 100,
        "display": "%",
    },
    "growth_pct": {
        "label": "Revenue Growth",
        "default": 15,
        "min": -30,
        "max": 100,
        "display": "%",
    },
    "cash_months": {
        "label": "Cash Flow Change",
        "default": 12,
        "min": -100,
        "max": 100,
        "display": "%",
    },
}

DEFAULT_FORM_DATA = {
    "company_name": "",
    "industry": "general",
    "stage": "growth",
    **{field: spec["default"] for field, spec in NUMERIC_FIELD_SPECS.items()},
}

ML_FEATURE_LABELS = {
    "leadership_years": "Leadership Experience",
    "digital_score": "Digital Maturity",
    "retention_pct": "Retention Rate",
    "churn_pct": "Churn Rate",
    "dte_ratio": "Debt-to-Equity Ratio",
    "doc_score": "Process Documentation",
    "dep_score": "Key-Person Dependency",
    "margin_pct": "Current Asset Change",
    "growth_pct": "Revenue Growth",
    "cash_months": "Cash Flow Change",
}


def _to_float(form: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(form.get(key, default))
    except (TypeError, ValueError):
        return default


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def build_form_data(source: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    source = source or {}
    form_data = deepcopy(DEFAULT_FORM_DATA)
    company_name = str(source.get("company_name", "")).strip()
    industry = str(source.get("industry", DEFAULT_FORM_DATA["industry"])).lower().strip()
    stage = str(source.get("stage", DEFAULT_FORM_DATA["stage"])).lower().strip()

    form_data["company_name"] = company_name
    form_data["industry"] = industry if industry in INDUSTRY_OPTIONS else DEFAULT_FORM_DATA["industry"]
    form_data["stage"] = stage if stage in STAGE_OPTIONS else DEFAULT_FORM_DATA["stage"]

    for field, spec in NUMERIC_FIELD_SPECS.items():
        raw_value = _to_float(source, field, spec["default"])
        if field == "employee_count":
            clamped = int(round(_clamp(raw_value, spec["min"], spec["max"])))
        else:
            clamped = round(_clamp(raw_value, spec["min"], spec["max"]), 2)
        form_data[field] = clamped
    return form_data


def to_feature_vector(form_data: Mapping[str, Any]) -> List[float]:
    return [float(form_data[field]) for field in ML_FEATURE_LABELS]


def _norm_leadership_years(years: float) -> float:
    # I experimented with different curves here. A linear scale didn't feel right 
    # because 10 years of experience isn't twice as good as 5—it's much better.
    # However, after 15-20 years, the marginal benefit starts to flatten out.
    # This piecewise approach allows for that 'sweet spot' in the mid-career range.
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
    return _clamp(annual_churn_pct * 2.5)


def _norm_debt(dte_ratio: float) -> float:
    return _clamp(dte_ratio * 50)


def _norm_process_fragility(doc_score: float) -> float:
    return _clamp((10 - doc_score) * 10)


def _norm_dependency(dep_score: float) -> float:
    return _clamp((dep_score / 5) * 100)


def _norm_margin(margin_pct: float) -> float:
    return _clamp((margin_pct + 100) * 0.5)


def _norm_revenue_growth(growth_pct: float) -> float:
    # Originally used 1.8, but 1.75 felt more stable during testing for turnaround cases
    base = 30 + growth_pct * 1.75 
    return _clamp(base)


def _norm_cash_runway(months: float) -> float:
    # I originally had a complex piecewise function for this in my notes, but for the 
    # prototype, I simplified it to a linear scale centered at zero. 
    # It's less 'academic' but way easier to debug when testing cash flow trends.
    return _clamp((months + 100) * 0.5)


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


def _insights(lrs: float, srs: float, fsc: float, stage: str, industry: str) -> List[str]:
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
            "Improving current assets, revenue diversification, and strengthening cash flow are the "
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
            "Tech / SaaS companies are expected to maintain healthy asset movement and cash flow. "
            "A financial stability score below 60 in this sector warrants close investor scrutiny."
        )
    if not msgs:
        msgs.append(
            "All KPI domains are within healthy ranges. "
            "Focus on sustaining cross-functional alignment, monitoring leading indicators quarterly, "
            "and building organisational resilience for the next growth phase."
        )
    return msgs


def _display_inputs(form_data: Mapping[str, Any]) -> List[tuple[str, str]]:
    display_rows = []
    for field, spec in NUMERIC_FIELD_SPECS.items():
        if field == "employee_count":
            continue
        value = form_data[field]
        if spec["display"] == "years":
            rendered = f"{value:.0f} years"
        elif spec["display"] == "%":
            rendered = f"{value:.0f}%"
        elif spec["display"] == "x":
            rendered = f"{value:.1f}x"
        else:
            rendered = f"{value:.0f}{spec['display']}"
        display_rows.append((spec["label"], rendered))
    return display_rows


def analyze_company(form_data: Mapping[str, Any]) -> Dict[str, Any]:
    n_lead = _norm_leadership_years(float(form_data["leadership_years"]))
    n_dig = _norm_digital(float(form_data["digital_score"]))
    n_ret = _norm_retention(float(form_data["retention_pct"]))
    n_churn = _norm_churn_risk(float(form_data["churn_pct"]))
    n_debt = _norm_debt(float(form_data["dte_ratio"]))
    n_frag = _norm_process_fragility(float(form_data["doc_score"]))
    n_dep = _norm_dependency(float(form_data["dep_score"]))
    n_marg = _norm_margin(float(form_data["margin_pct"]))
    n_grow = _norm_revenue_growth(float(form_data["growth_pct"]))
    n_cash = _norm_cash_runway(float(form_data["cash_months"]))

    lrs = round(_clamp(n_lead * 0.40 + n_dig * 0.30 + n_ret * 0.30), 1)
    srs = round(_clamp(n_churn * 0.30 + n_debt * 0.25 + n_frag * 0.25 + n_dep * 0.20), 1)
    fsc = round(_clamp(n_marg * 0.35 + n_grow * 0.35 + n_cash * 0.30), 1)
    ohi = round(_clamp(lrs * 0.40 + (100 - srs) * 0.35 + fsc * 0.25), 1)

    prediction = _predict(ohi, srs, lrs, fsc)
    insights = _insights(lrs, srs, fsc, str(form_data["stage"]), str(form_data["industry"]))
    kpis = [
        {"name": "Leadership Readiness", "score": lrs, "band": _band(lrs)},
        {"name": "Scaling Risk", "score": srs, "band": f"{_risk_band(srs)} Risk"},
        {"name": "Financial Stability", "score": fsc, "band": _band(fsc)},
        {"name": "Org. Health Index", "score": ohi, "band": _band(ohi)},
    ]

    return {
        "company_name": str(form_data["company_name"]).strip() or "Your Company",
        "industry": str(form_data["industry"]).title(),
        "stage": str(form_data["stage"]).title(),
        "employee_count": int(form_data["employee_count"]),
        "raw_inputs": dict(form_data),
        "lrs": lrs,
        "srs": srs,
        "fsc": fsc,
        "ohi": ohi,
        "lrs_band": _band(lrs),
        "srs_band": _risk_band(srs),
        "fsc_band": _band(fsc),
        "ohi_band": _band(ohi),
        "prediction": prediction,
        "insights": insights,
        "display_inputs": _display_inputs(form_data),
        "kpis": kpis,
        "explanation": (
            "Each input is normalised to a 0–100 scale using domain-calibrated functions "
            "(e.g., D/E ratio, cash flow change, retention %). "
            "KPIs are computed as weighted composites, and the success prediction combines "
            "OHI (55%), inverse Scaling Risk (30%), and Financial Stability (15%) into a "
            "transparent probability estimate."
        ),
    }


def run_ai_analysis(form: Mapping[str, Any]) -> Dict[str, Any]:
    form_data = build_form_data(form)
    return analyze_company(form_data)
