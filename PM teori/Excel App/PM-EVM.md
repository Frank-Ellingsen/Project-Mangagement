Integrating WBS, Gantt Charts & Earned Value Management for Project Control
Project management is all about balancing a project’s scope (work/quality), schedule (time), and cost (budget). These three constraints form the classic project management triangle (also known as the triple constraint), where changes to one affect the others. To effectively control and report on a project’s performance, project managers use a combination of tools and techniques that connect scope, schedule, cost, and performance metrics. Three key components of this integrated approach are the Work Breakdown Structure (WBS), the Gantt chart (project schedule), and Earned Value Management (EVM). [en.wikipedia.org]
In this explanation, we’ll explore how these elements work together in a cohesive model for project control and reporting. We’ll discuss each component conceptually, then illustrate how they come together in dashboard-style project control views, linking items such as budget lines and WBS elements to forecasts (EAC), variances, change orders, contracts, and payment progress. We’ll also introduce key EVM metrics (PV, EV, AC) and performance measures (SV, CV, SPI, CPI) and demonstrate how they align with the project management triangle, helping stakeholders make informed decisions.

Scope, Schedule & Cost: The Project Management Triangle
Every project manager must juggle three fundamental dimensions:
Scope: the work and deliverables of the project (and by extension, the quality/features). [en.wikipedia.org]
Schedule (Time): the timeline and deadlines to complete the work.
Cost (Budget): the financial resources available for the project.

Figure 1. The Cost–Scope–Time triangle. The three constraints are interdependent, while quality and the overall project outcome reflect how successfully they are balanced.
How to read the triangle: A constraint cannot usually be changed in isolation. Increasing scope normally requires more time, more cost, or both. Reducing the available time may require additional resources and therefore higher cost, or it may require a smaller scope. Cutting cost can likewise force schedule extensions, scope reductions, or different delivery methods. The center represents the project’s quality and overall outcome: unmanaged trade-offs can weaken the result, while explicit, approved trade-offs help preserve it.
These three form the Project Management Triangle (also called the triple constraint or iron triangle). The basic idea is that each side of the triangle influences the others: if you change one, the other two will be affected. For example, adding more scope (features or work) without adjusting the schedule or budget will likely cause delays or cost overruns. Good project control involves managing all three aspects together and maintaining balance so that the project stays on track to deliver the promised scope on schedule and within budget. [en.wikipedia.org], [en.wikipedia.org] [en.wikipedia.org]
To achieve this balance, project controlling and reporting rely on structured methods and visual tools. Two essential planning tools are the WBS (which defines what work is included) and the Gantt chart schedule (which shows when tasks happen). Earned Value Management then ties these plans to actual performance, measuring how we’re doing in terms of both schedule and cost simultaneously, and enabling forecasting.

Work Breakdown Structure (WBS): Foundation of Scope & Budget Control
A Work Breakdown Structure (WBS) is a hierarchical breakdown of the project scope into detailed, manageable components (deliverables, phases, and tasks). The WBS organizes all project work into a tree structure with progressively smaller WBS elements or work packages, each representing a portion of the overall scope. For example, a WBS for a construction project might have top-level categories such as 1.0 Planning, 2.0 Design, 3.0 Construction, 4.0 Contingency, and 5.0 Risk Provisions (as in the sample dashboard image), with each broken into subcomponents (e.g., under “1.0 Planning,” there could be sub-items for Engineering Consultant, Architect Contract, etc.). By giving every deliverable and phase a unique WBS code (e.g., 1.0, 1.1, 1.2), nothing in the project scope is left unaccounted for. [projectmanager.com]
Importantly for project control, each WBS element has an allocated budget or Budget at Completion (BAC) – the planned cost for that chunk of work. These budget lines become the basis for cost control and reporting. Project contracts, purchase orders, and change orders (scope or contract changes) are often aligned to WBS elements, so that costs are tracked against specific parts of the project. In other words, the WBS is the common thread linking scope definition, cost budgeting, and responsibility. In formal Earned Value systems, WBS elements at a certain level (often called control accounts) serve as the integration points where scope, schedule, and budgets converge and where performance is measured. This makes the WBS the foundation for all planning and controlling activities, ensuring that the scope (and quality) is clearly defined and tied to the project’s schedule and cost plan. [gatherinsights.com] [tensix.com]
In project controlling, a well-structured WBS enables detailed reporting. Project control dashboards often display financial data by WBS element (as shown in the sample dashboard screenshot provided by the user). Each line in the budget report corresponds to a WBS component or category, showing columns such as:
Original Budget (planned cost for that WBS element),
Contract (or baseline) amount (e.g. sum of contracts or planned cost for that work),
Change Orders (approved changes that adjust the baseline budget/contract),
Current Contract (baseline plus any changes),
Actual Costs / Total Paid to date (costs incurred so far, often also expressed as a percentage of budget or contract),
Estimate at Completion (EAC) for that component (the latest forecast of total cost for the WBS element when finished),
Variance (often shown as Variance at Completion—the difference between the initial budget and the forecast EAC for that element),
Payment/Progress (graphical bar showing progress or costs spent vs budget for that element).
For example, in the provided dashboard, the overall project (Project A) has an original Budget of ~£3.95M, but after £0.745M in change orders (+19% of original), the current contract value is ~£4.09M. The EAC is ~£4.58M, yielding a Variance of -£0.63M (meaning an expected £631k cost overrun vs the original budget). Also, Actual Cost (Total Paid) is £785.9k, which is about 20% of the budget spent so far (as indicated by the progress bar in the report). The project controller can drill down to see each WBS category’s status: for instance, the 1.0 Planning phase might have a small original budget but ended up with much higher costs due to change orders, thus showing a large negative variance on that line. Meanwhile, perhaps 3.0 Construction is under budget (positive variance), offsetting some of the overrun. By seeing each WBS element’s Budget vs Current Contract vs EAC vs Actuals side by side, controllers can identify which parts of the project are driving cost overruns, and focus their attention there.
Why WBS matters for controlling: Without a robust WBS (and properly managed change control on it), it’s nearly impossible to do precise variance reporting and performance tracking later on. The WBS ensures all scope and costs are captured in a structured way, so that as the project progresses, you can compare planned vs actual at various levels of detail (project total, phase, work package). It also helps assign responsibility – often each major WBS element has an owner (as in formal EVM, a Control Account Manager responsible for that scope, schedule, and budget segment). This clarity means that when variances occur, you can quickly pinpoint where (in which WBS element or control account) and why, and then take action. [tensix.com], [tensix.com]

Gantt Charts: Visualizing the Schedule
Once the WBS defines what work is needed, the next step is defining when each part of the work happens. This is done through project scheduling, often visualized as a Gantt chart. A Gantt chart is a timeline view of the project’s tasks and milestones showing their start/end dates and dependencies. Each WBS element is broken into tasks (or work packages) that appear as bars on the Gantt timeline, illustrating how the project will progress over time. Essentially, a Gantt chart “fills in” the WBS with a schedule, mapping out the sequence and duration of all tasks needed to deliver the scope. [projectmanager.com]

Figure 1. Illustrative Gantt chart. Read from left to right: each horizontal bar shows a task’s planned timing and duration; arrows show dependencies; the highlighted chain represents the critical path; the dashed line marks the reporting status date; and the diamond marks the handover milestone.
For example, if WBS 3.0 “Construction” includes tasks like 3.1 Site Preparation, 3.2 Foundation, 3.3 Framing, etc., the Gantt chart will show each of these tasks on a calendar with the expected start and finish dates, and any dependencies between them (like Foundation must finish before Framing begins). This makes it easier to identify the critical path – the sequence of tasks that determine the project’s finish date – and manage deadlines and resource allocation accordingly. [projectmanager.com]
The Gantt chart is also used to set the schedule baseline. Once the timeline is agreed upon, it becomes the reference for measuring schedule performance. During project execution, actual progress can be recorded on the Gantt (e.g., percentage of each task completed), and compared to the baseline plan to see if tasks are ahead or behind schedule. Modern project management tools allow baseline vs actual comparisons, often highlighting tasks that are late or milestones that are slipping. [projectmanager.com]
Connecting schedule to cost: When each task or WBS element on the Gantt chart is associated with a portion of the budget (for example, via resource costs or cost-loaded activities), the schedule can produce a time-phased budget plan. This is the foundation of Planned Value (PV) used in EVM. In other words, the Gantt chart + WBS + cost estimates yield the project’s planned spending over time, often called the Performance Measurement Baseline (PMB). Now we know what work is planned, when it’s planned to happen, and how much we budget for it at each stage. [gatherinsights.com]

Earned Value Management (EVM): Integrating Scope, Schedule & Cost Performance
With the scope and plan in place via the WBS and Gantt, how do we objectively measure project performance during execution? This is where Earned Value Management (EVM) comes in. EVM is a project performance measurement technique that integrates scope, schedule, and cost to give a comprehensive view of project health. In essence, EVM allows project controllers to answer: [6sigma.us]
Are we ahead or behind schedule?
Are we under or over budget?
Given our progress and spending so far, what is our likely final cost (EAC)?
To do this, EVM relies on three fundamental metrics, all derived from our WBS and baseline schedule/cost data and then updated with actual progress and costs:
Planned Value (PV) – the authorized budget for work planned to be done up to a given time. PV (also called Budgeted Cost of Work Scheduled, BCWS) tells how much value we intended to complete by now, according to the baseline plan. It is computed from the cost-loaded schedule: for each time period (e.g., month) you sum the budgets of all tasks that were supposed to be completed by that date. [6sigma.us]
Earned Value (EV) – the budgeted value of work actually completed to date (also called Budgeted Cost of Work Performed, BCWP). This is calculated by applying the planned budget to the percent of work actually finished. EV indicates how much of the planned work (in terms of value) has been earned by the project’s accomplishments so far. If a task was planned to cost $10k total and is 50% done, you have “earned” $5k worth of value on that task so far, contributing $5k to your EV. [6sigma.us]
Actual Cost (AC) – the actual money spent on the project work by that date (also called Actual Cost of Work Performed, ACWP). AC is gathered from the project’s financial systems (invoices paid, salaries, etc.). [6sigma.us]
By comparing these three values, EVM provides quantitative performance metrics that combine schedule and cost perspectives:
Key EVM Performance Metrics (and their interpretation in controlling/reporting):
Schedule Variance (SV) = EV – PV. If SV is positive, more work has been completed than planned (ahead of schedule); if SV is negative, less work has been done than planned (behind schedule). SV is measured in currency (or work hours) – it shows the value of work you are ahead or behind. [6sigma.us], [gatherinsights.com]
Schedule Performance Index (SPI) = EV / PV. This is an efficiency ratio for schedule. SPI > 1.0 means the project is progressing faster than planned (getting more work done per time than expected), while SPI < 1.0 means the project is progressing slower (schedule delay). [6sigma.us]
Cost Variance (CV) = EV – AC. If CV is positive, the project is under budget (it has spent less than budgeted for the work completed—a favorable outcome); if CV is negative, the project has a cost overrun (it has spent more than planned for the work completed so far). For example, if EV = $40k and AC = $45k at a certain point, CV = -$5k, indicating that the project is $5k over budget for the work performed. [6sigma.us], [gatherinsights.com] [6sigma.us]
Cost Performance Index (CPI) = EV / AC. This is an efficiency ratio for cost. CPI = 1.0 means you’re exactly on budget; CPI > 1.0 means cost performance is better than planned (delivering value for less cost); CPI < 1.0 means you are getting less value for each dollar spent (cost overrun). For instance, with EV $40k and AC $45k, CPI = 0.89, indicating that you are only getting $0.89 worth of planned work for each $1 spent (an inefficiency). [6sigma.us]
EVM in reports: When reporting to stakeholders, project controllers use SV and SPI to discuss schedule status, and CV and CPI to discuss cost status. For example, “We are currently 10% behind schedule (SPI = 0.90, meaning we’re only completing 90% of the planned work each week), but costs are on track (CPI = 1.00, spending matches budget) at this point.” These metrics help identify problem areas early, so managers can take corrective action. In formal EVM systems, they often analyze performance at control account (key WBS element) level first, then roll up to total project metrics. This way, a poor overall CPI or SPI can be traced to the specific WBS segment causing it, and project controllers or managers can focus on those issues. [gatherinsights.com]
EVM S-Curve: Visualizing Performance Over Time
A powerful way to present EVM data for reporting is the EVM S-curve chart. This is a cumulative graph of PV, EV and AC over time, which typically forms an “S” shape (since many projects start slow, accelerate, then slow down near completion). Such a chart is essentially a visual dashboard of integrated scope, schedule, and cost performance: [gatherinsights.com]

Figure 2. Illustrative EVM S-curve. At the status date, EV below PV indicates less work has been completed than planned, while AC above EV indicates that the cost incurred exceeds the budgeted value of the completed work. The vertical gaps correspond to schedule variance (SV = EV − PV) and cost variance (CV = EV − AC).
In the illustrative S-curve above (at the status date marked by the vertical line), we see that the EV curve is below the PV curve – meaning the project has accomplished less work than planned up to that point (a negative SV, behind schedule). Meanwhile, the AC curve is above the EV curve, indicating the project has spent more money than the value of work completed (a negative CV, i.e. cost overrun). [gatherinsights.com]
Project controllers use such visualizations to quickly communicate performance. The S-curve highlights both schedule and cost performance in one view. Ideally, all three lines (PV, EV, AC) stay close together – any significant divergence (gaps) is a red flag requiring management attention. For example, if EV is substantially below PV and AC, the project is both late and overspending. The project manager or controller would then investigate which WBS elements (which parts of the project) are causing the delays or overruns, so targeted corrective action can be taken. [gatherinsights.com]

Estimates, Forecasts & Variance Reporting in Project Control
While tracking current performance is vital, project controlling is also about looking forward. Projects rarely go exactly as planned – changes occur and performance can deviate from the baseline. Controllers therefore update forecasts and Estimate at Completion (EAC) to predict the likely total cost of the project upon completion. EAC is essentially the current forecast of the final project cost, combining actual costs to date with an updated estimate for remaining work. EAC can be calculated using different methods (e.g. dividing the total original budget by the current CPI if we expect current performance to continue, or adding Actual Cost (AC) to a new Estimate to Complete (ETC) based on revised plans). A closely related metric is Variance at Completion (VAC), often defined as BAC – EAC: the difference between the original budget (BAC, Budget at Completion) and the new forecast. A negative VAC (or a reported “over budget” variance) signals the project will exceed the budget unless corrected. [gatherinsights.com]
In the dashboard-style project controls view, these concepts come together:
At the project level, stakeholders see total Budget vs Current EAC and a resulting Variance. For example, “Budget 3.95M, EAC 4.58M, Over Budget by 0.63M” indicates a projected cost overrun of £0.63M, allowing management to quickly grasp that the project is trending over budget.
Change orders (approved scope changes) are reflected by adjusting the budget or current contract value, so controllers can differentiate between overruns due to scope changes versus pure inefficiencies. For instance, a project might be 19% over its original budget due to change orders – this suggests some cost increases were approved scope expansions (not just overruns) and thus informs how we interpret variances.
Commitments vs Actuals: The dashboard might show how much cost is already committed (under contract) and how much is actually spent. For example, “Committed: £4.09M (89% of EAC)” tells us that 89% of the forecasted cost is already under contract – this means future cost flexibility is limited. [gatherinsights.com]
Payment (Progress) bars illustrate the percent of budget or contract already expended for each WBS element, giving a quick sense of progress vs plan for each category (e.g., Planning phase 80% paid vs budget, etc.).
From a controlling/reporting perspective, these combined metrics let project controllers answer the big questions:
Are we on track to deliver the scope on time? (Check Schedule vs current progress: milestones and SV/SPI).
Are we within budget or heading for an overrun? (Check Actuals vs Budget: CV/CPI for efficiency, plus EAC vs Budget for forecasted outcome).
Where are the problem areas? (Look at which WBS elements have large variances or low performance indices, investigate causes – e.g., a specific phase has a CPI of 0.80, meaning severe cost overrun in that area).
Have there been significant scope changes? (Look at change orders and how they’ve affected the budget and schedule).
What decisions or actions are needed? (E.g., increase budget, adjust scope, accelerate schedule, reallocate resources).
By combining WBS, Gantt, and EVM data, project controllers create holistic reports and dashboards that connect scope, schedule, cost, and performance. This integrated view provides clarity for decision-making at all levels. Let’s summarize how these pieces fit together in a typical project control process:

How WBS, Gantt & EVM Work Together: Connecting Scope, Time, Cost & Performance
By following the process described above, the project team ensures that scope, schedule, and cost are planned together and then controlled together during execution. Here’s how they reinforce each other:
WBS provides the structure for all project work and is used to organize budget and cost tracking. It ensures full scope coverage and ties financial data (budgets, expenditures) to specific deliverables or phases.
The Gantt schedule uses the WBS to sequence and time-phase the work, creating the planned timeline and milestones. Combined with WBS budgets, it produces the planned value (PV) curve (i.e., how we expect to burn through the budget over time). This planned schedule and cost baseline is the reference point for performance measurement. [gatherinsights.com]
EVM then measures performance by comparing what was planned (PV) vs what has been accomplished (EV) vs what has been spent (AC). This single system yields both schedule performance (through SV/SPI) and cost performance (through CV/CPI) in one integrated framework. EVM answers “Are we on track on both time and money?” in quantifiable terms. [gatherinsights.com]
Project control dashboards bring it all together. They present high-level metrics (e.g. total EAC vs Budget with a variance) as well as detailed WBS-level breakdowns (budget, actual, forecast per component). Visual elements (S-curves, bar charts, pie charts of budget breakdown) help stakeholders quickly see status. For instance, a pie chart may show the budget distribution across WBS categories (Planning, Design, Construction, etc.), while bar indicators show payment or progress % in each category, and traffic-light colors highlight over-budget or delayed items.
Using such integrated reports, project controllers and managers can proactively manage the triple constraints. If EVM metrics show a problem (like CPI < 1 or SPI < 1), they’ll review the WBS line items to find which scope elements are causing the issues. They might then reprioritize tasks, reallocate resources, approve necessary changes, or update the schedule – thus closing the loop back to adjusting scope, time, and cost. [gatherinsights.com]

Chris Croft’s Twelve Steps to Managing a Project Successfully
This section adapts the twelve-step method taught by Chris Croft in Project Management Simplified. The approach is deliberately practical and lightweight: it combines network planning, critical-path analysis, contingency, resource planning, risk responses, Gantt-based monitoring, cost forecasting, communication, and review without creating excessive administrative overhead. Steps 1–8 establish the plan; Steps 9–12 guide action and control.
Chris Croft’s twelve-step project management method, adapted for this document
Phase Step Croft method Practical purpose and output
Planning 1 Define the project Agree the success criteria and major constraints with the customer in writing. Output: a clear, shared definition of project success and boundaries.
2 List the tasks Identify all work needed to produce the result. In this document, the task list can be organized through the WBS.
3 Estimate and plan dependencies Estimate time and cost for each task, identify dependencies, draw the activity network, and determine the critical path and float.
4 Add contingency Allow explicit time and cost reserves for uncertainty rather than assuming every estimate will be exact.
5 Consider crashing or overlapping Test whether critical activities can be shortened by adding resources or cost, or by overlapping work where the added risk is acceptable.
6 Draw the Gantt chart Convert the activity network into a time-scaled plan showing task bars, milestones, dependencies, and critical activities.
7 Calculate resource requirements Calculate resource demand over time and use the float of non-critical tasks to reduce overloads and level the plan.
8 Assess risks and prepare action plans Identify important risks and define both preventive actions to reduce likelihood and protective actions to reduce impact.
Action and control 9 Monitor progress against the Gantt chart Track actual progress and forecast dates, watching critical activities particularly closely.
10 Monitor cumulative cost Compare cumulative spending with the plan and forecast the likely final cost. EVM measures may be added where stronger integrated control is required.
11 Communicate progress and changes Communicate status, decisions, and changes; adjust the plan when evidence shows that corrective action or re-planning is necessary.
12 Review: learn and praise Capture lessons, recognize contributions, and carry useful learning into future projects.

Relationship to this document’s control model: Croft’s original method provides the practical management cycle. This document extends it by using a WBS to structure the task list, scope, accountability, and budget; a cost-loaded Gantt schedule to create the baseline; and EVM to strengthen Steps 9 and 10 with PV, EV, AC, SPI, CPI, and EAC. These are compatible enhancements, but EVM is not one of Croft’s original twelve steps. The resulting model retains the simplicity of Croft’s approach while adding more rigorous integrated control where project size, risk, or reporting requirements justify it.
Learning from Completed Projects with AI
Completed projects contain valuable knowledge in schedules, cost reports, EVM trends, risk and issue registers, change orders, decision logs, meeting notes, quality records, contracts, and close-out reviews. Traditional lessons-learned reports often fail because they depend on memory, use inconsistent formats, and are stored where future teams cannot readily find or apply them. AI can reduce this gap by processing both structured and unstructured records, identifying recurring patterns, and turning evidence into searchable, reusable recommendations. The objective is not to replace expert judgment, but to augment it with faster retrieval, cross-project comparison, and more consistent analysis.
An AI-Enabled Knowledge Cycle
AI-enabled learning cycle for completed projects
Stage AI-supported activity Human control and output

1. Capture Ingest approved project records and extract text, tables, metadata, dates, WBS codes, risks, decisions, and outcomes. The project owner confirms the authoritative sources, access rights, retention rules, and completeness of the close-out package.
2. Normalize Standardize terminology and tag records by project type, phase, WBS, supplier, geography, technology, risk category, cause, impact, and result. Subject-matter experts approve the taxonomy and resolve ambiguous or conflicting labels.
3. Analyze Summarize evidence; cluster similar lessons; detect repeated delays, overruns, defects, scope changes, and risk triggers; compare planned and actual performance. The review team validates causality, distinguishes correlation from evidence, and records confidence and exceptions.
4. Convert to action Draft concise lessons, root-cause questions, preventive actions, protective actions, checklists, estimating factors, and SMART recommendations. Named owners approve each recommendation, due date, applicability condition, and success measure.
5. Retrieve Use semantic search or retrieval-augmented generation to answer questions from authorized project evidence and return the most relevant precedents. Users receive source-grounded answers with project context, limitations, and traceability to the underlying records.
6. Reuse and improve Surface relevant lessons during initiation, estimating, planning, procurement, risk workshops, and control reviews; track whether recommendations were adopted. The PMO measures effectiveness, removes obsolete guidance, and updates standards, templates, and models.

Recommended technical pattern: Store the approved close-out package in a governed repository, create a searchable index, enrich the content with metadata and AI extraction, and use retrieval-augmented generation (RAG) so responses are grounded in the organization’s own records rather than generated from general model knowledge. A Microsoft-oriented implementation can use SharePoint or Azure storage for source records, document extraction and indexing services for knowledge mining, and an approved language model for summarization and question answering. The same pattern can support local or hybrid models where confidentiality, latency, sovereignty, or cost requires it.
What AI Can Discover
Estimating knowledge: systematic optimism or underestimation by WBS, discipline, supplier, or project type; better reference-class ranges for duration and cost.
Schedule knowledge: recurring critical-path bottlenecks, approval delays, dependency failures, effective crashing choices, and where contingency was used.
Cost knowledge: common drivers of poor CPI, change-order growth, procurement leakage, forecast error, and work packages with repeated overruns.
Risk knowledge: early warning signals, frequently realized risks, effective preventive and protective actions, and risks that were repeatedly missed.
Delivery knowledge: practices associated with good quality, fewer defects, faster decisions, stronger handovers, and improved stakeholder outcomes.
Governance and Quality Safeguards
AI-generated lessons should be treated as proposals until reviewed. The knowledge process must protect commercial, personal, security-sensitive, and contractual information; enforce role-based access; respect retention and data-residency requirements; and record source provenance, model version, review status, and approval history. Teams should test for hallucination, incomplete evidence, bias, duplicated lessons, and false causal claims. Human-in-the-loop validation is essential because experienced reviewers understand context, incentives, exceptional events, and tacit knowledge that may not appear in the records.
Suggested measures: percentage of projects with complete close-out data; time required to produce a reviewed lessons package; search success rate; percentage of new projects consulting relevant precedents; adoption rate of approved recommendations; reduction in repeated risks, schedule slippage, and cost variance; and user ratings of relevance and trust. These measures keep the focus on organizational learning and improved delivery—not merely on the volume of documents indexed or AI summaries produced.
Draft Workflow for a Simple Excel Project-Control System
The following draft shows how brainstorming can be converted into a controlled schedule and cost baseline in one simple Excel workbook. The design deliberately uses one task table as the source for the WBS, critical-path logic, safety margin, resources, Gantt chart, cost plan, and EVM reporting, avoiding duplicate data entry.

Figure 3. Draft workflow for a simple Excel-based project-control system. The Gantt chart and EVM S-curve use the same task, date, budget, progress, and actual-cost data.
Minimum Workbook Design
Proposed Excel workbook structure
Sheet Purpose Minimum fields or outputs

1. Setup Hold project-level controls and lists. Project name, start date, status date, calendar, contingency policy, reporting period, and resource names or rates.
2. Task Plan Act as the single source of task data. WBS, task, predecessor, duration, planned start and finish, early and late dates, float, critical flag, safety margin, resource, quantity or hours, rate, BAC, baseline dates, actual dates, percent complete, and AC.
3. Gantt Display the time-phased plan and status. Date grid with separate formatting for baseline bars, current forecast bars, actual progress, milestones, critical tasks, and the status date.
4. EVM Summarize performance by reporting period. Cumulative PV, EV, and AC; SV, CV, SPI, CPI, BAC, EAC, ETC, and VAC; line chart for the EVM S-curve.
5. Dashboard Present the management view. Key milestones, critical-path status, contingency remaining, resource exceptions, SPI, CPI, EAC, top variances, Gantt excerpt, and S-curve.

How the two visuals complement each other: The Gantt chart explains where and when schedule variance occurs by showing task-level timing, dependencies, critical path, baseline, forecast, and actual progress. The EVM S-curve explains how much integrated schedule and cost performance has diverged by comparing cumulative PV, EV, and AC. Both must be generated from the same WBS codes, baseline dates, task budgets, progress rules, actual costs, and status date. Excel can present a Gantt view using task dates and charting or conditional formatting, while a line or scatter chart can display cumulative PV, EV, and AC over time.
Keep the first version simple: use finish-to-start dependencies only, one accountable resource per task, workdays as durations, one approved baseline, a single status date, and a straightforward percent-complete rule. Add advanced features—multiple calendars, leads and lags, resource optimization, probabilistic schedules, or automated imports—only after the basic workbook is reliable and consistently maintained.
Conclusion & Key Takeaways for Project Controllers
In summary, WBS, Gantt charts, and EVM operate together as pillars of a solid project control system. The WBS defines what work is to be done (scope & deliverables) and underpins how we structure budgets and measure progress. The Gantt chart defines when each piece of work is done (timeline & dependencies, or schedule). Then EVM overlays how well we are doing in terms of both schedule and cost performance, by comparing planned vs earned vs actual values.
Project controlling and reporting use these tools in tandem to provide transparency and actionable insights on project health. A project control dashboard (such as the one exemplified) will tie WBS elements to financials and schedule metrics – showing the budget, actual spend, forecast (EAC), and variances at both summary and detailed levels. EVM’s performance metrics (SV, CV, SPI, CPI) are essential KPIs on such dashboards, instantly flagging behind-schedule or over-budget situations and enabling the team to forecast the final outcome and take corrective actions early. [gatherinsights.com]
For project controllers and managers, the key is to use this integrated approach to monitor trends and exceptions:
Watch the performance indices: If CPI or SPI drop below 1.0, identify which WBS areas are driving the inefficiencies and address them.
Update forecasts regularly: Use current EV and AC data to update EAC – this keeps stakeholders informed if the project will meet or exceed its budget.
Leverage visuals like S-curves and dashboards to communicate complex data in a comprehensible way. For instance, an EVM S-curve quickly reveals if you’re off track in cost or schedule by the gaps between PV, EV, and AC lines, and WBS-based budget tables show exactly where those gaps originate. [gatherinsights.com]
Balance the triple constraint: Always consider how any control decision (e.g., adding resources or cutting scope) impacts the project triangle of time, cost, scope. [en.wikipedia.org]
By mastering this conceptual model connecting scope, schedule, cost, and performance, project professionals can ensure better control and more insightful reporting, ultimately increasing the likelihood of project success through timely intervention and informed decision-making.
Glossary
Term Meaning
AC — Actual Cost The realized cost incurred for work performed by the status date.
BAC — Budget at Completion The total approved budget for the project or control account.
Control Account A management point where scope, schedule, budget, actual cost, and performance are integrated and assigned to an accountable owner.
CPI — Cost Performance Index Cost-efficiency ratio calculated as EV ÷ AC. A value below 1.0 indicates unfavorable cost performance.
CV — Cost Variance The difference between earned value and actual cost: EV − AC. A negative result indicates a cost overrun.
EAC — Estimate at Completion The current forecast of the project’s total final cost.
ETC — Estimate to Complete The expected cost required to finish the remaining work.
EV — Earned Value The approved budgeted value of work actually completed by the status date.
EVM — Earned Value Management A method that integrates scope, schedule, and cost to measure performance and forecast outcomes.
Gantt Chart A time-scaled schedule view in which task bars show planned or actual start dates, finish dates, durations, dependencies, and milestones.
Milestone A zero-duration schedule point representing a significant event, approval, or deliverable.
PMB — Performance Measurement Baseline The time-phased scope, schedule, and budget plan against which performance is measured.
PV — Planned Value The approved budget assigned to work scheduled to be completed by the status date.
S-Curve A cumulative chart of cost, value, progress, or resources over time; in EVM, it commonly compares PV, EV, and AC.
SPI — Schedule Performance Index Schedule-efficiency ratio calculated as EV ÷ PV. A value below 1.0 indicates unfavorable schedule performance.
SV — Schedule Variance The difference between earned value and planned value: EV − PV. A negative result indicates less work completed than planned.
VAC — Variance at Completion The expected budget difference at completion, commonly calculated as BAC − EAC.
WBS — Work Breakdown Structure A hierarchical decomposition of the total project scope into deliverables, work packages, and manageable components.
Work Package A defined unit of scope at the lowest practical WBS level that can be planned, budgeted, assigned, and controlled.
Best-Practice Guidelines for Excel Financial Analytics and Controlling
The following guidelines complement the project-control workbook and draw on the introductory financial-modeling themes associated with Giles Male’s Intro to Financial Modeling: forecasting, flows and balances, integrated statements, and disciplined model construction. The goal is a workbook that is simple to operate, transparent to review, and dependable for budgeting, forecasting, financial analysis, and management control.
Recommended Excel financial-model architecture
Tab group Purpose Typical content
00_Cover & Guide Explain how to use, update, and review the model. Purpose, owner, version, status date, units, sign convention, color key, tab map, update sequence, approval status, and change log.
01_Inputs Provide a controlled location for editable assumptions. Scenario selector, dates, rates, volumes, prices, inflation, exchange rates, resource rates, budget assumptions, tax, working-capital days, and contingency assumptions.
02_Actuals Store imported or approved historical data separately from forecasts. General-ledger actuals, invoices, commitments, payroll or hours, progress, balances, and source-system references.
03–06_Calculations Convert inputs and actuals into forecasts and control measures. Revenue or funding build, cost build, headcount and resource schedules, depreciation, working capital, debt, cash, project schedule, EVM, and scenario logic.
07_Financial Statements Show connected financial flows and closing balances. Income statement, balance sheet, cash-flow statement, or project equivalents such as budget, commitments, accruals, forecast, cash, and funding.
08_Checks Make errors and broken links visible. Balance checks, cash reconciliation, opening-to-closing roll-forwards, sources-equal-uses, control totals, duplicate tests, missing-data flags, and reasonableness tests.
09_Outputs Present decision-ready information without editable assumptions. Budget versus actual, forecast, variance, cash outlook, EAC, SPI, CPI, Gantt, S-curve, trend charts, scenarios, sensitivities, and management commentary.

Model-Building Guidelines
Design from the decision backward. State the questions the model must answer, the required outputs, users, reporting frequency, level of detail, and acceptable accuracy before building formulas.
Separate inputs, calculations, checks, and outputs. Users should know where values may be changed, where formulas run, where errors appear, and where results are consumed. Keep data flowing mainly from left to right and from earlier tabs to later tabs.
Use one source of truth for each assumption. Enter a driver once and reference it everywhere. Avoid hard-coded numbers inside formulas; assumptions such as escalation, productivity, contingency, tax, or payment terms should live in labelled cells.
Build a consistent time axis. Put dates in chronological columns, use real Excel dates rather than text labels, and select a periodicity—weekly, monthly, quarterly, or annual—that matches the decision. Clearly separate historical actuals, the status date, the current forecast, and outer years.
Distinguish flows from balances. Revenue, cost, cash receipts, payments, and project expenditure are flows measured over a period; cash, receivables, payables, inventory, debt, commitments, and remaining contingency are balances at a point in time. Opening balance + movements = closing balance should be explicit.
Make forecasts driver-based. Link forecast values to observable operational drivers such as price × volume, hours × rate, units × unit cost, headcount × salary, or schedule progress × budget. Use scenarios for uncertainty rather than overwriting the base case.
Reconcile budget, forecast, and actuals. Preserve the approved baseline, record authorized changes separately, and calculate the current budget, actual-to-date, commitments, estimate to complete, estimate at completion, and variance at completion without destroying prior versions.
Use consistent formulas and formatting. Keep one logical formula across each time row, use consistent units and decimal precision, label totals and subtotals, avoid unnecessary merged cells, and apply a documented color convention—for example, blue font for editable inputs, black for formulas, green for links, and red for warnings.
Include independent checks. A financial model is not complete without visible control tests. Examples include Assets = Liabilities + Equity, opening cash + net movement = closing cash, total WBS detail = project total, cumulative PV at completion = BAC, and sources = uses.
Keep outputs concise. Dashboards should focus on decisions and exceptions: budget versus actual, rolling forecast, cash, variance drivers, critical milestones, EAC, CPI, SPI, risks, and required actions. Do not turn the dashboard into another calculation sheet.
Document ownership and changes. Record the model owner, data owners, refresh sequence, review date, version, approved scenario, and material changes. Protect formula areas and use controlled filenames rather than emailing multiple uncontrolled copies.
Prefer simplicity and auditability. A shorter transparent formula is usually better than a clever formula that only its author understands. Complexity should be justified by a decision need, not by technical possibility.
Application to Budgeting and Project Controlling
For the workbook proposed in this document, the Setup and Inputs tabs hold the approved project calendar, status date, rates, assumptions, resource lists, and scenario controls. The Task Plan, cost schedules, and EVM engine perform calculations. The Checks tab verifies the WBS totals, baseline, cumulative PV, EV, AC, and opening-to-closing balances. The Gantt, EVM, and Dashboard tabs present outputs only. This architecture supports budgeting and rolling forecasts while preserving traceability from each management output back to its source assumption, actual transaction, task, and WBS code.
Recommended review rhythm: update actuals and progress on a fixed reporting date; lock the status date; refresh calculations; resolve all control checks; compare actual, budget, and forecast; review cash and resource implications; document major variances and assumptions; approve changes through governance; and publish a clearly versioned output pack. The workbook should never mix unapproved forecast changes with the approved baseline.
Key Excel Project-Controlling Principles
Use one integrated data structure
Link the WBS, schedule, budget, resources, actual costs, progress, and forecasts through consistent codes.
Separate workbook functions
Keep inputs, imported actuals, calculations, checks, and management outputs on distinct tabs.
Maintain a single source of truth
Enter each assumption, date, rate, and project value once; reference it rather than duplicating or hard-coding it.
Control the time dimension
Use real Excel dates, a consistent reporting period, and one clearly defined status date across the Gantt, cost forecast, and EVM calculations.
Protect the approved baseline
Keep the original baseline separate from approved changes, the current control budget, and the latest forecast.
Integrate schedule and cost
Time-phase the WBS budget through the Gantt schedule to produce Planned Value and compare it with Earned Value and Actual Cost.
Track complete cost exposure
Distinguish between actual costs, commitments, accruals, estimate to complete, estimate at completion, contingency, and remaining budget.
Use driver-based forecasts
Base forecasts on measurable drivers such as hours × rate, quantity × unit cost, progress × budget, or resource demand over time.
Make calculations transparent
Use short, consistent formulas, structured tables, clear labels, documented assumptions, and a standard formatting convention.
Build visible control checks
Include reconciliation tests for WBS totals, baseline values, source data, cumulative PV–EV–AC, opening and closing balances, missing dates, duplicate codes, and broken dependencies.
Report exceptions and trends
Dashboards should emphasize critical-path changes, milestone slippage, budget-versus-actual variance, CPI, SPI, EAC, contingency use, cash outlook, and required actions.
Preserve auditability
Record model ownership, data sources, refresh dates, version history, approved changes, assumptions, and management commentary.
Use Power Query where practical
Automate the import and normalization of actual-cost and progress data instead of repeatedly copying and pasting.
Keep the solution proportionate
Excel works best for controlled, understandable models. Move to a specialist project-controls system when volume, collaboration, security, audit-trail, or workflow requirements exceed spreadsheet capability.
Common Excel Errors in Project Controlling
Hard-coded values inside formulas
Budgets, rates, dates, or percentages are embedded directly in calculations instead of referenced from controlled input cells.
Mixed inputs and formulas
Editable assumptions, imported actuals, calculations, and outputs are combined on the same sheet, increasing overwrite risk.
Inconsistent WBS or cost codes
Schedule tasks, budgets, commitments, actual costs, and forecasts use different coding structures, preventing reliable reconciliation.
Text stored as dates or numbers
Dates and costs appear correctly but are stored as text, causing sorting, filtering, time-phasing, and aggregation errors.
Inconsistent status dates
The Gantt, percent complete, actual costs, forecasts, and EVM calculations use different reporting cut-off dates.
Overwriting the baseline
Current forecasts replace original planned dates or budgets, making true variance analysis impossible.
Uncontrolled budget changes
Approved changes, pending changes, transfers, and forecast overruns are mixed together.
Double-counting costs
Actuals, commitments, accruals, purchase orders, and forecasts overlap without clear definitions.
Incorrect EVM time-phasing
Planned Value is spread evenly without reflecting task timing, resource profiles, milestones, or valid earning rules.
Subjective percent-complete estimates
Progress is reported without measurable completion criteria, producing unreliable Earned Value.
Broken dependencies
Tasks have missing, circular, invalid, or manually overridden predecessor logic.
Incorrect critical-path calculations
Critical tasks are identified only by color or finish date rather than by network logic and total float.
Hidden formula inconsistencies
One cell in a time-series row contains a different formula from the surrounding cells.
Incorrect absolute and relative references
Formulas shift to the wrong row, column, rate, or date when copied.
Unprotected formula cells
Users can accidentally overwrite calculation logic or control totals.
Broken external links
Formulas depend on renamed, moved, inaccessible, or outdated workbooks.
Manual copy-and-paste updates
Actual-cost and progress data are repeatedly pasted into the model, increasing omission, duplication, and version errors.
Duplicate or missing records
Transactions, tasks, WBS codes, invoices, or resources are repeated or omitted.
Incorrect units or currencies
Hours, days, percentages, thousands, full currency amounts, and exchange rates are mixed without clear conversion.
Sign-convention errors
Costs, savings, variances, cash outflows, and contingency use switch between positive and negative conventions.
Missing reconciliation checks
WBS totals do not agree with project totals, cumulative PV does not equal BAC at completion, or opening balances do not roll forward correctly.
Misleading charts
Gantt bars and S-curves use different dates or datasets, cumulative and periodic values are mixed, or chart axes conceal important variance.
Excessive workbook complexity
Long nested formulas, volatile functions, duplicated sheets, and unnecessary macros make the model difficult to review and maintain.
No version or change control
Users cannot determine who changed the model, which forecast is approved, or which file is current.
No Excel exit threshold
The workbook continues to be used after project volume, collaboration, security, approval, or audit requirements exceed spreadsheet capability.
Best Practices for Excel Project Dashboards
Design for decisions
Show only information that supports action, escalation, approval, or forecasting.
Use one reporting date
Apply the same status date to schedule progress, costs, forecasts, and EVM.
Connect all visuals to the same data
The Gantt chart, S-curve, variance tables, and KPIs should use consistent WBS codes, budgets, dates, and actuals.
Prioritize key indicators
Include BAC, actual cost, commitments, EAC, VAC, CPI, SPI, contingency remaining, milestone status, and forecast completion date.
Focus on trends and exceptions
Highlight worsening performance, critical-path slippage, major variances, resource conflicts, and risks requiring decisions.
Separate summary from detail
Keep the main dashboard concise, with supporting detail available by WBS, work package, supplier, period, or cost category.
Use appropriate visuals
Gantt excerpt for schedule status
PV–EV–AC S-curve for integrated performance
Variance bars for budget versus forecast
Trend lines for CPI, SPI, and EAC
Tables for actions and explanations
Use color consistently
Apply a limited traffic-light convention with defined thresholds. Never rely on color alone—also use labels, symbols, or variance values.
Show baseline, actual, and forecast separately
Do not overwrite approved budget or schedule values with current forecasts.
Provide context for every KPI
Show current value, target or baseline, prior-period value, trend, reporting date, and threshold.
Include management commentary
Explain the cause, impact, corrective action, owner, and due date for significant exceptions.
Add data-quality checks
Display warnings for missing dates, duplicate WBS codes, incomplete actuals, broken formulas, or failed reconciliations.
Optimize dashboard performance
Use structured tables, efficient formulas, PivotTables, and Power Query; avoid unnecessary volatile formulas and duplicated calculations.
Keep formatting clean
Use aligned sections, consistent units, readable labels, restrained colors, and minimal decoration.
Preserve traceability
Users should be able to trace every dashboard value back to its source record, assumption, task, or calculation.
Document refresh and ownership
Display the model version, owner, data refresh time, reporting period, approval status, and selected scenario.
Recommended Project Dashboard KPIs
Executive Summary
Overall RAG status — combined cost, schedule, scope, risk, and quality condition
Forecast completion date
Budget at Completion (BAC)
Estimate at Completion (EAC)
Variance at Completion (VAC) = BAC − EAC
Contingency remaining
Top management decision required
Schedule
Schedule Performance Index (SPI) = EV ÷ PV
Schedule Variance (SV) = EV − PV
Milestones completed on time (%)
Critical-path delay
Forecast finish variance
Number of overdue critical tasks
Total float remaining
Tasks completed versus planned
Cost and Forecast
Actual Cost (AC)
Committed cost
Accrued cost
Cost Performance Index (CPI) = EV ÷ AC
Cost Variance (CV) = EV − AC
Estimate to Complete (ETC)
Forecast variance by WBS
Cash-flow variance
Uncommitted budget remaining
Scope and Change
Approved change value
Pending change value
Change value as a percentage of BAC
Number of open change requests
Scope completed (%)
Requirements or deliverables accepted (%)
Risk and Contingency
Total open risks
High-priority risks
Risk exposure trend
Contingency used
Contingency remaining
Overdue mitigation actions
Realized risk cost and schedule impact
Resources
Resource utilization
Overallocated resources
Planned versus actual hours
Forecast resource gap
Labor-rate variance
Productivity variance
Quality and Delivery
Deliverables accepted
Open defects or non-conformances
Rework cost
First-time approval rate
Overdue quality actions
Customer or stakeholder acceptance status
Governance and Data Quality
Overdue decisions and actions
Unresolved control-account variances
Missing progress updates
Failed data-quality checks
Days since last refresh
Forecast approval status
Reporting package submitted on time
For a simple executive dashboard, I recommend limiting the first page to 10–12 KPIs: overall status, forecast finish date, BAC, EAC, VAC, contingency remaining, SPI, CPI, milestone status, critical-path delay, top risk exposure, and required management action.
Tools to Reduce Excel Errors in Project Controlling
Excel Tables — structured ranges that expand automatically and use consistent formulas and references.
Data Validation — restrict entries to valid WBS codes, resources, dates, percentages, currencies, scenarios, and status values. [support.mi...rosoft.com]
Formula Error Checking — identifies inconsistent formulas, numbers stored as text, omitted cells, and unlocked formula cells; desktop Excel provides the fuller rule set. [support.mi...rosoft.com], [support.mi...rosoft.com]
Evaluate Formula — steps through a complex calculation to show where an incorrect result originates.
Trace Precedents and Trace Dependents — visually displays which cells feed a formula and which outputs depend on it. [support.mi...rosoft.com]
Watch Window — monitors important control cells such as BAC, EAC, CPI, SPI, contingency, and reconciliation totals while working elsewhere.
Conditional Formatting — flags missing fields, duplicate WBS codes, overdue tasks, negative float, failed checks, and out-of-range KPIs.
Worksheet Protection — locks formulas, baseline values, and control totals while leaving approved input cells editable. [support.mi...rosoft.com]
Power Query — imports, cleans, standardizes, combines, and refreshes actual-cost and progress data instead of relying on repeated copy-and-paste updates; its query-step diagnostics help investigate source errors. [support.mi...rosoft.com]
PivotTables and the Data Model — aggregate detailed transactions by WBS, period, supplier, resource, or cost category without duplicating formulas.
Named Ranges and Named Formulas — make important assumptions and control dates easier to understand and audit.
Structured References — reduce broken cell references by referring to table and column names instead of fixed ranges.
Excel Error Functions — use IFERROR, IFNA, ISERROR, ISNUMBER, ISTEXT, and ISBLANK carefully to detect invalid conditions; avoid using them merely to hide unresolved errors.
Duplicate and Missing-Record Checks — use COUNTIF, COUNTIFS, UNIQUE, FILTER, and XLOOKUP to identify duplicated WBS codes, unmatched transactions, or missing mappings.
Reconciliation Formulas — create dedicated checks such as WBS detail = project total, cumulative PV at completion = BAC, and opening balance + movements = closing balance.
Formula Consistency Checks — compare formulas across rows and periods or use FORMULATEXT to detect accidental changes.
Workbook Links and Connection Checks — review external links, query connections, and refresh errors before publishing reports.
Version History and Controlled Storage — use SharePoint or OneDrive versioning rather than circulating multiple uncontrolled workbook copies.
Change Log and Assumption Register — record who changed the model, what changed, why, when, and which forecast or baseline was approved.
Dedicated Checks Dashboard — summarize all failed controls in one place, using clear PASS/FAIL indicators and named owners for correction.
Framework for Project Control in Power BI
Power BI should become the governed reporting and analysis layer above the project’s operational sources—not another place for manual data entry. Excel can remain a controlled input or staging tool for smaller projects, while schedules, finance systems, procurement data, risk registers, resource records, and approved baselines feed a shared Power BI semantic model. The framework below preserves the document’s core principle: scope, schedule, cost, progress, forecast, risk, and change must be linked by consistent project, WBS, control-account, task, contract, resource, and date keys.

1. Define the Control Questions and Ownership
   Define the decisions the report must support: current status, forecast finish, final cost, critical-path exposure, change impact, resource constraints, cash requirements, risks, and corrective actions.
   Confirm the portfolio, project, control-account, and work-package levels at which performance will be reviewed.
   Assign owners for source data, the semantic model, measures, report pages, security, refresh monitoring, and monthly approval.
   Establish a common reporting calendar, status date, currency, units, sign convention, baseline definition, and KPI thresholds.
2. Build a Governed Data Pipeline
   Recommended Power BI project-control data pipeline
   Layer Purpose Typical content and controls
   Source systems Provide authoritative operational records. Approved baseline and current schedule, ERP actual costs and accruals, procurement commitments and changes, resource hours and rates, risk and issue registers, progress and earned-value inputs, and project master data.
   Staging and transformation Clean, standardize, map, and validate data before reporting. Power Query, dataflows, Fabric, or a data warehouse; standardized data types and currencies; WBS–cost-code mapping; deduplication; status-date controls; late-arriving actuals; and rejected-record logs.
   Semantic model Create one governed analytical model and measure library. Star schema, explicit relationships, date dimensions, approved DAX measures, KPI thresholds, calculation conventions, and row-level security.
   Reports and apps Deliver decision-focused views for different audiences. Executive, portfolio, project, cost, schedule, EVM, risk, change, resource, data-quality, and detailed drill-through pages.
   Governance and operations Keep the solution secure, current, controlled, and auditable. Workspaces, permissions, refresh schedules, gateways, monitoring, lineage, certification, deployment from development to test and production, usage review, and release notes.

3. Use a Project-Control Star Schema
   Use dimension tables for the entities by which users filter and group information, and fact tables for measurable events or periodic snapshots. Define the grain of every fact table explicitly—for example, one row per project–WBS–period for EVM or one row per transaction for actual costs. Prefer one-to-many, single-direction relationships from dimensions to facts, and avoid unnecessary many-to-many or bidirectional relationships.
   Suggested semantic-model tables
   Table type Suggested tables Key role in project control
   Dimensions Date, Project, WBS, Control Account, Task or Work Package, Organization, Resource, Supplier, Contract, Cost Category, Risk Category, Change Status, Currency, and Scenario or Baseline Version. Provide consistent hierarchies, labels, ownership, filtering, and drill paths across all reports.
   Schedule facts Baseline schedule, current forecast schedule, milestones, progress snapshots, float, critical flags, and resource assignments. Support baseline-versus-forecast comparisons, milestone trends, critical-path analysis, and task-level drill-through.
   Cost facts Approved budget, budget changes, actual transactions, accruals, commitments, cash payments, and forecasts. Support budget, actual, committed, cash, ETC, EAC, VAC, and cost variance reporting.
   EVM fact Periodic and cumulative PV, EV, and AC by project, WBS or control account, reporting period, and baseline version. Support SV, CV, SPI, CPI, EAC, ETC, VAC, and the integrated S-curve.
   Governance facts Risks, issues, changes, decisions, actions, quality records, and data-quality exceptions. Connect project performance to causes, responses, approvals, owners, and due dates.

4. Create a Governed Measure Library
   Baseline and forecast: Original BAC, approved changes, current control budget, AC, commitments, accruals, ETC, EAC, VAC, cash paid, cash forecast, and contingency remaining.
   EVM: PV, EV, AC, SV = EV − PV, CV = EV − AC, SPI = EV ÷ PV, CPI = EV ÷ AC, and selected EAC formulas with documented applicability.
   Schedule: Baseline finish, forecast finish, finish variance, milestones on time, overdue critical tasks, total float, critical-path delay, and schedule progress versus plan.
   Scope and change: Approved and pending change value, change as a percentage of BAC, open changes, accepted deliverables, and scope progress.
   Risk, resources, and quality: Risk exposure, overdue mitigations, resource utilization, overallocations, planned versus actual hours, quality defects, rework cost, and overdue actions.
   Data quality: Unmapped transactions, duplicate WBS codes, missing dates, stale updates, failed reconciliations, invalid status dates, and records excluded from reporting.
   Measures should be explicit, consistently named, stored in a dedicated measures table, described in business language, and tested against approved Excel control totals. Keep raw columns hidden when report users should consume a governed measure instead.
5. Design the Report as a Set of Control Views
   Recommended Power BI report pages
   Page Primary questions Suggested content
   Executive overview Are we on track, what is changing, and what decision is required? Overall status, forecast finish, BAC, EAC, VAC, contingency, CPI, SPI, milestone status, top risks, and management actions.
   Cost and forecast Where are variances and future cost exposure concentrated? Budget–actual–commitment–forecast waterfall, EAC bridge, variance by WBS and supplier, cash curve, and forecast commentary.
   Schedule and milestones Which activities or milestones threaten completion? Baseline versus forecast milestones, Gantt excerpt, critical tasks, float distribution, delay trend, and task-level drill-through.
   EVM How efficiently are cost and schedule being converted into completed scope? PV–EV–AC S-curve, CPI and SPI trends, SV and CV, EAC scenarios, and control-account variance analysis.
   Changes, risks, and actions What threatens the baseline, and who owns the response? Approved and pending changes, risk exposure, contingency use, issues, decisions, action owners, due dates, and aging.
   Resources and delivery Do capacity, productivity, and quality support the forecast? Resource demand and utilization, shortages, planned versus actual hours, productivity, deliverable acceptance, defects, and rework.
   Data quality and reconciliation Can management trust the report? Refresh status, source totals, reconciliation results, unmapped records, missing progress, duplicate keys, stale data, and failed controls.

6. Refresh, Security, and Lifecycle Controls
   Refresh: Align refresh timing with the reporting cut-off and source-system close. Use incremental refresh for large date-based fact tables when justified, and alert owners when a refresh or reconciliation fails.
   Date control: Use a dedicated, complete Date dimension; distinguish transaction date, accounting period, baseline date, forecast date, and status date. Do not mix them in one ambiguous relationship.
   Security: Apply least-privilege workspace permissions and row-level security when users should see only specified projects, business units, regions, or portfolios. Test every role before release.
   Lifecycle: Separate development, test, and production workspaces; promote only reviewed changes; retain release notes; certify approved semantic models; and avoid duplicating business logic across separate reports.
   Performance: Reduce unnecessary columns and granularity, preserve query folding where possible, prefer measures over avoidable calculated columns, and monitor slow pages, visuals, refreshes, and model growth.
7. Monthly Control Cycle
   Close the reporting period and lock the status date.
   Refresh schedule, progress, actual cost, commitment, accrual, risk, change, and resource data.
   Resolve failed loads, mappings, duplicate keys, missing records, and reconciliation differences.
   Validate totals against authoritative source reports and the approved baseline.
   Review critical path, milestone changes, forecast finish, PV, EV, AC, CPI, SPI, EAC, cash, contingency, and top risks.
   Record cause, impact, corrective action, owner, due date, and management decision for material exceptions.
   Approve the reporting package, publish the Power BI app, and preserve the period snapshot and commentary.
8. Staged Implementation Roadmap
   Practical Power BI implementation roadmap
   Stage Scope Exit criteria
9. Minimum viable control report One pilot project; governed Excel or source extracts; Project, WBS, Date, budget, actual, forecast, and progress tables; executive, cost, and EVM pages. Source totals reconcile, status date is consistent, core KPIs are approved, and users can trace dashboard values to WBS detail.
10. Integrated project control Automated finance and schedule feeds; commitments, changes, risks, resources, milestones, data-quality checks, and role-based access. Refresh is repeatable, security is tested, baseline changes are controlled, and the monthly cycle operates without manual rework.
11. Portfolio and advanced analytics Multiple projects, common taxonomy, benchmarks, historical snapshots, scenario analysis, forecasting, and AI-supported explanation or lessons retrieval. Portfolio definitions are standardized, performance is stable, model ownership is established, and analytics are demonstrably improving decisions.

What a Star Schema Is
A star schema is a data-modeling design in which:
Fact tables store measurable project-control events or snapshots.
Dimension tables describe the entities used to filter, group, and analyze those facts.
Each dimension connects directly to one or more fact tables, creating a star-like layout.
In Power BI, this design normally improves performance, usability, filtering behavior, and DAX simplicity. [learn.microsoft.com]

---

1. Dimension Tables
   Dimension tables answer questions such as:
   Which project?
   Which WBS element?
   Which reporting period?
   Which supplier?
   Which resource?
   Which cost category?
   Which baseline version?
   A dimension should normally contain:
   One unique key
   Descriptive attributes
   Hierarchies
   Categories used in slicers, rows, columns, and drill-downs
   For project control, useful dimensions include:
   Dimension Example attributes
   Project Project name, manager, portfolio, phase, status
   WBS WBS code, work package, control account, parent WBS
   Date Date, week, month, quarter, year, reporting period
   Supplier Supplier name, category, country
   Contract Contract number, type, package, owner
   Resource Resource, role, discipline, department
   Cost Category Labor, material, equipment, subcontract
   Baseline Version Original, approved revision, current baseline
   Risk Category Technical, commercial, schedule, safety
   Dimensions are generally relatively small compared with fact tables. Their purpose is to make facts understandable and filterable. [learn.microsoft.com]

---

2. Fact Tables
   Fact tables contain the numerical observations being analyzed.
   Examples include:
   Actual-cost transactions
   Monthly budget values
   Commitments
   Accruals
   Schedule snapshots
   Resource hours
   Risk exposure values
   Periodic PV, EV, and AC
   A fact table normally contains:
   Foreign keys linking to dimensions
   Dates
   Numeric amounts
   Quantities or hours
   Status or version identifiers
   For example, an EVM fact table might contain:
   Date Key Project Key WBS Key Baseline Key PV EV AC
   20260731 P101 WBS310 B01 500,000 440,000 470,000
   The dimension keys determine which analytical dimensions exist, while their values determine the fact table’s granularity. [learn.microsoft.com]

---

3. Grain: The Most Important Design Decision
   The grain defines exactly what one row represents.
   Examples:
   One row per accounting transaction
   One row per project–WBS–month
   One row per task–status date
   One row per resource–task–week
   One row per risk–reporting period
   Grain must be defined before loading data.
   For example:
   FactActualCost: one row per financial transaction
   FactEVM: one row per project–WBS–reporting period–baseline version
   FactScheduleSnapshot: one row per task–status date
   FactResourceHours: one row per resource–task–week
   Different grains should normally use different fact tables. Combining transactions, monthly summaries, and task snapshots in one table can produce duplication and incorrect totals.

---

4. Relationships
   The standard relationship is:
   Dimension: one → many :Fact
   For example:
   One project can have many cost transactions.
   One WBS element can have many EVM-period records.
   One date can relate to many actual-cost records.
   Filters normally flow from dimensions into fact tables. A project selection therefore filters every connected fact table consistently. Power BI relationships propagate these filters across the model; multiple filters are combined as an AND condition. [learn.microsoft.com]
   Preferred pattern
   One-to-many relationships
   Single-direction filtering
   Dimensions on the “one” side
   Facts on the “many” side
   Unique, nonblank dimension keys
   Use carefully
   Many-to-many relationships
   Bidirectional filtering
   Fact-to-fact relationships
   Ambiguous relationship paths
   These patterns are sometimes necessary, but they make filtering and totals harder to understand.

---

5. Conformed Dimensions
   A conformed dimension is shared by multiple fact tables.
   For example, the same Project, WBS, and Date dimensions can filter:
   Actual costs
   Budgets
   Commitments
   EVM
   Schedule snapshots
   Risks
   Resource hours
   This is what makes an integrated dashboard possible. Selecting one WBS element can simultaneously update cost variance, schedule milestones, PV–EV–AC, risks, and resource demand.
   The dimension must use the same definition across every source. If finance and scheduling use different WBS codes, a governed mapping process is required before the data enters the semantic model.

---

6. Date Dimensions
   A proper Date dimension contains one row for every date in the reporting range and attributes such as:
   Calendar date
   Week
   Month
   Quarter
   Year
   Fiscal period
   Reporting period
   Month-end flag
   Working-day flag
   Project controls frequently use several different dates:
   Transaction date
   Accounting date
   Baseline start and finish
   Forecast start and finish
   Actual start and finish
   Status date
   Risk due date
   Change approval date
   One Date dimension may play multiple roles. Usually, one relationship is active and the others are inactive, with DAX activating the correct relationship when needed. Alternatively, separate role-playing dimensions such as Accounting Date and Status Date can be used where this improves clarity.

---

7. Surrogate Keys
   A surrogate key is an internally generated identifier used to link dimensions and facts.
   Example:
   Project Key Project Code Project Name
   101 PRJ-0042 Terminal Upgrade
   The fact table stores 101, not necessarily the source-system project code.
   Surrogate keys help when:
   Different systems use different identifiers
   Business codes change
   Historical versions must be preserved
   Multiple sources contain overlapping keys
   Unknown or unmapped members must be handled

---

8. Slowly Changing Dimensions
   Some descriptive values change over time—for example:
   Project manager
   Organizational unit
   Supplier classification
   Project phase
   Control-account owner
   There are two common treatments:
   Type 1: overwrite the old value; suitable when history is not required.
   Type 2: add a new dimension row with effective dates; suitable when historical reports must retain the original classification.
   Power BI can model this, but Microsoft recommends considering a data warehouse and ETL process when large volumes or advanced slowly changing dimensions are required. [learn.microsoft.com]

---

9. Multiple Fact Tables
   A project-control model should usually have several facts rather than one enormous table.
   A practical structure is:
   FactBudget
   FactActualCost
   FactCommitment
   FactForecast
   FactEVM
   FactScheduleSnapshot
   FactResourceHours
   FactRisk
   FactChange
   Shared dimensions connect them conceptually.
   Do not join fact tables directly merely because both contain WBS or dates. Analyze them through shared dimensions and measures.

---

10. Star Schema Versus Snowflake Schema
    A star schema keeps descriptive attributes together in relatively denormalized dimensions.
    A snowflake schema splits dimensions into related subdimensions—for example:
    WBS → Control Account → Project
    Supplier → Supplier Category → Geography
    Snowflakes can reduce repeated data but introduce more relationships and more complex filter paths. For Power BI, a simpler, denormalized star is normally easier for users and measures. Microsoft describes indirect dimension relationships as characteristic of snowflake designs. [learn.microsoft.com]

---

11. Why It Helps DAX
    With a clean star schema, measures can remain concise:
    "Actual Cost"=∑▒( ├ "FactActualCost[Amount]" )
    "CPI"="EV" /"AC"
    "SPI"="EV" /"PV"
    The dimensions supply the filter context. The same Actual Cost measure automatically returns:
    Total-project cost
    Cost by WBS
    Cost by supplier
    Cost by month
    Cost by project and cost category
    This avoids building a separate formula for every dashboard view.

---

Figure 4. Illustrative Power BI project-control star schema. Shared dimensions filter multiple fact tables through one-to-many, single-direction relationships, enabling consistent analysis across cost, schedule, commitments, and EVM. 12. Example Project-Control Star
At the center:
FactEVM
FactActualCost
FactScheduleSnapshot
FactCommitment
Around them:
DimProject
DimWBS
DimDate
DimSupplier
DimContract
DimResource
DimCostCategory
DimBaseline
A WBS slicer filters all relevant facts. A month selection filters periodic cost, EVM, and schedule snapshots. A project selection restricts the complete dashboard to that project.

---

13. Common Modeling Errors
    Mixing facts and descriptions in the same wide table
    Combining fact tables with different grains
    Duplicate keys in dimensions
    Orphaned keys in fact tables
    Direct fact-to-fact relationships
    Excessive bidirectional filtering
    Many-to-many relationships used to mask poor source mappings
    Multiple ambiguous date paths
    Storing cumulative values without preserving period values
    Mixing baseline versions without a baseline dimension
    Using one giant flat Excel export as the final semantic model
    Power BI relationships do not themselves enforce source-data integrity, so these issues must be detected through transformations and reconciliation checks. [learn.microsoft.com]

---

Recommended Rule
For every table, write one sentence:
Dimension: “One row represents one unique **_.”
Fact: “One row represents one _** occurring for one **_ at one _**.”
Example DAX Measures for Project Control
The following examples assume a star schema with separate fact tables for budget, actual cost, commitments, forecasts, EVM, schedule snapshots, changes, and risks, plus shared Date, Project, WBS, and Baseline dimensions. Names should be adapted to the actual semantic model. Measures should be stored in a dedicated measures table and validated against approved source totals.
Core Cost and EVM Measures
Example DAX measures for cost and earned value
Measure Example DAX Purpose
BAC BAC = SUM ( FactBudget[ApprovedBudget] ) Returns the approved Budget at Completion in the current Project, WBS, and baseline filter context.
Actual Cost Actual Cost = SUM ( FactActualCost[Amount] ) Aggregates realized cost transactions.
Committed Cost Committed Cost = SUM ( FactCommitment[OpenCommitmentAmount] ) Shows remaining contractual exposure not yet recognized as actual cost.
PV PV = SUM ( FactEVM[PlannedValue] ) Returns Planned Value for the selected period and WBS scope.
EV EV = SUM ( FactEVM[EarnedValue] ) Returns the budgeted value of completed work.
AC AC = SUM ( FactEVM[ActualCost] ) Returns EVM actual cost at the same grain as PV and EV; reconcile it to the financial Actual Cost measure.
Schedule Variance Schedule Variance = [EV] - [PV] Shows whether less or more budgeted work has been earned than planned.
Cost Variance Cost Variance = [EV] - [AC] Shows the difference between earned value and cost incurred.
SPI SPI = DIVIDE ( [EV], [PV] ) Schedule efficiency; below 1.0 is unfavorable.
CPI CPI = DIVIDE ( [EV], [AC] ) Cost efficiency; below 1.0 is unfavorable.

Forecast and Exposure Measures
Example DAX measures for forecast and exposure
Measure Example DAX Purpose
ETC ETC = SUM ( FactForecast[EstimateToComplete] ) Returns the current bottom-up estimate for remaining work.
EAC Bottom-Up EAC Bottom-Up = [Actual Cost] + [ETC] Forecasts final cost using current actuals plus the approved remaining-work estimate.
EAC by CPI EAC by CPI = DIVIDE ( [BAC], [CPI] ) Assumes current cost efficiency continues for the remaining work.
EAC by CPI and SPI EAC by CPI and SPI = [AC] + DIVIDE ( [BAC] - [EV], [CPI] \* [SPI] ) Uses both cost and schedule efficiency where schedule pressure is expected to influence remaining cost.
VAC VAC = [BAC] - [EAC Bottom-Up] Shows expected budget headroom or overrun at completion.
Uncommitted Budget Uncommitted Budget = [BAC] - [Actual Cost] - [Committed Cost] Shows budget not yet consumed by actuals or open commitments.
Contingency Remaining Contingency Remaining = SUM ( FactBudget[ContingencyBudget] ) - SUM ( FactChange[ContingencyUsed] ) Tracks the approved contingency reserve still available.

Time-Intelligence and S-Curve Measures
Example DAX measures for cumulative curves and alternate dates
Measure Example DAX Purpose
PV Cumulative PV Cumulative = VAR Cutoff = MAX ( DimDate[Date] ) RETURN CALCULATE ( [PV], FILTER ( ALLSELECTED ( DimDate[Date] ), DimDate[Date] <= Cutoff ) ) Creates the cumulative Planned Value line for the S-curve while respecting report selections.
EV Cumulative EV Cumulative = VAR Cutoff = MAX ( DimDate[Date] ) RETURN CALCULATE ( [EV], FILTER ( ALLSELECTED ( DimDate[Date] ), DimDate[Date] <= Cutoff ) ) Creates the cumulative Earned Value line.
AC Cumulative AC Cumulative = VAR Cutoff = MAX ( DimDate[Date] ) RETURN CALCULATE ( [AC], FILTER ( ALLSELECTED ( DimDate[Date] ), DimDate[Date] <= Cutoff ) ) Creates the cumulative Actual Cost line.
Actual Cost by Accounting Date Actual Cost by Accounting Date = CALCULATE ( [Actual Cost], USERELATIONSHIP ( FactActualCost[AccountingDate], DimDate[Date] ) ) Activates an alternate date relationship when the model’s active relationship uses another date role.

Schedule, Change, Risk, and Data-Quality Measures
Example DAX measures for operational project control
Measure Example DAX Purpose
Forecast Finish Forecast Finish = MAX ( FactScheduleSnapshot[ForecastFinish] ) Returns the latest forecast finish in the current project or WBS context.
Finish Variance Days Finish Variance Days = DATEDIFF ( MAX ( FactScheduleSnapshot[BaselineFinish] ), [Forecast Finish], DAY ) Measures calendar-day movement from baseline to forecast finish.
Overdue Critical Tasks Overdue Critical Tasks = CALCULATE ( DISTINCTCOUNT ( FactScheduleSnapshot[TaskKey] ), FactScheduleSnapshot[IsCritical] = TRUE (), FactScheduleSnapshot[PercentComplete] < 1, FactScheduleSnapshot[ForecastFinish] < TODAY () ) Counts unfinished critical tasks whose forecast finish has passed. For historical reporting, replace TODAY() with the governed status date.
Approved Change Value Approved Change Value = CALCULATE ( SUM ( FactChange[ChangeAmount] ), FactChange[Status] = "Approved" ) Returns the value of approved changes only.
Pending Change Value Pending Change Value = CALCULATE ( SUM ( FactChange[ChangeAmount] ), FactChange[Status] = "Pending" ) Shows potential but not-yet-approved exposure.
Open Risk Exposure Open Risk Exposure = CALCULATE ( SUMX ( FactRisk, FactRisk[Probability] \* FactRisk[CostImpact] ), FactRisk[Status] = "Open" ) Calculates expected monetary exposure for open risks, assuming probability is stored as a decimal.
Unmapped Actuals Unmapped Actuals = CALCULATE ( COUNTROWS ( FactActualCost ), ISBLANK ( FactActualCost[WBSKey] ) ) Flags actual-cost records that cannot be assigned to a governed WBS key.
AC Reconciliation Difference AC Reconciliation Difference = [Actual Cost] - [AC] Tests whether financial actuals reconcile to EVM actual cost at the selected grain.

Implementation Notes
Use DIVIDE rather than the division operator when a denominator may be zero or blank; a blank result is normally preferable to a misleading zero.
Use CALCULATE to modify filter context for approved changes, open risks, status-date snapshots, and other controlled subsets.
Use USERELATIONSHIP only with an existing inactive relationship and document which date role the measure activates.
Do not calculate project totals by averaging WBS-level CPI or SPI. Calculate the ratio from rolled-up EV, PV, and AC so weighting remains correct.
Preserve periodic PV, EV, and AC in the fact table; derive cumulative S-curves as measures rather than storing only cumulative values.
Replace volatile TODAY() logic with a governed status-date measure for reproducible monthly reporting.
Format currency, percentages, days, and indices in the semantic model, and document the business definition, source, owner, and validation rule for every approved measure.
Minimal Excel Workbook Structure for Project Control
To set up a simple but robust Excel solution for project monitoring, we recommend a workbook with 4–5 sheets, each serving a clear purpose. Below is a suggested minimal workbook structure along with the key content each sheet holds:
Sheet Name Purpose Key Content & Fields
Setup / Inputs Project metadata and references.
(No frequent edits; houses core assumptions and lists.) – Project Info: Name, manager, start date, status date (current reporting date) [Bruk av E...Gantt i PM | Word].
– Reference Data: lists like team members, WBS code prefixes, budget categories, calendars (work days vs weekends if needed) [Bruk av E...Gantt i PM | Word].
– Reporting Parameters: e.g. current phase, baseline freeze date, any key assumptions. (Lock these cells to avoid accidental changes).
Task Plan (WBS/Schedule) Master task list – the single source of truth for all project scope, schedule, and cost data [Bruk av E...Gantt i PM | Word].
Columns in an Excel Table for each task:
– WBS Code & Task Name (to uniquely identify tasks and group them hierarchically) [Bruk av E...Gantt i PM | Word].
– Predecessors (for simplicity, allow one main predecessor per task, if needed, to sequence tasks).
– Planned Duration (in work days).
– Planned Start / Finish Dates (initial schedule baseline for each task).
– Actual Start / Finish Dates (or Forecast dates if updating planned schedule).
– % Complete (update this regularly to track progress).
– Budget (BAC) for the task (planned cost or effort).
– Actual Cost to Date (AC) (cumulative actual spend or effort for that task).
Gantt Chart (optional view) Visual timeline of the project schedule (based on Task Plan data). – A calendar grid with date columns (e.g. week or month scale) and conditional formatting to shade the cells corresponding to each task’s start/finish range [Bruk av E...Gantt i PM | Word].
– Highlight baseline vs actual or current schedule with different color bars (e.g. a thin bar for baseline, a thicker bar for current plan). Use a vertical line or shading to indicate the status date (today’s date) for context.
EVM / Metrics Performance calculations by period and overall. – Summary tables aggregating key values by project or WBS: total Planned Value (PV), Earned Value (EV), Actual Cost (AC) to date, and resulting SV, CV, SPI, CPI [Bruk av E...Gantt i PM | Word].
– If doing periodic (e.g. monthly) tracking, maintain a table of PV, EV, AC for each period and cumulatively (to plot trends and S-curves).
– Basic forecasts: current EAC (e.g. using formula like EAC = AC + (BAC - EV)) and Variance at Completion (VAC) = BAC - EAC.
– Simple charts, e.g. an EVM S-curve showing cumulative PV, EV, AC over time (to visualize schedule & cost performance) [Bruk av E...Gantt i PM | Word].

Dashboard / Summary Management summary for quick insight and reporting. – A one-page snapshot of project status: key KPIs (e.g. CPI, SPI, EAC vs Budget, days ahead/behind schedule), highlight any critical issues.
– Pivot tables or summary formulas to aggregate data by WBS or categories (e.g. total actual vs budget by phase).
– Charts for easy visualization: e.g., a budget vs actual bar chart by major WBS category, a small Gantt timeline for key milestones, stoplight indicators (RAG status) for schedule and cost health.
Tip: Use Excel’s Table feature for the Task Plan (and other structured data). Tables automatically expand as you add tasks and allow easier formulas with column names. They also work well with PivotTables and charts for the dashboard. Start with a simple design; you can later expand or add complexity once the basic structure is stable and consistently maintained. [Bruk av E...Gantt i PM | Word]

---

Step-by-Step Implementation
Step 1: Create a “Setup” Sheet: Open a new Excel workbook and create a sheet (tab) named Setup. In this sheet, list core project information and control parameters:
Project Name & Description – for reference.
Project Start Date – the starting timeline reference.
Status Date – the “as of” date for progress tracking (e.g. end of the current week or month). [Bruk av E...Gantt i PM | Word]
Calendar & Workdays – if needed, define working days vs weekends (for scheduling calculations).
Standard Fields – any global values like standard working hours/day, budgets for entire project (if known), or data validation lists (e.g., list of team members or status codes for tasks).
Keep this sheet simple and use it to store any input values that need to be referenced by formulas elsewhere (like the start date, or a list of valid WBS codes, etc.), which helps maintain one source for key inputs. Apply Excel data validation for fields like dates or status to ensure they meet expected formats (for example, allow only valid dates or only given list values). [Bruk av E...Gantt i PM | Word]
Step 2: Build the “Task Plan” Table (Scope & Schedule): Create a sheet named Task Plan. Set up a structured table (using Insert → Table) where each row is a project task. Include the columns listed above (WBS code, task name, predecessor, planned duration, start/finish dates, % complete, budget, actual cost, etc.). Consider the following when creating this table:
WBS Coding: Assign a WBS code and task name to each task. The codes create a hierarchy (e.g. 1, 1.1, 1.1.1) to allow grouping tasks by phases/deliverables. You can sort or filter by these codes to see summary levels. [Bruk av E...Gantt i PM | Word]
Schedule Dates: Enter the planned Duration (in days) and the initial Start date of each task. Then calculate the Finish date via formula. For example, if tasks are sequential (simple finish-to-start), set Start = IF(Predecessor is blank, Project Start Date from Setup sheet, End date of predecessor + 1) and Finish = Start + Duration - 1 (adjust for working days if needed). If you’re not comfortable with formulas for dependencies, you can manually enter Start/Finish dates for each task initially. [Bruk av E...Gantt i PM | Word]
Progress Tracking: As the project runs, update % Complete for each task (or mark tasks complete once finished). This will drive the Earned Value calculation: for each task, you can calculate EV = Budget \* %Complete. For example, a $10,000 task at 50% complete has earned $5,000 of value so far. Also record Actual Cost for each task (what has been spent). This can be updated from your cost tracking or accounting records (you might copy actuals into a column or use Power Query to import actual costs from another source in an advanced setup). [nasa.gov]
Organize Data: Keep the Task Plan as the master data sheet. Use filters or group by WBS to roll up and review subtotals by phase or deliverable. You can use a PivotTable to sum Budget vs Actual vs EV by each top-level WBS code for a quick overview of which parts of the project are over or under budget.
Step 3: Create a Gantt Chart View (Optional): On the Gantt sheet, build a timeline display for your schedule:
Set up a row for each task (or just major tasks/milestones for simplicity), and columns representing a time scale (e.g., column per week or per day).
Use conditional formatting to fill cells corresponding to each task’s planned duration: e.g., for each task row, you can apply a rule to shade a cell if its date falls between that task’s Start and Finish dates. This effectively creates horizontal bars. You may highlight baseline vs current schedule by drawing a lighter “baseline” bar and a darker bar for the current schedule of the same task, or by using different colors for tasks ahead/behind schedule. [Bruk av E...Gantt i PM | Word]
Add a vertical line or highlighted column for the current status date to see which tasks should have been done by now. You can then visually identify tasks that have not reached 100% by their planned finish (which indicates they’re behind schedule). Tip: Another way to create a Gantt in Excel is by using a stacked bar chart (with transparent parts) to represent tasks, or by using available Excel Gantt chart templates. For a simple, quick solution, the conditional formatting approach works well.
Step 4: Implement EVM Calculations (Integrated Cost & Schedule Performance): On the EVM sheet, set up formulas to calculate project performance metrics:
Calculate BAC (Budget at Completion) by summing all task Budget in your Task Plan.
Planned Value (PV): For each reporting period or status date, determine how much budgeted work should be done. An approximate way in Excel is: sum the budgets of all tasks that were scheduled (in the baseline) to be completed by the status date, plus partial credit for tasks in progress as of that date (e.g., if a task’s baseline plan says it should be 80% done by now, include 80% of that task’s budget in PV). A simpler approach is to track PV on a period-by-period basis: assign each task’s budget to the time period it’s planned to be done (or evenly spread it across its planned duration) and accumulate these values up to the status date.
Earned Value (EV): For each task, as noted above, compute EV = Budget × %Complete (make sure %Complete is in decimal form for calculation). Summing these across tasks gives total EV on the status date. [nasa.gov], [nasa.gov]
Actual Cost (AC): Sum of all Actual Cost to date (the Actual Cost column of all tasks up to the status date).
Schedule Variance (SV) = EV – PV. A negative SV means the project is behind schedule in value terms; a positive SV means ahead of schedule. [nasa.gov]
Cost Variance (CV) = EV – AC. A negative CV indicates a cost overrun (over budget for the work done); positive means cost savings so far. [nasa.gov]
Schedule Performance Index (SPI) = EV / PV. If SPI < 1, project is progressing slower than planned (e.g., 0.90 means only 90% of planned work accomplished); if > 1, ahead of schedule. [nasa.gov]
Cost Performance Index (CPI) = EV / AC. If CPI < 1, you’re getting less value per dollar (over budget); if > 1, you’re achieving more with each dollar (under budget). [nasa.gov]
Estimate at Completion (EAC): A simple formula is EAC = BAC / CPI (assumes current cost efficiency continues). Alternatively, if you suspect future performance will be as planned, use EAC = AC + (BAC – EV). [nasa.gov]
Variance at Completion (VAC) = BAC – EAC, indicating expected final variance (negative means a likely overrun).
All these formulas can be implemented with basic Excel arithmetic and functions like SUM and SUMIF (or using a PivotTable to aggregate by WBS or project). For periodic tracking, you might add a column for “Status Period” (e.g., month) in the Task Plan or use an EVM table with one row per reporting period, listing cumulative PV, EV, AC values; this allows you to draw the classic EVM “S-curve” by plotting PV, EV, and AC across time. [Bruk av E...Gantt i PM | Word]
Step 5: Build the Dashboard Summary: With the calculations in place, design a simple Dashboard sheet to summarize the key information for quick review:
Identify a handful of KPIs and status indicators that matter most: e.g., Total Budget vs EAC (to show if you’ll finish under or over budget), CPI and SPI (to summarize cost and schedule efficiency), Overall % Complete (EV/BAC, how much of total work value is done), and critical milestone dates vs baseline (to show any slip in major deliverables). [Bruk av E...Gantt i PM | Word]
Use Excel’s visualization features for clarity: Insert a bar or bullet chart comparing Budget vs EAC to highlight any variance, or a small pie chart for budget spent vs remaining. A simple traffic light (RAG) cell can indicate overall health: e.g., red if CPI or SPI < 0.9, yellow if around 1.0, green if > 1.0 thresholds.
Show tabular summaries for context: e.g., a table of top 5 WBS elements by largest budget overruns (negative variances) and their values, or a mini schedule table of upcoming milestones with planned vs forecast dates. These can be easily generated by sorting the Task Plan or using PivotTables to aggregate data.
Finally, validate your formulas by manually checking that totals make sense (e.g., verify that summing EV equals Budget × overall % complete, and that PV at project completion equals total budget). Use Excel’s built-in error checking features – e.g., show formula auditing arrows to ensure your references are correct, and examine Excel’s suggestions for errors or inconsistencies in formulas (the green triangle indicators). Incorporate a dedicated “Checks” section or sheet where you put tests like “Does total Actual Cost on Task Plan = AC on EVM sheet?” – and highlight if any check fails, so you can catch mistakes early. [Bruk av E...Gantt i PM | Word]

---

Essential KPIs & Calculations for Monitoring
A simple Excel-based project control dashboard should focus on a few essential metrics that cover schedule, cost, and overall progress. The following are recommended Key Performance Indicators (KPIs) and how to derive them in Excel:
Planned vs Actual Finish Dates: Monitor schedule adherence by comparing key milestone dates or a calculated Finish Variance (e.g., Finish Variance = Actual Finish – Baseline Finish) for tasks or phases. A positive variance indicates a task finished later than planned (delay), while negative means it finished early.
Tasks Completed vs Planned: Track how many tasks (or what percentage of total tasks) were planned to be completed by the status date vs how many actually are completed. This can be a simple metric of schedule progress if EVM isn’t fully implemented.
Budget vs Actual Cost: Compare total actual spending to date against the planned spend or budget. This can be visualized as a % of budget consumed to give a quick cost status (e.g., “$750k spent out of $4M budget = 18.75% of budget used”). [Bruk av E...Gantt i PM | Word]
CPI (Cost Performance Index): The ratio of earned value to actual cost, to indicate cost efficiency. E.g. if EV = $500k and AC = $550k, CPI = 0.91, indicating a cost overrun (only $0.91 value per $1 spent). [nasa.gov]
SPI (Schedule Performance Index): The ratio of earned value to planned value, indicating schedule efficiency. E.g. EV $80k vs PV $100k yields SPI = 0.80 (project is behind schedule, doing 80% of planned output). [nasa.gov]
EAC vs Budget: This forecast final cost compared to the original budget highlights expected overrun or underrun. E.g. if EAC = $1.2M vs Budget = $1M, the project is projected 20% over budget.
% Contingency Remaining: If your budget includes contingency or reserves, track how much is left unused as a health indicator for risk buffer. (E.g., contingency remaining $50k out of $100k initial = 50% reserves left).
For all these KPIs, use simple Excel formulas (addition, subtraction, division) referencing the appropriate cells from your Task Plan and EVM sheets. Where possible, set up Excel named ranges or structured table references for clarity – for instance, name the cell holding total BAC as Total_Budget, and the cell with current EAC forecast as Current_EAC. Then =Current_EAC - Total_Budget gives your forecast variance at completion (negative if overrun). Such names make formulas easier to read and audit.

---

Leveraging Excel Features & Best Practices
Even a simple Excel solution benefits greatly from some of Excel’s built-in features. Here are key techniques to make your project control workbook more robust and user-friendly:
Structured Tables: Use Excel Tables for any list of data (your Task Plan, actual cost log, risk register, etc.). Tables auto-expand and carry formulas down new rows automatically, reducing errors and maintenance work. [Bruk av E...Gantt i PM | Word]
Data Validation Lists: Restrict certain inputs (e.g., task status, responsible person, WBS code format) with data validation. For example, ensure a WBS code follows a specific pattern (like #.#.#) or that the task status is only “Not Started, In Progress, or Complete” by using a dropdown list for that column. This prevents typos that could break formulas (like mismatched codes). [Bruk av E...Gantt i PM | Word]
Conditional Formatting & Alerts: Set up conditional formats to highlight potential issues automatically. For example, if % Complete is 100% but there is no Actual Finish date, highlight the cell in red (to indicate missing data). If CPI or SPI < 1.0, mark them in red or orange. If a task’s Actual Finish is later than its Baseline Finish, highlight the slip in red, etc. This provides instant visual cues for problem areas.
PivotTables & Charts: Use PivotTables to aggregate data from the Task Plan by WBS, by month, by resource, etc., without writing complex formulas. For instance, a PivotTable can sum budget, EV, and actual cost by major WBS category to identify which phase is overspending. Pivot charts can then visualize these aggregations (like a bar chart of Actual vs Budget per phase). [Bruk av E...Gantt i PM | Word]
Power Query (Get & Transform): For more advanced use, Excel’s Power Query can automate the import of actual cost data from other files or systems (like a corporate financial system or time-tracking tool). This reduces manual copying and pasting and ensures your actuals are up-to-date each reporting cycle. [Bruk av E...Gantt i PM | Word]
Formula Auditing Tools: Excel provides tools like trace precedents/dependents and error checking to help ensure your formulas are referencing the right cells, and consistent formulas in columns. Use these to double-check that your computations (especially date calculations for the schedule, or EVM formulas) are correct and consistent down the column. [Bruk av E...Gantt i PM | Word]
Protect critical cells: As your spreadsheet becomes more complex, use cell protection (locking cells and protecting the sheet) for areas with formulas or baseline data that shouldn’t be altered inadvertently. Only input fields should be editable during periodic updates (e.g., percent complete, actual costs). [Bruk av E...Gantt i PM | Word]
Maintain one version of the truth: Resist the temptation to create multiple versions of the spreadsheet for different scenarios or “what-ifs” (unless you have a robust version control mechanism). Instead, keep one master workbook and add scenario or version controls inside it if needed (e.g., a dropdown to select different forecast scenarios), so that everyone works from the same data. This avoids inconsistencies and confusion from parallel copies. [Bruk av E...Gantt i PM | Word]

---

Simple Dashboard & Reporting Example
A well-designed executive dashboard in your Excel workbook provides a clear snapshot of project status. Focus on clarity – include the minimum information needed for decision-makers to understand project health:
Overall status (red/yellow/green indicator) – based on whether key metrics are within acceptable thresholds.
Budget vs Forecast Cost: e.g., show Budget, Actual to Date, and EAC in a small table or as a bar chart. This highlights your projected Variance at Completion at a glance (e.g., “Budget $1.0M vs EAC $1.1M: 10% overrun expected”).
Schedule Status: list major milestones with their planned vs current forecast dates and any variance, or a mini timeline graphic. You can extract this by filtering the Task Plan for milestone tasks (duration 0 or marked as milestones) and referencing their baseline and forecast finish dates.
Performance Indices: show CPI and SPI in large, boldly colored text or gauges. For example, CPI = 0.92 (red), SPI = 0.95 (orange) – any value below your threshold (e.g., 0.95) can be colored red to flag trouble.
Top variances: list the top 3–5 WBS elements or tasks with the largest cost variances or schedule slips, so management knows where the biggest problems lie. E.g., “Task 3.2 Design Phase – $50k over budget, 2 weeks late.”
Key risks or issues: optionally, include a line for any major risk or pending change that could impact cost/schedule, so it stays visible (e.g., “Risk: Procurement delay could cost +$100k, 4 weeks”).
You can create these visuals by referencing the data in your Task Plan/EVM sheets or using pivot charts. For instance, a bar chart can compare each top-level WBS’s Budget vs EAC. An S-curve line chart can display cumulative planned vs actual progress to illustrate trends over time (cumulative tasks completed or cumulative EV vs PV vs AC). A gauge or thermometer chart can show overall % of project complete. Many free Excel dashboard templates are available to get ideas for layout, but keep your first dashboard clean and simple – e.g., two or three charts and a short table of highlights, all on one sheet. [Bruk av E...Gantt i PM | Word]
[Bruk av E...Gantt i PM | Word]

---

Common Mistakes and How to Avoid Them
Even a well-designed Excel solution can go awry if not maintained with discipline. Here are common pitfalls in building project monitoring workbooks – and how to avoid them:
Mixing Data and Calculations: Mistake: Entering hard-coded numbers into formula cells or mixing input cells and output formulas on the same sheet. Solution: Separate inputs and calculations – for example, keep all raw data on the Task Plan (and possibly separate Actuals or Setup sheets) and perform calculations in dedicated columns or summary sheets. Use color-coding (e.g., blue font for input cells, black for formulas) to distinguish data vs calculations. [Bruk av E...Gantt i PM | Word]
Inconsistent or Missing Codes: Mistake: Using different names/codes for the same thing (e.g., a WBS code spelled differently in the cost sheet vs schedule sheet) or leaving fields blank. Solution: Use unique IDs for tasks (WBS codes) and always reference them for summing or lookup formulas. Employ data validation to ensure consistency of entries (e.g., restrict values to a predefined list). [Bruk av E...Gantt i PM | Word]
Overwriting the Baseline: Mistake: Changing original plan dates or budgets as the project progresses (thus losing the baseline). Solution: Maintain separate Baseline vs Actual/Forecast columns. This preserves the original plan for accurate variance calculations and accountability. [Bruk av E...Gantt i PM | Word]
No Reconciliation or Checks: Mistake: Not verifying that data ties out (e.g., forgetting to update a formula, leading to mismatched totals). Solution: Include a Checks section or sheet with formulas to compare key totals (like sum of task Actual Costs vs total Actual on the dashboard). Implement conditional formats or big warning text if a check fails (e.g., “ERROR: Task data and summary don’t match”). [Bruk av E...Gantt i PM | Word]
Excessive Complexity Early On: Mistake: Trying to incorporate too many advanced features (multiple calendars, complex dependencies, detailed resource loading) in Excel right away. Solution: Start simple – implement the core structure and get it working correctly with minimal features first. Add complexity gradually in controlled phases (see roadmap below). If the project outgrows what a spreadsheet can handle (e.g., thousands of tasks or multi-team collaboration), consider migrating to dedicated project management tools rather than forcing Excel to do everything. [Bruk av E...Gantt i PM | Word]

---

Phased Roadmap: Evolving from Simple to Advanced
Start with a basic Excel solution and improve it over time as needed. Below is a phased approach (Version 1–3) to enhance your project monitoring system gradually:
[Bruk av E...Gantt i PM | Word], [nasa.gov]
By following this phased approach, you ensure that your Excel-based project monitoring system stays simple and reliable at the start, and you can layer on capability as you gain confidence and as project complexity grows. [Bruk av E...Gantt i PM | Word]

---

In conclusion, a well-designed Excel project monitoring and control workbook can effectively support project managers in tracking schedule and cost performance using best practices:
It starts with a structured task list (WBS & schedule) that serves as the backbone for all tracking. [Bruk av E...Gantt i PM | Word]
It incorporates key metrics (e.g. budget vs actual, CPI, SPI, forecast vs baseline) to quantify progress and performance.
It employs Excel’s capabilities (tables, formulas, charts) for clarity and automation where possible.
It is built and expanded iteratively (simple baseline first, then EVM metrics, then advanced automations) to maintain usability and avoid errors.
By adhering to these guidelines and using the step-by-step plan, even users with limited technical experience can create a project control solution in Excel that is both simple and effective – providing valuable insight into project health and enabling timely, informed decision-making to keep projects on track.
Key KPIs for a Project Controls Dashboard: EVM & Beyond
A project monitoring dashboard for project controls should provide a holistic view of project health – covering schedule, cost, scope/change, risk, resources, quality, and forecast – with a focus on integrated Earned Value Management (EVM) metrics. To be effective, it should highlight a select set of key performance indicators (KPIs) that collectively answer critical questions: Are we on time? On budget? Within scope? What’s changed? What’s at risk? What’s ahead? These KPIs should be clear, actionable signals (backed by data) and balanced across different dimensions of project management.
[pathhub.ai]
In the context of project controls (where integrated scope–schedule–cost management is front and center), the core KPI set typically revolves around schedule and cost performance. EVM metrics such as Planned Value (PV), Earned Value (EV), and Actual Cost (AC) form the foundation, with performance indices (SPI, CPI) and forecasts (EAC, ETC) distilling these into actionable indicators of schedule and cost health. [Bruk av E...Gantt i PM | Word]
However, a balanced project dashboard also incorporates metrics for scope and change control (to ensure deliverables and changes stay managed), risk and contingency (to provide early warnings), resource utilization (to monitor team/workload health), quality (to catch issues that could derail the project), and governance/process (to flag any internal control problems). By combining these, you get a 360° view of project status.
Below is a structured catalog of recommended KPIs for an EVM-focused project monitoring dashboard. They are organized by key project dimensions, each with definitions and suggestions on measurement and visualization. Following the comprehensive list, we highlight a condensed top-10 selection suitable for a one-page executive-oriented dashboard, and discuss best practices for using project KPIs (including leading vs lagging indicators and common mistakes to avoid).

---

Schedule & Cost Performance (EVM) KPIs
These KPIs are at the heart of project controls – tracking schedule and budget performance through EVM. They quantify how well the project is progressing relative to its baseline plan, integrating time and cost performance:
Planned Value (PV) – Budgeted Cost of Work Scheduled (BCWS). What it measures: The authorized budget for work planned to be completed by the current date. PV is derived by time-phasing the project budget (Budget at Completion) across the schedule: by summing the budgeted cost of tasks that were scheduled to be done by now, you get the intended “value” of work that should have been accomplished to date. How to use it: PV provides the baseline reference for schedule progress in monetary terms; it is used with EV and AC to calculate other EVM metrics. [Bruk av E...Gantt i PM | Word]
Earned Value (EV) – Budgeted Cost of Work Performed (BCWP). What it measures: The planned (budgeted) value of the work actually completed to date. In practice, if a task’s total budget (or “Budget at Completion”) is $100k and it’s 60% complete, then $60k is “earned” – contributing that amount to EV. In EVM analysis, EV is the single measure that integrates scope and schedule progress with the cost baseline, by quantifying progress as a monetary value. How to use it: EV indicates how much of the total planned budget corresponds to the completed work so far, enabling apples-to-apples comparison with PV and AC. [6sigma.us]
Actual Cost (AC) – Actual Cost of Work Performed (ACWP). What it measures: The actual expenditures (or costs accrued) for the work completed to date. AC comes from the project’s financial tracking (e.g. invoices, labor costs). In an EVM system, AC is often time-phased similarly to PV/EV (so you have AC up to the status date). How to use it: AC is compared with EV to gauge cost performance (e.g., whether you’ve spent more or less than the value of work completed), and with PV to gauge if spending is as planned. [6sigma.us], [6sigma.us]
Schedule Variance (SV) – EV – PV. What it indicates: The difference between work performed and work planned, in money or work-hours terms, at a given point. A negative SV means the project has delivered less work than planned (i.e. behind schedule in terms of value of work), while a positive SV means ahead of schedule. Example: If EV = $40k and PV = $50k at week 8, SV = –$10k (meaning $10k of budgeted work is still incomplete, behind plan). Dashboard use: SV can be shown as a dollar (or hours) variance or as a percentage of PV (e.g., “15% behind schedule”). It gives a sense of the magnitude of schedule slippage or gain in terms of budgeted work. [6sigma.us], [pathhub.ai] [6sigma.us]
Schedule Performance Index (SPI) – EV / PV. What it indicates: The ratio of earned value to planned value, and a standard measure of schedule efficiency in EVM. Interpretation: SPI = 1.0 means work is exactly on schedule; SPI < 1.0 means the project is behind schedule (e.g., SPI 0.85 = project has only completed 85% of the planned work to date, thus 15% behind schedule); SPI > 1.0 means the project is ahead of schedule. Dashboard use: SPI is a high-level schedule KPI that can be shown as a number with RAG (Red/Amber/Green) coding, and possibly a small trend line. Example threshold: an SPI < 0.9 is often considered a critical warning level requiring intervention. [pathhub.ai]
Cost Variance (CV) – EV – AC. What it indicates: The difference between earned value and actual cost, i.e. “value over spend”. CV=0 means cost exactly equals value earned (on budget); negative CV means over-budget (e.g., EV $40k vs AC $45k gives CV = –$5k, a $5k cost overrun); positive CV means under budget (so far). Dashboard use: Like SV, this can be shown as a dollar variance or percentage (e.g. “$5k over budget” or “10% over budget” for negative CV). It highlights if the project is spending more or less than planned for the work accomplished. [6sigma.us]
Cost Performance Index (CPI) – EV / AC. What it indicates: The ratio of earned value to actual cost, showing cost efficiency. CPI = 1.0 means each $1 is delivering $1 of value (on budget); CPI < 1.0 means cost overrun (e.g., CPI 0.80 means you’re only getting 80 cents of value per $1 spent – a 20% overrun); CPI > 1.0 means cost under-run (spending less than budget for the work achieved). Dashboard use: Like SPI, CPI is a critical KPI for cost health. Display it as a number or gauge with thresholds (e.g. green ≥1, red <0.9). It can be complemented by a “budget utilized” percentage to show how much of the total budget has been consumed vs progress (for example, $800k of $4M spent, which is 20% of budget while project is 15% complete – signaling a possible front-loaded spend). [6sigma.us] [pathhub.ai]
Budget at Completion (BAC) – Total planned budget for the project (or for a WBS element). What it represents: The original approved project budget (or the latest baseline budget including approved changes). How it’s used: BAC is the reference against which final outcomes are measured. It’s usually shown as a static figure on an executive dashboard (e.g. “Budget: $4.0M”) and used to compare with actual and forecast costs. It doesn’t change unless scope changes are formally approved. Note: some dashboards break down BAC by major categories (WBS elements) for context.
Estimate at Completion (EAC) – Forecast final total cost of the project (or of a WBS element). What it indicates: Projected total cost of the project when finished, given current performance and any known changes. EAC can be determined via different methods. One common formula is EAC = BAC / CPI (if current cost efficiency is expected to continue), or EAC = AC + (BAC – EV) (if assuming remaining work will be on-plan). Dashboard use: EAC vs BAC (with the difference Variance at Completion (VAC) = BAC – EAC) is a top-level KPI for forecasting cost outcomes. For example, if Budget = $4.0M and EAC = $4.6M, the dashboard might display “Forecast Cost: $4.6M (Over Budget by $0.6M, or 15%)”. This gives executives a forward-looking view of whether the project will finish over or under budget, and by how much. [Bruk av E...Gantt i PM | Word]
Estimate to Complete (ETC) – Remaining cost to finish the project. What it indicates: the expected additional cost needed from now until completion (i.e. EAC – AC). Usage: Typically used internally by project controllers rather than as a headline KPI, but it’s a component of the EAC calculation and useful if you need to show how much more funding is required. It might appear on a detailed financial view of the dashboard or in supporting reports, but not always on an executive summary.
Forecast Completion Date & Schedule Variance – In addition to EVM’s SPI (which indicates schedule health at a high level), stakeholders often want to see when the project (or key milestones) will finish compared to the baseline date. What it indicates: whether the expected completion date has changed; a Finish Variance can be shown (e.g. “Forecast Finish is 2 weeks late”). A related KPI is Milestone Achievement % (Milestone Hit Rate) – the percentage of key milestones or phase gates met on time. Dashboard use: The project finish date can be displayed as a date alongside the baseline finish and variance (e.g., “Planned Finish: June 2027; Forecast Finish: August 2027 (8 weeks late)”). The Milestone Hit Rate can be shown as a percentage or fraction of milestones delivered on schedule (e.g. “3 of 5 milestones achieved on time (60%)”), perhaps with red/yellow/green coloring if it falls below a threshold. [pathhub.ai]
How to visualize schedule & cost KPIs:
For schedule metrics, a mini Gantt chart or milestone timeline can illustrate where key dates and delays occur. An EVM S-curve is a powerful visual to plot PV, EV, and AC over time, letting viewers instantly see schedule and cost performance trends (with EV below PV and AC indicating schedule slip and overspend). For cost, a budget vs forecast bar chart or bullet graph (showing BAC versus EAC) clearly highlights any projected overrun or saving. Efficiency indices CPI/SPI work well as large-number indicators or gauges with RAG coloring, accompanied by brief text (e.g. “SPI = 0.85 (behind schedule)”). Combine with trend arrows or sparkline charts to show if performance is improving or deteriorating over time. [Bruk av E...Gantt i PM | Word] [pathhub.ai]

---

Scope & Change Management KPIs
These KPIs track how the project’s scope is being controlled and whether changes are managed properly. They ensure that the delivered scope remains aligned with the plan and approved modifications:
% Scope Complete – Measures how much of the total project scope (deliverables or work) has been finished. This could be quantified as “deliverables completion percentage” (e.g., 15 of 20 major deliverables completed = 75% scope complete) or via EVM (EV/BAC: the percentage of total budgeted value earned, i.e. overall work completeness). Use: This KPI provides a high-level progress indicator for scope delivery (complementary to schedule progress). It can be visualized as a simple percentage or progress bar. [Bruk av E...Gantt i PM | Word]
Change Request Count & Impact – Tracks the number and significance of scope changes to the project. This can be split into approved changes vs pending (outstanding) changes. Particularly important in EVM-driven projects: Change Request Value (cumulative approved change amount) often directly ties to budget and scope increase. Use: Show the total added budget from changes (e.g., “+10% budget via change orders”) alongside number of changes, to contextualize cost/schedule variances. A high volume or value of changes can indicate scope creep or poor initial requirements. Visualize change metrics with a simple counter (e.g., number of changes) and a total change value (possibly as part of the budget section). If scope is managed via formal change control, a RAG indicator can highlight if changes are within the authorized contingency or not. [Bruk av E...Gantt i PM | Word]
Scope Stability / Creep – A derivative metric that shows scope growth as a percentage of initial scope (often measured via budget or requirements count). For example, “Scope change: +15% (budget increased from $4.0M to $4.6M including approved changes)”. Use: This helps stakeholders see if the project’s scope/budget expanded beyond what was originally planned (which might explain schedule/cost variances). Could be visualized as a simple percentage, possibly alongside commentary on primary change drivers.
Requirements or Deliverables Sign-off Rate – Measures how many project deliverables or requirements have been formally accepted or signed off by stakeholders (e.g., “12 of 15 requirements approved (80%)”). Use: Indicates progress and alignment with stakeholder expectations. If a low percentage of deliverables have been accepted relative to project completion, it could flag potential quality or scope acceptance issues. It can be visualized as a percentage or fraction of completion for the total scope items.

---

Risk & Contingency KPIs
These KPIs act as leading indicators of potential issues, measuring how well risks are being managed and how much contingency remains for uncertainties:
Number of Open Risks (by Severity) – The count of currently active project risks, often categorized by severity (e.g., 5 High-risk, 8 Medium, 10 Low). Use: Tracking open risks ensures active risk management. An increasing count of high severity risks is a leading indicator that future problems may arise if not mitigated. You can visualize this with a simple count or bar chart (grouped by risk level). [managementyogi.com]
Risk Exposure (Expected Impact) – The aggregate potential impact of all open risks, typically measured as the sum of (probability × impact) for each risk. Example: If two major risks each have a 30% chance of occurring, with $100k impact each, the total risk exposure = $60k, which might be 15% of the remaining budget. Use: This gives stakeholders a sense of the “forecast” cost of risks. If risk exposure grows or exceeds a certain percentage of the budget (say >20%), it’s a red flag requiring risk mitigation or increased contingency. Show it as a single number (with context like percentage of budget) or as a trend line over time. [pathhub.ai]
Contingency Reserve Remaining – The amount of unallocated contingency budget left to cover risks or changes. Use: Indicates how much risk buffer remains. For instance, if 80% of the contingency is already used halfway through the project, the project may be vulnerable to any further surprises. Often shown as a dollar value or percentage (e.g. “Contingency remaining: $50k (50%)”). A small gauge or bar could depict how much of the contingency fund is left, sometimes with color-coding if it drops below a threshold (e.g. below 25% triggers a red alert).
Mitigation Rate – The percentage of high-priority risks with approved mitigation plans in place (or responses executed). Use: Highlights if the team is proactively managing risks. A low mitigation/response rate (especially for critical risks) is a warning sign that the project isn’t adequately preparing for known threats. [pathhub.ai]
Issue Count / Aging – If you maintain a distinction between risks (uncertain future events) and issues (problems that have already occurred), track the number of active issues and possibly their average time to resolve. This metric indicates the project’s current challenges that need resolution (a lagging indicator of trouble). A rising issue count or slow resolution times can signal needed management intervention.
Visualization tip: Risk KPIs can be summarized in a small risk matrix or heatmap (e.g., a 3x3 grid showing how many risks fall into high/medium/low categories by probability vs impact). Alternatively, use iconic indicators – e.g., a warning icon if there are any critical risks above a certain exposure threshold. Trend charts tracking total risk exposure or number of open risks over time can show if the risk profile is improving or worsening.

---

Resource & Productivity KPIs
These KPIs ensure the project’s human and material resources are being utilized effectively and sustainably:
Resource Utilization Rate – Measures the percentage of available resource time being used on project work. For example, if a team member is available for 40 hours/week and working 32 hours on project tasks, that’s 80% utilization. Use: This KPI helps identify both under-utilization (which could mean inefficiency or misallocation) and over-utilization (risk of burnout or over-commitment). Guideline: Aim for a balanced utilization (often ~70–85% for sustained productivity); consistently above ~90% is a warning sign for burnout or quality issues. This can be shown with a gauge or bar for each key resource or an average for the team, using color bands for safe usage vs over-utilization. [pathhub.ai]
On-Time Task Completion Rate – The percentage of tasks completed by their planned finish dates. This is a granular counterpart to milestone hit rate: e.g., “85% of tasks (or story points) were finished on or before their scheduled dates”. Use: A high on-time completion rate often correlates with good team productivity and realistic planning, while a declining on-time rate may reveal chronic underestimation or obstacles hindering the team. Visualize this as a percentage with an upward or downward trend arrow. [pathhub.ai]
Productivity or Throughput – A measure of the team’s output over time, such as tasks completed per week or (in Agile contexts) velocity (story points per sprint). Use: Provides a view of whether the project’s work throughput is enough to meet deadlines. For traditional projects, you might use Earned Value per period (or simply count of tasks completed) vs planned, which ties back to SPI. In Agile teams, velocity trends can indicate if productivity is improving or dropping. Use a line chart to show trend over time; set expected range thresholds (e.g., stable velocity within ±10% of average is normal; a downward trend is a leading indicator of problems).
Resource Availability/Gaps – Tracks whether critical skill sets or roles are under-staffed or missing, which can jeopardize schedule. Example KPI: “Percent of key positions filled” or “Resource gap (hours or FTE) for critical skills”. Use: A significant unfilled resource need (especially on the project’s critical path) is a leading indicator of likely schedule delays or quality issues. Typically monitored by project managers or resource managers; an executive dashboard might highlight only major resource red flags (e.g., “3 key engineering roles unfilled”).

---

Quality & Delivery KPIs
These KPIs monitor whether the project’s outputs meet the required quality standards and acceptance criteria, helping to catch issues that could impact success:
Defect/Issue Trends – The number of open defects, bugs, or quality issues reported in the project’s deliverables, and their trend over time. Use: A spike in defects or persistent critical quality issues can delay acceptance of deliverables (affecting scope/schedule) and increase costs due to rework. Track open defects count and average resolution time; a trend chart or burn-down chart for defects is useful to see if the project is clearing issues or accumulating technical debt. For example, a downward trend in open defects is positive, while an upward trend is a warning (particularly late in the project).
Testing or Acceptance Rate – Measures the proportion of deliverables or work packages that have passed quality checks or client acceptance. Example: “90% of deliverables have passed quality assurance reviews on the first submission”. Use: Indicates the quality of work being delivered. A lower-than-target first-pass acceptance rate may signal potential rework (and could predict schedule/cost impacts). Visualize as a percentage or fraction (e.g., tasks passed vs tested, often as a progress bar or pie chart portion).
Rework/Defect Costs – The effort or cost spent on rework or fixing defects. Use: An increasing rework cost (or hours) is a lagging indicator of quality problems that could erode budget and schedule margins. If the project has a quality budget or buffer, show rework cost vs its allowance as a metric. This can be a bar or gauge (with RAG coloring if rework cost exceeds, say, 10% of total effort or budget).
Stakeholder Satisfaction (if measurable) – A less common but strategic KPI: results of stakeholder or client satisfaction surveys (scored on quality of deliverables, communication, etc.). Use: This can be a trailing indicator of project success and team performance. Typically measured at phase gates or after deliverables are handed over. A low score should prompt investigation into underlying issues (possibly linking back to scope or quality deficiencies).

---

Governance & Process KPIs
These KPIs monitor project governance, data quality, and internal process discipline – ensuring that the project control mechanisms themselves are functioning. They are particularly relevant in a project controls context (e.g., PMOs or project control teams, rather than high-level executives):
Overall Project Status (RAG) – A high-level Red/Amber/Green status indicator reflecting a holistic judgment of the project’s health across all areas (schedule, cost, scope, risk, etc.). Use: This is often a summary indicator for executives, derived from the other KPIs. For example, if multiple critical KPIs are outside thresholds (SPI/CPI < 0.9, major delays or overruns), the status might be red (at risk). Typically shown as a colored traffic-light icon or label (“On Track”, “At Risk”, etc.), it quickly communicates if the project is on course or needs attention. [pathhub.ai], [pathhub.ai]
Data Freshness / Update Timeliness – Ensures that the dashboard data is current and reliable. For instance, “Last Update Date” or days since last status update. Use: This reminds users if information might be outdated, and encourages regular updates (e.g., a red highlight if status data > X days old). For internal compliance, some organizations also track if status reports were submitted on time (e.g. by each project manager for each period).
Key Decision Turnaround – Measures any overdue approvals or decisions that the project is awaiting (for example, pending steering committee decisions, sign-offs, or design approvals). Use: These are leading indicators of potential delays: if crucial decisions or approvals are late (say the number of days a decision is overdue, or count of decisions pending past their due date), the project may stall. This can be simply listed as an alert on a dashboard to draw attention from governance bodies.
Project Change/Variance Approval – Ensures that changes or variances are processed properly. Example: the count of unresolved major variances or unapproved changes exceeding a threshold. Use: If significant scope changes or cost variances are not formally approved within the expected period, the project might be in a control lapse. Not typically shown to executives, but a PMO controller might track this to enforce process.
Compliance to Standards – If relevant, you might include a metric on adherence to process or regulatory requirements (e.g., “100% of required status reports delivered”, or quality audit results). These “governance” metrics assure leadership that project management processes are being followed. They are often binary or percentage metrics and can be included in internal team dashboards or footnotes rather than the main exec dashboard unless a specific compliance issue is a major concern.

---

Selecting the Top 10–15 KPIs for an Executive Dashboard
From the above, we can distill a shortlist of high-impact KPIs that together provide a comprehensive picture for senior stakeholders. A well-designed one-page executive project controls dashboard would typically include a mix of schedule, cost, and risk metrics, focusing on outcomes and forecasts, for example:
Overall Status (R/A/G) – At-a-glance health indicator summarizing project condition across all metrics (green = on track, etc.).
Forecast Completion Date vs Baseline – Shows whether the project is projected to finish on time (or how far ahead/behind). [pathhub.ai]
Milestone Achievement % (Hit Rate) – What portion of key milestones have been met on schedule (e.g., “80% on-time milestone delivery” – a proxy for schedule adherence). [pathhub.ai]
Budget at Completion (Baseline Budget) – The committed project budget for comparison (e.g., "$4.0M").
Estimate at Completion (Forecast Cost) – The current forecast of total project cost (e.g., "$4.5M"), ideally shown alongside BAC with variance.
Variance at Completion (Cost Overrun %) – The expected overrun or saving, i.e. EAC vs BAC difference (e.g., “+12% over budget” if EAC > BAC). [Bruk av E...Gantt i PM | Word]
Cost Performance Index (CPI) – Overall cost efficiency (EV/AC) at present; crucial if the audience is aware of EVM (color-coded green/yellow/red).
Schedule Performance Index (SPI) – Overall schedule efficiency (EV/PV); also critical as an integrated schedule indicator (with RAG status). [pathhub.ai]
Contingency Reserve Remaining – Percent or amount of budget contingency still available (% or $ remaining), signaling how much buffer is left for unforeseen issues.
Top Risk or Risk Exposure – Brief highlight of the most significant risk (with its impact) or total risk exposure as a % of budget – to flag potential threats beyond current performance. [pathhub.ai]
Scope Change (Approved Changes) – Total value of approved changes (and resulting % increase in budget or scope) since project start, to contextualize if variances are due to scope growth or execution issues.
Critical Path Status – E.g., a note on current critical path length or days of float remaining until a key milestone, highlighting if project has any schedule buffer left.
Key Milestone or Deliverable RAG – A status highlight for one or two upcoming or recently passed critical milestones (with their dates and status: on track, at risk, or missed).
Team Capacity Utilization – A high-level view of resource load (e.g., average team utilization this period, with indicator if it’s in a risky range).
Quality/Defects Status – Optionally, a top quality indicator, such as number of open critical issues or current defect trend (if quality problems have been a notable risk factor in the project).
Note: Not every project requires every category of metric on the executive dashboard. Tailor the selection to project priorities. For example, if resource overload is a big risk in your project, include a resource utilization KPI; if not, it may be omitted. Keep the top-level focus on the metrics that truly signify success or failure for your specific project. Typically, schedule and cost dominate, with a handful of supporting metrics for scope changes, risks, and other factors that drive those outcomes. [pathhub.ai], [pathhub.ai]
Leading vs Lagging Indicators: While many traditional project KPIs are lagging (they measure outcomes or past performance, like actual cost or variance after it occurs), it’s wise to include some leading indicators that predict future issues so you can act early. For instance, Risk Exposure is a leading indicator – if risk exposure is climbing, it suggests future cost or schedule problems if risks materialize. Resource utilization above 95% is a leading indicator for burnout and potential slip in quality or schedule. Buffer consumption (contingency used) is another – if you’ve burned most of your contingency early, future changes or risks could directly cause overruns. Even SPI and CPI can be considered leading indicators in that they allow you to forecast the final outcome (via EAC) and trigger early corrections. Balancing lagging and leading KPIs gives a richer picture: lagging KPIs highlight what has already happened (and whether you met past targets), while leading KPIs highlight what might happen if trends continue, prompting preemptive management actions. [managementyogi.com], [managementyogi.com] [pathhub.ai] [6sigma.us], [pathhub.ai]
Visualizing an all-up project dashboard: A multi-dimensional project controls dashboard might include several sections or tabs. For example, an Executive Summary page could display the top 10–12 KPIs with clear visual cues (RAG status, a few “big number” metrics, mini-charts), as described above. Supporting pages or drill-downs can then provide more detailed views for each area (e.g., a detailed cost sheet by WBS, a full risk register, a resource allocation chart, a quality dashboard with defect lists, etc.). In an Excel implementation, this might mean separate worksheets for detailed breakdowns, while in a BI tool like Power BI or Tableau it could mean separate interactive pages with filters. [pathhub.ai]
Common mistakes to avoid: As noted earlier, don’t overload the dashboard with too many KPIs or trivial data points – stick to the high-impact ones that guide decisions. Avoid vanity metrics that don’t influence project outcomes (e.g., “number of meetings held” might not correlate with success). Ensure each KPI has a clear target or threshold that defines success (e.g., SPI ≥ 1, CPI ≥ 1, Milestone hit rate ≥ 90%) and use simple color-coding to indicate status (e.g., green if within target, amber if slightly off, red if critical). Also, focus on timely updates and trend monitoring – a KPI measured only at project end (like final total cost) doesn’t help with course corrections. Finally, make sure the dashboard is not just a passive report: it should be linked to action. When a KPI goes red, there should be a plan for who needs to respond and how to get the project back on track. [pathhub.ai], [pathhub.ai] [pathhub.ai]
In summary, the ideal project monitoring dashboard will combine EVM-driven metrics (to track time and cost performance in an integrated way) with a handful of other KPIs that cover scope changes, risks, resources, and quality – the factors that often underlie deviations in time and cost. By selecting a focused set of KPIs, defining them clearly, and visualizing them with intuitive charts and color-coded indicators, you can create a dashboard that provides early warning signals and supports effective decision-making to keep the project under control.
Skill File Architecture: We propose a modular skill library in Markdown, organized by functional areas of the Excel-based project controls system. Each skill file is a self-contained AI agent "skill" (following Google Gemini's skill format) with clear tasks, constraints, and interfaces. These skills collaborate under an Orchestrator skill that coordinates their outputs for a cohesive solution. The skill files are numbered for clarity and future maintenance, e.g., 01_Excel_Project_Orchestrator.md, 02_Excel_Workbook_Architecture.md, etc.
Naming Convention: Each skill filename is prefixed with an order number (to enforce load sequence), followed by a descriptive name. Within each file, we use a standard structure:
Skill Title (H1): # Skill: [Skill Name]
Purpose & Scope (H2): The skill’s objective and boundaries.
Responsibilities (H2): What tasks the skill covers or decisions it makes.
Inputs (H2): Data, knowledge, or outputs from other skills required.
Outputs (H2): Deliverables produced (e.g., specific Excel sheets, formulas, or metrics).
Workflow (H2): Steps or logic the skill follows to produce its outputs.
Quality Assurance (H2): Built-in checks and safeguards for accuracy and consistency.
Best Practices (H2): Rules or constraints the skill follows to ensure maintainability and alignment with project control standards.
Interfaces & Data Contracts: Each skill clearly defines how it interacts with others:
Shared data structures (like the core project Task Plan table or the EVM metrics table).
Input/Output details (e.g., WBS skill produces a structured task list used by Gantt and EVM skills; EVM skill consumes schedule & cost data to compute performance metrics).
The Orchestrator ensures consistent timing (e.g., the sequence in which skills run to update the Excel model each reporting cycle).
Maintainability & Evolution: The skills are written to be reusable and easily modifiable. The structured approach means that updating a part of the process (e.g., migrating data to Power BI) can be done by replacing or augmenting a skill file without rewriting the entire system. The skill set anticipates future integration with Power BI: for example, the Dashboard skill could later be extended or complemented by a dedicated PowerBI integration skill, which could pull data from Excel or from enterprise sources as needed.

---

Below are the complete content of each Markdown skill file. These files can be copied into Google Gemini's knowledge base (e.g., in a GitHub repository for the Gem) to act as Agent Skills. The Orchestrator skill coordinates the rest, which cover specific domains: workbook architecture, WBS & budget, scheduling & Gantt, EVM & performance tracking, forecasting, dashboard/reporting & KPIs, data quality & checks, and governance (risk & change management).
Each skill is written as a specification and instructional file for the AI, with sections for purpose, responsibilities, inputs, outputs, constraints, workflow, and checks, to ensure robust and consistent project control practices.
