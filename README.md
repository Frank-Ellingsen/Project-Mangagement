# Project Controlling Control Tower

An automated, interactive **Project Controlling & Earned Value Management (EVM) Control Tower** designed for engineering, maritime, and defense sector projects. This workspace integrates analytical data processing, automated auditing, Excel reporting, and a Streamlit dashboard.

The application adheres strictly to **Edward Tufte's Data-Ink Ratio** principles and features automated agentic audit routines to track variances, forecasts, and schedule risks.

---

## 🏗️ System Architecture

The workspace is structured into a database layer, a CLI automation layer, and a web dashboard layer:

```
Project Mng/
├── AI_Controller/
│   ├── agent_skills_app.py        # Streamlit Web Application (Control Tower)
│   ├── build_duckdb.py            # DuckDB database builder (Analytical Layer)
│   ├── build_sqlite.py            # SQLite database builder (Transactional Layer)
│   ├── run_agents.py              # Multi-agent audit routines script
│   ├── excel_report_agent.py      # Automated Excel workbook report writer
│   ├── build_pbi_project.py       # Power BI Developer project compiler (.pbip)
│   ├── verify_dataset.py          # Data validation check
│   ├── tufte_cli_dashboard.py     # Terminal-based dashboard (Tufte-compliant)
│   ├── STREAMLIT_APP_README.md    # Streamlit tech stack README
│   └── STREAMLIT_USER_GUIDE.md    # Streamlit end-user usage guide
├── Data/
│   ├── CSV/                       # Raw source data (timesheets, materials, etc.)
│   ├── DuckDB/                    # Analytical DuckDB instance
│   └── SQLite/                    # Transactional SQLite instance
├── .agents/                       # Custom agent skill instruction folders
├── run_all.ps1                    # Powershell Master Orchestrator script
└── USER_GUIDE.md                  # Master Workspace Guide
```

---

## 🛠️ Tech Stack & Core Decisions

1. **Analytical Database (DuckDB)**:
   * Powering high-speed aggregations and analytical views for Earned Value Management (EVM) metrics.
   * Compiles views for `v_project_evm_summary` and `v_wbs_evm_metrics`.
2. **Transactional Database (SQLite)**:
   * Powering transactional tables such as the project `raid_log`, overtime thresholds, and log audit trails.
3. **Frontend (Streamlit & Plotly)**:
   * Provides a clean, modern web interface.
   * Uses **Plotly Express** to render schedule Gantt charts with a high data-ink ratio (e.g., zero vertical gridlines, progress displayed directly on bars, and semantic red/green highlighting for cost overruns).
4. **Excel Reports Agent (OpenPyXL)**:
   * Automatically generates advanced, formula-driven spreadsheets (`vessel_construction_report.xlsx`) to support offline analysis.

---

## 🚀 Getting Started

### 1. Installation
Install the required Python dependencies:
```bash
pip install streamlit duckdb pandas plotly openpyxl
```

### 2. Initialization & Execution
You can run the entire workspace using the **Powershell Master Orchestrator**:
```powershell
./run_all.ps1
```
*Alternatively, you can run individual parts manually:*

* **Build Databases**:
  ```bash
  python AI_Controller/build_duckdb.py
  python AI_Controller/build_sqlite.py
  ```
* **Verify Integrity**:
  ```bash
  python AI_Controller/verify_dataset.py
  ```
* **Launch Streamlit Web App**:
  ```bash
  streamlit run AI_Controller/agent_skills_app.py
  ```

---

## 🎨 Tufte Visual Design Standards
This workspace applies Edward Tufte's principles of visual clarity:
* **Muted Colors**: Colors are reserved for warning and error states. Slate (`#2c3e50`) is used for on-track metrics, while Crimson (`#e74c3c`) calls out cost overruns (CPI < 0.95).
* **Maximize Data-Ink**: Background drop shadows, heavy table borders, and decorative icons have been eliminated.
* **Direct Labeling**: Gantt chart bars display completion percentages directly to avoid legend noise.
* **Alignment**: Numbers are right-aligned, text is left-aligned, and decimals are vertically aligned in all summary tables.
