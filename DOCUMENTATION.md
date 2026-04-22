# Complete Project Documentation

## Project: HR Insight Lab – Data-Driven Organizational Health Assessment

**Author:** Mikhael Nabil Salama Rezk  
**Neptun Code:** IHUTSC  
**Date:** March 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Technology Stack & Dependencies](#technology-stack--dependencies)
4. [File-by-File Reference](#file-by-file-reference)
5. [How to Set Up](#how-to-set-up)
6. [How to Run](#how-to-run)
7. [Feature Guide](#feature-guide)
8. [Database Schema](#database-schema)
9. [Architecture Decisions](#architecture-decisions)
10. [Contributors & Acknowledgments](#contributors--acknowledgments)

---

## Project Overview

**HR Insight Lab** is a local, open-source decision support system for assessing organizational health. It integrates leadership, people, operations, and financial data into four composite KPIs and generates evidence-based strategic assessments.

**Problem Solved:**  
Managers lack transparent, unified frameworks for understanding organizational readiness. Commercial platforms are opaque and expensive. This system is open, auditable, lightweight, and practical.

**Key Features:**
- Transparent KPI formulas (no black boxes)
- Role-based dashboards (CEO, HR, Finance, Operations)
- SQLite-backed analysis history
- CSV batch upload for multi-company analysis
- Local machine learning scoring (gradient boosting)
- PDF report generation
- Demo HRIS integrations (BambooHR, Workday)
- Complete user authentication and RBAC

**Technology:**
- Python 3.11, Flask 3.1, SQLite
- scikit-learn for ML, ReportLab for PDFs
- Vanilla JavaScript for interactivity
- CSS Grid for responsive design

---

## Directory Structure

```
c:\Thesis_Hr_system\
├── .git/                           # Git version control
├── .venv/                          # Python virtual environment
├── .gitignore                      # Git ignore rules
│
├── README.md                       # Quick start guide
├── THESIS.md                       # Complete thesis narrative (this file)
├── DOCUMENTATION.md                # Complete project documentation (this file)
├── requirements.txt                # Python dependencies
│
├── app.py                          # Flask application (main entry point)
├── analysis_engine.py              # Analytics & KPI computation engine
├── data_store.py                   # SQLite persistence layer
├── ml_engine.py                    # Machine learning model
├── hr_integrations.py              # Demo HRIS provider payloads
├── reporting.py                    # PDF report generation
├── section_data.py                 # Thesis section content
├── generate_documentation.py       # Thesis PDF generator (legacy)
│
├── hr_analysis.db                  # Local SQLite database (created at runtime)
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Complete styling (600+ lines)
│   └── js/
│       └── main.js                # Client-side interactivity
│
└── templates/                      # Jinja2 HTML templates
    ├── base.html                  # Shared layout & navigation
    ├── home.html                  # Landing page
    ├── login.html                 # Authentication form
    ├── analysis.html              # Analysis workspace (primary UI)
    ├── dashboard.html             # Role-based dashboard view
    ├── history.html               # Analysis history page
    └── section.html               # Thesis section viewer
```

---

## Technology Stack & Dependencies

### Runtime Environment

| Component | Version | Purpose | Notes |
|-----------|---------|---------|-------|
| Python | 3.11.1 | Runtime | Installed locally; .venv recommended |
| pip | Latest | Package manager | No external pyenv needed |

### Python Packages

All dependencies are in `requirements.txt`:

```
Flask==3.1.0
numpy==1.26.4
reportlab==4.4.4
scikit-learn==1.7.2
```

**Why each package:**

- **Flask 3.1.0**
  - Lightweight web framework
  - Handles HTTP routing, template rendering, session management
  - Chosen for minimal overhead and clarity (not Django, which is heavier)
  - Used for: All routes (`/`, `/login`, `/analysis`, `/dashboard/<role>`, `/history`, etc.)

- **NumPy 1.26.4**
  - Numerical computing library
  - Required by scikit-learn for array operations
  - **Pinned to 1.26.4:** Newer versions (1.27+) require CPU instruction support (X86_V2) not available on all machines
  - Used for: Feature vectors, normalization arrays

- **scikit-learn 1.7.2**
  - Machine learning library
  - Provides GradientBoostingRegressor for ML scoring
  - Alternative considered: Custom ML implementation (rejected—scikit-learn is industry standard)
  - Used for: Training synthetic company profiles, predicting success probability

- **ReportLab 4.4.4**
  - PDF generation library
  - Builds formatted analysis reports
  - Alternative considered: WeasyPrint (requires additional system dependencies)
  - Used for: `/analysis/<id>/pdf` route, generating downloadable reports

### Frontend Technologies (No External Libraries)

| Technology | Usage |
|-----------|-------|
| HTML5 | Semantic markup for forms, dashboards, reports |
| CSS3 | Grid layout, custom components, theming via CSS variables |
| Vanilla JavaScript | KPI button clicks, dashboard panel updates, score card animations |
| Jinja2 | Template rendering (built into Flask) |

**Design decision:** No Bootstrap, Tailwind, or jQuery—prefer minimal dependencies and explicit control over styling. CSS + Vanilla JS is sufficient for this scope.

### Database

- **SQLite 3** (built into Python)
- File-based relational database stored as `hr_analysis.db`
- Suitable for development and single-server deployment
- For production: Consider PostgreSQL or MySQL

---

## File-by-File Reference

### Backend Modules

#### `app.py` (520 lines)
**Purpose:** Main Flask application and route controller.

**Key Sections:**
- **Imports & Config** (lines 1–40): Flask setup, secret key, max upload size
- **THESIS_CONTENT** (lines 42–55): Thesis metadata displayed on home page
- **FUTURE_WORK_EXTENSIONS** (lines 57–90): Feature list displayed on analysis page
- **ROLE_FOCUS** (lines 92–240): Dashboard KPI specifications per role
- **Helper Functions** (lines 242–350):
  - `login_required()`: Decorator for protected routes
  - `load_current_user()`: Flask before_request hook
  - `_score_from_result()`: Extract scores from result object
  - `_band_for_value()`: Classify score into band (e.g., "Strong", "Watchlist")
  - `build_role_dashboard()`: Construct dashboard data for a role
  - `_validate_csv_row()`: Validate and note CSV row anomalies
  - `_analysis_context()`: Build template context for analysis page
- **Routes** (lines 352–520):
  - `GET /`: Home page
  - `GET/POST /login`: Authentication
  - `GET /logout`: Session termination
  - `GET/POST /analysis`: Analysis workspace
  - `GET /history`: Analysis history
  - `GET /analysis/<int:analysis_id>/pdf`: PDF export
  - `GET /section/<int:number>`: Thesis section viewer
  - `GET /dashboard/<role>`: Role-specific dashboard

**Key Design:**
- All routes except `/` and `/login` require `@login_required` decorator
- RBAC enforced in dashboard route: `if g.user["role"] not in role_config["allowed_roles"]: abort(403)`
- CSV validation and batch analysis handled in single POST handler
- Template context built once per request via `_analysis_context()` helper

#### `analysis_engine.py` (400 lines)
**Purpose:** Pure Python analytics module (decoupled from web framework).

**Key Sections:**
- **Configuration** (lines 1–100):
  - `INDUSTRY_OPTIONS`: Industry categories
  - `STAGE_OPTIONS`: Company stage (startup, growth, mature, turnaround)
  - `NUMERIC_FIELD_SPECS`: Field metadata (min, max, default, label, display)
  - `DEFAULT_FORM_DATA`: Safe defaults for all form fields
  - `ML_FEATURE_LABELS`: Feature names for ML model
- **Utility Functions** (lines 102–140):
  - `_to_float()`: Safe conversion to float with default
  - `_clamp()`: Constrain value to [lo, hi] range
  - `build_form_data()`: Normalize form input and build form data dict
  - `to_feature_vector()`: Convert form data to list for ML
- **Normalization Functions** (lines 142–195):
  - `_norm_leadership_years()`: Years → 0–100 scale (piecewise)
  - `_norm_digital()`: 1–10 scale → 0–100
  - `_norm_retention()`: % → % (identity, already 0–100)
  - `_norm_churn_risk()`: % × 2.5
  - `_norm_debt()`: D/E ratio × 50
  - `_norm_process_fragility()`: (10 − doc_score) × 10
  - `_norm_dependency()`: (dep_score / 5) × 100
  - `_norm_margin()`: (margin_pct + 100) × 0.5
  - `_norm_revenue_growth()`: 30 + growth_pct × 1.8
  - `_norm_cash_runway()`: (cash_months + 100) × 0.5
- **Banding Functions** (lines 197–215):
  - `_band()`: Map score to "Strong", "Moderate", "Needs Attention"
  - `_risk_band()`: Map risk score to "High", "Medium", "Low"
- **Prediction Logic** (lines 217–285):
  - `_predict()`: Map OHI + SRS + FSC → success probability and verdict
- **Insight Generation** (lines 287–330):
  - `_insights()`: Generate context-aware recommendations based on KPI profile
  - `_display_inputs()`: Format inputs for display in report
- **Main Computation** (lines 332–395):
  - `analyze_company()`: Core logic—normalize inputs, compute KPIs, predict, generate insights
  - `run_ai_analysis()`: Wrapper that calls build_form_data() then analyze_company()

**Design Philosophy:**
- All computation is pure functions (no side effects, no global state)
- Input normalization is configurable and auditable
- KPI formulas are explicit and top-level
- Output is a rich dictionary with raw_inputs, KPI scores, bands, prediction, insights, display data
- Zero dependencies on Flask or web framework

#### `data_store.py` (185 lines)
**Purpose:** SQLite persistence and authentication.

**Key Sections:**
- **Configuration** (lines 1–20):
  - `DB_PATH`: Location of SQLite database
  - `DEFAULT_USERS`: Seeded demo accounts
- **DB Connection** (lines 22–30):
  - `get_connection()`: Open SQLite connection with Row factory
- **Initialization** (lines 32–70):
  - `init_db()`: Create schema if not exists; seed default users if empty
- **Authentication** (lines 72–90):
  - `authenticate_user(username, password)`: Lookup and hash-verify (Werkzeug security)
  - `get_user_by_id(user_id)`: Load user session
- **Analysis Persistence** (lines 92–130):
  - `save_analysis()`: Insert analysis record with payload and result JSON
  - `_hydrate_analysis()`: Reconstruct analysis object from DB row
  - `get_analysis_by_id()`: Fetch single analysis with user metadata
- **Querying** (lines 132–180):
  - `list_recent_analyses()`: Get N most recent (admin sees all, others see own)
  - `list_company_history()`: Get all runs for a specific company

**Key Design:**
- Passwords hashed with Werkzeug's `generate_password_hash()` (scrypt-based)
- JSON serialization for payload and result (easy export, versioning)
- Foreign key between analyses and users
- Created_at timestamps in ISO format for sorting

#### `ml_engine.py` (120 lines)
**Purpose:** Local machine learning model for success probability.

**Key Sections:**
- **Model Cache** (lines 1–15): Global cache to avoid retraining
- **Synthetic Data Generation** (lines 17–35):
  - `_random_sample()`: Generate randomized company profile
  - Uses same distribution as test scenarios
- **Model Training** (lines 37–70):
  - `_train_model()`: Fit GradientBoostingRegressor on 900 synthetic samples
  - 80/20 train/test split
  - Reports R² and MAE on test set
- **Model Bundle** (lines 72–85):
  - `get_model_bundle()`: Lazy-load cached model
  - `get_model_summary()`: Return model metadata for display
- **Prediction** (lines 87–115):
  - `get_ml_prediction()`: Predict probability and compute feature contributions
  - Contributions = delta from baseline × feature importance × 100
  - Returns top 5 contributors for explainability

**Key Design:**
- Lazy initialization (model trained on first call, then cached)
- Uses same feature vector format as KPI logic for consistency
- Feature contributions enable "why" explanations without full SHAP analysis

#### `hr_integrations.py` (65 lines)
**Purpose:** Demo HRIS provider payloads.

**Key Sections:**
- **Provider Registry** (lines 1–20):
  - `AVAILABLE_PROVIDERS`: List of available import sources
- **Demo Payloads** (lines 22–60):
  - `DEMO_PROVIDER_PAYLOADS`: Hardcoded BambooHR and Workday profiles
  - Each payload is a complete form data dictionary
- **Import Function** (lines 62–65):
  - `fetch_provider_profile()`: Return copy of demo payload

**Future Integration:**
Replace demo payloads with:
```python
def fetch_provider_profile(provider_key, credentials):
    if provider_key == "bamboohr":
        return bamboohr_api.get_employee_profile(credentials)
    elif provider_key == "workday":
        return workday_api.get_workforce_profile(credentials)
```

#### `reporting.py` (100 lines)
**Purpose:** PDF report generation.

**Key Sections:**
- **Imports & Setup** (lines 1–15): ReportLab utilities
- **PDF Builder** (lines 17–110):
  - `build_analysis_pdf()`: Main function
  - Constructs BytesIO buffer with title, company info, KPI table, inputs table, recommendations, ML section
  - Uses custom table styles and spacing

**Design:**
- Returns BytesIO buffer (not file)—compatible with Flask `send_file()`
- Two-column table layout for KPI section
- ML contributions in sortable table format
- Supports PDF export for archived reports

#### `section_data.py` (400 lines)
**Purpose:** Thesis section content (displayed on web and in PDF generator).

**Key Sections:**
- **SECTIONS Dictionary**: Maps section numbers to content
- Each section contains:
  - Title, description, key concepts
  - KPI definitions, formulas, rationale
  - Test case scenarios

---

### Frontend Files

#### `templates/base.html`
**Purpose:** Shared HTML layout.

**Sections:**
- `<header>` with site brand and navigation
- User bar showing current user and role
- Flash message stack for alerts
- `<main>` content block (overridden by child templates)
- `<footer>` with copyright and links

**Key Features:**
- Conditional nav based on `current_user` (login/logout links)
- Flash categories (success, warning, danger) with CSS styling

#### `templates/login.html`
**Purpose:** Authentication form.

**Sections:**
- Left side: Demo user cards showing credentials
- Right side: Login form with username/password input

**Key Features:**
- Displays all seeded demo users (no sign-up implementation)
- SSL-ready (uses POST for credentials, though TLS not enabled locally)

#### `templates/analysis.html`
**Purpose:** Main analysis workspace.

**Sections:**
- Hero section with workspace description
- Utility grid: ML model summary, HRIS provider import, CSV upload panel
- Analysis form: Company profile, leadership & people, risk & operations, financial performance
- Batch result table (if results available)
- Verdict banner (if analysis completed)
- ML scoring section with feature contributions
- KPI breakdown grid
- Recommendations and submitted inputs
- Recent analysis history table

**Key Features:**
- Form values sticky (pre-filled from `form_data` context)
- CSV upload shows expected headers as hint text
- Batch results ranked by OHI with validation notes
- Verdict color-coded (success/warning/danger)
- ML prediction table with +/- contribution visualization

#### `templates/dashboard.html`
**Purpose:** Role-based dashboard.

**Sections:**
- Dashboard title and goal (context-specific)
- Metadata bar showing latest analysis used
- KPI card grid (3 cards per role, clickable)
- Score panel showing selected KPI (score, band, detail)
- Role selector buttons to switch dashboards

**Key Features:**
- Interactive KPI selection (click word to see score)
- Score panel updates via JavaScript
- Active state styling on selected KPI

#### `templates/history.html`
**Purpose:** Analysis history and longitudinal tracking.

**Sections:**
- History summary: total runs, average probability, average OHI
- History table: ID, company, source, probability, OHI, created date, PDF link

**Key Features:**
- Summary stats at top for quick glance
- Sortable table (client-side sorting via links)
- PDF export links for each record
- Allows trend analysis across companies

#### `templates/home.html`
**Purpose:** Landing page.

**Sections:**
- Hero section with thesis title and abstract
- Thesis section links
- Quick start instructions

#### `templates/section.html`
**Purpose:** Thesis section viewer.

**Render:**
- Dynamic section content from `section_data.py`
- Section title, description, formulas, examples

---

### Static Assets

#### `static/css/style.css` (600+ lines)
**Purpose:** Complete styling system.

**Key Sections:**
- **CSS Variables** (lines 1–50): Colors (primary, text, muted, surfaces, etc.)
- **Reset & Base** (lines 52–100): Typography, spacing, base element styles
- **Layout Components** (lines 102–200):
  - `.container`: Max-width container
  - `.grid.two/three/four`: Multi-column grids
  - `.panel`, `.card`: Box components with spacing
- **Navigation** (lines 202–250): Header, nav links, brand styling
- **Forms & Inputs** (lines 252–320): Input styling, labels, buttons
- **Tables** (lines 322–380): Data table styling with borders and padding
- **Utility Classes** (lines 382–450):
  - `.chip`: Small label badge
  - `.score-card`: KPI card with animation
  - `.verdict-banner`: Outcome box (color-coded)
  - `.dashboard-*`: Dashboard-specific components
  - `.auth-*`: Auth page styling
  - `.flash-*`: Alert boxes
- **Responsive Design** (lines 452–500): Media queries for tablets/mobile
- **Animations** (lines 502–550): Fade-in, score card transitions

**Design Philosophy:**
- CSS Grid for layouts (not float, not flex-only)
- CSS variables for theming (easy rebranding)
- Mobile-first approach
- No external framework (Bootstrap, Tailwind)—explicit control

#### `static/js/main.js` (45 lines)
**Purpose:** Client-side interactivity.

**Key Functions:**
- **Score card animation**: Fade-in with staggered delay (lines 1–15)
- **KPI button click handler** (lines 17–45):
  - Extract data attributes from clicked button
  - Update dashboard panel (title, detail, score, band)
  - Toggle active state on KPI cards

**Design:**
- Vanilla JS (no jQuery)
- Unobtrusive JavaScript (progressive enhancement)
- Event delegation not needed (simple button clicks)

---

## How to Set Up

### Prerequisites

- Python 3.10+ (tested on 3.11.1)
- pip (comes with Python)
- Git (for version control)
- 500MB free disk space (for .venv and SQLite)

### Step-by-Step Installation

**1. Clone the repository**
```bash
git clone https://github.com/MI804-png/Thesis_BSC_2026.git
cd Thesis_BSC_2026
```

**2. Create a virtual environment**
```bash
python -m venv .venv
```

**3. Activate the virtual environment**
- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Verify installation**
```bash
python -c "import flask; import sklearn; import reportlab; print('All dependencies installed successfully')"
```

**6. Run the Flask app**
```bash
python app.py
```

You should see:
```
WARNING: This is a development server. Do not use it in production applications.
Running on http://127.0.0.1:5000
```

**7. Open in browser**
```
http://127.0.0.1:5000
```

### Troubleshooting

**Issue: ModuleNotFoundError: No module named 'flask'**
- Ensure .venv is activated: `which python` should show `.venv/.../python`
- Reinstall: `pip install -r requirements.txt`

**Issue: Address already in use (port 5000)**
- Change port in `app.py`: `app.run(port=5001, debug=True, use_reloader=False)`
- Or kill existing process: `lsof -ti :5000 | xargs kill -9` (Mac/Linux)

**Issue: NumPy "X86_V2" CPU instruction error**
- Already solved in requirements.txt (numpy==1.26.4)
- If still occurs, contact system admin about CPU compatibility

**Issue: SQLite database locked**
- Restart Flask app: `Ctrl+C` then `python app.py`
- Check if app crashed; clear `hr_analysis.db` and restart if needed

---

## How to Run

### Starting the Application

```bash
# Activate .venv (if not already active)
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\Activate.ps1  # Windows PowerShell

# Run the Flask app
python app.py
```

### Accessing the Web Interface

1. Open browser: `http://127.0.0.1:5000`
2. Click **Sign In** or navigation link
3. Use demo credentials (see THESIS.md section 5.2)
4. Navigate to **AI Analysis** or **History**

### Running Analyses

#### Manual Analysis
1. Go to `/analysis`
2. Fill in company details (or load HRIS demo)
3. Click **Run Analysis & Save Locally**
4. Review results, recommendations, and ML probability

#### Batch CSV Analysis
1. Prepare CSV with headers (see THESIS.md Appendix A)
2. Go to `/analysis`
3. Upload CSV via **CSV Bulk Ingestion**
4. View results ranked by OHI
5. Click any PDF link to download report

#### View Dashboard
1. Go to `/dashboard/ceo` (or hr, finance, operations)
2. Click KPI words to see details
3. Switch between roles to see different metrics

#### History & Trends
1. Go to `/history`
2. See all saved analyses and summary stats
3. Click PDF link to download any report

### Stopping the Application

Press `Ctrl+C` in terminal.

---

## Feature Guide

### 1. Authentication & RBAC

**Users**
- 5 seeded accounts: admin, ceo, hr, finance, operations
- Passwords hashed with scrypt (Werkzeug)
- Session-based (cookie-based after login)

**Role-Based Access Control**
- Each route checks `g. user["role"]` against allowed roles
- Dashboard routes enforce: `if user.role not in role_config["allowed_roles"]: abort(403)`
- Users see only their own analysis history (admin sees all)

**Demo Credentials**
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| CEO | ceo | ceo123 |
| HR | hr | hr123 |
| Finance | finance | finance123 |
| Operations | operations | operations123 |

### 2. Analysis Workflow

**Input Dimensions**
- Company profile: name, industry, stage, employee count
- Leadership & people: experience, digital maturity, retention
- Risk & operations: churn, debt, process documentation, key-person dependency
- Financial: current asset change, revenue growth, cash flow change

**Processing**
- All inputs normalized to 0–100 internal scale
- Four KPIs computed via explicit weighted formulas
- Success probability derived from OHI + SRS + FSC
- Verdict and time horizon assigned based on probability
- Insights generated based on weak KPI domains
- ML model provides independent prediction

**Output**
- KPI scores and bands
- Success probability and verdict
- Time horizon and summary
- Strategic recommendations
- ML probability and feature contributions
- Submitted inputs for audit trail

**Storage**
- Saved to SQLite with payload and result snapshots
- Accessible via `/history` for trend analysis
- Exportable as PDF via `/analysis/<id>/pdf`

### 3. CSV Batch Upload

**Format**
```
company_name,industry,stage,employee_count,leadership_years,digital_score,retention_pct,churn_pct,dte_ratio,doc_score,dep_score,margin_pct,growth_pct,cash_months
```

**Validation**
- Unknown industries defaulted to "general"
- Unknown stages defaulted to "growth"
- Missing numerics use defaults
- Out-of-range values clamped to [min, max]
- Validation notes recorded (e.g., "Churn Rate clamped")

**Results**
- Ranked by OHI (highest first)
- Summary: file name, row count, average probability
- Each row: company name, OHI, probability, verdict, notes, PDF link
- Each row saved as separate analysis record

### 4. PDF Export

**Content**
- Title page with analysis metadata
- KPI snapshot table
- Input values table (audit trail)
- Strategic recommendations
- ML section with top 5 feature contributions

**Usage**
- `/analysis/<id>/pdf` returns application/pdf
- Browser offers download or inline view
- Suitable for board reports, archived decisions

### 5. HRIS Import Demo

**Providers**
- **BambooHR**: Loads demo profile (Atlas Retail Group)
- **Workday**: Loads demo profile (Northstar Manufacturing)

**Process**
1. Select provider from dropdown
2. Click **Load Demo Feed**
3. Form pre-fills with provider data
4. User can edit before submitting

**Future Enhancement**
- Replace hardcoded payloads with live API calls
- Support real BambooHR/Workday authentication

### 6. Dashboard Interaction

**Clickable KPIs**
- Each KPI name is a button
- Click to see detailed score, band, and context
- Score panel updates dynamically

**Role-Specific Views**
- CEO: OHI, SRS, growth, LRS
- HR: LRS, retention, capability maturity, dependency
- Finance: FSC, margins, debt, cash flow
- Operations: Fragility, stability, SRS

**Latest Analysis**
- Dashboard shows which saved analysis is being used
- Users can switch to older analyses for comparison

### 7. History & Trends

**History Page**
- All saved analyses (own for non-admin, all for admin)
- Summary stats: total count, average probability, average OHI
- Sortable table with company, source, scores, date, PDF link

**Trend Tracking**
- Run same company twice to see trend on analysis page
- Shows OHI delta and probability delta
- Useful for monitoring intervention effects

---

## Database Schema

### `hr_analysis.db`

SQLite database auto-created at runtime.

**Table: `users`**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

**Seeded Rows:**
```
(1, 'admin', <scrypt_hash>, 'admin', 'System Administrator', '2026-03-23T...')
(2, 'ceo', <scrypt_hash>, 'ceo', 'Chief Executive Officer', '2026-03-23T...')
(3, 'hr', <scrypt_hash>, 'hr', 'HR Director', '2026-03-23T...')
(4, 'finance', <scrypt_hash>, 'finance', 'Finance Manager', '2026-03-23T...')
(5, 'operations', <scrypt_hash>, 'operations', 'Operations Lead', '2026-03-23T...')
```

**Table: `analyses`**
```sql
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    source TEXT NOT NULL,
    provider TEXT,
    batch_name TEXT,
    created_by INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    FOREIGN KEY(created_by) REFERENCES users(id)
);
```

**Columns:**
- `id`: Auto-incrementing primary key
- `company_name`: User-entered company name (or "Your Company" if blank)
- `source`: 'manual' (form), 'csv' (batch), 'import' (provider demo)
- `provider`: 'bamboohr', 'workday', or NULL
- `batch_name`: CSV file name if source='csv'
- `created_by`: Foreign key to users table
- `created_at`: ISO timestamp (UTC)
- `payload_json`: JSON snapshot of input form data
- `result_json`: JSON snapshot of KPI/prediction results

**Example Row:**
```json
{
    "id": 1,
    "company_name": "Acme Corp",
    "source": "manual",
    "payload_json": {"company_name": "Acme Corp", "industry": "technology", ...},
    "result_json": {"lrs": 77.9, "srs": 33.2, "fsc": 58.4, "ohi": 69.1, ...}
}
```

---

## Architecture Decisions

### 1. Layered Architecture (Presentation → Application → Analytics → Data)

**Rationale:**
- Separation of concerns enables independent evolution
- Analytics engine decoupled from web framework (testable in isolation)
- Easy to swap backends (Flask → FastAPI, SQLite → PostgreSQL)
- Clear contracts between layers

**Alternative Considered:**
  - Keeping everything in one main file. I quickly realized this would become 
    a maintenance nightmare as the UI grew, so I split the logic early.

### 2. Transparent, Auditable KPI Formulas

**Rationale:**
- Commercial platforms use black-box algorithms; users don't understand how scores are computed
- This system makes all math explicit; managers can audit every number
- Formulas are based on HR literature (not arbitrary)

**Alternative Considered:**
  - Going with a pure ML model. While it might be "smarter," I decided against 
    it because I wanted managers to be able to audit the math themselves.

### 3. Local Storage (SQLite) Instead of Cloud

**Rationale:**
- Zero infrastructure required (suitable for thesis demo)
- Single-server deployment (no network latency)
- Data stays on local machine (suitable for sensitive HR data)
- Easy to inspect (standard SQL tools)

**Alternative Considered:**
  - PostgreSQL or a full cloud DB. I stuck with SQLite because it’s zero-config 
    and keeps all the sensitive HR data on the local machine for this demo.

### 4. Vanilla JavaScript (No Frontend Framework)

**Rationale:**
- Minimal scope: only KPI button clicks and panel updates
- No build step required
- Clear client-side code
- Fast load time

**Alternative Considered:**
- React (overkill for this scope)
- Vue.js (still unnecessary)

### 5. Session-Based Authentication (Not API Token)

**Rationale:**
- Server-rendered HTML (not SPA)
- Simpler session management
- Works with HTML forms (no JavaScript required for basic auth)

**Alternative Considered:**
- JWT tokens (not needed for server-rendered app)

### 6. CSV Batch Upload Over API Integration

**Rationale:**
- Works offline (no need for live HRIS connection)
- Easy to test and validate
- Flexible (users can curate data before upload)

**Future:** Live HRIS APIs (BambooHR, Workday) will replace/supplement CSV

### 7. Gradient Boosting ML (Not Deep Learning)

**Rationale:**
- Excellent performance on tabular data (10 features, ~900 synthetic samples)
- Interpretable (feature importances)
- Fast training (<1s for synthetic data)
- Industry standard (scikit-learn)

**Alternative Considered:**
- Linear regression (less expressive)
- Neural networks (overkill, hard to explain)

---

## Contributors & Acknowledgments

**Author:** Mikhael Nabil Salama Rezk (Neptun: IHUTSC)

**Thesis Advisor:** [Your advisor name]  
**University:** [Your institution]  
**Date:** March 2026

**Technology Credits:**
- Flask community for excellent web framework
- scikit-learn team for accessible ML library
- ReportLab for PDF generation
- SQLite developers for embedded database

**References:**
- Bondarouk & Ruël (2013): HRIS strategic value
- Cascio & Boudreau (2011): HR metrics and ROI
- Christopher & Holweg (2011): Supply chain resilience
- Gorry & Scott Morton (1971): DSS framework
- Kaplan & Norton (1992): Balanced Scorecard

---

## Appendix: Environment Variables (Optional)

For production deployment, set:

```bash
export FLASK_SECRET_KEY="your-secure-random-key-here"
export FLASK_ENV="production"
export FLASK_DEBUG="0"
```

For development (defaults):
```bash
export FLASK_SECRET_KEY="local-thesis-hr-secret"  # INSECURE—DO NOT use in production
export FLASK_ENV="development"
export FLASK_DEBUG="1"
```

---

**End of Documentation**

For more details, see:
- [THESIS.md](THESIS.md) – Complete thesis narrative with system design rationale
- [README.md](README.md) – Quick start guide
- Source code comments in individual Python modules
