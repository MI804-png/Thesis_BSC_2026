from __future__ import annotations

import csv
import io
import os
from functools import wraps
from statistics import mean
from typing import Any, Callable

from flask import Flask, abort, flash, g, redirect, render_template, request, send_file, session, url_for

from analysis_engine import (
    DEFAULT_FORM_DATA,
    INDUSTRY_OPTIONS,
    NUMERIC_FIELD_SPECS,
    STAGE_OPTIONS,
    build_form_data,
    run_ai_analysis,
)
from data_store import (
    DEFAULT_USERS,
    authenticate_user,
    get_analysis_by_id,
    get_user_by_id,
    init_db,
    list_company_history,
    list_recent_analyses,
    save_analysis,
)
from hr_integrations import AVAILABLE_PROVIDERS, fetch_provider_profile
from ml_engine import get_ml_prediction, get_model_summary
from reporting import build_analysis_pdf
from section_data import SECTIONS

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-thesis-hr-secret")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

init_db()

THESIS_CONTENT = {
    "title": "Design and Implementation of a Data-Driven HR and Management Decision Support System for Organizational Performance and Risk Analysis",
    "abstract": (
        "Modern organizations increasingly require data-driven tools to support managerial decision-making "
        "and organizational performance evaluation. Traditional HR systems are often administrative and provide "
        "limited strategic analytics. This project demonstrates a role-based HR and management analytics platform "
        "that unifies company profile data, leadership factors, investment context, financial performance, and "
        "operational indicators into a single analysis workflow."
    ),
    "sections": [
        "Introduction and Problem Definition",
        "Literature Review and Related Work",
        "System Design and Architecture",
        "Implementation and System Development",
        "Results, Evaluation, and Future Work",
    ],
}

FUTURE_WORK_EXTENSIONS = [
    {
        "title": "Machine Learning Scoring",
        "priority": "High",
        "detail": (
            "Replaces weighted formulas with a locally trained gradient boosting model calibrated on a synthetic "
            "organisational dataset derived from the current scoring logic."
        ),
    },
    {
        "title": "CSV Bulk Ingestion Pipeline",
        "priority": "High",
        "detail": (
            "Accepts structured CSV uploads for multi-company batch analysis, with validation notes, "
            "outlier flagging, storage, and comparative ranking."
        ),
    },
    {
        "title": "Persistent Database Integration",
        "priority": "Medium",
        "detail": (
            "Uses SQLite locally to store analysis history, enable trend tracking, and support longitudinal "
            "performance monitoring."
        ),
    },
    {
        "title": "User Authentication and RBAC",
        "priority": "Medium",
        "detail": (
            "Implements role-based access control with authenticated sessions so each manager role receives "
            "its authorised dashboard view."
        ),
    },
    {
        "title": "PDF Report Export",
        "priority": "Medium",
        "detail": (
            "Generates a downloadable, formatted PDF analysis report per saved company case, suitable for "
            "board reporting and audit documentation."
        ),
    },
    {
        "title": "Real-Time HR Data Integration",
        "priority": "Future",
        "detail": (
            "Provides local BambooHR and Workday demo connectors that prefill the analysis form using provider-style "
            "payloads and can be replaced with live API credentials later."
        ),
    },
]

ROLE_FOCUS = {
    "ceo": {
        "title": "CEO View",
        "goal": "Strategic alignment, growth readiness, and enterprise-wide risk posture.",
        "allowed_roles": ["ceo", "admin"],
        "kpis": [
            {
                "name": "Overall Organizational Health Index",
                "score_key": "ohi",
                "fallback": 82,
                "band": "Strong",
                "summary": "Cross-functional health snapshot for executive review.",
                "detail": "This score blends leadership readiness, inverse scaling risk, and financial stability into a single strategic signal.",
            },
            {
                "name": "Scaling Risk Score",
                "score_key": "srs",
                "fallback": 41,
                "band": "Medium Risk",
                "summary": "Expansion risk level across people, debt, and process stability.",
                "detail": "This score tracks the pressure created by churn, leverage, fragile processes, and dependency concentration.",
            },
            {
                "name": "Revenue Growth Outlook",
                "raw_key": "growth_pct",
                "fallback": 74,
                "band": "Positive",
                "summary": "Forward-looking growth momentum used in board planning.",
                "detail": "This score reflects the current top-line growth trend and whether present commercial performance supports expansion plans.",
            },
        ],
    },
    "hr": {
        "title": "HR View",
        "goal": "Leadership readiness, people capability, and talent stability.",
        "allowed_roles": ["hr", "admin"],
        "kpis": [
            {
                "name": "Leadership Readiness Score",
                "score_key": "lrs",
                "fallback": 76,
                "band": "Strong",
                "summary": "Executive capability and succession resilience indicator.",
                "detail": "This score combines leadership experience, digital maturity, and retention performance to estimate people-side readiness.",
            },
            {
                "name": "Talent Retention",
                "raw_key": "retention_pct",
                "fallback": 80,
                "band": "Stable",
                "summary": "Retention trend across core teams and high-value roles.",
                "detail": "This score reflects annual talent stability and whether employee turnover is likely to disrupt delivery capacity.",
            },
            {
                "name": "Capability Maturity",
                "calc": "capability_maturity",
                "fallback": 69,
                "band": "Developing",
                "summary": "Workforce capability depth and process readiness signal.",
                "detail": "This score indicates how prepared the organisation is to support growth through repeatable skills, tooling, and role depth.",
            },
        ],
    },
    "finance": {
        "title": "Finance View",
        "goal": "Capital efficiency, asset movement, cash flow trends, and debt pressure.",
        "allowed_roles": ["finance", "admin"],
        "kpis": [
            {
                "name": "Current Asset Change",
                "raw_key": "margin_pct",
                "fallback": 68,
                "band": "Moderate",
                "summary": "Movement in near-term assets across the latest reporting period.",
                "detail": "This score shows whether liquid and near-liquid assets are moving in a direction that supports short-term operating flexibility.",
            },
            {
                "name": "Debt Ratio",
                "raw_key": "dte_ratio",
                "fallback": 52,
                "band": "Watchlist",
                "summary": "Leverage pressure relative to balance-sheet resilience.",
                "detail": "This score indicates how much debt structure is constraining financial flexibility and increasing downside exposure.",
            },
            {
                "name": "Cash Flow Change",
                "raw_key": "cash_months",
                "fallback": 71,
                "band": "Healthy",
                "summary": "Period-over-period cash flow direction and stability signal.",
                "detail": "This score reflects whether operating cash movement is improving fast enough to support obligations, hiring, and planned investment.",
            },
        ],
    },
    "operations": {
        "title": "Operations View",
        "goal": "Execution reliability, process fragility, and delivery confidence.",
        "allowed_roles": ["operations", "admin"],
        "kpis": [
            {
                "name": "Process Fragility",
                "calc": "process_fragility",
                "fallback": 47,
                "band": "Needs Attention",
                "summary": "Measures undocumented workflows and brittle dependencies.",
                "detail": "This score estimates how easily delivery quality could degrade when informal process knowledge is lost or disrupted.",
            },
            {
                "name": "Operational Stability",
                "calc": "operational_stability",
                "fallback": 73,
                "band": "Stable",
                "summary": "Consistency of execution across day-to-day delivery activity.",
                "detail": "This score reflects how reliably the organisation can sustain output, handoffs, and operational quality under normal load.",
            },
            {
                "name": "Scaling Risk Score",
                "score_key": "srs",
                "fallback": 44,
                "band": "Medium Risk",
                "summary": "Delivery risk introduced by growth pressure and control gaps.",
                "detail": "This score shows whether current operating structure can absorb growth without creating service, people, or coordination failures.",
            },
        ],
    },
}


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if g.user is None:
            flash("Sign in to access the local analysis workspace.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@app.before_request
def load_current_user() -> None:
    user_id = session.get("user_id")
    g.user = get_user_by_id(user_id)


@app.context_processor
def inject_global_template_data() -> dict[str, Any]:
    return {"current_user": g.user}


def _score_from_result(item: dict[str, Any], result: dict[str, Any] | None) -> float:
    if result is None:
        return float(item["fallback"])
    if "score_key" in item:
        return float(result[item["score_key"]])
    if "raw_key" in item:
        return float(result["raw_inputs"][item["raw_key"]])
    if item.get("calc") == "capability_maturity":
        return round((float(result["raw_inputs"]["digital_score"]) * 10 + float(result["raw_inputs"]["doc_score"]) * 10) / 2, 1)
    if item.get("calc") == "process_fragility":
        return round((10 - float(result["raw_inputs"]["doc_score"])) * 10, 1)
    if item.get("calc") == "operational_stability":
        return round((float(result["lrs"]) + (100 - float(result["srs"]))) / 2, 1)
    return float(item["fallback"])


def _band_for_value(item: dict[str, Any], score: float) -> str:
    if item.get("raw_key") == "dte_ratio":
        return "Watchlist" if score >= 1 else "Healthy"
    if item.get("raw_key") in {"margin_pct", "cash_months", "growth_pct", "retention_pct"}:
        return "Positive" if score >= 0 else "Negative"
    return item["band"]


def build_role_dashboard(role_key: str, latest_result: dict[str, Any] | None) -> dict[str, Any] | None:
    config = ROLE_FOCUS.get(role_key)
    if config is None:
        return None
    role_data = {
        "title": config["title"],
        "goal": config["goal"],
        "allowed_roles": config["allowed_roles"],
        "kpis": [],
    }
    for item in config["kpis"]:
        score = _score_from_result(item, latest_result)
        role_data["kpis"].append(
            {
                "name": item["name"],
                "score": round(score, 1),
                "band": _band_for_value(item, score),
                "summary": item["summary"],
                "detail": item["detail"],
            }
        )
    return role_data


def _validate_csv_row(row: dict[str, str]) -> list[str]:
    notes: list[str] = []
    industry = str(row.get("industry", "")).strip().lower()
    stage = str(row.get("stage", "")).strip().lower()
    if industry and industry not in INDUSTRY_OPTIONS:
        notes.append("Industry defaulted")
    if stage and stage not in STAGE_OPTIONS:
        notes.append("Stage defaulted")

    for field, spec in NUMERIC_FIELD_SPECS.items():
        raw_value = str(row.get(field, "")).strip()
        if not raw_value:
            notes.append(f"{spec['label']} defaulted")
            continue
        try:
            numeric = float(raw_value)
        except ValueError:
            notes.append(f"{spec['label']} invalid")
            continue
        if numeric < spec["min"] or numeric > spec["max"]:
            notes.append(f"{spec['label']} clamped")
    return notes


def _build_history_summary(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not records:
        return None
    probabilities = [record["result"]["prediction"]["probability"] for record in records]
    ohi_scores = [record["result"]["ohi"] for record in records]
    return {
        "total": len(records),
        "avg_probability": round(mean(probabilities), 1),
        "avg_ohi": round(mean(ohi_scores), 1),
        "latest_company": records[0]["company_name"],
    }


def _build_company_trend(company_name: str, user_id: int, role: str) -> dict[str, Any] | None:
    history = list_company_history(company_name, user_id, role)
    if len(history) < 2:
        return None
    latest = history[0]["result"]
    oldest = history[-1]["result"]
    return {
        "company_name": company_name,
        "runs": len(history),
        "delta_ohi": round(latest["ohi"] - oldest["ohi"], 1),
        "delta_probability": round(
            latest["prediction"]["probability"] - oldest["prediction"]["probability"],
            1,
        ),
    }


def _analysis_context(**overrides: Any) -> dict[str, Any]:
    user_history = list_recent_analyses(g.user["id"], g.user["role"], limit=12)
    context = {
        "future_work": FUTURE_WORK_EXTENSIONS,
        "providers": AVAILABLE_PROVIDERS,
        "industry_options": INDUSTRY_OPTIONS,
        "stage_options": STAGE_OPTIONS,
        "model_summary": get_model_summary(),
        "form_data": dict(DEFAULT_FORM_DATA),
        "result": None,
        "batch_result": None,
        "recent_analyses": user_history,
        "history_summary": _build_history_summary(user_history),
        "company_trend": None,
        "local_demo_users": DEFAULT_USERS,
    }
    context.update(overrides)
    return context


@app.route("/")
def home():
    return render_template("home.html", thesis=THESIS_CONTENT)


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("analysis"))

    if request.method == "POST":
        user = authenticate_user(request.form.get("username", ""), request.form.get("password", ""))
        if user is None:
            flash("Invalid username or password.", "danger")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash(f"Signed in as {user['full_name']}.", "success")
            return redirect(request.args.get("next") or url_for("analysis"))

    return render_template("login.html", demo_users=DEFAULT_USERS)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("login"))


@app.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    context = _analysis_context()

    if request.method == "POST":
        action = request.form.get("action", "run-analysis")

        if action == "import-provider":
            provider_key = request.form.get("provider", "bamboohr")
            try:
                form_data = build_form_data(fetch_provider_profile(provider_key))
            except ValueError as exc:
                flash(str(exc), "danger")
                return render_template("analysis.html", **context)
            flash(f"Imported local demo data from {provider_key.title()}.", "success")
            context["form_data"] = form_data
            return render_template("analysis.html", **context)

        if action == "csv-upload":
            uploaded = request.files.get("csv_file")
            if uploaded is None or not uploaded.filename:
                flash("Select a CSV file to run bulk analysis.", "warning")
                return render_template("analysis.html", **context)

            content = uploaded.read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(content))
            rows = []
            ranking = []
            batch_name = uploaded.filename
            for index, row in enumerate(reader, start=2):
                form_data = build_form_data(row)
                result = run_ai_analysis(form_data)
                result["ml_prediction"] = get_ml_prediction(form_data)
                analysis_id = save_analysis(
                    created_by=g.user["id"],
                    company_name=result["company_name"],
                    payload=form_data,
                    result=result,
                    source="csv",
                    batch_name=batch_name,
                )
                notes = _validate_csv_row(row)
                row_summary = {
                    "row_number": index,
                    "analysis_id": analysis_id,
                    "company_name": result["company_name"],
                    "ohi": result["ohi"],
                    "probability": result["prediction"]["probability"],
                    "verdict": result["prediction"]["verdict"],
                    "notes": notes,
                }
                rows.append(row_summary)
                ranking.append(row_summary)

            ranking.sort(key=lambda item: item["ohi"], reverse=True)
            batch_result = {
                "filename": batch_name,
                "count": len(rows),
                "average_probability": round(mean(item["probability"] for item in rows), 1) if rows else 0,
                "top_company": ranking[0] if ranking else None,
                "rows": ranking,
            }
            flash(f"Processed {len(rows)} records from {batch_name}.", "success")
            context = _analysis_context(batch_result=batch_result)
            return render_template("analysis.html", **context)

        form_data = build_form_data(request.form)
        result = run_ai_analysis(form_data)
        result["ml_prediction"] = get_ml_prediction(form_data)
        analysis_id = save_analysis(
            created_by=g.user["id"],
            company_name=result["company_name"],
            payload=form_data,
            result=result,
            source="manual",
        )
        result["analysis_id"] = analysis_id
        context = _analysis_context(
            form_data=form_data,
            result=result,
            company_trend=_build_company_trend(result["company_name"], g.user["id"], g.user["role"]),
        )
        flash(f"Saved analysis #{analysis_id} for {result['company_name']}.", "success")
        return render_template("analysis.html", **context)

    return render_template("analysis.html", **context)


@app.route("/history")
@login_required
def history():
    records = list_recent_analyses(g.user["id"], g.user["role"], limit=40)
    return render_template(
        "history.html",
        records=records,
        history_summary=_build_history_summary(records),
    )


@app.route("/analysis/<int:analysis_id>/pdf")
@login_required
def export_analysis_pdf(analysis_id: int):
    record = get_analysis_by_id(analysis_id)
    if record is None:
        abort(404)
    if g.user["role"] != "admin" and record["created_by"] != g.user["id"]:
        abort(403)
    pdf_buffer = build_analysis_pdf(record)
    safe_name = record["company_name"].replace(" ", "_")
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{safe_name}_analysis_report.pdf",
        mimetype="application/pdf",
    )


@app.route("/section/<int:number>")
def section_view(number: int):
    sec = SECTIONS.get(number)
    if sec is None:
        abort(404)
    return render_template("section.html", sec=sec)


@app.route("/dashboard/<role>")
@login_required
def dashboard(role: str):
    role_key = role.lower()
    role_config = ROLE_FOCUS.get(role_key)
    if role_config is None:
        abort(404)
    if g.user["role"] not in role_config["allowed_roles"]:
        abort(403)

    latest_analysis = list_recent_analyses(g.user["id"], g.user["role"], limit=1)
    latest_result = latest_analysis[0]["result"] if latest_analysis else None
    role_data = build_role_dashboard(role_key, latest_result)
    return render_template(
        "dashboard.html",
        role=role_data,
        role_key=role,
        latest_analysis=latest_analysis[0] if latest_analysis else None,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
