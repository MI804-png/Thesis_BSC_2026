from flask import Flask, render_template, request, abort

from analysis_engine import run_ai_analysis
from section_data import SECTIONS

app = Flask(__name__)

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

ROLE_FOCUS = {
    "ceo": {
        "title": "CEO View",
        "goal": "Strategic alignment, growth readiness, and enterprise-wide risk posture.",
        "kpis": ["Overall Organizational Health Index", "Scaling Risk Score", "Revenue Growth Outlook"],
    },
    "hr": {
        "title": "HR View",
        "goal": "Leadership readiness, people capability, and talent stability.",
        "kpis": ["Leadership Readiness Score", "Talent Retention", "Capability Maturity"],
    },
    "finance": {
        "title": "Finance View",
        "goal": "Capital efficiency, margin resilience, and debt pressure.",
        "kpis": ["Profit Margin", "Debt Ratio", "Cash Runway"],
    },
    "operations": {
        "title": "Operations View",
        "goal": "Execution reliability, process fragility, and delivery confidence.",
        "kpis": ["Process Fragility", "Operational Stability", "Scaling Risk Score"],
    },
}


@app.route("/")
def home():
    return render_template("home.html", thesis=THESIS_CONTENT)


@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    result = None
    if request.method == "POST":
        result = run_ai_analysis(request.form)
    return render_template("analysis.html", result=result)


@app.route("/section/<int:number>")
def section_view(number: int):
    sec = SECTIONS.get(number)
    if sec is None:
        abort(404)
    return render_template("section.html", sec=sec)


@app.route("/dashboard/<role>")
def dashboard(role: str):
    role_data = ROLE_FOCUS.get(role.lower())
    if role_data is None:
        role_data = {
            "title": "General View",
            "goal": "High-level cross-functional insights.",
            "kpis": ["Organizational Health", "Risk Trend", "Execution Quality"],
        }
    return render_template("dashboard.html", role=role_data, role_key=role)


if __name__ == "__main__":
    app.run(debug=True)
