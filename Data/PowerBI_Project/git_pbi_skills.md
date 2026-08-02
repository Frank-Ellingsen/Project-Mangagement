# Power BI Project Controlling Skills

## Overview

This guide captures the Power BI pattern used for this project-control dashboard: a compact, executive-ready report that combines EVM, schedule health, milestone delivery, and scenario-based variance logic in a single PBIP-based package.

The design goal is to make the report feel like a real operating dashboard rather than a generic data dump. The result should support portfolio review, project governance, and executive decision-making with clear KPI cards, structured narrative, and scenario sensitivity.

## What this project delivers

- A Power BI project package built around PBIP and TMDL files.
- A semantic model that connects project, cost, schedule, and progress data.
- DAX measures for EVM and variance tracking.
- A scenario selector that can switch between conservative, baseline, and aggressive assumptions.
- A report structure with pages for executive overview, financial control, and delivery narrative.

## Core data sources

The semantic model is built from these sources:

- projects
- wbs_elements
- timesheets
- material_costs
- physical_progress
- resources
- ScenarioSelection

These sources support the following business questions:

- Where is the project over or under budget?
- Is the schedule slipping or recovering?
- Which work packages are at risk?
- How do the results change under different assumptions?

## Semantic model design principles

1. Keep the model simple and executive-friendly.
2. Prefer measures over raw columns for reporting logic.
3. Separate base data from business logic.
4. Use a scenario table for threshold-based decision support.
5. Keep visuals minimal, labeled clearly, and consistent with the project narrative.

## Recommended measure layer

The dashboard should expose measures such as:

- BAC
- AC
- EV
- PV
- SV
- CV
- CPI
- SPI
- EAC (Typical)
- VAC
- Latest Percent Complete
- Variance RAG

### Example DAX pattern

```DAX
BAC = SUM(projects[BaselineBudget])
AC = SUM(material_costs[ActualCost]) + SUM(timesheets[ActualHoursCost])
EV = SUM(physical_progress[EarnedValue])
PV = SUM(physical_progress[PlannedValue])
SV = [EV] - [PV]
CV = [EV] - [AC]
CPI = DIVIDE([EV], [AC])
SPI = DIVIDE([EV], [PV])
EAC = DIVIDE([BAC], [CPI])
VAC = [BAC] - [EAC]
```

## RAG and scenario logic

A useful control is a scenario selector that changes the thresholds used for variance interpretation.

Example logic:

```DAX
Variance RAG =
VAR CVValue = [CV]
VAR SVValue = [SV]
VAR Scenario = SELECTEDVALUE(ScenarioSelection[Scenario], "Baseline")
RETURN
SWITCH(
    TRUE(),
    Scenario = "Conservative" && (CVValue < -0.1 || SVValue < -0.1), "Red",
    Scenario = "Aggressive" && (CVValue < -0.05 || SVValue < -0.05), "Amber",
    CVValue >= 0 && SVValue >= 0, "Green",
    "Amber"
)
```

This keeps the status logic readable while allowing the report to reflect different risk tolerance levels.

## Report structure

### 1. Executive Overview

Purpose: provide a high-level PMO view.
Suggested visuals:

- KPI cards for BAC, AC, EV, and percent complete
- Status summary by project
- Milestone and delivery health view

### 2. Financial Control

Purpose: focus on EVM and variance interpretation.
Suggested visuals:

- Cost and value trend chart
- Cost variance and schedule variance cards
- CPI and SPI cards
- Scenario selector in a compact, button-group style control
- Overall RAG indicator

### 3. Client Delivery

Purpose: explain delivery status and narrative.
Suggested visuals:

- WBS delivery status table
- Milestone completion view
- Delivery narrative card with actions and focus areas

## Visual design guidance

- Use restrained, executive styling.
- Favor direct labels and minimal decorative clutter.
- Use consistent color meaning: green for healthy, amber for caution, red for at risk.
- Place selectors where they are easy to find but do not dominate the page.
- Keep hierarchy clear with compact KPI cards and simple chart composition.

## Git and PBIP workflow

When working on this Power BI project:

1. Update the generator or source definitions first.
2. Regenerate the PBIP package after structural changes.
3. Validate the output for semantic and report consistency.
4. Keep the report metadata and measure definitions versioned in Git.
5. Review changes that affect measures, page layout, or scenario logic carefully.

### Typical regeneration command

```powershell
python AI_Controller/build_pbi_project.py
```

## PMO checklist for this dashboard

- Data model includes projects, costs, WBS, and progress.
- Measures are available for EVM and variance assessment.
- RAG logic is present and scenario-aware.
- Report pages are structured for executive reporting.
- The selector behaves like a real dashboard control.
- The layout is visually balanced and presentation-ready.

## Final recommendation

Use this dashboard as a practical control tower for project delivery: not just a static report, but a decision-support layer for PMO, finance, and delivery leadership.
