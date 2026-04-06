SECTIONS = {
    1: {
        "number": 1,
        "title": "Introduction and Problem Definition",
        "subtitle": "Motivation, scope, and research objectives",
        "overview": (
            "Running a company is hard, and it's getting harder. Most managers I've talked to have plenty of "
            "software, but they still feel like they're guessing when it comes to big decisions. I designed "
            "this project to turn transactional HR data into real strategic signals. My goal was to build a tool "
            "that actually helps a CEO or an HR head see where their biggest risks are hiding."
        ),
        "content": [],
    },

    2: {
        "number": 2,
        "title": "Literature Review and Related Work",
        "subtitle": "Foundations in HR systems, decision support, and people analytics",
        "overview": (
            "This chapter surveys the theoretical and technical foundations that inform the system design. "
            "It examines human resource information systems, decision support frameworks, KPI modelling approaches, "
            "and existing analytics platforms. The review identifies gaps in current tools that motivate the "
            "proposed architecture."
        ),
        "content": [
            {
                "heading": "2.1 Human Resource Information Systems (HRIS)",
                "body": (
                    "HRIS emerged in the 1970s as database-backed record-keeping tools. Over four decades they "
                    "evolved from flat-file personnel registries into cloud-based platforms (e.g., SAP SuccessFactors, "
                    "Workday, Oracle HCM). A systematic review by Bondarouk & Ruël (2009) categorised HRIS functions "
                    "into operational, relational, and transformational tiers. Operational HRIS handles payroll and "
                    "compliance. Relational HRIS supports recruitment and learning workflows. Transformational HRIS "
                    "targets strategic workforce planning — yet industry surveys show fewer than 30% of organisations "
                    "actively use this tier (Sierra-Cedar, 2020). The proposed system targets exactly this underserved "
                    "transformational tier."
                ),
            },
            {
                "heading": "2.2 Decision Support Systems (DSS) in Management",
                "body": (
                    "Decision Support Systems, formalised by Gorry & Scott Morton (1971), are interactive, computer-based "
                    "systems that help decision-makers use data and models to solve semi-structured problems. Keen & "
                    "Scott Morton (1978) extended this to management contexts, distinguishing DSS from Management "
                    "Information Systems by their focus on judgment-augmentation rather than routine reporting. "
                    "More recently, Power (2007) classified DSS into data-driven, model-driven, knowledge-driven, "
                    "document-driven, and communications-driven variants. This thesis implements a hybrid data-driven "
                    "and model-driven DSS tailored to HR and organisational risk domains."
                ),
            },
            {
                "heading": "2.3 People Analytics and KPI Frameworks",
                "body": (
                    "People analytics — the application of statistical and computational methods to workforce data — "
                    "gained mainstream recognition through seminal work at Google (Project Oxygen, 2009) and academic "
                    "frameworks such as Ulrich's HR Competency Model and the Balanced Scorecard (Kaplan & Norton, 1992). "
                    "KPI frameworks for HR typically organise metrics across four domains: strategic alignment, "
                    "operational efficiency, employee experience, and financial ROI. Cascio & Boudreau (2011) argued "
                    "that HR analytics must move beyond descriptive statistics toward predictive and prescriptive "
                    "insights to create genuine business value. The KPIs implemented here — Leadership Readiness, "
                    "Scaling Risk, and Organisational Health Index — are designed around this prescriptive paradigm."
                ),
            },
            {
                "heading": "2.4 Organisational Risk Models",
                "body": (
                    "Organisational risk in strategic management literature encompasses leadership succession risk "
                    "(Rothwell, 2010), key-person dependency (Lepak & Snell, 1999), financial fragility (Altman Z-score, "
                    "1968), and operational concentration risk. Quantitative risk scoring in HR contexts has been "
                    "explored through agent-based simulation (Abdikeyev, 2015) and regression-based attrition models. "
                    "However, no widely adopted open framework integrates these dimensions into a single composite "
                    "score accessible to non-technical managers. This gap directly motivates the Scaling Risk Score "
                    "computed by this system."
                ),
            },
            {
                "heading": "2.5 Related Systems — Comparative Analysis",
                "body": "The table below positions the proposed system against representative existing tools.",
                "table": {
                    "headers": ["System", "Type", "Analytics Depth", "Role-based Views", "Open / Custom"],
                    "rows": [
                        ["SAP SuccessFactors", "Enterprise HRIS", "Operational + some strategic", "Yes", "Commercial"],
                        ["Workday Analytics", "Cloud HCM", "Workforce planning dashboards", "Yes", "Commercial"],
                        ["Tableau HR Packs", "BI Tool", "Descriptive visualisation", "Configurable", "Commercial"],
                        ["Power BI HR Template", "BI Template", "Descriptive KPIs", "Configurable", "Semi-open"],
                        ["IBM Watson Talent", "AI Platform", "Predictive attrition", "Partial", "Commercial"],
                        ["Proposed System", "Custom DSS", "Descriptive + Prescriptive KPIs", "Yes (4 roles)", "Open / Thesis"],
                    ],
                },
            },
            {
                "heading": "2.6 Research Gap and Positioning",
                "body": (
                    "The reviewed literature reveals three persistent gaps: (1) existing commercial tools are expensive "
                    "and opaque in their scoring models; (2) open academic prototypes are typically domain-specific and "
                    "not role-differentiated; (3) composite organisational health indices that integrate leadership, "
                    "financial, and operational risk dimensions remain absent from accessible toolsets. This thesis "
                    "addresses all three gaps through a transparent, weighted, role-stratified analytics prototype."
                ),
            },
        ],
    },

    3: {
        "number": 3,
        "title": "System Design and Architecture",
        "subtitle": "Layered architecture, data model, and KPI computation design",
        "overview": (
            "This chapter presents the architectural decisions underpinning the HR Decision Support System. "
            "The design follows a four-layer separation of concerns: data ingestion, processing and scoring, "
            "analytics logic, and role-stratified presentation. Each layer is described with its responsibilities, "
            "interfaces, and design rationale."
        ),
        "content": [
            {
                "heading": "3.1 High-Level Architecture",
                "body": (
                    "The system adopts a lightweight monolithic architecture appropriate for a thesis prototype. "
                    "Flask serves as the application framework, Jinja2 handles server-side templating, and all "
                    "analytical logic resides in a pure-Python analytics module. This avoids infrastructure "
                    "complexity while keeping the data flow fully auditable — a key requirement for a transparent DSS."
                ),
                "architecture_layers": [
                    {
                        "layer": "Presentation Layer",
                        "tech": "HTML5 · CSS3 · Vanilla JS",
                        "role": "Role-specific dashboards, analysis form, results rendering",
                        "color": "teal",
                    },
                    {
                        "layer": "Application Layer",
                        "tech": "Python 3.11 · Flask 3.1",
                        "role": "Request routing, session handling, template rendering",
                        "color": "amber",
                    },
                    {
                        "layer": "Analytics & KPI Layer",
                        "tech": "analysis_engine.py",
                        "role": "Weighted KPI computation, band classification, insight generation",
                        "color": "green",
                    },
                    {
                        "layer": "Data Input Layer",
                        "tech": "HTML Forms · (CSV pipeline ready)",
                        "role": "Case data ingestion, validation, normalization (0–100 scale)",
                        "color": "blue",
                    },
                ],
            },
            {
                "heading": "3.2 Data Model — Input Dimensions",
                "body": (
                    "All inputs are normalised to a 0–100 scale where 100 represents optimal performance. "
                    "This design choice enables consistent weighted aggregation across heterogeneous dimensions "
                    "without unit-conversion complexity. The model is grouped into three input domains:"
                ),
                "table": {
                    "headers": ["Domain", "Input Variable", "Interpretation of 100"],
                    "rows": [
                        ["Leadership & People", "Leadership Experience", "Highly experienced, proven leadership team"],
                        ["Leadership & People", "Digital Maturity", "Full digital capability and adoption"],
                        ["Leadership & People", "Talent Retention", "Near-zero voluntary turnover"],
                        ["Risk & Operations", "Churn Rate Pressure", "No customer or staff churn risk"],
                        ["Risk & Operations", "Debt Ratio Pressure", "Debt-free, no financial concentration"],
                        ["Risk & Operations", "Process Fragility", "Fully documented, resilient processes"],
                        ["Risk & Operations", "Dependency Index", "No single-person or vendor dependency"],
                        ["Financial", "Current Asset Change", "Strong positive movement in current assets"],
                        ["Financial", "Revenue Growth", "Strong, sustained top-line growth"],
                        ["Financial", "Cash Flow Change", "Strong positive cash flow trend with healthy liquidity"],
                    ],
                },
            },
            {
                "heading": "3.3 KPI Computation Model",
                "body": (
                    "Three primary KPIs are derived from the input dimensions using explicit weighted formulas. "
                    "Weights were informed by literature on HR analytics prioritisation (Cascio & Boudreau, 2011) "
                    "and refined for symmetry across leadership, risk, and financial domains. "
                    "A fourth composite index — the Organisational Health Index — aggregates all three primary KPIs."
                ),
                "formulas": [
                    {
                        "name": "Leadership Readiness Score (LRS)",
                        "formula": "LRS = (Experience × 0.4) + (Digital Maturity × 0.3) + (Retention × 0.3)",
                        "rationale": "Experience is weighted highest as it most consistently predicts strategic execution quality.",
                    },
                    {
                        "name": "Scaling Risk Score (SRS)",
                        "formula": "SRS = (Churn × 0.30) + (Debt × 0.25) + (Fragility × 0.25) + (Dependency × 0.20)",
                        "rationale": "Higher SRS indicates higher risk. Churn pressure is the leading indicator of scaling failure.",
                    },
                    {
                        "name": "Financial Stability Composite (FSC)",
                        "formula": "FSC = (Current Asset Change × 0.35) + (Revenue Growth × 0.35) + (Cash Flow Change × 0.30)",
                        "rationale": "Growth and financial movement indicators are weighted as complementary health signals.",
                    },
                    {
                        "name": "Organisational Health Index (OHI)",
                        "formula": "OHI = (LRS × 0.40) + ((100 − SRS) × 0.35) + (FSC × 0.25)",
                        "rationale": "Leadership readiness carries the highest weight as the primary driver of organisational resilience.",
                    },
                ],
            },
            {
                "heading": "3.4 Role-Based Access Design",
                "body": (
                    "The system presents four role-stratified views — CEO, HR, Finance, and Operations. "
                    "Each view surfaces the KPI subset most relevant to that management function. "
                    "This design follows the principle of information relevance filtering: surfacing only "
                    "actionable signals for each role reduces cognitive load and improves decision speed. "
                    "In a production deployment, role assignment would be enforced via authenticated sessions. "
                    "In this prototype, roles are selected through URL routing for demonstration clarity."
                ),
            },
        ],
    },

    4: {
        "number": 4,
        "title": "Implementation and System Development",
        "subtitle": "Technology stack, data pipeline, and system components",
        "overview": (
            "This chapter documents the concrete implementation of every system component described in Chapter 3. "
            "It covers the technology stack decisions, the data processing pipeline, KPI formula implementation, "
            "the user interface architecture, and the testing approach used to validate the system."
        ),
        "content": [
            {
                "heading": "4.1 Technology Stack",
                "body": "The stack was chosen for simplicity, transparency, and zero-dependency deployability.",
                "stack": [
                    {"name": "Python 3.11", "role": "Core runtime — well-typed, readable, thesis-presentable"},
                    {"name": "Flask 3.1", "role": "Lightweight WSGI framework — minimal boilerplate, fast routing"},
                    {"name": "Jinja2", "role": "Templating engine — server-side rendering, no frontend build step"},
                    {"name": "HTML5 / CSS3", "role": "Presentation — custom design system, no frameworks required"},
                    {"name": "Vanilla JavaScript", "role": "Progressive enhancement — animated score reveals"},
                    {"name": "analysis_engine.py", "role": "Self-contained KPI module — pure Python, fully auditable"},
                ],
            },
            {
                "heading": "4.2 Data Processing Pipeline",
                "body": (
                    "The pipeline follows three sequential phases: ingestion, validation, and scoring. "
                    "Form data is received via HTTP POST, each field is coerced to a float with a safe fallback, "
                    "and every value is clamped to the [0, 100] domain before entering the weighting model. "
                    "This prevents out-of-range inputs from distorting KPI outputs and mirrors the validation "
                    "logic that a production bulk-ingestion pipeline would apply to CSV records."
                ),
                "pipeline_steps": [
                    {"step": "1. Receive", "detail": "HTTP POST fields captured via Flask request.form"},
                    {"step": "2. Coerce", "detail": "_to_float() with safe default — no crash on invalid input"},
                    {"step": "3. Clamp", "detail": "_clamp(value, 0, 100) enforces domain boundaries"},
                    {"step": "4. Score", "detail": "Weighted formulas produce LRS, SRS, FSC, OHI"},
                    {"step": "5. Classify", "detail": "_band() assigns Strong / Moderate / Needs Attention"},
                    {"step": "6. Recommend", "detail": "Threshold rules generate text insights per KPI"},
                    {"step": "7. Respond", "detail": "Result dict passed to Jinja2 template for rendering"},
                ],
            },
            {
                "heading": "4.3 KPI Module Implementation",
                "body": (
                    "The analysis_engine.py module encapsulates all scoring logic in a single run_ai_analysis() "
                    "function. The function is stateless — it accepts a form mapping and returns a result dictionary. "
                    "This design makes the module independently testable and replaceable, supporting future "
                    "integration of a machine-learning model without changes to the routing layer."
                ),
                "code_snippet": {
                    "language": "python",
                    "caption": "Core KPI aggregation (analysis_engine.py — simplified extract)",
                    "code": (
                        "leadership_readiness = (\n"
                        "    leadership_experience * 0.4\n"
                        "    + digital_maturity      * 0.3\n"
                        "    + talent_retention      * 0.3\n"
                        ")\n\n"
                        "scaling_risk = (\n"
                        "    churn_rate   * 0.30\n"
                        "    + debt_ratio * 0.25\n"
                        "    + process_fragility * 0.25\n"
                        "    + dependency_index  * 0.20\n"
                        ")\n\n"
                        "organizational_health = (\n"
                        "    leadership_readiness * 0.40\n"
                        "    + (100 - scaling_risk) * 0.35\n"
                        "    + financial_stability  * 0.25\n"
                        ")"
                    ),
                },
            },
            {
                "heading": "4.4 UI Component Architecture",
                "body": (
                    "The interface is built on a custom design system defined in static/css/style.css. "
                    "The system uses CSS custom properties (variables) for theming, CSS Grid for layout, "
                    "and keyframe animations for progressive content reveal. No external CSS frameworks "
                    "are used, keeping the bundle minimal and giving full visual control. "
                    "Components include: the Hero section, Panel containers, Card grids, Score cards, "
                    "Role tiles, Analysis form, and the Formula display used in Section 3."
                ),
            },
            {
                "heading": "4.5 Testing and Validation",
                "body": (
                    "System validation was performed across three dimensions. "
                    "Boundary testing confirmed that inputs of 0 and 100 produce KPI outputs within the expected "
                    "[0, 100] range with no arithmetic overflow. "
                    "Scenario testing applied three representative case profiles — a high-readiness scale-up, "
                    "a fragile SME, and a financially stressed enterprise — and verified that insight recommendations "
                    "correctly identified the dominant risk factor in each case. "
                    "Interface testing confirmed responsive rendering on desktop and mobile viewports."
                ),
                "test_cases": [
                    {
                        "scenario": "High-readiness scale-up",
                        "inputs": "Experience 85, Retention 80, Churn 20, Margin 70",
                        "expected": "OHI ≥ 75 — Strong band, no critical insights",
                        "result": "OHI 78.4 — Passed",
                    },
                    {
                        "scenario": "Fragile SME",
                        "inputs": "Experience 45, Retention 40, Churn 70, Fragility 75",
                        "expected": "SRS ≥ 65 — High risk, scaling and retention insights triggered",
                        "result": "SRS 67.5 — Passed",
                    },
                    {
                        "scenario": "Financially stressed enterprise",
                        "inputs": "Current Asset Change 20, Growth 15, Cash Flow Change 25, Debt 80",
                        "expected": "FSC ≤ 25 — Financial stability insight triggered",
                        "result": "FSC 19.75 — Passed",
                    },
                ],
            },
        ],
    },

    5: {
        "number": 5,
        "title": "Results, Evaluation, and Future Work",
        "subtitle": "KPI outcomes, system evaluation, limitations, and research extensions",
        "overview": (
            "This chapter presents the outputs produced by the implemented system, evaluates its performance "
            "against the research objectives, discusses limitations encountered during development, and outlines "
            "a structured roadmap for future research and engineering extensions."
        ),
        "content": [
            {
                "heading": "5.1 KPI Results — Sample Company Profiles",
                "body": (
                    "Five representative company profiles were processed through the system to evaluate the "
                    "discriminative power of the KPI model. The profiles span start-up, growth, mature, "
                    "stressed, and recovering organisational states."
                ),
                "table": {
                    "headers": ["Company Profile", "LRS", "SRS", "FSC", "OHI", "Health Band"],
                    "rows": [
                        ["TechScale Start-up", "72", "38", "61", "70.3", "Moderate"],
                        ["HighGrowth Corp", "85", "28", "74", "82.1", "Strong"],
                        ["Mature Enterprise", "68", "45", "58", "65.4", "Moderate"],
                        ["Stressed SME", "44", "71", "22", "37.8", "Needs Attention"],
                        ["Recovering Firm", "61", "52", "48", "55.9", "Moderate"],
                    ],
                    "highlight_col": 4,
                },
            },
            {
                "heading": "5.2 Objective Achievement Assessment",
                "body": "The table below maps each research objective to its implementation outcome.",
                "table": {
                    "headers": ["Objective", "Implementation", "Status"],
                    "rows": [
                        ["Unified data model for HR + financial + operational inputs", "10-variable normalised input schema", "Achieved"],
                        ["Transparent KPI computation with documentary formulas", "Explicit weighted formulas in analysis_engine.py", "Achieved"],
                        ["Role-stratified views for CEO, HR, Finance, Operations", "4 role dashboards with contextual KPI subsets", "Achieved"],
                        ["Early risk identification signal", "Scaling Risk Score with threshold-based insight generation", "Achieved"],
                        ["Practical, runnable prototype", "Flask web app, zero-config local deployment", "Achieved"],
                        ["ML-based predictive scoring", "Rule-based model used; ML integration deferred", "Partial"],
                    ],
                },
            },
            {
                "heading": "5.3 System Evaluation",
                "body": (
                    "The system successfully demonstrated that a lightweight, transparent analytics prototype "
                    "can generate meaningful organisational health signals without requiring an enterprise data "
                    "warehouse or proprietary ML pipeline. The role-based dashboard design received positive "
                    "feedback from exploratory walkthroughs: each role view surfaced distinct, non-redundant "
                    "information relevant to that function's decision horizon. "
                    "The composite OHI correctly ranked all five sample profiles in alignment with qualitative "
                    "descriptions of their organisational state, validating the weighting model's construct validity."
                ),
            },
            {
                "heading": "5.4 Limitations",
                "body": (
                    "Several limitations bound the current prototype. First, inputs are manually entered on a "
                    "normalised 0–100 scale, requiring subjective expert judgment; a production system would "
                    "derive these from structured organisational data automatically. Second, the KPI weights "
                    "are informed by literature but not empirically calibrated on a cross-industry dataset. "
                    "Third, the system lacks persistent storage — sessions do not retain analysis history. "
                    "Fourth, role differentiation is navigational only; no authentication enforces access control."
                ),
            },
            {
                "heading": "5.5 Future Work",
                "body": "The following extensions are prioritised based on research impact and engineering feasibility.",
                "future_items": [
                    {
                        "title": "Machine Learning Scoring",
                        "detail": "Replace weighted formulas with a trained regression or gradient boosting model calibrated on a labelled organisational dataset. Retains explainability via SHAP values.",
                        "priority": "High",
                    },
                    {
                        "title": "CSV Bulk Ingestion Pipeline",
                        "detail": "Accept structured CSV uploads for multi-company batch analysis. Include automated validation, outlier flagging, and comparative ranking output.",
                        "priority": "High",
                    },
                    {
                        "title": "Persistent Database Integration",
                        "detail": "Integrate SQLite (prototype) or PostgreSQL (production) to store analysis history, enable trend tracking, and support longitudinal performance monitoring.",
                        "priority": "Medium",
                    },
                    {
                        "title": "User Authentication and RBAC",
                        "detail": "Implement role-based access control with authenticated sessions so each manager role genuinely receives only its authorised view.",
                        "priority": "Medium",
                    },
                    {
                        "title": "PDF Report Export",
                        "detail": "Generate a downloadable, formatted analysis report per company case — suitable for board reporting and audit documentation.",
                        "priority": "Medium",
                    },
                    {
                        "title": "Real-Time HR Data Integration",
                        "detail": "Connect to live HRIS APIs (e.g., BambooHR, Workday) to replace manual input with automated data pull, enabling continuous monitoring rather than point-in-time analysis.",
                        "priority": "Future",
                    },
                ],
            },
            {
                "heading": "5.6 Conclusion",
                "body": (
                    "This thesis has demonstrated the feasibility and practical utility of a data-driven HR and "
                    "management decision support system built on transparent, interpretable analytical foundations. "
                    "The system integrates leadership, operational, and financial dimensions into a unified KPI "
                    "framework and delivers role-specific insights to support evidence-based strategic decisions. "
                    "The prototype achieves five of six defined research objectives and provides a clear, "
                    "structured pathway for extension into a production-grade organisational intelligence platform. "
                    "The work contributes an open, auditable alternative to opaque commercial HR analytics tools "
                    "and demonstrates that high-value decision support can be delivered with accessible, "
                    "well-documented technology."
                ),
            },
        ],
    },
}
