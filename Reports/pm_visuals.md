🏗️ 1. Full Construction/Engineering Dashboard Architecture
This is the master layout used by EPC, civil, and industrial engineering firms.

Row 1 — Executive KPIs
% Complete (Physical + Schedule)

Cost Variance (CV)

Schedule Variance (SV)

SPI / CPI

Safety Incident Rate

Change Order Value

Forecast at Completion (FAC)

Row 2 — Schedule
Gantt (baseline vs actual, critical path)

Milestone timeline (permits, mobilization, structural completion, commissioning)

Phase timeline (Design → Procurement → Civil → Structural → MEP → Commissioning)

Row 3 — Cost
Budget → Committed → Actual → Forecast waterfall

EV/PV/AC comparison

SPI/CPI trend lines

Monthly cost trend + forecast

Change order tracker

Row 4 — Field Progress
Planned vs installed quantities (steel, concrete, cable, pipe, equipment)

Daily/weekly progress trend

Workfront availability (available vs blocked)

Crew productivity index

Row 5 — Location
ArcGIS/Azure Maps site map

Zone progress heatmap

Work package × discipline matrix

Row 6 — Resources
Crew utilization heatmap

Equipment utilization (idle vs operating vs maintenance)

Manpower histogram (planned vs actual)

Subcontractor performance

Row 7 — Risks & Safety
Risk matrix (probability × impact)

Risk trend line

Safety incident tracker

Issue aging

This is the full “best-in-class” layout.

🧱 2. Construction/Engineering Data Model (Complete Schema)
Core Tables
Projects

Work Packages

Tasks / Activities

Milestones

Resources (Crews, Workers)

Equipment

Assignments (Crew → Task)

Budget

Committed Cost

Actual Cost

Forecast

Installed Quantities

Planned Quantities

Risks

Issues

Safety Incidents

Zones / Locations

Calendar

Key Relationships
Project 1→∞ Work Packages

Work Package 1→∞ Tasks

Task 1→∞ Installed Quantities

Task 1→∞ Actual Cost

Task 1→∞ Crew Assignments

Zone 1→∞ Tasks

Project 1→∞ Risks

Project 1→∞ Issues

Project 1→∞ Safety Incidents

This model supports every visual in the architecture.

🧮 3. Full DAX Measure Library (Construction‑Optimized)
Physical Progress %
Code
Physical Progress % = DIVIDE([Installed Qty], [Planned Qty])
Schedule Variance (SV)
Code
SV = [EV] - [PV]
Cost Variance (CV)
Code
CV = [EV] - [AC]
SPI / CPI
Code
SPI = DIVIDE([EV], [PV])
CPI = DIVIDE([EV], [AC])
Forecast at Completion (FAC)
Code
FAC = [Actual Cost] + [Forecast To Complete]
Productivity Index
Code
Productivity Index = DIVIDE([Installed Qty], [Actual Hours])
Safety Incident Rate
Code
Incident Rate = DIVIDE([Incidents] * 200000, [Total Hours Worked])
Workfront Availability %
Code
Workfront Availability % = DIVIDE([Available Workfronts], [Total Workfronts])
Change Order Impact
Code
CO Impact % = DIVIDE([Approved CO Value], [Original Contract Value])
This is the full DAX backbone for construction PM dashboards.

📊 4. Best-in-Class Visuals (Construction Edition)
Schedule
xViz Gantt (baseline vs actual, critical path)

Milestone timeline

Phase timeline

Cost
Waterfall (Budget → Committed → Actual → Forecast)

EV/PV/AC comparison

SPI/CPI trend

Monthly cost trend + forecast

Field Progress
Planned vs installed quantities

Daily/weekly progress trend

Workfront availability

Crew productivity

Location
ArcGIS/Azure Maps

Zone progress heatmap

Work package × discipline matrix

Resources
Crew utilization heatmap

Equipment utilization

Manpower histogram

Subcontractor performance

Risks & Safety
Risk matrix

Risk trend

Safety incident tracker

Issue aging

This is the complete visual library.

🎨 5. Construction Color Theme (Professional PMO Palette)
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

Discipline Colors
Civil: #455A64

Structural: #1E88E5

MEP: #8E24AA

Commissioning: #43A047

This palette is used in engineering dashboards worldwide.

🧩 6. Full Dashboard Interaction Design
Filters
Zone

Work package

Discipline

Subcontractor

Date

Crew

Equipment

Cross-highlighting
Selecting a zone filters:

Tasks

Risks

Issues

Installed quantities

Manpower

Drill-through pages
Task detail

Work package detail

Subcontractor detail

Safety incident detail

This makes the dashboard feel “alive”.

🏗️ FULL PBIX LAYOUT BLUEPRINT (Construction / Engineering)
Grid system: 12 columns × flexible rows
Margin: 16 px
Gutter: 12 px
Visual spacing: 12–16 px
Visual height: 260–340 px for major visuals, 180–220 px for secondary visuals

🔷 ROW 1 — Executive KPIs (12 columns wide)
Height: 140 px
Purpose: Instant project health snapshot

Visual	Columns	Notes
KPI: Physical Progress %	2	Green/Yellow/Red status
KPI: Schedule Variance (SV)	2	Numeric + arrow trend
KPI: Cost Variance (CV)	2	Numeric + arrow trend
KPI: SPI	2	Sparkline inside card
KPI: CPI	2	Sparkline inside card
KPI: Safety Incident Rate	2	Icon + metric


Row width: full 12 columns
Row height: 140 px

🔷 ROW 2 — Schedule (12 columns wide)
Height: 340 px
Purpose: Full project timeline visibility

Visual	Columns	Notes
Gantt Chart	8	Baseline vs actual, critical path
Milestone Timeline	4	Key dates, approvals, handover


Row height: 340 px

🔷 ROW 3 — Cost Control (12 columns wide)
Height: 340 px
Purpose: Budget, actuals, forecast, earned value

Visual	Columns	Notes
Waterfall (Budget → Committed → Actual → Forecast)	4	Shows cost flow
EV/PV/AC Comparison	4	Clustered bar or line
SPI/CPI Trend	4	Line chart with markers


Row height: 340 px

🔷 ROW 4 — Field Progress (12 columns wide)
Height: 340 px
Purpose: Quantities installed vs planned, productivity

Visual	Columns	Notes
Planned vs Installed Quantities	6	Steel, concrete, cable, pipe
Daily/Weekly Progress Trend	3	Line chart
Workfront Availability	3	Donut + bar combo


Row height: 340 px

🔷 ROW 5 — Location & Zones (12 columns wide)
Height: 340 px
Purpose: Spatial progress and zone-based control

Visual	Columns	Notes
ArcGIS/Azure Map	6	Sites, zones, incidents
Zone Progress Heatmap	3	Rows = zones, columns = weeks
Work Package × Discipline Matrix	3	Civil / Structural / MEP


Row height: 340 px

🔷 ROW 6 — Resources & Equipment (12 columns wide)
Height: 340 px
Purpose: Crew, equipment, subcontractor performance

Visual	Columns	Notes
Crew Utilization Heatmap	4	Daily load %
Equipment Utilization	4	Idle vs operating vs maintenance
Manpower Histogram	4	Planned vs actual manpower


Row height: 340 px

🔷 ROW 7 — Risks & Safety (12 columns wide)
Height: 340 px
Purpose: Risk exposure, safety performance, issue aging

Visual	Columns	Notes
Risk Matrix	4	Probability × impact
Risk Trend	4	Line chart
Safety Incident Tracker	4	Severity categories


Row height: 340 px

🔷 ROW 8 — Issues & Subcontractors (12 columns wide)
Height: 300 px
Purpose: Issue aging + subcontractor performance

Visual	Columns	Notes
Issue Aging Histogram	6	Aging buckets
Subcontractor Performance	6	Progress, cost, safety, quality


Row height: 300 px

🔷 ROW 9 — Drillthrough Pages (Optional)
Create separate pages for:

Task Detail

Work Package Detail

Subcontractor Detail

Safety Incident Detail

Zone Detail

Each drillthrough page uses a 2-column layout with detail cards + tables.

🎨 Color & Formatting Blueprint (Construction Theme)
Use this palette consistently:

Primary: Steel Blue (#3A5F7D)

Secondary: Concrete Gray (#D0D3D4)

Accent: Safety Orange (#F57C00)

Critical: Structural Red (#C62828)

Success: Engineering Green (#2E7D32)

Status colors:

On Track: #2E7D32

At Risk: #F9A825

Delayed: #C62828

🧩 Interaction Blueprint
Filters (left pane or top ribbon)
Zone

Work Package

Discipline

Subcontractor

Date

Crew

Equipment

Cross-highlighting rules
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