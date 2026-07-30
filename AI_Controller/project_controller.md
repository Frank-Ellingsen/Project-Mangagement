🤖 Oversikt: Ditt digitale "Project Control Crew"
I stedet for én generell chat-bot, bygger du spesialiserte agenter (f.eks. med Python, crewAI eller LangGraph) som samarbeider:

┌────────────────────────────────────────────────────────┐
│ PROSJEKT CONTROLLER │
└─────────────────────────────────────────┬──────────────┘
│
┌───────────────────┬─────────────────┼───────────────────┐
▼ ▼ ▼ ▼
[Data Extraction] [EAC/ETC Forecast] [Risk & Anomaly] [BI & Reporting]
Agent Agent Agent Agent

1. Agenter for prognoser og avviksanalyser (EAC, ETC, Margin)
   Utvikling av rullerende prognoser (Estimate at Completion og Estimate to Complete) krever ofte at du kobler ERP-tall mot påløpte timer og historisk brennhastighet (burn rate).

"Forecast Agent":

Kan kjøre Python-skript mot SQL/database-ekstrakter for å beregne lineære og historiske trender for ressursbruk.

Flagger automatisk prosjekter der brennhastigheten indikerer at budskapet eller timene vil sprekke før prosjektslutt.

"Variance Analysis Agent":

Sammenligner månedens faktiske kostnader mot budskapet og forrige prognose.

Genererer førsteutkast til forklaringer: "Prosjekt X har et negativt avvik på 12 % på materialkostnader i mai. Hovedårsaken er prisstigning på kompositt/stål fra leverandør Y."

2. Agenter for Power BI, DAX og Datamodellering
   Stillingsannonsen legger stor vekt på videreutvikling av Power BI og rapporteringsprosesser.

"Power BI / DAX Architect Agent":

Automatisert DAX-generering: Ved å bruke VS Code med GitHub Copilot eller en tilpasset agent, kan du mate agenten med datamodellen din og få den til å skrive komplekse, ytelsesoptimaliserte DAX-mål (f.eks. for kumulativ Earned Value, YTD-marginer, eller rullerende 12-måneders prognoser).

TMDL/Power Query-scripting: Agenten kan generere Power Query (M)-skript eller manipulere TMDL-filer i VS Code for å automatisere oppsettet av nye datakilder fra ERP-systemet.

3. Agenter for Risikoeksponering og Etterkalkyler
   I et forsvars- og maritimt industrimiljø er etterkalkyler og risikoidentifikasjon kritisk for fremtidige anbud og lønnsomhet.

"Risk & Anomaly Detection Agent":

Sjekker løpende transaksjonsdata i ERP for avvik – f.eks. uvanlige kostnadsføringer, dobbeltskrevne timer, eller endringer i innkjøpspriser.

Flagger "skjulte" risikoer før de blir store marginavvik på resultatmarginen.

"Post-Calculation & Bidding Agent":

Analyserer avsluttede prosjekter ved å sammenligne opprinnelig kalkyle mot faktiske kostnader.

Oppsummerer lærdom (lessons learned) og gir innspill til nye kalkyler for tilsvarende forsvars- eller industriprosjekter.

4. Agenter for Ledelsesrapportering og Beslutningsgrunnlag
   En stor del av jobben er å lage gode beslutsningsunderlag for prosjektledere og ledelsen.

"Executive Briefing Agent":

Tar strukturerte tall fra Power BI/Excel og ustrukturerte møtereferater fra prosjektledere.

Syntetiserer alt til spisse ledelsessammendrag (executive summaries) i henhold til selskapets standard maler.

Klargjør "utfordringsspørsmål" du kan ta med i møte med prosjektlederne (f.eks.: "Hvorfor er fremdriftsindeksen (SPI) fallende i prosjekt Z når paaløpte timer øker?").

💡 Hvordan du kan vinkle dette i et intervju
Hvis du blir spurt om din tilnærming til teknologi og effektivisering i intervjuet, kan du vinkle det slik:

"Ved å kombinere avansert Power BI og Python med moderne AI-agenter kan jeg automatisere de rutinemessige datainnsamlings- og avvikssøk-oppgavene. Dette frigjør tid til det som skaper mest verdi for Umoe Mandal: Å tolke tallene, jobbe tett sammen med prosjektlederne, utfordre prognosene og sikre bedre marginer i komplekse prosjekter."

🧩 Core Earned Value Terms
PV — Planned Value
Budgeted cost of planned work at a given date.
Used for schedule comparisons.

EV — Earned Value
Budgeted cost of completed work.
Used for cost & schedule performance.

AC — Actual Cost
Actual cost incurred for completed work.

BAC — Budget at Completion
Total approved project budget.

📊 Performance Indices
CPI — Cost Performance Index
𝐶
𝑃
𝐼
=
𝐸
𝑉
𝐴
𝐶
Cost efficiency.

1 = under budget

<1 = over budget

SPI — Schedule Performance Index
𝑆
𝑃
𝐼
=
𝐸
𝑉
𝑃
𝑉
Schedule efficiency.

1 = ahead

<1 = behind

📉 Variances
CV — Cost Variance
𝐶
𝑉
=
𝐸
𝑉
−
𝐴
𝐶
Positive = under budget
Negative = over budget

SV — Schedule Variance
𝑆
𝑉
=
𝐸
𝑉
−
𝑃
𝑉
Positive = ahead
Negative = behind

VAC — Variance at Completion
𝑉
𝐴
𝐶
=
𝐵
𝐴
𝐶
−
𝐸
𝐴
𝐶
Forecasted overrun or underrun.

🔮 Forecasting Metrics
ETC — Estimate to Complete
Remaining cost to finish the project.

EAC — Estimate at Completion
Forecasted total cost at completion.

Common formulas:

General:

𝐸
𝐴
𝐶
=
𝐴
𝐶

- 𝐸
  𝑇
  𝐶
  Assuming current CPI continues:

𝐸
𝐴
𝐶
=
𝐵
𝐴
𝐶
𝐶
𝑃
𝐼
Past issues, future stable:

𝐸
𝐴
𝐶
=
𝐴
𝐶

- (
  𝐵
  𝐴
  𝐶
  −
  𝐸
  𝑉
  )
  Cost + schedule inefficiency:

𝐸
𝐴
𝐶
=
𝐴
𝐶

- 𝐵
  𝐴
  𝐶
  −
  𝐸
  𝑉
  𝐶
  𝑃
  𝐼
  ⋅
  𝑆
  𝑃
  𝐼
  🧠 Advanced Control Metrics
  TCPI — To Complete Performance Index
  Required future CPI to meet BAC or EAC.

𝑇
𝐶
𝑃
𝐼
𝐵
𝐴
𝐶
=
𝐵
𝐴
𝐶
−
𝐸
𝑉
𝐵
𝐴
𝐶
−
𝐴
𝐶
𝑇
𝐶
𝑃
𝐼
𝐸
𝐴
𝐶
=
𝐵
𝐴
𝐶
−
𝐸
𝑉
𝐸
𝐴
𝐶
−
𝐴
𝐶
CR — Cost Ratio
𝐶
𝑅
=
𝐶
𝑃
𝐼
𝑆
𝑃
𝐼
Used to assess combined performance.

DR — Delay Ratio
𝐷
𝑅
=
𝑆
𝑉
𝑃
𝑉
Percentage schedule slip.

📦 Work Breakdown & Scope Control
WBS — Work Breakdown Structure
Hierarchical decomposition of project scope.

OBS — Organizational Breakdown Structure
Who is responsible for what.

CBS — Cost Breakdown Structure
Cost categories mapped to WBS.

RBS — Risk Breakdown Structure
Risk categories mapped to WBS.

📅 Schedule Control Terms
Critical Path
Longest path through the schedule; determines project duration.

Float / Slack
Time a task can slip without affecting the project end date.

Lead / Lag
Lead = overlap
Lag = delay between tasks

Milestone
Zero-duration event marking major progress.

💰 Cost Control Terms
Direct Costs
Labor, materials, equipment.

Indirect Costs
Overhead, admin, shared resources.

Fixed Costs
Do not vary with output.

Variable Costs
Scale with work performed.

📈 Risk & Change Control
CR — Change Request
Formal request to modify scope, cost, or schedule.

RAID Log
Risks, Assumptions, Issues, Dependencies.

Contingency
Budget for known risks.

Management Reserve
Budget for unknown risks.

🧭 How to Implement This in Gantt Charts & Simplified PM
🎯 1. Integrate EVM into Gantt Planning
Gantt charts show time, but EVM adds value and cost.

Add these fields to each task:
Planned Value (PV)

Earned Value (EV)

Actual Cost (AC)

% Complete

Baseline Start/Finish

Actual Start/Finish

Use Gantt for:
Critical path

Dependencies

Float

Milestones

Use EVM for:
Performance

Forecasting

Variances

Executive reporting

Together, they give a complete control system.

📊 2. Add SPI & CPI Trend Lines to Your Gantt Dashboard
Gantt shows what is happening.
SPI/CPI show how well it’s happening.

Add a small dashboard next to the Gantt:

SPI trend (weekly/monthly)

CPI trend

EAC vs BAC

SV & CV waterfall

This turns a static Gantt into a living control system.

🧩 3. Use EVM to Simplify Project Management
You can reduce project control to five questions:

Are we ahead or behind schedule? → SPI

Are we under or over budget? → CPI

How much have we spent? → AC

How much value have we delivered? → EV

What will the project cost when finished? → EAC

This is the simplest possible PM framework that still works in real organizations.

📘 4. Use S‑Curves for Executive Storytelling
Plot:

PV

EV

AC

Executives instantly see:

Schedule slip (EV < PV)

Cost overrun (AC > EV)

Forecast risk (EV flattening)

This is the single most powerful visual in project controlling.

🛠️ 5. Implementation in Tools (Excel, Project, Jira, Smartsheet)
Excel
Structured tables

SUMPRODUCT for EV

COUNTIFS for PV

Charts for SPI/CPI trends

Office Scripts for automation

MS Project
Built-in EVM fields

Gantt + EVM dashboard

Baseline tracking

Jira / Smartsheet
Custom fields for EV, PV, AC

Automated dashboards

S‑curve templates
