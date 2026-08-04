---
name: excel-project-controlling
description: Guide the creation and update of Excel-based project controlling dashboards using Power Query, Power Pivot, Star Schema models, and Tufte-compliant formatting.
---

# Skill: Excel Project Controlling App Builder

This skill guides the agent in building, updating, and explaining Excel-based project controlling applications using Power Query (ETL), Power Pivot (data modeling/DAX), and Edward Tufte's Data-Ink Ratio formatting principles.

## When to Use
Activate this skill when:
* Asked to design or update Excel sheets, databases, or reports for project controlling.
* Designing Power Query import steps or mapping relational database files (CSV/SQL) into a Star Schema.
* Writing DAX measures for an Excel Data Model (Power Pivot).
* Formatting tables, charts, S-curves, or dashboards inside MS Excel.

## 1. Data Source Mapping (Star Schema)
Data tables are stored in the Excel App directory: [PM teori/Excel App/CSV/](file:///c:/Users/frank/Desktop/Project%20Mng/PM%20teori/Excel%20App/CSV). Define and maintain the following relationships:

* **Dimension Tables (Dim)**:
  * `Dim_Project.csv`: Project metadata (Project_ID, Project_Name, Start_Date, End_Date, BAC, Sector).
  * `Dim_WBS.csv`: Work Breakdown Structure task details (WBS_ID, WBS_Code, Activity_Name, Type, Total_Budget).
  * `Dim_Resource.csv`: Project team members and equipment (Resource_ID, Resource_Name, Role, Hourly_Rate).
  * `Dim_Calendar.csv`: Daily date table spanning the project duration (Date, Year, Month, Month_Name, Quarter, Week_Number, Is_Weekday).

* **Fact Tables (Fact)**:
  * `Fact_Baseline_PV.csv`: Planned value weekly allocations (Date, WBS_ID, Planned_Value). Connects to `Dim_Calendar[Date]` (1-to-many) and `Dim_WBS[WBS_ID]` (1-to-many).
  * `Fact_Actual_Costs.csv`: Daily transaction logs (Date, WBS_ID, Resource_ID, Actual_Cost, Hours_Worked). Connects to `Dim_Calendar[Date]`, `Dim_WBS[WBS_ID]`, and `Dim_Resource[Resource_ID]`.
  * `Fact_Physical_Progress.csv`: Periodic (weekly) progress updates (Date, WBS_ID, Physical_Progress_Pct). Connects to `Dim_Calendar[Date]` and `Dim_WBS[WBS_ID]`.

## 2. Power Query (ETL) Guidelines
When instructing on Power Query steps, recommend:
1. **Set Data Types Explicitly**: Date columns as `Date`, numeric currencies as `Decimal Number` or `Currency`, WBS/Resource/Project IDs as `Text`.
2. **Handle Nulls**: Replace nulls in numeric fact columns (`Planned_Value`, `Actual_Cost`, `Hours_Worked`) with `0` to avoid calculation errors in DAX.
3. **Disable Load for Staging Queries**: Only load final Star Schema dimensions and facts to the Data Model (uncheck "Enable Load to Worksheet" but keep "Add this data to the Data Model" checked).

## 3. Power Pivot (DAX Measures)
Implement the following explicit DAX measures in the Power Pivot Data Model:

```dax
-- Budget at Completion (BAC)
[BAC] := SUM(Dim_WBS[Total_Budget])

-- Planned Value (PV)
[Total PV] := SUM(Fact_Baseline_PV[Planned_Value])

-- Actual Cost (AC)
[Total AC] := SUM(Fact_Actual_Costs[Actual_Cost])

-- Total Hours
[Total Hours] := SUM(Fact_Actual_Costs[Hours_Worked])

-- Latest Physical Progress Percent (Semi-additive Snapshot)
[Latest_Physical_Progress_Pct] := 
VAR SelectedDate = MAX(Dim_Calendar[Date])
VAR LastReportedDate = 
    CALCULATE(
        MAX(Fact_Physical_Progress[Date]),
        Fact_Physical_Progress[Date] <= SelectedDate
    )
RETURN
    CALCULATE(
        MAX(Fact_Physical_Progress[Physical_Progress_Pct]),
        Fact_Physical_Progress[Date] = LastReportedDate
    )

-- Earned Value (EV) = SUMX over WBS (Budget * Current Progress)
[Total EV] := 
SUMX(
    Dim_WBS,
    Dim_WBS[Total_Budget] * [Latest_Physical_Progress_Pct]
)

-- Cost Variance (CV) & Schedule Variance (SV)
[CV] := [Total EV] - [Total AC]
[SV] := [Total EV] - [Total PV]

-- Indices
[CPI] := DIVIDE([Total EV], [Total AC])
[SPI] := DIVIDE([Total EV], [Total PV])

-- Forecasts
[EAC] := DIVIDE([BAC], [CPI])
[ETC] := [EAC] - [Total AC]
[VAC] := [BAC] - [EAC]
```

## 4. Edward Tufte Styling Guidelines for Excel Dashboards
Apply the following strict visual principles when building dashboards or styling Pivot Tables:

* **Erase Gridlines**: Turn off sheet gridlines on the dashboard tab (`View -> Show -> Uncheck Gridlines`).
* **Table Layouts**:
  * Remove all vertical borders.
  * Use only thin horizontal borders: one below the header row, and one below the totals row.
  * Left-align text columns, right-align numeric and currency columns.
  * Ensure decimal places are vertically aligned (e.g. format as `#,##0.00`).
  * Place units (`NOK`, `Hours`) in the column header (e.g. `Budget (NOK)`) and keep the data rows as pure numbers.
* **Muted, Functional Colors**:
  * Use light grey for baselines/plans, dark grey/black for actuals, and slate blue for earned value.
  * Accent colors (bright red or amber) must be reserved exclusively to highlight critical variances (`CPI < 0.95`, `SPI < 0.90`) or risk signals.
* **Direct Labeling**:
  * Label the S-Curves directly at the end of the line (e.g., placing the words "Planned Value", "Earned Value", "Actual Cost" adjacent to their respective curves) rather than using a detached color legend.
