Power BI Project Management — Skill & Best‑Practice Guide (power-bi-project-management.md)

1. Purpose
   A Power BI project management report provides a single source of truth for tasks, milestones, risks, costs, dependencies, and delivery readiness. It replaces spreadsheets, slide decks, and inconsistent status reporting with automated, real‑time governance.

2. Core Data Model (Required Tables)
   2.1 Tasks / Activities
   TaskID

Task Name

WBS Code

Phase / Category

Owner / Resource

Start Date

End Date

Duration

Percent Complete

Baseline Start / End

Actual Start / End

Dependency TaskID

RAG Status (Red/Amber/Green)

Today Date (for dynamic calculations)

2.2 Milestones
MilestoneID

Milestone Name

Planned Date

Actual Date

Status (On Track / Delayed / Blocked)

Executive Summary Flag (for leadership dashboards)

2.3 Resources
ResourceID

Role

Hourly Rate

Allocation %

Planned Hours

Actual Hours

2.4 Cost Tables
Labor Rates

Material Costs

Planned Cost

Actual Cost

Baseline Cost

Variance (Actual – Baseline)

2.5 Calendar Table
A dynamic calendar table is mandatory for Gantt timelines, cost curves, and scenario planning.

3. Essential DAX Measures
   3.1 Schedule Measures
   DAX
   Duration Days = DATEDIFF(Tasks[StartDate], Tasks[EndDate], DAY)

Percent Complete = DIVIDE(SUM(Tasks[CompletedHours]), SUM(Tasks[PlannedHours]))

IsDelayed = IF(Tasks[ActualEnd] > Tasks[BaselineEnd], 1, 0)
3.2 RAG Logic
DAX
RAG Status =
SWITCH(
TRUE(),
[Percent Complete] < 0.5 && [IsDelayed] = 1, "Red",
[Percent Complete] < 0.8 && [IsDelayed] = 1, "Amber",
"Green"
)
3.3 Cost Measures
DAX
Baseline Cost = SUM(Costs[BaselineCost])
Actual Cost = SUM(Costs[ActualCost])
Cost Variance = [Actual Cost] - [Baseline Cost]
Cost Variance % = DIVIDE([Cost Variance], [Baseline Cost])
3.4 Timeline Measures
DAX
Today = TODAY()

IsActive =
IF(
Today >= Tasks[StartDate] &&
Today <= Tasks[EndDate],
1,
0
)
3.5 Milestone Health
DAX
Milestone Status =
IF(Milestones[ActualDate] > Milestones[PlannedDate], "Delayed", "On Track") 4. Recommended Visuals
4.1 Gantt Chart (Project Timeline)
Use Gantt custom visual or native stacked bar

Show baseline vs actual

Include dependency arrows

Color by RAG

Add today line for context

4.2 WBS Tree Visual
Hierarchy: Phase → Work Package → Task

Use Decomposition Tree or HierarchySlicer

Show roll‑up metrics: cost, hours, completion %

4.3 Milestone Heatmap
Matrix: Milestones × Status

Conditional formatting for delayed items

Executive‑friendly summary (leaders manage outcomes, not tasks)

4.4 RAG Dashboard
KPI cards for Red / Amber / Green counts

Trend of RAG over time

Drill‑through to root‑cause analysis

4.5 Cost & Budget Visuals
Waterfall: baseline → changes → actual

Line chart: cumulative cost curve

Bar chart: cost variance by phase

4.6 Resource Utilization
Heatmap: resource × week

Over‑allocation alerts

Planned vs actual hours

4.7 Risk & Issue Register
Table with severity, probability, owner

Bubble chart for risk impact vs likelihood

RAG color coding

4.8 Scenario Planning
What‑If parameters:

Delay days

Inflation %

Resource rate changes

Visuals update dynamically

5. Executive Reporting Best Practices
   5.1 Milestone‑Driven Reporting
   Executives care about outcomes, not tasks.
   Use milestone summaries to answer:

Are we on track?

Which milestones are delayed?

Where is leadership support needed?

5.2 Standardized Governance
One data model for all teams

Automated refresh

Role‑based access

Consistent RAG logic

5.3 Real‑Time Monitoring
Auto‑refresh from project systems

Alerts for delays, cost overruns

Live dashboards for PMO

5.4 Integration
Connect Power BI to:

MS Project

Planner

Jira

Azure DevOps

ERP cost systems

6. Page Layout Templates
   6.1 PMO Overview Page
   KPI cards: schedule, cost, scope

RAG summary

Milestone status

Top risks

Executive notes

6.2 Delivery Team Page
Gantt

WBS tree

Task table

Resource utilization

6.3 Cost & Finance Page
Cost curve

Variance waterfall

Forecast vs actual

Scenario planning sliders

6.4 Risk & Issue Page
Risk matrix

Issue log

Mitigation actions

7. Advanced Features
   7.1 Dependency Mapping
   Network diagram (custom visual)

Critical path highlighting

7.2 Earned Value Management (EVM)
Add measures:

PV (Planned Value)

EV (Earned Value)

AC (Actual Cost)

SPI, CPI

EAC (Estimate at Completion)

7.3 Delivery Readiness Score
Composite KPI combining:

RAG

Risk severity

Resource availability

Milestone health

7.4 AI Insights
Anomaly detection on cost

Predictive delays

Natural language summaries

8. Checklist for Enterprise PMO Dashboards
   Data
   Calendar table

Baseline vs actual fields

Dependencies

Milestones

RAG logic

Cost tables

Visuals
Gantt

WBS

RAG

Milestones

Cost curves

Resource heatmaps

Risks

Governance
Standardized definitions

Automated refresh

Role‑based access

Executive summaries

Scenario planningS
