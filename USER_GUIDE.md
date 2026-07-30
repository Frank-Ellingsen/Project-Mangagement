# Project Controlling Workspace User Guide

Welcome to your automated Project Controlling Workspace. This repository is customized for financial controllers to manage costs, schedules, variances, and forecasts using DuckDB, SQLite, and Python, while adhering to Edward Tufte's data-ink ratio principles and Chris Croft's critical path scheduling.

---

## 🚀 The "Push Button" Orchestrator

The easiest way to work with this workspace is via the master orchestrator script: **[run_all.ps1](file:///c:/Users/frank/Desktop/Project%20Mng/run_all.ps1)**.

To launch the menu, open a PowerShell terminal in the workspace folder and run:
```powershell
./run_all.ps1
```

### Menu Options
1. **Build Databases (DuckDB & SQLite)**: Loads the raw CSVs into DuckDB and SQLite and sets up the EVM Views.
2. **Run EVM Data Verification check**: Performs consistency checks across memory joins and SQL view databases.
3. **Print Tufte CLI Performance Dashboard**: Outputs a clean, borderless ASCII EVM dashboard to your console.
4. **Run Excel Reports Agent**: Generates the interactive, formula-driven [vessel_construction_report.xlsx](file:///c:/Users/frank/Desktop/Project%20Mng/Data/vessel_construction_report.xlsx).
5. **Compile Power BI Project (.pbip)**: Compiles the [Vessel_Performance.pbip](file:///c:/Users/frank/Desktop/Project%20Mng/Data/PowerBI_Project/Vessel_Performance.pbip) developer structure.
6. **Run Agentic Control Crew Audits**: Runs audit routines for all 4 agents.
7. **Start Interactive Streamlit Dashboard**: Launches the local Streamlit visual web dashboard.
8. **Run Pipeline (1 to 6 in sequence)**: Compiles databases, verifies data, displays CLI statistics, writes Excel workbooks, compiles PBI projects, and runs agent audits in a single sweep.

---

## 📂 Data Directory Structure

All data files are located in the [Data/](file:///c:/Users/frank/Desktop/Project%20Mng/Data) folder:
* **[CSV/](file:///c:/Users/frank/Desktop/Project%20Mng/Data/CSV)**: Contains the relational source files (`timesheets.csv`, `material_costs.csv`, etc.).
* **[DuckDB/](file:///c:/Users/frank/Desktop/Project%20Mng/Data/DuckDB)**: Holds the analytical data engine database (`project_controlling.db`).
* **[SQLite/](file:///c:/Users/frank/Desktop/Project%20Mng/Data/SQLite)**: Holds the transactional audit database (`project_controlling.db`).

---

## 🛠️ Individual Script Reference

If you prefer to run files individually from the command line:

### 1. Rebuild Databases
```powershell
python AI_Controller/build_duckdb.py
python AI_Controller/build_sqlite.py
```

### 2. Verify Data
```powershell
python AI_Controller/verify_dataset.py
```

### 3. CLI Dashboard
```powershell
python AI_Controller/tufte_cli_dashboard.py
```

### 4. Excel Reports Agent
```powershell
python AI_Controller/excel_report_agent.py
```
*Generates:* [vessel_construction_report.xlsx](file:///c:/Users/frank/Desktop/Project%20Mng/Data/vessel_construction_report.xlsx)

### 5. Compile Power BI Project (.pbip)
```powershell
python AI_Controller/build_pbi_project.py
```
*Generates:* [Vessel_Performance.pbip](file:///c:/Users/frank/Desktop/Project%20Mng/Data/PowerBI_Project/Vessel_Performance.pbip)

### 6. Run Agent Audits
```powershell
python AI_Controller/run_agents.py
```

### 7. Run Agent Control Tower Streamlit App
```powershell
streamlit run AI_Controller/agent_skills_app.py
```
*For detailed app documentation, see:*
* **[STREAMLIT_APP_README.md](file:///c:/Users/frank/Desktop/Project%20Mng/AI_Controller/STREAMLIT_APP_README.md)** (Technical Architecture & Setup)
* **[STREAMLIT_USER_GUIDE.md](file:///c:/Users/frank/Desktop/Project%20Mng/AI_Controller/STREAMLIT_USER_GUIDE.md)** (End-User Feature Walkthrough)
