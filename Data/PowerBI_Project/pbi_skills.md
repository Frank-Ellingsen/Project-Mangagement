# Power BI Project Management — Skill & Best-Practice Guide

## 1. Purpose
A Power BI project management report provides a single source of truth for tasks, milestones, risks, costs, dependencies, and delivery readiness. This guide outlines the standard semantic model, essential DAX measures, and visual design rules required to build clean, minimalist, and high-performance project control dashboards.

---

## 2. Core Data Model (Workspace Schema)

The semantic model is built using the following relational tables and fields, sourced from CSV/database flat files:

### 2.1 projects
* **ProjectID** (Key): Unique identifier for the project.
* **ProjectName**: Name of the vessel or construction project (e.g., vessel construction, engineering design).
* **ProjectManager**: PM responsible for delivery.
* **BudgetAtCompletion_BAC**: Total baseline budget for the project.
* **StartDate** / **EndDate**: Planned/baseline duration dates.
* **Status**: Overall lifecycle state (e.g., Active, Completed, On Hold).

### 2.2 wbs_elements
* **WBS_ID** (Key): Unique work breakdown structure identifier.
* **ProjectID** (FK): Links to `projects`.
* **WBS_Code**: Hierarchical code (e.g., `1.1`, `1.2.1`).
* **ElementName**: Descriptive name of the work package (e.g., Hull Fabrication, Outfitting).
* **PlannedCost**: Baseline cost allocated to this element.
* **PlannedHours**: Baseline labor hours allocated to this element.

### 2.3 resources
* **ResourceID** (Key): Unique identifier for personnel.
* **ResourceName**: Name of the engineer, technician, or contractor.
* **Role**: Engineering/shipyard role.
* **HourlyRate**: Standard cost rate per hour.

### 2.4 timesheets
* **TimesheetID** (Key): Unique timesheet log identifier.
* **ResourceID** (FK): Links to `resources`.
* **WBS_ID** (FK): Links to `wbs_elements`.
* **WorkDate**: Date labor was performed.
* **HoursWorked**: Standard/overtime decimal hours.
* **ApprovalStatus**: Timesheet workflow state (e.g., Approved, Pending).
* **LaborCost**: Calculated column (`[HoursWorked] * [HourlyRate]`).

### 2.5 material_costs
* **PurchaseID** (Key): Procurement log identifier.
* **WBS_ID** (FK): Links to `wbs_elements`.
* **PurchaseDate**: Date materials were ordered/received.
* **Description**: Item description.
* **Quantity**: Number of units.
* **UnitPrice**: Individual unit cost.
* **TotalActualCost**: Actual procurement cost.

### 2.6 physical_progress
* **ProgressID** (Key): Progress entry identifier.
* **WBS_ID** (FK): Links to `wbs_elements`.
* **RecordDate**: Reporting cutoff date.
* **PercentComplete**: Physical progress percentage (0.00 to 1.00).
* **ReportedBy**: Reviewer/Controller confirming the status.

### 2.7 ScenarioSelection
* **Scenario**: Disconnected parameter table for sensitivity modeling containing:
  * `Conservative`
  * `Baseline`
  * `Aggressive`

---

## 3. Essential DAX Measures

### 3.1 Base Cost & Budget Measures
```DAX
BAC = SUM('wbs_elements'[PlannedCost])
```
```DAX
Actual Labor Cost = SUM('timesheets'[LaborCost])
```
```DAX
Actual Material Cost = SUM('material_costs'[TotalActualCost])
```
```DAX
AC = [Actual Labor Cost] + [Actual Material Cost]
```

### 3.2 Earned Value & Progress Measures
```DAX
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
```
```DAX
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
```
```DAX
EV = SUMX(VALUES('wbs_elements'[WBS_ID]), [BAC] * [Latest Percent Complete])
```
```DAX
PV = [BAC] * [Planned % Complete]
```

### 3.3 Variance & Performance Indexes
```DAX
SV = [EV] - [PV]
```
```DAX
CV = [EV] - [AC]
```
```DAX
CPI = DIVIDE([EV], [AC], 1.0)
```
```DAX
SPI = DIVIDE([EV], [PV], 1.0)
```

### 3.4 Forecasting (EAC / ETC / VAC)
```DAX
EAC (Typical) = DIVIDE([BAC], [CPI], [BAC])
```
```DAX
EAC (Atypical) = [AC] + ([BAC] - [EV])
```
```DAX
ETC (Estimate to Complete) = [EAC (Typical)] - [AC]
```
```DAX
VAC (Variance at Completion) = [BAC] - [EAC (Typical)]
```

### 3.5 Dynamic Scenario-Based RAG Logic
Determines project status dynamically based on risk tolerance settings chosen in the `ScenarioSelection` slicer:
```DAX
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

---

## 4. Visual Design Standards (Tufte Principles)

All visual elements must adhere strictly to Edward Tufte's **Data-Ink Ratio** principles to maximize clarity and minimize cognitive load:

### 4.1 Tables & Matrices
* **Gridlines**: Remove vertical gridlines. Use subtle horizontal dividers only.
* **Alignment**:
  * Text/Name columns: **Left-align**
  * Numeric/Financial columns: **Right-align**
  * Decimals: Vertically aligned.
* **Spacing**: Compact padding to increase density without sacrificing legibility.

### 4.2 KPI Cards
* **Borders & Shadows**: Delete all background drop shadows and heavy borders.
* **Icons**: Avoid decorative, non-functional icons. Let the metric and its threshold color communicate state.
* **Sizing**: Use clean, large typographic callouts with small descriptive labels.

### 4.3 S-Curves & Line Charts
* **Legends**: Avoid separate color legends. Use direct annotations/labels placed next to the lines (`PV`, `EV`, `AC`) to reduce visual scanning.
* **Muted Aesthetics**: Use soft, neutral tones (slate, gray) for the background grid lines and non-critical data.
* **Highlights**: Reserve bright colors (like Red or Amber) exclusively to flag variance anomalies or critical risks.

### 4.4 Gantt Charts
* **Visual Clutter**: Hide complex grid patterns and decorative timeline bars.
* **Direct Labeling**: Label phases and milestones directly on the timeline elements.

---

## 5. Report Layout Standard

A consistent 3-page configuration targets specific organizational roles:

### 5.1 Executive Overview
* **Target**: Project Board / PMO Directors.
* **Focus**: High-level portfolio tracking, milestones, and delivery readiness.
* **Visuals**: BAC/AC/EV KPI cards, overall progress bars, and high-level project status breakdowns.

### 5.2 Financial Control
* **Target**: Project Controller / CFO.
* **Focus**: Detailed EVM performance, forecasting, and scenario sensitivity.
* **Visuals**: Cumulative S-curve (PV vs. EV vs. AC), Cost & Schedule Variance cards, and a dynamic Scenario Selector slicer.

### 5.3 Client Delivery
* **Target**: Project Engineering Lead / Shipbuilding Manager.
* **Focus**: Work package status, timesheet tracking, and milestone completion.
* **Visuals**: WBS delivery tables, resources utilization matrix, and delivery narrative.
