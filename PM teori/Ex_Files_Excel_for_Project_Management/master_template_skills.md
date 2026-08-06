# Master Project Controlling Excel Template - Skill Guide

This document describes the structure, data flows, key formulas, and dashboard elements of the newly created [Master_Project_Controlling_Template.xlsx](file:///C:/Users/frank/Desktop/Project%20Mng/PM%20teori/Ex_Files_Excel_for_Project_Management/Master_Project_Controlling_Template.xlsx).

## 1. Inventory of Consolidated Sheets

The master template consolidates all exercises and templates into a clean, normalized layout structured as follows:

| Layer | Sheet Name | Core Table / Range | Purpose / Key Columns |
| :--- | :--- | :--- | :--- |
| **Cover & Admin** | `Cover` | `tbl_Cover_Contents` | Project metadata, revision logs, and dynamic Table of Contents. |
| | `Glossary` | `tbl_Glossary` | Definitions of EVM, scheduling, and risk indicators. |
| | `Method Roadmap` | `tbl_Method_Roadmap` | Visual step-by-step roadmap mapping project phases. |
| | `PM-EVM Compliance`| `tbl_PMEVM_Compliance`| Standard checklist for auditing EVM compliance. |
| **Review & Setup** | `Review` | `tbl_Review_ActionLog` | Action item tracking log (Action ID, Description, Severity, Status). |
| | `PID` | `tbl_PID_ProjectControls`<br>`tbl_PID_RiskControl`<br>`tbl_PID_Financials` | Define Project Controls role matrix, risk registers, and baseline financials. |
| | `Setup` | `tbl_Setup_Controls`<br>`tbl_Setup_RAG` | Parameter ranges (Currency, Update Frequencies) and RAG status thresholds. |
| **Scope & Schedule**| `Task Plan` | `tbl_Task_Plan` | Standard schedule baseline with durations, dependencies, and resources. |
| | `Task Capture` | `tbl_Task_Capture` | Weekly actual data tracking sheets (WBS ID, actual hours, actual costs). |
| | `Resource Grid` | `tbl_Resource_WeeklyGrid`<br>`tbl_Resource_MonthlySummary`| Standard team weekly hour-booking grids and monthly summaries. |
| **Data Model (Star)**| `Dim_Project` | `tbl_Dim_Project` | Project Dimension (ID, Name, Start Date, End Date, BAC). |
| | `Dim_WBS` | `tbl_Dim_WBS` | WBS Work Breakdown Structure Dimension (WBS Code, Element Name, Type). |
| | `Dim_Resource` | `tbl_Dim_Resource` | Team resource registry (ID, Name, Role, Standard Hourly Rate). |
| | `Dim_Calendar` | `tbl_Dim_Calendar` | Auto-generated daily dates (Year, Month, Quarter, Week Number, IsWeekday). |
| | `Fact_Baseline_PV` | `tbl_Fact_Baseline_PV` | Planned Value allocation baseline (Date, WBS ID, Planned Value). |
| | `Fact_Actual_Costs`| `tbl_Fact_Actual_Costs` | Transactional actual expenditures (Date, WBS ID, Resource ID, Cost, Hours). |
| | `Fact_Physical_Progress`| `tbl_Fact_Physical_Progress` | Periodic physical completion progress (Date, WBS ID, Progress %). |
| **Analytics & BI** | `EVM Dashboard` | `tbl_Dashboard_RAGLegend`<br>`tbl_Dashboard_WBSPerformance`<br>`tbl_Dashboard_WeeklyTrends` | High-level summary RAG cards, WBS-level EVM tables, and weekly trends. |
| | `Red Actions` | `tbl_Red_Action_Recommendations`| Automatically pulls elements with CPI < 0.95 or SPI < 0.90 to assign corrective actions. |
| | `Pivot Summary` | `tbl_Pivot_DescriptiveStats`| High-level pivot aggregations and weekly statistics. |
| | `EVM` | `tbl_EVM_Weekly`<br>`tbl_EVM_Validation` | Periodic EVM indicators calculation sheet and error validation audits. |
| | `EVM Charts` | `tbl_Charts_GanttHelper`<br>`tbl_Charts_RAGLegend`<br>`tbl_Charts_SCurveHelper`| Helper structures for drawing S-Curves and in-cell bar charts. |
| | `Simple Gantt Model`| `tbl_SimpleGantt_Mapping`<br>`tbl_SimpleGantt_TaskSummary`<br>`tbl_SimpleGantt_Legend` | Gantt chart generator utilizing conditional formatting rules. |
| | `PERT Diagram` | `tbl_PERT_Data`<br>`tbl_PERT_Legend` | Critical Path Method (CPM) and PERT calculations (ES, EF, Slack). |

---

## 2. Core Business Logic & Calculations (EVM Formulas)

* **Planned Value (PV)**: Summed from `tbl_Fact_Baseline_PV` up to the reporting date.
* **Actual Cost (AC)**: Summed from `tbl_Fact_Actual_Costs` up to the reporting date.
* **Earned Value (EV)**: calculated at the WBS level as:
  $$\text{EV} = \text{BAC (Dim\_WBS)} \times \text{Latest Physical Progress \%}$$
* **Cost Variance (CV)**: $EV - AC$
* **Schedule Variance (SV)**: $EV - PV$
* **Cost Performance Index (CPI)**: $\frac{EV}{AC}$ (Target $\ge 1.0$)
* **Schedule Performance Index (SPI)**: $\frac{EV}{PV}$ (Target $\ge 1.0$)
* **Estimate at Completion (EAC)**: $\frac{BAC}{CPI}$
* **Variance at Completion (VAC)**: $BAC - EAC$

---

## 3. Formatting and Tufte Compliance Checklist

When updating or extending the master template, ensure compliance with the following:
1. **No Sheet Gridlines**: Always disable sheet gridlines on the `EVM Dashboard` and final output sheets.
2. **Text Alignments**: Left-align all names, codes, and text fields; right-align numbers, percentages, and currencies.
3. **No Vertical Borders**: Use only thin horizontal grey borders to separate sections.
4. **Direct S-Curve Labeling**: Label actual, baseline, and earned lines directly on the chart rather than using a standard bottom legend.
5. **Restricted Highlighting**: Colors like red or amber must only be used when `CPI < 0.95` or `SPI < 0.90` to highlight project risks.
