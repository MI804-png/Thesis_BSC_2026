from __future__ import annotations

from copy import deepcopy

from analysis_engine import DEFAULT_FORM_DATA
from external_apis import get_demo_employee_profiles


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
    {
        "key": "randomuser_tech",
        "label": "Live Tech Startup (RandomUser)",
        "description": "Generates a technology-sector startup profile using the free RandomUser API for realistic employee metadata.",
    },
    {
        "key": "randomuser_finance",
        "label": "Live Finance Firm (RandomUser)",
        "description": "Generates a finance-sector mature-stage profile using the free RandomUser API for realistic employee metadata.",
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


def _build_randomuser_profile(industry: str, stage: str, base_overrides: dict) -> dict:
    """
    Build an analysis form payload enriched with real employee names & metadata
    fetched from the RandomUser public API (no API key required).
    https://randomuser.me
    """
    profile_data = get_demo_employee_profiles(count=6, nationality="us")
    employees = profile_data.get("employees", [])
    # Derive a company name from the first employee's city if available
    city = employees[0]["city"] if employees else "Metro"
    suffix_map = {
        "technology": "Tech Solutions",
        "finance": "Capital Partners",
        "manufacturing": "Industrial Group",
        "retail": "Commerce Co.",
        "healthcare": "Health Systems",
        "saas": "Cloud Labs",
        "consulting": "Advisory Services",
        "energy": "Energy Corp",
        "logistics": "Logistics Network",
        "general": "Enterprise Group",
    }
    suffix = suffix_map.get(industry, "Enterprise Group")
    company_name = f"{city} {suffix}"

    payload = {
        **DEFAULT_FORM_DATA,
        **base_overrides,
        "company_name": company_name,
        "industry": industry,
        "stage": stage,
        "_live_employees": employees,
        "_source": "RandomUser API",
    }
    return payload


_RANDOMUSER_PROVIDER_CONFIGS = {
    "randomuser_tech": {
        "industry": "technology",
        "stage": "growth",
        "base_overrides": {
            "employee_count": 95,
            "leadership_years": 7,
            "digital_score": 8.5,
            "retention_pct": 83,
            "churn_pct": 14,
            "dte_ratio": 0.4,
            "doc_score": 7,
            "dep_score": 2,
            "margin_pct": 22,
            "growth_pct": 38,
            "cash_months": 18,
        },
    },
    "randomuser_finance": {
        "industry": "finance",
        "stage": "mature",
        "base_overrides": {
            "employee_count": 410,
            "leadership_years": 16,
            "digital_score": 6.5,
            "retention_pct": 88,
            "churn_pct": 8,
            "dte_ratio": 1.2,
            "doc_score": 8.5,
            "dep_score": 1.5,
            "margin_pct": 14,
            "growth_pct": 7,
            "cash_months": 20,
        },
    },
}


def fetch_provider_profile(provider_key: str) -> dict:
    provider_key = provider_key.lower().strip()

    # Local demo payloads
    payload = DEMO_PROVIDER_PAYLOADS.get(provider_key)
    if payload is not None:
        return deepcopy(payload)

    # Live RandomUser-backed providers
    config = _RANDOMUSER_PROVIDER_CONFIGS.get(provider_key)
    if config is not None:
        return _build_randomuser_profile(
            industry=config["industry"],
            stage=config["stage"],
            base_overrides=config["base_overrides"],
        )

    raise ValueError(f"Unknown HR provider: {provider_key}")
