from __future__ import annotations

from copy import deepcopy

from analysis_engine import DEFAULT_FORM_DATA


AVAILABLE_PROVIDERS = [
    {
        "key": "bamboohr",
        "label": "BambooHR Demo Feed",
        "description": "Loads a local BambooHR-style sample payload into the analysis form.",
    },
    {
        "key": "workday",
        "label": "Workday Demo Feed",
        "description": "Loads a local Workday-style sample payload into the analysis form.",
    },
]


DEMO_PROVIDER_PAYLOADS = {
    "bamboohr": {
        **DEFAULT_FORM_DATA,
        "company_name": "Atlas Retail Group",
        "industry": "retail",
        "stage": "growth",
        "employee_count": 340,
        "leadership_years": 11,
        "digital_score": 6.5,
        "retention_pct": 78,
        "churn_pct": 19,
        "dte_ratio": 0.9,
        "doc_score": 6,
        "dep_score": 2.5,
        "margin_pct": 8,
        "growth_pct": 16,
        "cash_months": 10,
    },
    "workday": {
        **DEFAULT_FORM_DATA,
        "company_name": "Northstar Manufacturing",
        "industry": "manufacturing",
        "stage": "mature",
        "employee_count": 620,
        "leadership_years": 14,
        "digital_score": 7,
        "retention_pct": 84,
        "churn_pct": 10,
        "dte_ratio": 0.7,
        "doc_score": 7.5,
        "dep_score": 2,
        "margin_pct": 12,
        "growth_pct": 9,
        "cash_months": 14,
    },
}


def fetch_provider_profile(provider_key: str) -> dict:
    provider_key = provider_key.lower().strip()
    payload = DEMO_PROVIDER_PAYLOADS.get(provider_key)
    if payload is None:
        raise ValueError(f"Unknown HR provider: {provider_key}")
    return deepcopy(payload)
