"""
external_apis.py
Thin wrappers around free public APIs (no API key required) sourced from
github.com/public-apis/public-apis. Used to enrich the HR analysis tool
with real-world economic, city quality-of-life, currency and demo-profile data.

APIs used:
  - World Bank Open Data  https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
  - Teleport Urban Areas  https://developers.teleport.org/
  - Frankfurter           https://www.frankfurter.app/docs
  - REST Countries        https://restcountries.com
  - RandomUser            https://randomuser.me
"""
from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

_TIMEOUT = 6  # seconds for all outbound requests


# ---------------------------------------------------------------------------
# World Bank Open Data  (no auth required)
# Docs: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
# ---------------------------------------------------------------------------

WORLD_BANK_INDICATORS = {
    "gdp_growth": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "label": "GDP Growth Rate (%)",
        "description": "Annual GDP growth at constant 2015 US$ prices.",
    },
    "unemployment": {
        "code": "SL.UEM.TOTL.ZS",
        "label": "Unemployment Rate (%)",
        "description": "Unemployment as % of total labour force (ILO modelled estimate).",
    },
    "employment_ratio": {
        "code": "SL.EMP.TOTL.SP.ZS",
        "label": "Employment-to-Population Ratio (%)",
        "description": "Employment-to-population ratio for ages 15+ (ILO modelled estimate).",
    },
    "gdp_per_capita": {
        "code": "NY.GDP.PCAP.CD",
        "label": "GDP per Capita (current US$)",
        "description": "Gross domestic product divided by midyear population.",
    },
}


def get_world_bank_indicator(
    country_code: str,
    indicator_key: str,
    most_recent_years: int = 5,
) -> dict[str, Any]:
    """
    Fetch a World Bank indicator for *country_code* (ISO-2, e.g. "US", "GB").
    Returns a dict with ``label``, ``country``, ``values`` (list of dicts with
    ``year`` and ``value``), and ``source``.
    """
    indicator = WORLD_BANK_INDICATORS.get(indicator_key)
    if indicator is None:
        return {"error": f"Unknown indicator key: {indicator_key}"}

    url = (
        f"https://api.worldbank.org/v2/country/{country_code}"
        f"/indicator/{indicator['code']}"
        f"?format=json&mrv={most_recent_years}&per_page={most_recent_years}"
    )
    try:
        response = requests.get(url, timeout=_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        # World Bank returns [metadata, [records]]
        records = data[1] if isinstance(data, list) and len(data) > 1 else []
        values = [
            {"year": int(r["date"]), "value": round(r["value"], 2) if r["value"] is not None else None}
            for r in records
            if r.get("value") is not None
        ]
        values.sort(key=lambda x: x["year"], reverse=True)
        return {
            "indicator_key": indicator_key,
            "label": indicator["label"],
            "description": indicator["description"],
            "country": country_code.upper(),
            "values": values,
            "source": "World Bank Open Data",
            "source_url": "https://data.worldbank.org",
        }
    except Exception as exc:
        logger.warning("World Bank API error for %s / %s: %s", country_code, indicator_key, exc)
        return {"error": str(exc), "indicator_key": indicator_key, "label": indicator["label"], "values": []}


def get_world_bank_country_profile(country_code: str) -> dict[str, Any]:
    """
    Fetch GDP growth, unemployment, and employment ratio for a country
    and return them as a combined profile dict.
    """
    results: dict[str, Any] = {"country": country_code.upper(), "indicators": {}}
    for key in ("gdp_growth", "unemployment", "employment_ratio"):
        data = get_world_bank_indicator(country_code, key, most_recent_years=3)
        results["indicators"][key] = data
    return results


# ---------------------------------------------------------------------------
# Teleport Urban Areas quality-of-life scores  (no auth required)
# Docs: https://developers.teleport.org/api/
# ---------------------------------------------------------------------------

def get_teleport_city_scores(city_name: str) -> dict[str, Any]:
    """
    Search for *city_name* in the Teleport API and return quality-of-life
    scores for the matched urban area.  Returns a dict with ``city``,
    ``urban_area``, ``scores`` (list), and ``summary``.
    """
    search_url = f"https://api.teleport.org/api/cities/?search={requests.utils.quote(city_name)}&embed=city:search-results/city:item/city:urban_area/ua:scores"
    try:
        response = requests.get(search_url, timeout=_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        results = (
            data.get("_embedded", {})
            .get("city:search-results", [])
        )
        if not results:
            return {"error": f"No city found for: {city_name}", "city": city_name, "scores": []}

        first = results[0]
        item = first.get("_embedded", {}).get("city:item", {})
        ua_embed = item.get("_embedded", {}).get("city:urban_area", {})
        scores_embed = ua_embed.get("_embedded", {}).get("ua:scores", {})
        urban_name = ua_embed.get("name", city_name)
        teleport_scores = scores_embed.get("teleport_city_score", 0)
        categories = scores_embed.get("categories", [])

        scores = [
            {
                "name": cat.get("name", ""),
                "score": round(cat.get("score_out_of_10", 0), 1),
                "color": cat.get("color", "#888"),
            }
            for cat in categories
        ]

        return {
            "city": city_name,
            "urban_area": urban_name,
            "teleport_score": round(teleport_scores, 1),
            "scores": scores,
            "source": "Teleport API",
            "source_url": "https://teleport.org",
        }
    except Exception as exc:
        logger.warning("Teleport API error for %s: %s", city_name, exc)
        return {"error": str(exc), "city": city_name, "scores": []}


# ---------------------------------------------------------------------------
# Frankfurter Exchange Rates  (no auth required)
# Docs: https://www.frankfurter.app/docs
# ---------------------------------------------------------------------------

def get_exchange_rates(base_currency: str = "USD", target_currencies: list[str] | None = None) -> dict[str, Any]:
    """
    Fetch the latest exchange rates from Frankfurter for *base_currency*.
    If *target_currencies* is provided, only those rates are returned.
    Returns a dict with ``base``, ``date``, ``rates``, and ``source``.
    """
    url = f"https://api.frankfurter.app/latest?from={base_currency.upper()}"
    if target_currencies:
        url += "&to=" + ",".join(c.upper() for c in target_currencies)
    try:
        response = requests.get(url, timeout=_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return {
            "base": data.get("base", base_currency.upper()),
            "date": data.get("date", ""),
            "rates": data.get("rates", {}),
            "source": "Frankfurter API",
            "source_url": "https://www.frankfurter.app",
        }
    except Exception as exc:
        logger.warning("Frankfurter API error: %s", exc)
        return {"error": str(exc), "base": base_currency.upper(), "rates": {}}


# ---------------------------------------------------------------------------
# REST Countries  (no auth required)
# Docs: https://restcountries.com
# ---------------------------------------------------------------------------

def get_country_info(country_name: str) -> dict[str, Any]:
    """
    Fetch basic country data (official name, capital, region, population,
    currencies, languages) from REST Countries by common name.
    """
    url = f"https://restcountries.com/v3.1/name/{requests.utils.quote(country_name)}?fields=name,capital,region,subregion,population,currencies,languages,flag,cca2"
    try:
        response = requests.get(url, timeout=_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if not data:
            return {"error": f"Country not found: {country_name}"}
        country = data[0]
        currencies = {code: info.get("name", code) for code, info in country.get("currencies", {}).items()}
        languages = list(country.get("languages", {}).values())
        return {
            "name": country.get("name", {}).get("official", country_name),
            "cca2": country.get("cca2", ""),
            "capital": (country.get("capital") or ["N/A"])[0],
            "region": country.get("region", ""),
            "subregion": country.get("subregion", ""),
            "population": country.get("population", 0),
            "currencies": currencies,
            "languages": languages,
            "flag": country.get("flag", ""),
            "source": "REST Countries",
            "source_url": "https://restcountries.com",
        }
    except Exception as exc:
        logger.warning("REST Countries API error for %s: %s", country_name, exc)
        return {"error": str(exc), "name": country_name}


# ---------------------------------------------------------------------------
# RandomUser  (no auth required)
# Docs: https://randomuser.me
# ---------------------------------------------------------------------------

def get_demo_employee_profiles(
    count: int = 6,
    nationality: str = "us",
) -> dict[str, Any]:
    """
    Generate realistic demo employee profiles using the RandomUser API.
    Returns a dict with ``employees`` (list) and ``source``.
    """
    url = f"https://randomuser.me/api/?results={count}&nat={nationality}&inc=name,email,location,dob,phone,picture"
    try:
        response = requests.get(url, timeout=_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        raw = data.get("results", [])
        employees = []
        titles = ["Software Engineer", "Product Manager", "HR Specialist", "Finance Analyst",
                  "Operations Manager", "Marketing Lead", "Data Scientist", "DevOps Engineer",
                  "UX Designer", "Business Analyst", "Legal Counsel", "Customer Success Manager"]
        departments = ["Engineering", "Product", "HR", "Finance", "Operations", "Marketing"]
        for i, person in enumerate(raw):
            name = person.get("name", {})
            location = person.get("location", {})
            dob = person.get("dob", {})
            picture = person.get("picture", {})
            employees.append({
                "full_name": f"{name.get('first', '')} {name.get('last', '')}",
                "email": person.get("email", ""),
                "phone": person.get("phone", ""),
                "city": location.get("city", ""),
                "country": location.get("country", ""),
                "age": dob.get("age", 0),
                "title": titles[i % len(titles)],
                "department": departments[i % len(departments)],
                "thumbnail": picture.get("thumbnail", ""),
            })
        return {
            "employees": employees,
            "count": len(employees),
            "source": "RandomUser API",
            "source_url": "https://randomuser.me",
        }
    except Exception as exc:
        logger.warning("RandomUser API error: %s", exc)
        return {"error": str(exc), "employees": [], "count": 0}


# ---------------------------------------------------------------------------
# Convenience: combined market-context snapshot
# ---------------------------------------------------------------------------

INDUSTRY_COUNTRY_MAP: dict[str, str] = {
    "technology": "US",
    "saas": "US",
    "finance": "GB",
    "healthcare": "US",
    "manufacturing": "DE",
    "retail": "US",
    "consulting": "GB",
    "energy": "NO",
    "logistics": "NL",
    "general": "US",
}

INDUSTRY_CITY_MAP: dict[str, str] = {
    "technology": "San Francisco",
    "saas": "Austin",
    "finance": "London",
    "healthcare": "Boston",
    "manufacturing": "Munich",
    "retail": "Chicago",
    "consulting": "New York",
    "energy": "Oslo",
    "logistics": "Amsterdam",
    "general": "New York",
}


def get_market_context(industry: str = "general", country_code: str | None = None) -> dict[str, Any]:
    """
    Return a combined market-context snapshot for the given *industry*
    including World Bank economic indicators, Teleport city scores,
    and Frankfurter exchange rates.
    """
    resolved_country = (country_code or INDUSTRY_COUNTRY_MAP.get(industry, "US")).upper()
    city = INDUSTRY_CITY_MAP.get(industry, "New York")

    world_bank = get_world_bank_country_profile(resolved_country)
    teleport = get_teleport_city_scores(city)
    fx_rates = get_exchange_rates("USD", ["EUR", "GBP", "JPY", "CHF"])

    return {
        "industry": industry,
        "country": resolved_country,
        "world_bank": world_bank,
        "teleport": teleport,
        "fx_rates": fx_rates,
    }
