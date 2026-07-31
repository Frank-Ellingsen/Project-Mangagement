# Project Controlling Control Tower

An automated, interactive **Project Controlling & Earned Value Management (EVM) Control Tower** designed for engineering, maritime, and defense sector projects. This workspace integrates analytical data processing, automated agentic auditing, Excel reporting, Power BI compilation, and a Streamlit web dashboard — all governed by **Edward Tufte's Data-Ink Ratio** principles and **PRINCE2** project management standards.

---

## 📋 Project Overview & Portfolio Scope

Originally built around a single vessel project, the Control Tower now aggregates and tracks a **6-project portfolio** spanning various stages of execution:

1. **PRJ-001 (Composite Vessel Construction):** Baseline BAC 1,500,000 NOK. Currently **99.5% complete**, suffering from a 🔴 24.0% cost overrun driven by WBS 1.0 labor rates.
2. **PRJ-002 (Patrol Vessel Carbon Mold Design):** Baseline BAC 800,000 NOK. **0.0% complete** (Planned).
3. **PRJ-003 (Subsea Cable Installation Frame):** Baseline BAC 1,200,000 NOK. **30.0% complete** (Active).
4. **PRJ-004 (Autonomous Workboat Hull Weldments):** Baseline BAC 2,000,000 NOK. **70.0% complete** (Active).
5. **PRJ-005 (Defense Logistics Pontoon Build):** Baseline BAC 1,000,000 NOK. **90.0% complete** (Active).
6. **PRJ-006 (Lightweight Composite Cargo Hatch):** Baseline BAC 600,000 NOK. **100.0% complete** (Delivered 🟢 under budget at 586,500 NOK).

### Current Portfolio Health Snapshot

| Metric                           | Value         | Status                   |
| :------------------------------- | :------------ | :----------------------- |
| **Total Portfolio BAC**          | 7,100,000 NOK | Baseline                 |
| **Total Portfolio AC**           | 5,220,810 NOK | Active Spend             |
| **Total Portfolio EV**           | 4,752,500 NOK | Value Earned             |
| **Portfolio CPI**                | 0.91          | 🟡 Muted Cost Overrun    |
| **Portfolio Cost Variance (CV)** | -468,310 NOK  | 🔴 9% budget overrun     |
| **Overall Portfolio Progress**   | 66.9%         | In-progress              |

---

## 🏗️ System Architecture

The workspace is structured into a **data layer**, a **CLI automation layer**, a **web dashboard layer**, and an **agent skill framework**:

```
Project Mng/
├── AI_Controller/
│   ├── agent_skills_app.py        # Streamlit Web Application (Control Tower)
│   ├── streamlit_dashboard.py     # Alternative Streamlit dashboard (S-Curve focus)
│   ├── build_duckdb.py            # DuckDB database builder (Analytical Layer)
│   ├── build_sqlite.py            # SQLite database builder (Transactional Layer)
│   ├── run_agents.py              # Multi-agent audit routines script
│   ├── excel_report_agent.py      # Automated Excel workbook report writer
│   ├── build_pbi_project.py       # Power BI Developer project compiler (.pbip)
│   ├── verify_dataset.py          # Data validation & cross-check script
│   ├── tufte_cli_dashboard.py     # Terminal-based dashboard (Tufte-compliant)
│   ├── generate_mock_data.py      # Mock data generator (creates CSV fixtures)
│   ├── generate_excel_data.py     # Excel-friendly flat-file generator
│   ├── STREAMLIT_APP_README.md    # Streamlit technical architecture README
│   ├── STREAMLIT_USER_GUIDE.md    # Streamlit end-user usage guide
│   ├── tufte_pm_visual_guide.md   # Edward Tufte data-ink design guide
│   ├── datamodel_erd.md           # Database ERD & relational rules
│   ├── bi_datamodel_and_dax.md    # Power BI star schema & DAX measures
│   ├── reporting_workflow.md      # End-to-end data pipeline workflow
│   ├── project_controller.md      # Agent architecture & EVM terminology
│   ├── project financial controller agents.md  # Agent skill definitions
│   ├── my_toolstack.md            # AI research tool stack reference
│   └── tools plus.md              # Tool ecosystem mapping
├── Data/
│   ├── CSV/                       # Raw source data (8 relational CSV files)
│   │   ├── projects.csv
│   │   ├── wbs_elements.csv
│   │   ├── resources.csv
│   │   ├── resource_assignments.csv
│   │   ├── timesheets.csv
│   │   ├── material_costs.csv
│   │   ├── physical_progress.csv
│   │   └── raid_log.csv
│   ├── DuckDB/                    # Analytical DuckDB instance
│   │   └── project_controlling.db
│   ├── SQLite/                    # Transactional SQLite instance
│   │   └── project_controlling.db
│   ├── PowerBI_Project/           # Compiled Power BI .pbip project
│   │   ├── Vessel_Performance.pbip
│   │   ├── Vessel_Performance.SemanticModel/
│   │   └── Vessel_Performance.Report/
│   ├── excel_friendly/            # Excel-friendly flat files (semicolon-delimited)
│   └── PRJ-001_Project_Initiation_Document.md  # PRINCE2 PID
├── .agents/
│   ├── skills/                    # 13 agent skill instruction folders
│   └── rules/                     # Agent governance rules
├── index.html                     # Static HTML Control Tower dashboard
├── run_all.ps1                    # PowerShell Master Orchestrator script
├── README.md                      # This file
└── USER_GUIDE.md                  # Master Workspace User Guide
```

---

## 🛠️ Tech Stack & Core Decisions

### 1. Analytical Database — DuckDB

Powering high-speed aggregations and analytical views for Earned Value Management (EVM) metrics. Compiles SQL views for:

- `v_wbs_evm_metrics` — Per-WBS BAC, AC, EV, CPI, CV, EAC (Typical & Atypical), Percent Complete
- `v_project_evm_summary` — Project-level rollup: Total BAC, AC, EV, CV, CPI, EAC, VAC, Progress %

### 2. Transactional Database — SQLite

Powering transactional tables such as the project `raid_log`, overtime threshold audits, and log audit trails. Mirrors the same EVM views as DuckDB for cross-engine verification.

### 3. Frontend — Streamlit & Plotly

Provides a clean, modern web interface with:

- **Interactive Gantt charts** (Plotly Express timeline) with Tufte-compliant styling (zero vertical gridlines, direct bar labeling, semantic red/green highlighting)
- **S-Curve charts** (Plotly Graph Objects) with direct labeling
- **KPI metric cards** with conditional color thresholds (CPI < 0.95 = crimson)
- **What-If simulation sliders** for EAC/VAC forecasting
- **6 stakeholder persona views** (Executive, PM, Engineering Lead, Yard Manager, Procurement, Quality Inspector)

### 4. Static HTML Dashboard — `index.html`

A standalone, browser-ready Control Tower dashboard with:

- Interactive tabbed navigation (Dashboard, Stakeholders, Skill Inspector, Live Crew)
- Tufte-compliant KPI cards, Gantt bars, and tables
- A built-in **What-If Corrective Simulator** with sliders for labor/material savings and schedule crashing
- An embedded EVM glossary with AACE/PMI compliance notes

### 5. Excel Reports — OpenPyXL

Automatically generates advanced, formula-driven spreadsheets (`vessel_construction_report.xlsx`) with:

- Interactive EVM dashboard tab with live Excel formulas (`=E9/D9` for CPI, `=C9/F9` for EAC)
- Gantt & Critical Path tab using Chris Croft scheduling methodology
- Conditional formatting for cost overrun alerts

### 6. Power BI Project — `.pbip` Compiler

Generates a complete Power BI Developer project structure with:

- Star schema data model (fact tables + dimension tables)
- DAX measures for BAC, AC, EV, CPI, SPI, EAC, VAC
- Power Query (M) expressions for CSV ingestion and labor cost enrichment
- Relationship definitions between all tables

### 7. Agent Skill Framework — 13 Specialized Agents

A registry of domain-specific agent skills, each with a `SKILL.md` instruction file:

| Agent                            | Category              | Role                                                                                                     |
| :------------------------------- | :-------------------- | :------------------------------------------------------------------------------------------------------- |
| `project-controller-agent`       | Financial Control     | Calculates EVM metrics (CPI/SPI), forecasts EAC/VAC, flags WBS cost variance anomalies                   |
| `project-cfo-agent`              | Financial Control     | Audits portfolio profitability, cash flow burn rates, labor/material split, Margin at Completion         |
| `project-contract-manager-agent` | Governance & Risk     | Tracks Variation Orders (VO/VOR), scope modifications, baseline budget revisions, contractual milestones |
| `project-controlling-evm`        | Financial Control     | Core mathematical engine executing EVM formulas and status thresholds                                    |
| `project-engineering-lead-agent` | Operations & Schedule | Monitors engineering design schedules, drawing release dates, design hour burn rates                     |
| `project-evaluation-agent`       | Governance & Risk     | Conducts post-project financial audits (etterkalkyle), analyzes baseline deviations, compiles benchmarks |
| `project-manager-agent`          | Operations & Schedule | Coordinates project milestones, resource allocation, critical path scheduling, task dependencies         |
| `project-procurement-agent`      | Operations & Schedule | Audits purchase orders, committed costs vs actual invoices, supplier lead times, vendor delivery risks   |
| `project-production-agent`       | Operations & Schedule | Tracks shipyard/shop-floor labor productivity, physical assembly milestones, structural completion       |
| `project-quality-agent`          | Governance & Risk     | Tracks Non-Conformity Reports (NCRs), inspection pass rates, estimates financial rework impact           |
| `project-research-agent`         | Governance & Risk     | Conducts shipbuilding rate benchmarking, market research, software tool evaluations                      |
| `project-support-agent`          | Governance & Risk     | Manages project documentation, timesheet compliance collection, administrative logs                      |
| `tufte-dashboard-designer`       | Financial Control     | Applies Edward Tufte's Data-Ink Ratio principles to UI components                                        |

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.9+**
- **PowerShell 5+** (for the orchestrator script)

### 2. Installation

Install the required Python dependencies:

```bash
pip install streamlit duckdb pandas plotly openpyxl
```

### 3. Initialization & Execution

You can run the entire workspace using the **PowerShell Master Orchestrator**:

```powershell
.\run_all.ps1
```

This launches an interactive menu with 10 options:

| Option  | Action                                |
| :------ | :------------------------------------ |
| **[1]** | Build Databases (DuckDB & SQLite)     |
| **[2]** | Run EVM Data Verification check       |
| **[3]** | Print Tufte CLI Performance Dashboard |
| **[4]** | Run Excel Reports Agent               |
| **[5]** | Compile Power BI Project (.pbip)      |
| **[6]** | Run Agentic Control Crew Audits       |
| **[7]** | Run Executive Board Report Exporter   |
| **[8]** | Start Interactive Streamlit Dashboard |
| **[9]** | Run Full Pipeline (1–7 in sequence)   |
| **[10]**| Exit                                  |

_Alternatively, you can run individual components manually:_

#### Build Databases

```bash
python AI_Controller/build_duckdb.py
python AI_Controller/build_sqlite.py
```

#### Verify Data Integrity

```bash
python AI_Controller/verify_dataset.py
```

#### Launch Streamlit Web App

```bash
streamlit run AI_Controller/agent_skills_app.py
```

#### Run Agent Audits (CLI)

```bash
python AI_Controller/run_agents.py
```

#### Generate Excel Report

```bash
python AI_Controller/excel_report_agent.py
```

#### Compile Power BI Project

```bash
python AI_Controller/build_pbi_project.py
```

#### View CLI Dashboard

```bash
python AI_Controller/tufte_cli_dashboard.py
```

---

## 🎨 Tufte Visual Design Standards

This workspace applies Edward Tufte's principles of visual clarity across all interfaces:

- **Muted Colors**: Colors are reserved for warning and error states. Slate (`#2c3e50`) is used for on-track metrics, while Crimson (`#e74c3c`) calls out cost overruns (CPI < 0.95).
- **Maximize Data-Ink**: Background drop shadows, heavy table borders, and decorative icons have been eliminated.
- **Direct Labeling**: Gantt chart bars display completion percentages directly to avoid legend noise.
- **Alignment**: Numbers are right-aligned, text is left-aligned, and decimals are vertically aligned in all summary tables.
- **Zero Vertical Gridlines**: All Plotly charts remove vertical gridlines per Tufte's data-ink ratio directive.

See [`AI_Controller/tufte_pm_visual_guide.md`](AI_Controller/tufte_pm_visual_guide.md) for the full visual design guide.

---

## 📊 Data Model

The project uses a relational schema with 8 core tables. See [`AI_Controller/datamodel_erd.md`](AI_Controller/datamodel_erd.md) for the full ERD.

### Core Tables

| Table                  | Description                                                                |
| :--------------------- | :------------------------------------------------------------------------- |
| `projects`             | Project header (ID, name, manager, BAC, dates, status)                     |
| `wbs_elements`         | Work Breakdown Structure elements (WBS_ID, code, name, planned cost/hours) |
| `resources`            | Resource registry (ID, name, role, hourly rate)                            |
| `resource_assignments` | Resource-to-WBS allocation mapping                                         |
| `timesheets`           | Daily labor hour logs (resource, WBS, date, hours, approval)               |
| `material_costs`       | Purchase invoices (WBS, date, description, quantity, unit price, total)    |
| `physical_progress`    | Weekly physical completion % per WBS element                               |
| `raid_log`             | Risks, Assumptions, Issues, Dependencies register                          |

### EVM Views (DuckDB & SQLite)

| View                     | Description                                               |
| :----------------------- | :-------------------------------------------------------- |
| `v_wbs_latest_progress`  | Latest physical progress % per WBS element                |
| `v_wbs_labor_actuals`    | Aggregated labor cost and hours per WBS                   |
| `v_wbs_material_actuals` | Aggregated material cost per WBS                          |
| `v_wbs_evm_metrics`      | Master EVM metrics per WBS (BAC, AC, EV, CPI, CV, EAC, %) |
| `v_project_evm_summary`  | Project-level rollup of all EVM metrics                   |

### EVM Formulas

| Metric             | Formula                  | Description                                      |
| :----------------- | :----------------------- | :----------------------------------------------- |
| **BAC**            | Baseline Budget          | Total authorized budget for the project          |
| **PV**             | BCWS                     | Budgeted cost of work scheduled                  |
| **EV**             | BCWP = BAC × % Complete  | Budgeted cost of work performed                  |
| **AC**             | ACWP = Labor + Materials | Actual cost of work performed                    |
| **CPI**            | EV / AC                  | Cost performance index (< 1.0 = overrun)         |
| **SPI**            | EV / PV                  | Schedule performance index (< 1.0 = delay)       |
| **CV**             | EV − AC                  | Cost variance                                    |
| **EAC (Typical)**  | BAC / CPI                | Forecast assuming current cost trends persist    |
| **EAC (Atypical)** | AC + (BAC − EV)          | Forecast assuming remaining work at planned rate |
| **VAC**            | BAC − EAC                | Variance at completion                           |
| **TCPI**           | (BAC − EV) / (BAC − AC)  | To-complete performance index                    |

---

## 📚 Documentation Index

| Document                                                                                                             | Description                                                       |
| :------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| [`README.md`](README.md)                                                                                             | This file — project overview & quick start                        |
| [`USER_GUIDE.md`](USER_GUIDE.md)                                                                                     | Master workspace user guide (orchestrator menu, script reference) |
| [`AI_Controller/STREAMLIT_APP_README.md`](AI_Controller/STREAMLIT_APP_README.md)                                     | Streamlit app technical architecture & setup                      |
| [`AI_Controller/STREAMLIT_USER_GUIDE.md`](AI_Controller/STREAMLIT_USER_GUIDE.md)                                     | Streamlit app end-user navigation guide                           |
| [`AI_Controller/tufte_pm_visual_guide.md`](AI_Controller/tufte_pm_visual_guide.md)                                   | Edward Tufte data-ink design principles for PM visuals            |
| [`AI_Controller/datamodel_erd.md`](AI_Controller/datamodel_erd.md)                                                   | Database ERD & relational integrity rules                         |
| [`AI_Controller/bi_datamodel_and_dax.md`](AI_Controller/bi_datamodel_and_dax.md)                                     | Power BI star schema, DAX measures, and visual layout             |
| [`AI_Controller/reporting_workflow.md`](AI_Controller/reporting_workflow.md)                                         | End-to-end data pipeline (ingestion → reporting)                  |
| [`AI_Controller/project_controller.md`](AI_Controller/project_controller.md)                                         | Agent architecture & EVM terminology glossary                     |
| [`AI_Controller/project financial controller agents.md`](AI_Controller/project%20financial%20controller%20agents.md) | Agent skill definitions & multi-agent collaboration patterns      |
| [`AI_Controller/my_toolstack.md`](AI_Controller/my_toolstack.md)                                                     | AI research tool stack reference                                  |
| [`AI_Controller/tools plus.md`](AI_Controller/tools%20plus.md)                                                       | Tool ecosystem mapping & upgrade path                             |
| [`Data/PRJ-001_Project_Initiation_Document.md`](Data/PRJ-001_Project_Initiation_Document.md)                         | PRINCE2 Project Initiation Document (PID)                         |

---

## 📂 Data Directory Structure

All data files are located in the [`Data/`](Data) folder:

- **[CSV/](Data/CSV)**: Contains the 8 relational source files (timesheets, materials, WBS, resources, etc.)
- **[DuckDB/](Data/DuckDB)**: Holds the analytical DuckDB instance (`project_controlling.db`)
- **[SQLite/](Data/SQLite)**: Holds the transactional SQLite instance (`project_controlling.db`)
- **[PowerBI_Project/](Data/PowerBI_Project)**: Compiled Power BI `.pbip` developer project
- **[excel_friendly/](Data/CSV/excel_friendly)**: Excel-friendly flat files (semicolon-delimited, European decimal format)

---

## 🔄 Data Pipeline

The workspace follows a local-first, deterministic data pipeline:

```
1. Data Sources (CSV) → 2. Database Build (DuckDB + SQLite) → 3. Verification
         ↓
4. EVM Views (SQL) → 5. Agent Audits (Python) → 6. Excel Reports (OpenPyXL)
         ↓
7. Power BI Project (.pbip) → 8. Streamlit Dashboard (Web UI)
```

The **PowerShell Master Orchestrator** (`run_all.ps1`) can execute the full pipeline (steps 1–6) in sequence via menu option **[8]**.

---

## 📜 License & Attribution

This is a personal project management workspace. All data is simulated/mock data for demonstration purposes. The project adheres to:

- **AACE International Practice Standard 10S-90** (EVM)
- **PMI Practice Standard for Earned Value Management**
- **PRINCE2** project management methodology
- **Edward Tufte's Data-Ink Ratio** principles for visual design
- **Chris Croft's** critical path scheduling methodology
