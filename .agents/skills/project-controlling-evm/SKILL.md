---
name: project-controlling-evm
description: Load and analyze project control CSV datasets (timesheets, costs, progress) to compute EVM metrics and detect schedule/budget variances.
---

# Skill: Project Controlling & EVM Analyst

This skill guides the agent in querying, calculating, and explaining Earned Value Management (EVM) metrics using the workspace project data.

## When to Use
Activate this skill when:
* Asked to run financial reviews or audit project files.
* Calculating Planned Value (PV), Earned Value (EV), Actual Cost (AC), or forecasting metrics (EAC, ETC, VAC).
* Generating timesheet anomaly reports or looking for resource/task overruns.

## How to Use

### 1. Data Source Mapping
The relational data tables are located under [AI_Controller/mock_data/](file:///c:/Users/frank/Desktop/Project%20Mng/AI_Controller/mock_data). Use the following tables:
* `projects.csv`: General project settings.
* `wbs_elements.csv`: Planned budgets (`PlannedCost`) and hours (`PlannedHours`) per task.
* `resources.csv`: Resource standard rates (`HourlyRate`).
* `timesheets.csv`: Daily logged hours per employee and WBS.
* `material_costs.csv`: Invoiced purchases per WBS.
* `physical_progress.csv`: Weekly percent complete reports per WBS.

### 2. Math & Business Logic
* **Actual Cost (AC)**: `SUM(Timesheets.HoursWorked * Resources.HourlyRate) + SUM(Material_Costs.TotalActualCost)` grouped by WBS.
* **Earned Value (EV)**: `WBS_Elements.PlannedCost * Latest_Physical_Progress.PercentComplete` (always find the progress entry with the maximum `RecordDate` relative to the reporting date).
* **Cost Performance Index (CPI)**: `EV / AC`. If `CPI < 0.95`, flag a cost overrun.
* **Schedule Performance Index (SPI)**: `EV / PV`. If `SPI < 0.90`, flag a schedule lag.

### 3. Output Requirements
* Write queries and calculations using clean, dependency-free Python or DuckDB SQL.
* Format financial numbers using thousands separators (e.g. `100,000.00 NOK`).
* Present reports containing the WBS, Element Name, BAC, AC, EV, CPI, and Status.
