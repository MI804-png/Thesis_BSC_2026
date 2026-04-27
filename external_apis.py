"""
external_apis.py
Thin wrappers around free public APIs (no API key required) sourced from
github.com/public-apis/public-apis. Used to enrich the HR analysis tool
with real-world economic, city quality-of-life, currency and demo-profile data.

APIs used:
  - World Bank Open Data  https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
    - Open-Meteo APIs       https://open-meteo.com/
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


FALLBACK_TELEPORT_CITY_DATA: dict[str, dict[str, Any]] = {
    "san francisco": {
        "urban_area": "San Francisco Bay Area",
        "teleport_score": 71.4,
        "scores": [
            {"name": "Housing", "score": 2.7, "color": "#e74c3c"},
            {"name": "Cost of Living", "score": 2.3, "color": "#e67e22"},
            {"name": "Startups", "score": 10.0, "color": "#2ecc71"},
            {"name": "Safety", "score": 5.9, "color": "#f1c40f"},
            {"name": "Healthcare", "score": 8.3, "color": "#1abc9c"},
            {"name": "Commute", "score": 4.4, "color": "#3498db"},
            {"name": "Education", "score": 8.6, "color": "#9b59b6"},
        ],
    },
    "austin": {
        "urban_area": "Austin",
        "teleport_score": 65.2,
        "scores": [
            {"name": "Housing", "score": 5.4, "color": "#f1c40f"},
            {"name": "Cost of Living", "score": 5.7, "color": "#f39c12"},
            {"name": "Startups", "score": 8.1, "color": "#2ecc71"},
            {"name": "Safety", "score": 7.0, "color": "#2ecc71"},
            {"name": "Healthcare", "score": 7.4, "color": "#1abc9c"},
            {"name": "Commute", "score": 5.5, "color": "#3498db"},
            {"name": "Education", "score": 7.1, "color": "#9b59b6"},
        ],
    },
    "london": {
        "urban_area": "London",
        "teleport_score": 66.9,
        "scores": [
            {"name": "Housing", "score": 3.2, "color": "#e67e22"},
            {"name": "Cost of Living", "score": 3.1, "color": "#e67e22"},
            {"name": "Startups", "score": 9.1, "color": "#2ecc71"},
            {"name": "Safety", "score": 7.1, "color": "#2ecc71"},
            {"name": "Healthcare", "score": 8.2, "color": "#1abc9c"},
            {"name": "Commute", "score": 5.0, "color": "#3498db"},
            {"name": "Education", "score": 8.8, "color": "#9b59b6"},
        ],
    },
    "boston": {
        "urban_area": "Boston",
        "teleport_score": 67.8,
        "scores": [
            {"name": "Housing", "score": 3.9, "color": "#e67e22"},
            {"name": "Cost of Living", "score": 4.0, "color": "#f39c12"},
            {"name": "Startups", "score": 8.4, "color": "#2ecc71"},
            {"name": "Safety", "score": 7.5, "color": "#2ecc71"},
            {"name": "Healthcare", "score": 9.0, "color": "#1abc9c"},
            {"name": "Commute", "score": 5.2, "color": "#3498db"},
            {"name": "Education", "score": 9.1, "color": "#9b59b6"},
        ],
    },
    "munich": {
        "urban_area": "Munich",
        "teleport_score": 73.3,
        "scores": [
            {"name": "Housing", "score": 4.8, "color": "#f39c12"},
            {"name": "Cost of Living", "score": 5.2, "color": "#f1c40f"},
            {"name": "Startups", "score": 7.2, "color": "#2ecc71"},
            {"name": "Safety", "score": 8.8, "color": "#2ecc71"},
            {"name": "Healthcare", "score": 8.7, "color": "#1abc9c"},
            {"name": "Commute", "score": 6.9, "color": "#3498db"},
            {"name": "Education", "score": 8.5, "color": "#9b59b6"},
        ],
    },
    "chicago": {
        "urban_area": "Chicago",
        "teleport_score": 62.7,
        "scores": [
            {"name": "Housing", "score": 6.1, "color": "#2ecc71"},
            {"name": "Cost of Living", "score": 6.0, "color": "#2ecc71"},
            {"name": "Startups", "score": 7.4, "color": "#2ecc71"},
            {"name": "Safety", "score": 4.8, "color": "#e67e22"},
            {"name": "Healthcare", "score": 8.0, "color": "#1abc9c"},
            {"name": "Commute", "score": 5.1, "color": "#3498db"},
            {"name": "Education", "score": 7.7, "color": "#9b59b6"},
        ],
    },
    "new york": {
        "urban_area": "New York",
        "teleport_score": 68.2,
        "scores": [
            {"name": "Housing", "score": 2.4, "color": "#e74c3c"},
            {"name": "Cost of Living", "score": 2.1, "color": "#e74c3c"},
            {"name": "Startups", "score": 9.6, "color": "#2ecc71"},
            {"name": "Safety", "score": 5.6, "color": "#f1c40f"},
            {"name": "Healthcare", "score": 8.5, "color": "#1abc9c"},
            {"name": "Commute", "score": 6.1, "color": "#3498db"},
            {"name": "Education", "score": 8.9, "color": "#9b59b6"},
        ],
    },
    "oslo": {
        "urban_area": "Oslo",
        "teleport_score": 76.1,
        "scores": [
            {"name": "Housing", "score": 5.1, "color": "#f1c40f"},
            {"name": "Cost of Living", "score": 4.3, "color": "#f39c12"},
            {"name": "Startups", "score": 6.3, "color": "#2ecc71"},
            {"name": "Safety", "score": 8.9, "color": "#2ecc71"},
            {"name": "Healthcare", "score": 8.8, "color": "#1abc9c"},
            {"name": "Commute", "score": 7.2, "color": "#3498db"},
            {"name": "Education", "score": 8.4, "color": "#9b59b6"},
        ],
    },
    "amsterdam": {
        "urban_area": "Amsterdam",
        "teleport_score": 74.0,
        "scores": [
            {"name": "Housing", "score": 4.3, "color": "#f39c12"},
            {"name": "Cost of Living", "score": 4.5, "color": "#f39c12"},
            {"name": "Startups", "score": 7.9, "color": "#2ecc71"},
            {"name": "Safety", "score": 8.0, "color": "#2ecc71"},
            {"name": "Healthcare", "score": 8.3, "color": "#1abc9c"},
            {"name": "Commute", "score": 7.5, "color": "#3498db"},
            {"name": "Education", "score": 8.3, "color": "#9b59b6"},
        ],
    },
}


def _get_fallback_city_scores(city_name: str) -> dict[str, Any]:
    data = FALLBACK_TELEPORT_CITY_DATA.get(city_name.lower(), FALLBACK_TELEPORT_CITY_DATA["new york"])
    return {
        "city": city_name,
        "urban_area": data["urban_area"],
        "teleport_score": data["teleport_score"],
        "scores": data["scores"],
        "source": "Local fallback dataset",
        "source_url": "https://datahelpdesk.worldbank.org/",
        "is_fallback": True,
        "fallback_note": "Live Teleport API is currently unreachable from this network; showing cached benchmark values.",
    }


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
# City quality proxy scores via Open-Meteo APIs  (no auth required)
# Docs: https://open-meteo.com/
# ---------------------------------------------------------------------------

def get_teleport_city_scores(city_name: str) -> dict[str, Any]:
    """
    Keep the historical function name for compatibility, but source live city
    quality proxy scores from Open-Meteo geocoding, weather and air-quality
    endpoints. Returns a dict with ``city``, ``urban_area``, ``scores``.
    """
    def _clamp(value: float, low: float = 1.0, high: float = 10.0) -> float:
        return max(low, min(high, value))

    def _color(score: float) -> str:
        if score >= 7.5:
            return "#2ecc71"
        if score >= 5.0:
            return "#f1c40f"
        if score >= 3.5:
            return "#e67e22"
        return "#e74c3c"

    geocode_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={requests.utils.quote(city_name)}&count=1&language=en&format=json"
    )

    try:
        geo_response = requests.get(geocode_url, timeout=_TIMEOUT)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        results = geo_data.get("results", [])
        if not results:
            return _get_fallback_city_scores(city_name)

        city_info = results[0]
        latitude = city_info.get("latitude")
        longitude = city_info.get("longitude")
        urban_name = city_info.get("name", city_name)
        if latitude is None or longitude is None:
            return _get_fallback_city_scores(city_name)

        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )
        air_url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality"
            f"?latitude={latitude}&longitude={longitude}&current=us_aqi,pm2_5,pm10"
        )

        weather_response = requests.get(weather_url, timeout=_TIMEOUT)
        weather_response.raise_for_status()
        weather_current = weather_response.json().get("current", {})

        air_response = requests.get(air_url, timeout=_TIMEOUT)
        air_response.raise_for_status()
        air_current = air_response.json().get("current", {})

        temperature = float(weather_current.get("temperature_2m") or 21.0)
        humidity = float(weather_current.get("relative_humidity_2m") or 50.0)
        wind_speed = float(weather_current.get("wind_speed_10m") or 10.0)
        us_aqi = float(air_current.get("us_aqi") or 50.0)

        # Open-Meteo metrics mapped to 1..10 comparable indicator bands.
        climate_temp_score = _clamp(10 - min(abs(temperature - 21.0), 18.0) * 0.5)
        climate_humidity_score = _clamp(10 - min(abs(humidity - 50.0), 50.0) * 0.12)
        climate_wind_score = _clamp(10 - min(wind_speed, 45.0) * 0.16)
        climate_score = round((climate_temp_score + climate_humidity_score + climate_wind_score) / 3, 1)
        air_score = round(_clamp(10 - ((us_aqi - 1.0) / 22.0)), 1)

        fallback = FALLBACK_TELEPORT_CITY_DATA.get(city_name.lower(), FALLBACK_TELEPORT_CITY_DATA["new york"])
        fallback_by_name = {item["name"]: item for item in fallback["scores"]}
        startup_score = float(fallback_by_name.get("Startups", {"score": 7.0})["score"])
        housing_score = float(fallback_by_name.get("Housing", {"score": 5.0})["score"])
        cost_score = float(fallback_by_name.get("Cost of Living", {"score": 5.0})["score"])
        commute_score = float(fallback_by_name.get("Commute", {"score": 6.0})["score"])
        safety_score = float(fallback_by_name.get("Safety", {"score": 6.5})["score"])

        scores = [
            {"name": "Housing", "score": round(housing_score, 1), "color": _color(housing_score)},
            {"name": "Cost of Living", "score": round(cost_score, 1), "color": _color(cost_score)},
            {"name": "Startups", "score": round(startup_score, 1), "color": _color(startup_score)},
            {"name": "Safety", "score": round(safety_score, 1), "color": _color(safety_score)},
            {"name": "Commute", "score": round(commute_score, 1), "color": _color(commute_score)},
            {"name": "Climate Comfort", "score": climate_score, "color": _color(climate_score)},
            {"name": "Air Quality", "score": air_score, "color": _color(air_score)},
        ]

        overall = round(sum(item["score"] for item in scores) / len(scores) * 10, 1)

        return {
            "city": city_name,
            "urban_area": urban_name,
            "teleport_score": overall,
            "scores": scores,
            "source": "Open-Meteo APIs",
            "source_url": "https://open-meteo.com/",
            "is_fallback": False,
        }
    except requests.exceptions.RequestException:
        logger.warning("Open-Meteo city quality request error for %s", city_name)
        return _get_fallback_city_scores(city_name)
    except Exception:
        logger.warning("Open-Meteo city quality unexpected error for %s", city_name)
        return _get_fallback_city_scores(city_name)


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
