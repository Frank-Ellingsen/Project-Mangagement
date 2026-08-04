---
name: power-bi-project-controlling
description: Build and update Power BI project controlling dashboards (.pbip / TMDL) using custom DAX measures, scenario parameters, and Tufte visual standards.
---

# Skill: Power BI Project Controlling Dashboard Builder

This skill guides the agent in building, updating, and maintaining Power BI project controlling reports in PBIP (Power BI Project) format, writing clean DAX measures, managing scenario parameters, and applying Edward Tufte's Data-Ink Ratio visual design rules.

## When to Use
Activate this skill when:
* Asked to design, build, or update Power BI reports or semantic models for project controlling.
* Editing TMDL (Tabular Model Definition Language) files, report layouts, or PBIP project structures.
* Writing or troubleshooting DAX measures (especially EVM metrics, calendar-based snap-shots, or scenario-based status triggers).
* Formatting Power BI tables, KPI cards, S-curve line charts, or timeline gantt visuals.
* Version-controlling Power BI reports or using Python build scripts like `build_pbi_project.py`.

## 1. Semantic Model Design
The standard semantic model is built as a Star Schema with the following tables:
* **Dimensions (Dim)**:
  * `projects`: Project details (ProjectID, ProjectName, ProjectManager, BudgetAtCompletion_BAC, StartDate, EndDate, Status).
  * `wbs_elements`: WBS hierarchy (WBS_ID, ProjectID, WBS_Code, ElementName, PlannedCost, PlannedHours).
  * `resources`: Resource pool (ResourceID, ResourceName, Role, HourlyRate).
  * `ScenarioSelection`: Disconnected slicer table containing `Conservative`, `Baseline`, and `Aggressive`.
* **Facts (Fact)**:
  * `timesheets`: Labor transactions (TimesheetID, ResourceID, WBS_ID, WorkDate, HoursWorked, ApprovalStatus, LaborCost).
  * `material_costs`: Material invoices (PurchaseID, WBS_ID, PurchaseDate, Description, Quantity, UnitPrice, TotalActualCost).
  * `physical_progress`: Cumulative weekly physical status (ProgressID, WBS_ID, RecordDate, PercentComplete, ReportedBy).

Relationships:
* Connect all fact date fields (`timesheets[WorkDate]`, `material_costs[PurchaseDate]`, `physical_progress[RecordDate]`) to the calendar/date table.
* Connect WBS IDs to `wbs_elements[WBS_ID]` (1-to-many).
* Connect Resource IDs to `resources[ResourceID]` (1-to-many).

## 2. Essential DAX Measure Layer
Define explicit, optimized measures for all business calculations:

```dax
-- Budget / Cost Base
BAC = SUM('wbs_elements'[PlannedCost])
Actual Labor Cost = SUM('timesheets'[LaborCost])
Actual Material Cost = SUM('material_costs'[TotalActualCost])
AC = [Actual Labor Cost] + [Actual Material Cost]

-- Physical Progress & S-Curve Dates
Latest Percent Complete = 
VAR SelectedDate = MAX('physical_progress'[RecordDate])
RETURN
SUMX(
    VALUES('wbs_elements'[WBS_ID]),
    VAR LatestWBSProgressDate = 
        CALCULATE(
            MAX('physical_progress'[RecordDate]), 
            'physical_progress'[RecordDate] <= SelectedDate
        )
    RETURN 
        CALCULATE(
            MAX('physical_progress'[PercentComplete]), 
            'physical_progress'[RecordDate] = LatestWBSProgressDate
        )
)

Planned % Complete = 
VAR StartDate = MIN('projects'[StartDate])
VAR EndDate = MAX('projects'[EndDate])
VAR CurrentDate = MAX('physical_progress'[RecordDate])
RETURN
IF(
    EndDate <= StartDate,
    0,
    DIVIDE(DATEDIFF(StartDate, CurrentDate, DAY), DATEDIFF(StartDate, EndDate, DAY), 0)
)

-- Earned & Planned Values
EV = SUMX(VALUES('wbs_elements'[WBS_ID]), [BAC] * [Latest Percent Complete])
PV = [BAC] * [Planned % Complete]

-- Variances & Performance Index
SV = [EV] - [PV]
CV = [EV] - [AC]
CPI = DIVIDE([EV], [AC], 1.0)
SPI = DIVIDE([EV], [PV], 1.0)

-- EAC Forecasting
EAC (Typical) = DIVIDE([BAC], [CPI], [BAC])
EAC (Atypical) = [AC] + ([BAC] - [EV])
ETC = [EAC (Typical)] - [AC]
VAC = [BAC] - [EAC (Typical)]
```

## 3. Dynamic RAG Status & Scenario Selector
Implement scenario-aware risk thresholds linked to the `ScenarioSelection` parameter table:

```dax
Variance RAG = 
VAR Scenario = SELECTEDVALUE(ScenarioSelection[Scenario], "Baseline")
VAR CostVariancePct = DIVIDE([CV], [BAC], 0)
VAR ScheduleVariancePct = DIVIDE([SV], [BAC], 0)
VAR CostAmberThreshold = SWITCH(Scenario, "Conservative", 0.08, "Baseline", 0.12, "Aggressive", 0.18, 0.12)
VAR CostRedThreshold = SWITCH(Scenario, "Conservative", 0.15, "Baseline", 0.20, "Aggressive", 0.30, 0.20)
VAR ScheduleAmberThreshold = SWITCH(Scenario, "Conservative", 0.05, "Baseline", 0.10, "Aggressive", 0.15, 0.10)
VAR ScheduleRedThreshold = SWITCH(Scenario, "Conservative", 0.10, "Baseline", 0.15, "Aggressive", 0.25, 0.15)
RETURN
SWITCH(
    TRUE(),
    ABS(CostVariancePct) >= CostRedThreshold || ABS(ScheduleVariancePct) >= ScheduleRedThreshold, "Red",
    ABS(CostVariancePct) >= CostAmberThreshold || ABS(ScheduleVariancePct) >= ScheduleAmberThreshold, "Amber",
    "Green"
)
```

## 4. Edward Tufte Visual Layout Standards
Ensure all dashboards maintain a high data-ink ratio:
* **Tables/Matrices**: Remove vertical gridlines. Use thin horizontal borders under headers and totals. Left-align text columns, right-align numeric/decimal columns, and ensure decimal places align vertically.
* **KPI Cards**: Remove borders and drop shadows. Use simple typography for values and small text for labels. No decorative icons.
* **Line Charts / S-Curves**: Direct-label lines (PV, EV, AC) at the end of the curves. Avoid separate legends. Use muted greys for the background gridlines, slate blue for EV, light grey for PV, and black/dark grey for AC. Use Red or Amber exclusively to highlight active variances.
* **Gantt Charts**: Hide complex backgrounds and decorative elements; display clean phase blocks with labels directly on the blocks or milestones.

## 5. Git and PBIP Project Workflow
PBIP (Power BI Project) format stores metadata in text format (TMDL/JSON), enabling full Git tracking:
1. When changes are made, run the Python build script from the workspace root:
   ```powershell
   python AI_Controller/build_pbi_project.py
   ```
2. Open the generated `.pbip` or compiled `.pbix` report locally to inspect changes.
3. Commit modified TMDL and JSON layout configurations to version control to trace measure updates and layout revisions.
