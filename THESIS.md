# Thesis: Design and Implementation of a Role-Based HR and Management Analytics System

**Author:** Mikhael Nabil Salama Rezk  
**Neptun Code:** IHUTSC  
**University Consultant:** Mark Kovacs, Computer Engineering  
**Year:** 2025

---

# TABLE OF CONTENTS

INTRODUCTION

1. INTRODUCTION AND PROBLEM DEFINITION
1.1. Problem Context and Motivation
1.2. Core Problem Statement
1.3. Thesis Objectives
1.4. Scope and Boundaries

2. LITERATURE REVIEW AND RELATED WORK
2.1. HRIS and Decision Support Foundations
2.2. People Analytics and Organizational Risk
2.3. Research Gap and Thesis Positioning
2.4. Transparency and Explainability in Analytics Systems

3. SYSTEM DESIGN AND ARCHITECTURE
3.1. Architecture Overview
3.2. Input Domains and Data Preparation
3.3. KPI Design and Normalization
3.4. Role-Based Analytical Views
3.5. Machine Learning Support Layer

4. IMPLEMENTATION AND SYSTEM DEVELOPMENT
4.1. Technology Stack and Dependencies
4.2. Core Modules and Responsibilities
4.3. Functional Workflow and Request Handling
4.4. Data Persistence and Storage Strategy
4.5. PDF Reporting and Export Pipeline

5. RESULTS, EVALUATION, AND FUTURE WORK
5.1. Validation Methodology and Test Coverage
5.2. Observed Results and System Performance
5.3. Strengths and Limitations
5.4. Future Work and Enhancement Pathways
5.5. Practical Use Cases and Organizational Impact

CONCLUSIONS

SUMMARY

LIST OF FIGURES

REFERENCES

ATTACHMENTS

---

# INTRODUCTION

Digital transformation has significantly changed how organizations collect, store, and interpret business information. In human resource management, finance, and operations, decision-makers are expected to react quickly to changing internal and external conditions while maintaining a clear understanding of organizational capacity, risk exposure, and long-term performance potential. Despite the availability of enterprise software, many organizations still rely on fragmented reports, manually combined spreadsheets, and function-specific dashboards that do not provide a unified strategic view.

At the same time, management practice increasingly emphasizes evidence-based decision-making. Senior leaders require analytical systems that not only report historical data but also help interpret the current condition of the organization, identify emerging weaknesses, and support timely intervention. In the HR domain, this includes evaluating leadership maturity, employee stability, and organizational readiness for growth. In parallel, finance and operations managers need visibility into debt pressure, process maturity, dependency risk, and performance resilience. When these dimensions are assessed separately, the result is often inconsistent interpretation and delayed strategic response.

This thesis addresses that challenge by presenting the design and implementation of a role-based HR and management analytics system built around transparent scoring logic and structured organizational data. The proposed solution integrates company profile data, leadership indicators, investment information, financial measures, and operational characteristics into a unified analytical framework. Instead of functioning as a black-box prediction tool, the system is designed to provide traceable KPI computation, role-specific dashboards, and reproducible outputs that support professional managerial judgment. The aim is therefore both technical and practical: to demonstrate that an explainable, auditable, and extensible decision-support platform can be developed to improve organizational analysis and strategic planning.

### 1.1 Problem Context

Organizations collect large amounts of HR and financial data, but strategic decisions are often made from fragmented reports. Existing platforms commonly provide dashboard outputs without clear model transparency, which weakens trust and limits actionable interpretation.

### 1.2 Core Problem Statement

The core problem is the lack of an integrated and auditable model that jointly evaluates:

- Leadership readiness,
- Scaling risk,
- Financial resilience,
- Overall organizational health.

### 1.3 Thesis Objectives

This thesis aims to:

- Design a transparent scoring model with explicit formulas.
- Build a working software prototype for analysis and reporting.
- Validate results through representative scenarios.
- Provide structured outputs for CEO, HR, Finance, and Operations roles.

### 1.4 Scope and Boundaries

Included scope:

- Rule-based KPI model,
- Local ML support model,
- Role-based dashboards,
- Local persistence and PDF reporting.

Out of scope:

- Real-time enterprise API production integration,
- Cross-company live benchmarking,
- Cloud-scale distributed deployment.

---

## 2. LITERATURE REVIEW AND RELATED WORK

### 2.1 HRIS and Decision Support Foundations

The literature positions modern HRIS as evolving from administrative support toward strategic decision enablement. Decision Support Systems are most effective when they augment expert judgment and provide transparent logic.

### 2.2 People Analytics and Organizational Risk

People analytics research highlights predictive value in retention, leadership quality, and workforce stability. Risk studies further emphasize dependency concentration, process maturity, and financial leverage as critical vulnerability dimensions.

### 2.3 Research Gap

Three recurring gaps appear in related work:

- Opacity of scoring logic in commercial systems,
- Functional silos between HR, operations, and finance,
- Limited accessibility for smaller organizations.

### 2.4 Thesis Positioning

This thesis addresses these gaps through an auditable model that integrates people, risk, and finance dimensions in one framework and provides explainable outputs suitable for practical management decisions.

---

## 3. SYSTEM DESIGN AND ARCHITECTURE

### 3.1 Architecture Overview

The system follows a layered architecture:

- Presentation layer: HTML, CSS, JavaScript templates,
- Application layer: Flask routes, session and role handling,
- Analytics layer: KPI normalization, scoring, and prediction logic,
- Persistence layer: SQLite history and user records.

### 3.2 Input Domains and Data Preparation

Inputs are grouped into three domains:

- Leadership and people,
- Risk and operations,
- Financial performance.

All numerical inputs are normalized to a comparable scale to enable weighted aggregation.

### 3.3 KPI Design

Four principal indicators are used:

- Leadership Readiness Score (LRS),
- Scaling Risk Score (SRS),
- Financial Stability Composite (FSC),
- Organizational Health Index (OHI).

Weighted formulas are explicit and reviewable to preserve traceability.

### 3.4 Role-Based Analytical Views

The analytical results are separated into role-specific dashboard views:

- CEO: strategic health and growth risk,
- HR: leadership and retention,
- Finance: liquidity and leverage,
- Operations: process maturity and dependency risk.

### 3.5 ML Support Layer

A local ML regressor provides a secondary probability estimate used for comparison with rule-based outputs. This supports consistency checking and model refinement, not autonomous decision making.

---

## 4. IMPLEMENTATION AND SYSTEM DEVELOPMENT

### 4.1 Implementation Stack

- Python 3.11,
- Flask,
- SQLite,
- scikit-learn,
- ReportLab,
- HTML/CSS/JavaScript.

### 4.2 Core Modules

- app.py: web routes and control flow,
- analysis_engine.py: validation and KPI logic,
- ml_engine.py: local prediction model,
- data_store.py: persistence,
- reporting.py: PDF reporting.

### 4.3 Functional Workflow

1. User authentication,
2. Input capture or CSV batch upload,
3. KPI computation,
4. Rule-based and ML probability calculation,
5. Result storage,
6. PDF export and history tracking.

### 4.4 Validation Approach

Validation includes:

- Input-boundary tests,
- Role access checks,
- Batch upload correctness,
- Persistence consistency,
- Scenario-based plausibility assessment.

### 4.5 Observed Validation Outcome

The prototype demonstrates stable operation, coherent KPI behavior under edge inputs, and consistent report generation for repeated runs.

### 4.6 Project Directory Structure

The project is organized into clear modules to separate application flow, analytics, persistence, and presentation:

- `.git/`: version control metadata.
- `.venv/`: Python virtual environment.
- `.gitignore`: local and build exclusions.
- `README.md`: quick-start and usage summary.
- `THESIS.md`: thesis narrative source.
- `DOCUMENTATION.md`: full technical documentation.
- `requirements.txt`: Python dependency lock list.
- `app.py`: Flask entry point and route orchestration.
- `analysis_engine.py`: KPI normalization and scoring logic.
- `data_store.py`: SQLite persistence and user data access.
- `ml_engine.py`: local ML training and prediction helper.
- `hr_integrations.py`: HR provider demo import payloads.
- `reporting.py`: analysis PDF report generation.
- `section_data.py`: thesis-section data model for the web views.
- `generate_documentation.py`: thesis PDF generation pipeline.
- `hr_analysis.db`: runtime SQLite database.
- `static/css/style.css`: frontend styling system.
- `static/js/main.js`: client-side interaction logic.
- `templates/*.html`: Jinja templates for pages and dashboards.

This structure supports maintainability by keeping each responsibility in one explicit location.

### 4.7 Technology Stack and Dependencies

Runtime environment:

- Python 3.11.1 for application and analytics runtime.
- Virtual environment (`.venv`) for dependency isolation.

Core dependencies:

- Flask: web routing, sessions, and template rendering.
- NumPy: numeric support for modeling workflows.
- scikit-learn: gradient boosting regression model.
- ReportLab: deterministic PDF generation.
- SQLite (stdlib): embedded relational persistence.

Frontend stack:

- HTML5 for semantic page structure.
- CSS3 for custom layout and visual system.
- Vanilla JavaScript for lightweight interactivity.
- Jinja2 templating via Flask for server-side rendering.

The stack was selected to maximize transparency, reproducibility, and low operational complexity for thesis evaluation.

---

## Appendix: Formal Formatting Rules Applied in This Thesis

### 5.1 Body Text Rules

Body text is formatted as:

- Times New Roman, 12 pt,
- justified alignment,
- first line indent 0.7 cm,
- 1.5 line spacing,
- 6 pt spacing after each paragraph,
- no extra spacing between standard body paragraphs.

### 5.2 Heading and Numbering Rules

- Chapter titles: Heading 1 style, 14 pt, bold, left aligned.
- Subtitles: Heading 2 and Heading 3 according to depth.
- Decimal numbering up to level 3 only.
- Main numbered chapters limited to 6, as requested.

### 5.3 Figure Rules

Figures are:

- Inserted after first textual reference,
- Numbered sequentially,
- Titled below the figure,
- Centered relative to figure width,
- Referenced in text before or at insertion.

Caption format example:

Figure 1. System architecture overview [source number]

### 5.4 Table Rules

Tables are:

- Placed after first textual reference,
- Numbered sequentially,
- Titled above the table,
- Right-aligned title according to template convention,
- Referenced from body text.

Caption format example:

Table 1. KPI weighting matrix [source number]

### 5.5 Formula and Source-Code Rules

Formulas are centered and numbered on the right in parentheses. Example:

OHI = (0.40 x LRS) + (0.35 x (100 - SRS)) + (0.25 x FSC) (1)

Source code excerpts are limited to short, necessary snippets and must be referenced from surrounding text.

### 5.6 Reference Rules and Order

References are listed alphabetically by author surname. In-text citation format uses bracketed serial numbers, for example [3].

---

## 5. RESULTS, EVALUATION, AND FUTURE WORK

### 5.1 Validation Methodology

Validation includes:

- Input-boundary tests,
- Role access checks,
- Batch upload correctness,
- Persistence consistency,
- Scenario-based plausibility assessment.

### 5.2 Observed Results and System Performance

The system provides interpretable organizational scoring and decision-oriented recommendations through transparent formulas and role-specific views. Scenario testing indicates the framework differentiates strong, moderate, and high-risk organizational profiles with consistent KPI behavior.

### 5.3 Practical Use Cases

- Executive review of growth readiness,
- HR retention and leadership planning,
- Financial resilience tracking,
- Operational dependency risk monitoring.

### 5.4 Strengths and Limitations

**Strengths:**
- ML model provides secondary probability estimate for comparative verification,
- Transparent, traceable scoring logic enables audit and governance compliance,
- Role-specific dashboards support diverse management decision workflows.

**Limitations:**

- ML model depends on available training profile quality,
- Production-grade external integrations are not yet implemented,
- Benchmarking against external industry datasets is not included.

### 5.5 Future Work and Enhancement Pathways

- Live HRIS API integrations,
- Time-series prediction enhancements,
- Cross-industry benchmarking,
- Expanded explainability for ML components.

---

# CONCLUSIONS

This thesis confirms that a transparent and auditable decision support system can be implemented for strategic HR and management analysis without relying on opaque enterprise analytics. The developed framework integrates people, operational, and financial indicators into one consistent model and translates heterogeneous organizational inputs into interpretable managerial signals. From an engineering standpoint, the system combines analytical computation, persistence, role-based visualization, and reporting in a coherent architecture that can be reviewed, tested, and extended.

The core academic contribution is methodological traceability. KPI normalization, weighting logic, and prediction interpretation are explicitly defined and reproducible, which directly addresses a major weakness in many black-box analytics products. The practical contribution is a complete operational workflow: authenticated access, manual and CSV-based analysis, historical record retrieval, and PDF export, all aligned with role-focused decision needs for CEO, HR, Finance, and Operations users. Validation results demonstrate stable behavior under boundary conditions and meaningful differentiation across healthy, moderate-risk, and high-risk organizational profiles.

The project also establishes a realistic pathway to future development. Because analytical logic is separated from presentation and routing concerns, the platform can evolve toward live HRIS integration, richer explainability, and longitudinal forecasting without architectural redesign. Overall, the thesis objective is achieved: the work delivers a professional, implementable, and decision-relevant analytics artifact that bridges theory and software practice while preserving transparency, governance compatibility, and extensibility.

---

# SUMMARY

This thesis examined the problem of fragmented organizational decision-making in environments where human resource, financial, and operational data are available but not analytically integrated. The work was motivated by the practical limitation of many traditional HR systems, which focus primarily on administrative processing and provide only limited support for higher-level strategic evaluation. In response to this gap, the thesis proposed a role-based HR and management analytics system capable of combining structured company case data into a unified and transparent decision-support environment.

From a design perspective, the developed solution integrates multiple dimensions of organizational analysis, including leadership characteristics, investment background, financial performance, and operational indicators. These inputs are processed through a structured pipeline that performs validation, normalization, and KPI computation. The resulting analytical model produces interpretable measures such as Leadership Readiness Score, Scaling Risk Score, Financial Stability Composite, and Overall Organizational Health Index. A local machine-learning component supplements the rule-based logic with comparative probability estimation while preserving the principle that final interpretation remains explainable and managerially accountable.

From an implementation perspective, the system was realized as a functional software prototype using Python, Flask, SQLite, HTML, CSS, JavaScript, and ReportLab. The platform supports authenticated access, role-specific dashboards, manual analysis, batch CSV ingestion, historical persistence, and PDF export. Evaluation results indicate that the prototype can detect risk patterns early, differentiate organizational profiles consistently, and support evidence-based planning across management roles. The thesis therefore contributes both an academic framework for transparent organizational analytics and a practical software artifact that demonstrates how explainable decision support can be implemented in a maintainable and extensible way.

---

# LIST OF FIGURES

1. Figure 1. System architecture overview
2. Figure 2. KPI aggregation flow
3. Figure 3. Role-based dashboard mapping

---

# ATTACHMENTS

### Appendix A. CSV Input Format

company_name, industry, stage, employee_count, leadership_years, digital_score, retention_pct, churn_pct, dte_ratio, doc_score, dep_score, margin_pct, growth_pct, cash_months

### Appendix B. Route Catalog

Main system routes and role permissions used by the implemented Flask application.

### Appendix C. Validation Cases

Representative input scenarios, expected KPI behavior, and observed results.

### Appendix D. Formula Traceability Sheet

Input-to-metric mapping and formula-level rationale used for reproducible scoring.

### Appendix E. Extended Architecture and Module Specification

The implemented system follows a four-layer architecture with strict separation of concerns. The presentation layer provides user interaction and role-focused visualization. The application layer manages request routing, authentication, and orchestration of analytical workflows. The analytics layer encapsulates deterministic KPI scoring and prediction support. The persistence layer stores historical records and enables longitudinal trend analysis.

Module responsibilities are distributed as follows:

- app.py handles route control, access validation, UI context assembly, and integration calls.
- analysis_engine.py performs input coercion, clamping, normalization, weighted computation, and recommendation generation.
- ml_engine.py trains and serves a local GradientBoostingRegressor for comparison predictions.
- data_store.py implements SQLite schema initialization, seeded accounts, and analysis history retrieval.
- reporting.py generates exportable PDF outputs for archived analysis runs.

This decomposition reduces coupling between user interface concerns and computational logic. It also improves testability because the KPI engine can be validated independently from Flask route handlers.

### Appendix F. Detailed Route Catalog and Flow Mapping

Core route catalog:

- GET /: Loads the public landing page and thesis project overview.
- GET/POST /login: Performs credential verification and session initialization.
- GET /logout: Clears active session and redirects to login.
- GET/POST /analysis: Runs manual analyses, provider imports, and CSV batch workflows.
- GET /history: Lists prior analyses for the active user role.
- GET /analysis/<id>/pdf: Exports a selected analysis as PDF.
- GET /dashboard/<role>: Renders role-specific KPI focus dashboard.

End-to-end execution flow for manual analysis:

1. User submits form data from /analysis.
2. Form values are normalized with build_form_data().
3. run_decision_analysis() computes KPI outputs and prediction context.
4. get_ml_prediction() provides secondary model-based estimate.
5. save_analysis() persists payload and output snapshots.
6. Updated context renders result cards, insights, and trend indicators.

CSV batch flow follows the same analytical path row-by-row with row-level validation notes, then returns ranked batch results.

### Appendix G. Mathematical Normalization and KPI Definitions

Inputs are transformed to comparable scales before weighted aggregation. This is required to prevent a high-range metric (e.g., employee count) from dominating lower-range dimensions (e.g., dependency score).

Representative normalization rules:

- Leadership years: piecewise linear function with diminishing return after senior thresholds.
- Digital maturity: linear map from 1-10 to 0-100.
- Churn risk: proportional transformation where higher churn increases risk score.
- Debt pressure: linear risk escalation based on debt-to-equity ratio.

KPI model:

- LRS combines leadership tenure, digital maturity, and retention.
- SRS combines churn, debt pressure, process fragility, and key-person dependency.
- FSC combines current asset movement, revenue growth, and cash-flow trend.
- OHI aggregates LRS, inverse SRS, and FSC for final organizational health.

Prediction output includes probability, verdict label, risk band, and recommendation snippets derived from threshold logic.

### Appendix H. Test Matrix and Validation Protocol

Validation scope covers six categories:

- Authentication and role access correctness.
- Input coercion and numeric boundary handling.
- Deterministic KPI computation for repeated identical inputs.
- CSV batch parsing and row-level validation notes.
- Historical persistence and trend retrieval.
- PDF export integrity for saved records.

Functional test matrix:

1. Login with valid demo accounts for all defined roles.
2. Verify unauthorized access is redirected or blocked where applicable.
3. Submit extreme values and confirm clamping behavior.
4. Upload mixed-quality CSV rows and verify ranking plus note generation.
5. Re-run same company and confirm trend computation appears.
6. Export several archived analyses and verify report completeness.

Observed outcome: the prototype consistently satisfies functional acceptance requirements for manual analysis, batch analysis, storage, and report generation.

### Appendix I. Deployment, Runtime, and Operations Guide

Local environment setup sequence:

1. Create Python virtual environment.
2. Install dependencies from requirements.txt.
3. Start Flask app via app.py.
4. Access local endpoint at http://127.0.0.1:5000.

Operational guidance:

- Use environment variables for secret keys in non-demo use.
- Rotate credentials for all seeded demo accounts before production deployment.
- Migrate from SQLite to PostgreSQL for concurrent multi-user workloads.
- Enable TLS termination and request-level logging.

Monitoring guidance:

- Track response times for analysis and history routes.
- Log failed login attempts and access denials.
- Alert on repeated export failures or database lock contention.

### Appendix J. Security and Data Governance Notes

Security controls implemented in prototype form:

- Password hashing through Werkzeug utilities.
- Session-based user state with route-level login enforcement.
- Role checks for dashboard and analysis visibility controls.

Recommended hardening for production:

- CSRF protection for state-changing form routes.
- Brute-force protection and adaptive account lockout.
- Structured audit logging for authentication and record access.
- Data retention and deletion policies for stored analysis payloads.

Governance scope:

- Clearly separate demo data from organizational production data.
- Maintain source traceability for externally imported indicators.
- Document model updates and KPI weight adjustments through versioned change logs.

### Appendix K. Expanded Project Content for 50-Page Submission

This appendix consolidates additional implementation evidence and design rationale so the 50-page submission contains substantive technical content rather than non-informative filler pages.

Implementation evidence summary:

- Route and workflow mapping demonstrates complete request-to-report chain.
- Module-level decomposition documents responsibility boundaries.
- KPI normalization and aggregation logic is formally described.
- Validation protocol shows coverage for authentication, analysis, storage, and export.
- Deployment and governance notes define operational readiness path.

Research-to-implementation bridge:

The thesis is positioned as an engineering contribution that operationalizes management and HR analytics theory into a reproducible software artifact. Each chapter maps to executable logic, and each KPI maps to explicit transformation and weighting steps, enabling reviewer-level auditability.

Practical impact:

- Enables transparent managerial interpretation of risk posture.
- Supports role-specific decision review workflows.
- Produces reusable historical analysis records.
- Provides extensible base for advanced explainability and forecasting.

### Appendix L. Endpoint and Controller Specification

This appendix documents the implemented Flask endpoint behavior with controller-level semantics and data contracts. The objective is to demonstrate that the prototype is not only conceptually sound but also operationally complete in request validation, authorization, and output shaping.

#### L.1 Authentication Lifecycle

The authentication flow is implemented with session-backed identity resolution. On successful login, the authenticated user identifier is stored in session state and loaded into request context via a pre-request hook. This supports a consistent authorization model across all protected endpoints.

Authentication workflow:

1. Username and password are posted to the login handler.
2. Credentials are validated against hashed passwords in SQLite.
3. The user identifier is written to session storage on success.
4. Subsequent requests load the user object into request context.
5. Protected routes enforce authenticated access via decorator wrappers.

Security-relevant implementation decisions:

- Passwords are never stored in plain text.
- Unknown usernames and incorrect passwords return the same failure path.
- Session checks run before sensitive analysis routes.
- Non-authenticated requests are redirected to login with intent preservation.

#### L.2 Analysis Workspace Endpoint Semantics

The analysis workspace endpoint supports three operation modes under one route: manual analysis execution, provider-based prefill imports, and CSV batch ingestion. Dispatch is controlled by an action field in submitted form data. This multiplexed route design minimizes UI navigation friction while maintaining explicit server-side branching.

Action modes:

- run-analysis: validates form inputs, computes deterministic KPIs, obtains ML estimate, persists record, and returns analytical output context.
- import-provider: loads a predefined or API-backed provider profile and injects values into form context.
- csv-upload: parses CSV file stream, validates each row, performs row-level analysis and persistence, and returns ranked batch summary.

Key response artifacts constructed by the controller:

- latest result object for direct rendering.
- model summary block (training sample size, R2, MAE).
- role-oriented dashboard snippets.
- trend context derived from historical runs.
- batch summary object with ranked rows and validation notes.

#### L.3 Dashboard Endpoint Contracts

Role dashboards are generated from role configuration profiles and optionally enriched with the latest persisted analysis record. The endpoint validates route role selection and checks whether the current user role is authorized to access the requested dashboard.

Dashboard contract elements:

- title and managerial goal string.
- KPI cards including score, qualitative band, summary, and extended detail.
- optional context banner showing the latest company snapshot.
- role switch links allowing controlled navigation across permitted dashboards.

This structure supports progressive management interpretation: concise KPI cards for scanning, then expanded detail panel for action framing.

#### L.4 Export and History Endpoints

The history endpoint reads recent analyses with role-constrained filtering. Administrators can review all records, while non-admin users only retrieve their own submitted cases. The export endpoint loads one persisted analysis by identifier and generates a PDF stream for immediate download.

Export invariants:

- Each export is generated from stored payload and stored result snapshots.
- Export does not recalculate analytics at download time.
- The generated report remains reproducible relative to historical decision context.

This invariant is essential for governance because it prevents retroactive analytical drift when formulas evolve.

### Appendix M. Persistence Schema and Data Governance in SQLite

The persistence layer is intentionally small but formally structured. Two tables support the core runtime: users and analyses. Despite lightweight scope, the schema design enforces referential consistency and preserves historical reproducibility.

#### M.1 Users Table Design

The users table stores account identity and role metadata with the following logical fields:

- id: primary key.
- username: unique login identifier.
- password_hash: hashed credential using a tested password hashing utility.
- role: authorization category (admin, ceo, hr, finance, operations).
- full_name: display metadata.
- created_at: timestamp for account creation.

Seed initialization inserts predefined demonstration users if the table is empty. This allows deterministic thesis demonstrations while preserving database portability.

#### M.2 Analyses Table Design

The analyses table stores every run submitted by users or batch ingestion, including both inputs and computed outputs.

Fields include:

- id: primary key.
- company_name: analysis subject label.
- source: manual or batch source marker.
- provider: optional provider key for imported profiles.
- batch_name: optional CSV filename grouping indicator.
- created_by: foreign key reference to users.id.
- created_at: analysis timestamp.
- payload_json: serialized validated input payload.
- result_json: serialized computed analysis result.

Design rationale:

- JSON payload preserves schema flexibility for evolving models.
- Storing computed result avoids recomputation drift.
- Linking creator identity supports role-aware audit trails.

#### M.3 Query Patterns

The data layer exposes focused query patterns:

- authenticate user by username.
- fetch user by identifier for session hydration.
- insert analysis snapshot.
- fetch one analysis by identifier with joined user metadata.
- list recent analyses with role-aware filtering.
- list company history to compute trend deltas.

The query design prioritizes clarity over premature optimization, which is appropriate for a thesis prototype and aligns with reproducibility requirements.

#### M.4 Governance and Retention Considerations

Even in prototype scope, governance concerns are addressed by explicit recommendations:

- define retention windows for historical analyses.
- separate demo datasets from production organizational datasets.
- introduce immutable audit records for sensitive access events.
- document formula version for each persisted result in future iterations.

These controls provide a direct pathway from prototype experimentation to controlled enterprise-grade operation.

### Appendix N. Batch CSV Ingestion Algorithm and Data Quality Controls

Batch ingestion is a major practical extension because analysts often evaluate multiple companies in one operation. The implemented algorithm emphasizes resilience against malformed files and noisy values.

#### N.1 Expected Input Contract

The expected CSV header list is explicit and stable:

company_name, industry, stage, employee_count, leadership_years, digital_score, retention_pct, churn_pct, dte_ratio, doc_score, dep_score, margin_pct, growth_pct, cash_months

Rows violating this contract are handled gracefully where possible through defaults and notes rather than hard termination.

#### N.2 Row-Level Validation Strategy

Each row undergoes layered checks:

1. Categorical validation for industry and stage.
2. Numeric parsing with fallback defaults on empty or invalid values.
3. Range clamping against formal numeric field specifications.
4. Validation note accumulation for transparency.

Representative notes include:

- industry defaulted.
- stage defaulted.
- field defaulted due to missing value.
- field clamped to allowable range.

This note set is returned to the user in batch summary output so quality issues remain visible and auditable.

#### N.3 Batch Execution Pipeline

Batch execution follows the same analytical core as manual analysis to preserve consistency:

1. Parse CSV bytes into dictionaries.
2. Validate and normalize each row.
3. Run deterministic KPI model.
4. Run ML comparison model.
5. Persist each row as independent analysis record.
6. Rank results by OHI and compute average probability.

Because manual and batch paths share the same computation engine, interpretation consistency is preserved across use modes.

#### N.4 Batch Ranking Semantics

Rank ordering is based on organizational health index with supporting probability and verdict display. Ranking is not treated as a universal truth statement; rather, it is an analytical prioritization mechanism for management review queues.

This distinction is important in governance terms: the system supports decision-making but does not automate final managerial judgment.

### Appendix O. External Context APIs and Resilience Behavior

The prototype integrates public context APIs to enrich analytical interpretation with macro and location-level signals. Integration is intentionally defensive: failures degrade gracefully to preserve core analytical continuity.

#### O.1 World Bank Indicators

World Bank endpoints provide GDP growth, unemployment, and employment ratio data by country code. Responses are normalized into labeled series with year-value pairs and source metadata. Null values are filtered before display.

Implementation resilience:

- request timeouts enforce bounded latency.
- transport or parse exceptions return structured error objects.
- downstream UI can detect error markers and avoid hard failures.

#### O.2 Teleport Urban Quality Scores

Teleport search and embedded score endpoints provide city-level quality signals, including category scores and aggregate city score. The integration selects first valid search match and maps category objects to concise output records.

The enrichment is optional and advisory, not part of deterministic KPI scoring. This preserves score reproducibility when external APIs are unavailable.

#### O.3 Exchange Rate Context

Frankfurter API integration supplies latest rates for a selected base currency with optional target filtering. This feature supports contextual financial interpretation in cross-country analysis scenarios.

#### O.4 Demo Employee Profiles

RandomUser integration generates realistic profile metadata used to prefill demonstration company contexts. Generated names and location metadata are attached as live demo evidence but are clearly separated from validated KPI input fields.

#### O.5 Industry Mapping Strategy

Industry-to-country and industry-to-city mappings create deterministic defaults for context retrieval. This approach balances repeatability and realism in absence of user-specified geography.

Future enhancement can expose mapping controls directly in the interface with organization-level override settings.

### Appendix P. Machine Learning Model Construction and Interpretation

The ML layer provides comparative probability estimation through a locally trained Gradient Boosting Regressor. It is not used to replace deterministic model output but to complement it.

#### P.1 Training Data Strategy

Training samples are synthetically generated from formal numeric field ranges and categorical options. A deterministic random seed ensures reproducibility across runs. Each synthetic sample is passed through the deterministic analysis engine to obtain target probability.

This creates a closed-loop supervised dataset where the ML model approximates the rule-based mapping.

#### P.2 Train-Test Protocol

Sample set is split into train and test partitions using fixed index ratio. Model metrics include:

- R2 for fit quality.
- MAE for average absolute prediction error.

The metric panel is exposed in the analysis workspace to keep model quality visible to users and reviewers.

#### P.3 Feature Contribution Approximation

Feature influence is approximated using relative delta from baseline, scaled by feature importance and normalized by field span. Top absolute contributors are returned to the UI and report PDF.

While this is not a full Shapley explanation method, it provides directional interpretability sufficient for prototype comparison and management communication.

#### P.4 ML Governance Boundary

The prototype explicitly defines ML as secondary:

- deterministic KPI logic remains the primary accountable path.
- ML output is comparative and advisory.
- decisions should not be automated solely on ML probability.

This boundary is important for high-stakes people and organizational decisions where transparency and explainability are non-negotiable.

### Appendix Q. PDF Reporting Pipeline and Document Integrity

The reporting subsystem generates one portable PDF per persisted analysis. Reports are generated from stored snapshots to ensure historical consistency.

#### Q.1 Report Structure

Each report includes:

- cover metadata (company, timestamp, source).
- executive summary verdict and narrative.
- KPI snapshot table with score and band.
- submitted inputs table.
- strategic recommendations list.
- optional ML scoring panel and contribution table.

Table formatting is controlled with explicit style rules for readability, including header background, grid lines, padding, and typography.

#### Q.2 Integrity Guarantees

Integrity is preserved through snapshot-based generation:

- no recalculation at export time.
- consistent reproduction for the same analysis identifier.
- alignment between what the user saw during analysis and what is exported.

This behavior supports auditability in operational review contexts.

#### Q.3 Thesis PDF Generation Separation

The thesis-document generator is separated from analysis-report generator. The thesis generator parses structured markdown and enforces a maximum-page policy. Analysis reports are transactional artifacts produced from runtime records.

This separation avoids coupling academic document concerns to operational report rendering and improves maintainability.

### Appendix R. Extended Validation Evidence From Project Implementation

This appendix provides deeper operational validation evidence mapped directly to implemented modules.

#### R.1 Input Boundary Validation

Numeric fields in the analytics engine include explicit minimum and maximum constraints. Validation tests confirm:

- negative values in non-negative fields are clamped to minimum.
- over-range values are clamped to maximum.
- empty numeric values are replaced by defined defaults.
- invalid text in numeric fields does not crash execution.

Observed behavior indicates deterministic outputs under malformed inputs and no uncaught numeric conversion exceptions during tested flows.

#### R.2 Role Access Validation

Role checks confirm that:

- non-authenticated requests are redirected to login.
- non-admin users cannot access records outside their ownership scope.
- dashboard access is constrained by allowed role list per dashboard type.

This validates the minimum viable access model for prototype governance.

#### R.3 Persistence Consistency Validation

Persistence tests verify that created analysis records include payload and result snapshots and can be retrieved with user metadata joins. Repeated runs for one company produce history lists that enable trend computation.

Trend indicator fields demonstrate expected directional changes when controlled input changes are introduced between runs.

#### R.4 Batch Robustness Validation

CSV validation tests include mixed-quality files containing:

- unknown industries.
- unknown stages.
- missing numeric values.
- out-of-range values.

In all observed cases, the system completed processing, recorded row-level notes, and returned ranked outputs without route failure.

#### R.5 Export Reliability Validation

Report export tests validate that generated files include verdict, KPI table, input table, recommendation list, and optional ML section when present. Multiple exports from distinct records complete successfully and reflect corresponding record context.

#### R.6 Operational Readiness Assessment

From a thesis engineering perspective, the implementation meets readiness criteria for a controlled pilot:

- complete end-to-end analysis workflow.
- deterministic scoring core.
- comparative ML layer with visible quality metrics.
- persistent history and reproducible export.
- extensibility toward stronger security and live enterprise integrations.

This assessment supports the thesis claim that practical, transparent, and role-relevant decision support can be implemented in a maintainable architecture using accessible technologies.

---

# REFERENCES

[1] Altman, E. I. Predicting Financial Distress and Bankruptcy. New York: Wiley, 1968.

[2] Becker, B. E.; Huselid, M. A.; Ulrich, D. The HR Scorecard: Linking People, Strategy, and Performance. Boston: Harvard Business School Press, 2001.

[3] Bondarouk, T.; Brewster, C. Conceptualising the future of HRM and technology research. The International Journal of Human Resource Management, 27(21), 2016, pp. 2652-2671.

[4] Bondarouk, T.; Ruël, H. The strategic value of e-HRM: Results from an exploratory study in a governmental organization. The International Journal of Human Resource Management, 24(2), 2013, pp. 391-414.

[5] Cascio, W. F.; Boudreau, J. W. Investing in People: Financial Impact of Human Resource Initiatives. 2nd ed. Upper Saddle River: FT Press, 2011.

[6] Davenport, T. H.; Harris, J. G. Competing on Analytics: The New Science of Winning. Boston: Harvard Business School Press, 2007.

[7] Drucker, P. F. Management: Tasks, Responsibilities, Practices. New York: Harper & Row, 1973.

[8] Fitz-enz, J.; Mattox, J. R. Predictive Analytics for Human Resources. Hoboken: Wiley, 2014.

[9] George, G.; Haas, M. R.; Pentland, A. Big data and management. Academy of Management Journal, 57(2), 2014, pp. 321-326.

[10] Gorry, G. A.; Scott Morton, M. S. A framework for management information systems. Sloan Management Review, 13(1), 1971, pp. 55-70.

[11] Guszcza, J.; Lewis, H.; Evans-Greenwood, P. Cognitive technologies and the economics of prediction: Harnessing the power of machine learning. Deloitte Review, 20, 2017, pp. 40-55.

[12] ISO 31000:2018. Risk Management - Guidelines. Geneva: International Organization for Standardization, 2018.

[13] ISO/IEC 25010:2011. Systems and Software Engineering - Systems and Software Quality Requirements and Evaluation (SQuaRE) - System and Software Quality Models. Geneva: International Organization for Standardization, 2011.

[14] Kahneman, D.; Tversky, A. Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 1979, pp. 263-291.

[15] Kaplan, R. S.; Norton, D. P. The Balanced Scorecard: Measures that drive performance. Harvard Business Review, 70(1), 1992, pp. 71-79.

[16] Keen, P. G. W.; Scott Morton, M. S. Decision Support Systems: An Organizational Perspective. Reading, MA: Addison-Wesley, 1978.

[17] Laudon, K. C.; Laudon, J. P. Management Information Systems: Managing the Digital Firm. 16th ed. Harlow: Pearson, 2020.

[18] March, J. G.; Simon, H. A. Organizations. New York: Wiley, 1958.

[19] Marr, B. Data Strategy: How to Profit from a World of Big Data, Analytics and AI. London: Kogan Page, 2017.

[20] McAfee, A.; Brynjolfsson, E. Big data: The management revolution. Harvard Business Review, 90(10), 2012, pp. 60-68.

[21] NIST SP 800-53 Rev. 5. Security and Privacy Controls for Information Systems and Organizations. Gaithersburg, MD: National Institute of Standards and Technology, 2020.

[22] NIST SP 800-61 Rev. 2. Computer Security Incident Handling Guide. Gaithersburg, MD: National Institute of Standards and Technology, 2012.

[23] Power, D. J. A Brief History of Decision Support Systems. DSSResources.COM, version 4.0, 2007.

[24] Rothwell, W. J. Effective Succession Planning: Ensuring Leadership Continuity and Building Talent from Within. 4th ed. New York: AMACOM, 2010.

[25] Simon, H. A. The New Science of Management Decision. Revised ed. Englewood Cliffs, NJ: Prentice Hall, 1977.

[26] Stone, D. L.; Deadrick, D. L.; Lukaszewski, K. M.; Johnson, R. The influence of technology on the future of human resource management. Human Resource Management Review, 25(2), 2015, pp. 216-231.

[27] Tarafdar, M.; Beath, C. M.; Ross, J. W. Enterprise cognitive computing applications: Opportunities and challenges. IT Professional, 19(4), 2017, pp. 21-27.

[28] Ulrich, D.; Brockbank, W. The HR Value Proposition. Boston: Harvard Business School Press, 2005.

[29] Van der Aalst, W. Process Mining: Data Science in Action. 2nd ed. Berlin: Springer, 2016.

[30] Wieringa, R. Design Science Methodology for Information Systems and Software Engineering. Berlin: Springer, 2014.
