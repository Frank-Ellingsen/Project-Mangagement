🧱 1. Core Quantity & Progress Measures
Installed Quantity
Code
Installed Qty = SUM(InstalledQuantities[InstalledQty])
Planned Quantity
Code
Planned Qty = SUM(PlannedQuantities[PlannedQty])
Physical Progress %
Code
Physical Progress % = DIVIDE([Installed Qty], [Planned Qty])
Daily Installed Quantity
Code
Daily Installed Qty = SUM(InstalledQuantities[InstalledQty])
Weekly Installed Quantity
Code
Weekly Installed Qty =
CALCULATE(
    [Installed Qty],
    ALLEXCEPT(Calendar, Calendar[Week])
)
Workfront Availability %
Code
Workfront Availability % =
DIVIDE([Available Workfronts], [Total Workfronts])
🧭 2. Schedule / Earned Value Measures
Planned Value (PV)
Code
PV = SUM(EVM[PV])
Earned Value (EV)
Code
EV = SUM(EVM[EV])
Actual Cost (AC)
Code
AC = SUM(EVM[AC])
Schedule Variance (SV)
Code
SV = [EV] - [PV]
Cost Variance (CV)
Code
CV = [EV] - [AC]
Schedule Performance Index (SPI)
Code
SPI = DIVIDE([EV], [PV])
Cost Performance Index (CPI)
Code
CPI = DIVIDE([EV], [AC])
Variance at Completion (VAC)
Code
VAC = [Budget At Completion] - [Forecast At Completion]
Forecast at Completion (FAC)
Code
Forecast At Completion = [Actual Cost] + [Forecast To Complete]
💰 3. Cost, Budget & Forecasting Measures
Budget
Code
Budget = SUM(Budget[BudgetAmount])
Committed Cost
Code
Committed Cost = SUM(Committed[CommittedAmount])
Actual Cost
Code
Actual Cost = SUM(Actuals[ActualAmount])
Forecast Cost
Code
Forecast Cost = SUM(Forecast[ForecastAmount])
Cost Variance %
Code
Cost Variance % = DIVIDE([Cost Variance], [Budget])
Change Order Value
Code
Change Order Value = SUM(ChangeOrders[ApprovedValue])
Change Order Impact %
Code
Change Order Impact % =
DIVIDE([Change Order Value], [Original Contract Value])
Monthly Cost Trend
Code
Monthly Cost = CALCULATE([Actual Cost], ALLEXCEPT(Calendar, Calendar[Month]))
👷 4. Resource / Crew / Manpower Measures
Actual Hours
Code
Actual Hours = SUM(Assignments[ActualHours])
Planned Hours
Code
Planned Hours = SUM(Assignments[PlannedHours])
Manpower Count
Code
Manpower Count = DISTINCTCOUNT(Assignments[WorkerID])
Crew Utilization %
Code
Crew Utilization % =
DIVIDE([Actual Hours], [Planned Hours])
Productivity Index
Code
Productivity Index =
DIVIDE([Installed Qty], [Actual Hours])
Equipment Operating Hours
Code
Equipment Operating Hours = SUM(EquipmentLogs[OperatingHours])
Equipment Idle Hours
Code
Equipment Idle Hours = SUM(EquipmentLogs[IdleHours])
Equipment Utilization %
Code
Equipment Utilization % =
DIVIDE([Equipment Operating Hours], [Equipment Operating Hours] + [Equipment Idle Hours])
⚠️ 5. Risk & Safety Measures
Risk Score
Code
Risk Score =
SUMX(
    Risks,
    Risks[Probability] * Risks[Impact]
)
Total Risks
Code
Total Risks = COUNTROWS(Risks)
High Risks
Code
High Risks =
CALCULATE(
    COUNTROWS(Risks),
    Risks[Impact] = "High"
)
Risk Trend
Code
Risk Trend =
CALCULATE([Risk Score], ALLEXCEPT(Calendar, Calendar[Month]))
Safety Incidents
Code
Safety Incidents = COUNTROWS(Safety)
Lost Time Injuries (LTI)
Code
LTI = CALCULATE(COUNTROWS(Safety), Safety[Severity] = "LTI")
Safety Incident Rate
Code
Incident Rate =
DIVIDE([Safety Incidents] * 200000, [Total Hours Worked])
📋 6. Issue Management Measures
Open Issues
Code
Open Issues =
CALCULATE(
    COUNTROWS(Issues),
    Issues[Status] = "Open"
)
Issue Aging (Days Open)
Code
Issue Aging =
DATEDIFF(Issues[CreatedDate], Issues[ClosedDate], DAY)
Average Issue Aging
Code
Avg Issue Aging = AVERAGE(Issues[DaysOpen])
🗺️ 7. Location / Zone Measures
Zone Progress %
Code
Zone Progress % =
DIVIDE([Installed Qty], [Planned Qty])
Zone Risk Score
Code
Zone Risk Score =
CALCULATE([Risk Score], ALLEXCEPT(Zones, Zones[ZoneID]))
Zone Manpower
Code
Zone Manpower =
CALCULATE([Manpower Count], ALLEXCEPT(Zones, Zones[ZoneID]))
🧮 8. Time Intelligence Measures
Current Month
Code
Current Month = MAX(Calendar[Month])
Previous Month Actual Cost
Code
Prev Month Actual Cost =
CALCULATE([Actual Cost], DATEADD(Calendar[Date], -1, MONTH))
Month-over-Month Cost Change
Code
MoM Cost Change = [Actual Cost] - [Prev Month Actual Cost]
Year-to-Date Cost
Code
YTD Cost =
TOTALYTD([Actual Cost], Calendar[Date])
🏆 9. Executive Summary Measures
Project Health Score
Code
Project Health Score =
([Physical Progress %] * 0.4) +
([SPI] * 0.2) +
([CPI] * 0.2) +
((1 - [Incident Rate]) * 0.2)
Overall Status (Text)
Code
Overall Status =
SWITCH(
    TRUE(),
    [Project Health Score] >= 0.85, "On Track",
    [Project Health Score] >= 0.70, "At Risk",
    "Delayed"
)