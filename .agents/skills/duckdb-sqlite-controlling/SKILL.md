---
name: duckdb-sqlite-controlling
description: Query, update, and manage local-first DuckDB and SQLite databases for project controlling data analysis.
---

# Skill: Local Database Controlling (DuckDB & SQLite)

This skill guides the agent in querying, managing, and updating the local-first database engines used in this project controlling workspace: **DuckDB** for analytical workloads (views, roll-ups, EVM) and **SQLite** for transactional/lookup workloads (timesheets, resource records, RAID logs).

## When to Use
Activate this skill when:
* Asked to extract, query, or check database records in SQLite or DuckDB.
* Writing SQL queries for analytical views or reports.
* Updating relational records (timesheets, WBS entries, progress reports).
* Re-compiling or building the local databases from CSV files.

## 1. Database Connections & Paths
The databases are stored under the [Data/](file:///c:/Users/frank/Desktop/Project%20Mng/Data) folder:
* **DuckDB (Analytical)**: Connect to the database at `c:\Users\frank\Desktop\Project Mng\Data\DuckDB\project_controlling.db` using:
  ```python
  import duckdb
  con = duckdb.connect(r"c:\Users\frank\Desktop\Project Mng\Data\DuckDB\project_controlling.db")
  ```
* **SQLite (Transactional)**: Connect to the database at `c:\Users\frank\Desktop\Project Mng\Data\SQLite\project_controlling.db` using:
  ```python
  import sqlite3
  conn = sqlite3.connect(r"c:\Users\frank\Desktop\Project Mng\Data\SQLite\project_controlling.db")
  ```

## 2. Integrated EVM Database Schema
Both databases share the same analytical view layer, compiled dynamically from the CSV files. Utilize these views for querying:
* `v_wbs_latest_progress`: Filters `physical_progress` to return only the latest cumulative progress percentage per WBS element.
* `v_wbs_labor_actuals`: Joins `timesheets` and `resources` to calculate cumulative actual labor hours worked and labor cost per WBS element.
* `v_wbs_material_actuals`: Aggregates material invoices from `material_costs` per WBS element.
* `v_wbs_evm_metrics`: Connects WBS elements with actuals and progress to calculate BAC, AC, EV, CV, CPI, and Forecasted EAC (Typical & Atypical).
* `v_project_evm_summary`: Rolls up all metrics to the portfolio/project level, providing Total BAC, AC, EV, CV, Project CPI, EAC Typical, VAC, and Overall progress %.

## 3. Query Guidelines & SQL Examples

### 3.1 Fetching Project EVM Summary (DuckDB)
```sql
SELECT 
    Total_BAC, 
    Total_AC, 
    Total_EV, 
    Total_CV, 
    Project_CPI, 
    Total_EAC_Typical, 
    Total_VAC, 
    Overall_Progress_Pct 
FROM v_project_evm_summary;
```

### 3.2 Finding Overrun Activities (SQLite / DuckDB)
```sql
SELECT 
    WBS_Code, 
    ElementName, 
    BAC, 
    AC, 
    EV, 
    CV, 
    CPI, 
    EAC_Typical
FROM v_wbs_evm_metrics
WHERE CV < 0
ORDER BY CV ASC;
```

### 3.3 Listing Timesheet Errors or Non-Approved Logged Hours
```sql
SELECT 
    t.TimesheetID, 
    r.ResourceName, 
    t.WorkDate, 
    t.HoursWorked, 
    t.ApprovalStatus
FROM timesheets t
JOIN resources r ON t.ResourceID = r.ResourceID
WHERE t.ApprovalStatus != 'Approved'
ORDER BY t.WorkDate DESC;
```

## 4. Re-building / Refreshing the Databases
When transactional CSV files are modified (e.g. timesheets or progress logs), rebuild the database files to synchronize them:
* **DuckDB Rebuild**:
  ```powershell
  python AI_Controller/build_duckdb.py
  ```
* **SQLite Rebuild**:
  ```powershell
  python AI_Controller/build_sqlite.py
  ```
Always run these scripts after updating CSV mock data or receiving new transaction records in the workspace.
