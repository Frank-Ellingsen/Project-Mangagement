PROJECT CONTROLS DASHBOARD SPECIFICATION DOCUMENT
Version: 1.0
Domain: Construction / Engineering
Prepared for: Frank
Prepared by: Copilot (Microsoft)

1. Purpose & Objectives
The Project Controls Dashboard provides unified visibility into schedule, cost, progress, resources, risks, safety, and field execution for construction/engineering projects.
It enables:

Early detection of schedule and cost deviations

Real‑time field progress tracking

Accurate earned value performance (SPI/CPI)

Crew and equipment utilization monitoring

Risk and safety management

Executive‑level reporting for PMO and leadership

The dashboard supports multi‑project portfolios and single megaprojects.

2. User Roles & Use Cases
Primary Users
Project Director

Construction Manager

Project Controls Lead

Cost Engineer

Scheduler / Planner

Safety Manager

Subcontractor Manager

Executive Leadership

Key Use Cases
Monitor schedule performance (SV, SPI)

Track cost performance (CV, CPI)

Compare planned vs installed quantities

Identify zone‑level delays and bottlenecks

Review safety incidents and risk exposure

Evaluate subcontractor performance

Forecast cost at completion (FAC)

Drill into work packages and tasks

3. Dashboard Architecture (Page Layout)
The dashboard uses a 12‑column responsive grid.

Row 1 — Executive KPIs
Physical Progress %

Schedule Variance (SV)

Cost Variance (CV)

SPI

CPI

Safety Incident Rate

Row 2 — Schedule
Gantt Chart (baseline vs actual, critical path)

Milestone Timeline

Row 3 — Cost Control
Budget → Committed → Actual → Forecast Waterfall

EV/PV/AC Comparison

SPI/CPI Trend

Row 4 — Field Progress
Planned vs Installed Quantities

Daily/Weekly Progress Trend

Workfront Availability

Row 5 — Location & Zones
ArcGIS/Azure Map

Zone Progress Heatmap

Work Package × Discipline Matrix

Row 6 — Resources & Equipment
Crew Utilization Heatmap

Equipment Utilization

Manpower Histogram

Row 7 — Risks & Safety
Risk Matrix

Risk Trend

Safety Incident Tracker

Row 8 — Issues & Subcontractors
Issue Aging Histogram

Subcontractor Performance

Drillthrough Pages
Task Detail

Work Package Detail

Subcontractor Detail

Safety Incident Detail

Zone Detail

4. Visual Specifications
4.1 Gantt Chart
Visual: xViz Gantt or Microsoft Gantt

Fields: Task, Start, Finish, Baseline Start/Finish, % Complete

Features: Critical path, slippage highlighting, hierarchy

4.2 Milestone Timeline
Fields: Milestone Name, Date, Category

Categories: Permits, Mobilization, Structural, MEP, Commissioning

4.3 Waterfall (Cost Flow)
Categories: Budget, Change Orders, Committed, Actual, Forecast

4.4 EV/PV/AC Comparison
Visual: Clustered bar or line

Fields: PV, EV, AC

4.5 Planned vs Installed Quantities
Visual: Combo chart

Fields: Planned Qty, Installed Qty

4.6 Zone Progress Heatmap
Rows: Zones

Columns: Weeks

Color: % Complete

4.7 Crew Utilization Heatmap
Rows: Crews

Columns: Days

Color: Utilization %

4.8 Risk Matrix
Axes: Probability × Impact

Color: Severity

4.9 Safety Incident Tracker
Categories: Near Miss, First Aid, MTC, LTI

5. Data Model Specification
5.1 Fact Tables
Tasks

InstalledQuantities

PlannedQuantities

ActualCost

CommittedCost

Budget

Forecast

EVM

Assignments

EquipmentLogs

Risks

Issues

SafetyIncidents

5.2 Dimension Tables
Projects

WorkPackages

Zones

Subcontractors

Workers

Crews

Equipment

Calendar

5.3 Relationship Rules
Projects → WorkPackages → Tasks

Tasks → InstalledQuantities / PlannedQuantities / ActualCost / EVM

Tasks → Zones

Tasks → Subcontractors

Assignments → Workers → Crews

EquipmentLogs → Equipment

All facts → Calendar

6. DAX Measure Library
The dashboard uses the full construction DAX library you already received, including:

Physical Progress %

SV, CV, SPI, CPI

EV, PV, AC

Productivity Index

Equipment Utilization %

Incident Rate

Zone Progress %

Project Health Score

All measures follow star‑schema best practices.

7. Filters & Interactions
Filters
Project

Zone

Work Package

Discipline

Subcontractor

Date

Crew

Equipment

Cross‑highlighting
Selecting a zone filters:

Tasks

Risks

Issues

Installed quantities

Manpower

Drillthrough
Task → Task Detail

Work Package → WP Detail

Subcontractor → SC Detail

Safety Incident → Incident Detail

8. Theme & Styling
Primary Colors
Steel Blue (#3A5F7D)

Concrete Gray (#D0D3D4)

Safety Orange (#F57C00)

Structural Red (#C62828)

Engineering Green (#2E7D32)

Status Colors
On Track: #2E7D32

At Risk: #F9A825

Delayed: #C62828

Typography
Segoe UI

Segoe UI Semibold for titles

Card Style
White background

Gray border

Blue text

9. Performance & Governance
Performance Requirements
All visuals must load in < 2 seconds

All DAX must be column‑store optimized

No bi‑directional relationships

No calculated columns for time intelligence

Data Refresh
Daily refresh for cost, quantities, risks

Hourly refresh optional for field progress

Security
Row‑level security (RLS) by:

Project

Zone

Subcontractor

10. Deployment & Maintenance
Deployment Targets
Power BI Service

Workspace: Project Controls

App: Project Controls Dashboard

Maintenance
Monthly review of DAX performance

Quarterly update of theme

Annual schema review

11. Acceptance Criteria
The dashboard is considered complete when:

All visuals match the layout blueprint

All DAX measures produce correct results

All drillthrough pages function

All filters work across visuals

Performance meets requirements

PMO signs off on accuracy