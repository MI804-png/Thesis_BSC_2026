# HR Insight Lab

HR Insight Lab is a local Flask-based thesis prototype for analysing organisational health through a mix of transparent KPI scoring, role-based dashboards, saved history, batch uploads, and PDF reporting.

The project was built around the thesis:

**Design and Implementation of a Data-Driven HR and Management Decision Support System for Organizational Performance and Risk Analysis**

Instead of acting like a static thesis website, the current version works as a hands-on local demo. A user can sign in, submit a company profile, generate an analysis, compare runs over time, upload CSV files for batch processing, export reports as PDFs, and open dashboards tailored to different management roles.

## What The App Does

The system combines leadership, people, operations, and financial inputs into four main signals:

- Leadership Readiness Score
- Scaling Risk Score
- Financial Stability Composite
- Overall Organizational Health Index

Those scores drive a rule-based organisational assessment and are also paired with a local machine-learning prediction model. The weighted KPI logic remains visible and explainable, while the ML layer adds a second local prediction view for comparison.

## Main Features

- Local login system with seeded demo users
- Role-based access control for CEO, HR, Finance, Operations, and Admin views
- AI Analysis workspace for single-company assessment
- SQLite-backed history for saved runs and simple trend tracking
- CSV batch ingestion for analysing multiple companies in one upload
- PDF export for each saved analysis
- Demo HRIS imports for BambooHR and Workday style payloads
- Interactive dashboards that highlight KPI details by role

## Technology Stack

- Python 3.11+
- Flask 3.1
- SQLite
- scikit-learn
- ReportLab
- HTML, CSS, and vanilla JavaScript

## Project Structure

- `app.py`: Flask routes, authentication flow, RBAC, CSV handling, dashboards, and PDF export
- `analysis_engine.py`: form defaults, input validation, KPI scoring, and rule-based prediction logic
- `ml_engine.py`: local gradient boosting model training and scoring
- `data_store.py`: SQLite schema, demo users, and saved analysis history
- `hr_integrations.py`: local demo provider payloads
- `reporting.py`: PDF generation
- `templates/`: Jinja templates for pages and dashboards
- `static/`: CSS and JavaScript assets
- `hr_analysis.db`: local SQLite database created at runtime

## Local Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the application:

```bash
python app.py
```

4. Open the local site:

```text
http://127.0.0.1:5000
```

The development server is configured to run locally on port 5000.

## Demo Accounts

The application seeds local users automatically when the database is created.

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin` | `admin123` |
| CEO | `ceo` | `ceo123` |
| HR | `hr` | `hr123` |
| Finance | `finance` | `finance123` |
| Operations | `operations` | `operations123` |

Use `admin` if you want unrestricted access to all dashboards and saved records.

## Typical Workflow

1. Sign in with one of the local accounts.
2. Open the AI Analysis workspace.
3. Enter a company profile manually, or preload a demo profile from the HRIS import panel.
4. Run the analysis and save it locally.
5. Review the KPI breakdown, rule-based verdict, ML probability, and recommendations.
6. Export the result as a PDF if needed.
7. Open the History page to review saved analyses.
8. Open a role dashboard to inspect KPI summaries from the perspective of that manager role.

## CSV Batch Upload Format

The batch upload feature expects a CSV file with these headers:

```text
company_name,industry,stage,employee_count,leadership_years,digital_score,retention_pct,churn_pct,dte_ratio,doc_score,dep_score,margin_pct,growth_pct,cash_months
```

Notes about batch processing:

- Unknown industries or stages are defaulted to safe local values.
- Missing numeric fields fall back to defaults.
- Out-of-range numeric values are clamped.
- Each processed row is saved as its own analysis record.
- Batch results are ranked by OHI and include PDF export links.

## Dashboards And Access Rules

Each dashboard is intentionally limited by role:

- CEO dashboard: executive health, growth outlook, and scaling risk
- HR dashboard: leadership readiness, retention, and capability maturity
- Finance dashboard: current asset change, debt pressure, and cash flow change
- Operations dashboard: process fragility, operational stability, and scaling risk
- Admin role: full access to every dashboard and all saved records

Non-admin users can only see their own saved analysis history.

## Local Data And Persistence

The application stores its data in `hr_analysis.db`.

This database currently holds:

- seeded user accounts
- manual analysis runs
- CSV-imported analysis runs
- payload snapshots for each saved case
- computed result snapshots for export and history review

No external database is required for the current prototype.

## Machine Learning Layer

The ML section uses a locally trained `GradientBoostingRegressor` from scikit-learn.

Important context:

- the model is trained on synthetic data derived from the current scoring assumptions
- it is useful as a prototype decision-support layer, not as a production-ready predictor
- the rule-based KPI engine remains the most transparent explanation path in the app

## HRIS Import Mode

The BambooHR and Workday options currently load local demo payloads that prefill the analysis form.

They do not call live external APIs yet. The import flow was designed so real credentials and real API requests can be added later without rewriting the analysis page structure.

## PDF Reporting

Each saved analysis can be exported as a PDF report. The exported document includes:

- company details
- submitted input values
- KPI results
- verdict summary
- recommendations
- ML scoring section

## Known Limits

This is a local prototype, so a few constraints are intentional:

- authentication is session-based and intended for demo use
- the ML model is not trained on real enterprise data
- HRIS integrations use local mock data only
- SQLite is suitable for local testing, not large multi-user deployment
- the Flask server is configured for development, not production hardening

## Thesis Documentation Script

The repository also contains `generate_documentation.py`, which generates a long-form PDF thesis document. That file reflects the academic documentation side of the project, while the web app demonstrates the interactive prototype.

## Hurdles and Lessons Learned

- **PDF Layouts are painful:** Getting ReportLab to handle long strategic recommendations without cutting off text took way more time than the actual math.
- **The Data Problem:** I realized early on that "perfect" data doesn't exist. That's why I added the clamping logic—to stop the system from crashing if someone enters a weird outlier.
- **ML vs. Rules:** The biggest surprise was how often the simple weighted formulas actually outperformed the ML model on edge cases. It really reinforced the value of transparency over complexity.

## Summary

The current project is no longer just a thesis landing page. It is a local decision-support prototype that lets a user sign in, analyse companies, store results, compare runs, export reports, and inspect different dashboard views from the perspective of management roles.
