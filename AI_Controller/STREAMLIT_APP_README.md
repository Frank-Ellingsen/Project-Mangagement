# Agent Control Tower Streamlit Application README

## 📌 Overview

The **Agent Control Tower Streamlit Application** (`AI_Controller/agent_skills_app.py`) is an interactive, web-based Business Intelligence dashboard built specifically for **Project Controllers**, **Financial Controllers**, and **Project Managers** managing complex engineering and maritime projects.

The application integrates Earned Value Management (EVM) data from **DuckDB** and transactional audit data from **SQLite**, presenting tailored views across 13 domain-specific **Agent Skills** and 6 **Stakeholder Personas**.

---

## 🛠️ Technology Stack

* **Frontend & Framework**: Python, [Streamlit](https://streamlit.io/)
* **Analytical Engine**: [DuckDB](https://duckdb.org/) (`v_project_evm_summary`, `v_wbs_evm_metrics`)
* **Transactional Engine**: [SQLite](https://sqlite.org/) (`raid_log`, overtime audits, transaction logs)
* **Data Visualization**: [Plotly Express & Graph Objects](https://plotly.com/python/) (Tufte Data-Ink compliant)
* **Data Processing**: Pandas, NumPy

---

## 📂 File Architecture

```
Project Mng/
├── AI_Controller/
│   ├── agent_skills_app.py        # Main Streamlit web application
│   ├── build_duckdb.py            # DuckDB analytical database builder
│   ├── build_sqlite.py            # SQLite audit database builder
│   ├── run_agents.py              # Multi-agent audit routines script
│   ├── STREAMLIT_APP_README.md    # Technical README (this file)
│   └── STREAMLIT_USER_GUIDE.md    # End-user navigation guide
├── Data/
│   ├── DuckDB/project_controlling.db
│   └── SQLite/project_controlling.db
└── run_all.ps1                    # Master launcher script (Option 8)
```

---

## 🎨 Design System: Edward Tufte's Data-Ink Principles

The app strictly adheres to Edward Tufte's visual guidelines to maximize data-ink ratio:
1. **Zero Vertical Gridlines**: Removed vertical lines from all Plotly Gantt charts and timeline figures (`showgrid=False`).
2. **Borderless & Shadowless Metrics**: Clean, unbordered KPI cards with high-contrast typography.
3. **Direct Data Labeling**: Percent complete progress annotations (`97.5%`, `100.0%`) rendered directly on chart bars instead of detached legends.
4. **Muted Palette with Selective Highlights**: Muted slate (`#2c3e50`) for on-track metrics; bright crimson (`#e74c3c`) reserved strictly for active cost/schedule overruns (CPI < 0.95).

---

## 🚀 Installation & Quickstart

### Prerequisites
Ensure Python 3.9+ is installed along with required packages:
```bash
pip install streamlit duckdb pandas plotly
```

### Initializing Databases
Before launching the app, compile the DuckDB and SQLite database backends:
```powershell
python AI_Controller/build_duckdb.py
python AI_Controller/build_sqlite.py
```

### Launching the Web App
From the project root folder, run:
```powershell
streamlit run AI_Controller/agent_skills_app.py
```
*Alternatively, run `./run_all.ps1` and select Option `[8]`.*

---

## 📊 Key Features & Views

1. **Front Page (Agent Control Tower Dashboard)**:
   * **5 KPI Metric Cards**: Budget at Completion (BAC), Actual Cost (AC), Earned Value (EV), Project CPI, Physical Progress.
   * **Interactive Schedule Gantt Chart**: Tufte-style Gantt chart with project context switcher (PRJ-001, PRJ-002, Portfolio view).
   * **4 Domain Tabs**: EVM & Forecasts, CFO & Cost Share, Contract & Risk Audit, Production & Assembly.
2. **Stakeholder Reports**:
   * Tailored briefs for 6 key personas (Executive/CFO, PM, Engineering Lead, Yard Manager, Procurement Lead, Quality Inspector).
3. **Individual Agent Skill Inspector**:
   * Raw skill instruction inspector across all 13 specialized agent `.md` files.
4. **Live Crew Execution Console**:
   * Single-click runner executing live Python audit routines against database engines.

---

## 🔗 Related Documentation
* [STREAMLIT_USER_GUIDE.md](file:///C:/Users/frank/Desktop/Project%20Mng/AI_Controller/STREAMLIT_USER_GUIDE.md) – End-user step-by-step navigation guide.
* [USER_GUIDE.md](file:///C:/Users/frank/Desktop/Project%20Mng/USER_GUIDE.md) – Master workspace operating manual.
