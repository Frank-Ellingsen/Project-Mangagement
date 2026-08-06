# User Guide: Building & Maintaining the Project Controlling Master Template

This user guide describes how to use the automated Python pipeline to rebuild the Master Excel Template, ingest new project datasets, and maintain the application.

---

## 1. Prerequisites

To run the automation pipeline, you must have Python installed along with the `openpyxl` library:

```powershell
pip install openpyxl
```

---

## 2. Rebuilding the Master Template & Test Workbook

A single automation script, `run_project_controlling_pipeline.py`, manages the entire build process.

### How to Run:
Open a terminal in the root folder of the project controlling directory and execute:

```powershell
python run_project_controlling_pipeline.py
```

### What the Script Accomplishes:
1. **Schema Extraction:** Scans `Project_Controlling_App3.xlsx` and exports structural data tables to CSV files.
2. **Template Reset:** Generalizes the tables in the workbook by clearing all project-specific records (actual costs, progress entries, resource rosters, baseline values) and writing clean placeholders. Saves the result as `Master_Project_Controlling_Template.xlsx`.
3. **Mock Data Population:** Generates a new project test dataset (**PRJ999: Shipyard Assembly Beta**) and populates the master template tables.
4. **Visual Enhancements:**
   * **Gantt Charts:** Applies conditional formatting rules to highlight the status date column (red dotted borders + light red background) and milestone cells (gold fill + border).
   * **S-Curve Chart:** Adds Cost Variance (CV) and Schedule Variance (SV) columns to the helper data table, maps them onto the Line Chart, and enables numeric data labels.
   * **RAG Columns:** Applies conditional formatting (Red/Amber/Green) to the status cards on the dashboard based on CPI thresholds.
5. **Output Generation:** Saves the fully populated and formatted test sheet as `Test_Master_Mock_Populated_Final.xlsx`.

---

## 3. Populating the Template for a New Project

To load a new actual project instead of mock data:

### Step 1: Prepare Your Project CSV Files
Place your files in the `mock_data_test/` folder with these exact filenames and table layouts:
* `tbl_Dim_Project.csv`: Project metadata (ID, Name, Start, End, BAC, Sector).
* `tbl_Dim_WBS.csv`: Work Breakdown Structure elements and baseline budgets.
* `tbl_Dim_Resource.csv`: Standard roster names, roles, and hourly rates.
* `tbl_Fact_Baseline_PV.csv`: Planned value weekly allocations.
* `tbl_Fact_Actual_Costs.csv`: Daily actual hour and cost transactions.
* `tbl_Fact_Physical_Progress.csv`: Periodic physical percent complete snapshot records.
* `tbl_Task_Plan.csv`: Activity start/end schedule dates and resource assignments.
* `tbl_Task_Capture.csv`: Timesheet actual records.
* `tbl_Review_ActionLog.csv` & `tbl_PID_RiskControl.csv`: Audit and risk logs.

### Step 2: Run the Pipeline
Execute the build command:
```powershell
python run_project_controlling_pipeline.py
```

### Step 3: Refresh Excel Data Models
Once you open `Test_Master_Mock_Populated_Final.xlsx` in Microsoft Excel:
1. Go to the **Data** tab on the ribbon.
2. Click **Refresh All** to update the Power Pivot data models and reload the dashboards.
