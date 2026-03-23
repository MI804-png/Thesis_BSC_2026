from __future__ import annotations

import random
from typing import Any, Dict

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

from analysis_engine import (
    DEFAULT_FORM_DATA,
    ML_FEATURE_LABELS,
    NUMERIC_FIELD_SPECS,
    analyze_company,
    build_form_data,
    to_feature_vector,
)


_MODEL_CACHE: dict[str, Any] | None = None


def _random_sample(rng: random.Random) -> dict[str, Any]:
    sample = dict(DEFAULT_FORM_DATA)
    sample["company_name"] = f"Synthetic Org {rng.randint(1000, 9999)}"
    sample["industry"] = rng.choice(["general", "technology", "saas", "manufacturing", "finance"])
    sample["stage"] = rng.choice(["startup", "growth", "mature", "turnaround"])
    for field, spec in NUMERIC_FIELD_SPECS.items():
        if field == "employee_count":
            sample[field] = rng.randint(spec["min"], 3000)
        else:
            sample[field] = round(rng.uniform(spec["min"], spec["max"]), 2)
    return build_form_data(sample)


def _train_model() -> dict[str, Any]:
    rng = random.Random(42)
    samples = [_random_sample(rng) for _ in range(900)]

    features = [to_feature_vector(sample) for sample in samples]
    targets = [analyze_company(sample)["prediction"]["probability"] for sample in samples]

    split_index = int(len(samples) * 0.8)
    train_x = features[:split_index]
    train_y = targets[:split_index]
    test_x = features[split_index:]
    test_y = targets[split_index:]

    model = GradientBoostingRegressor(random_state=42)
    model.fit(train_x, train_y)
    predictions = model.predict(test_x)

    return {
        "model": model,
        "feature_names": list(ML_FEATURE_LABELS),
        "feature_labels": ML_FEATURE_LABELS,
        "training_samples": len(samples),
        "r2": round(r2_score(test_y, predictions), 4),
        "mae": round(mean_absolute_error(test_y, predictions), 3),
        "baseline": {
            field: sum(sample[field] for sample in samples) / len(samples)
            for field in ML_FEATURE_LABELS
        },
        "ranges": {
            field: max(1.0, NUMERIC_FIELD_SPECS[field]["max"] - NUMERIC_FIELD_SPECS[field]["min"])
            for field in ML_FEATURE_LABELS
        },
    }


def get_model_bundle() -> dict[str, Any]:
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        _MODEL_CACHE = _train_model()
    return _MODEL_CACHE


def get_model_summary() -> Dict[str, Any]:
    bundle = get_model_bundle()
    return {
        "name": "Gradient Boosting Regressor",
        "training_samples": bundle["training_samples"],
        "r2": bundle["r2"],
        "mae": bundle["mae"],
    }


def get_ml_prediction(form_data: dict[str, Any]) -> Dict[str, Any]:
    bundle = get_model_bundle()
    model = bundle["model"]
    feature_vector = [to_feature_vector(form_data)]
    prediction = round(float(model.predict(feature_vector)[0]), 1)

    importances = getattr(model, "feature_importances_", [])
    contributions = []
    for index, field in enumerate(bundle["feature_names"]):
        baseline = bundle["baseline"][field]
        span = bundle["ranges"][field]
        delta = (float(form_data[field]) - baseline) / span
        contribution = round(delta * float(importances[index]) * 100, 2)
        contributions.append(
            {
                "label": bundle["feature_labels"][field],
                "value": round(float(form_data[field]), 2),
                "contribution": contribution,
            }
        )

    contributions.sort(key=lambda item: abs(item["contribution"]), reverse=True)
    top_contributors = contributions[:5]

    return {
        "probability": prediction,
        "model_name": "Gradient Boosting Regressor",
        "training_samples": bundle["training_samples"],
        "r2": bundle["r2"],
        "mae": bundle["mae"],
        "top_contributors": top_contributors,
        "explanation": (
            "The ML score is produced by a locally trained gradient boosting model calibrated on a synthetic "
            "organisational dataset derived from the current scoring logic. The contribution view highlights the "
            "largest feature movements relative to the training baseline."
        ),
    }
