# Agent Control Tower Streamlit Application User Guide

Welcome to the **Agent Control Tower User Guide**. This manual guides project controllers, managers, and executives through using the interactive Streamlit web app (`AI_Controller/agent_skills_app.py`).

---

## 🧭 Navigation Overview

The application features a left sidebar navigation menu with **4 primary views**:

```
📌 Navigation Views
 ├── 1. Agent Control Tower (Front Page)
 ├── 2. 👥 Stakeholder Reports
 ├── 3. Individual Agent Skill Inspector
 └── 4. 🤖 Live Crew Execution
```

---

## 1. ⚓ Front Page: Agent Control Tower Dashboard

When you open the application, you are presented with the **Agent Control Tower Front Page**:

### A. Executive KPI Metrics Bar (Top)

- **Budget at Completion (BAC)**: Baseline total budget allocated across the 6-project portfolio (7,100,000 NOK).
- **Actual Cost (AC)**: Cumulative actual expenditure (5,220,810 NOK).
- **Earned Value (EV)**: Value of work physically completed to date (4,752,500 NOK).
- **Project CPI**: Cost Performance Index (`0.91` - highlighted in red to indicate portfolio-wide overrun).
- **Physical Progress**: Overall completion percentage (`66.9%`).

### B. Interactive Schedule & WBS Gantt Chart

- **Context Switcher Dropdown**: Toggle schedule view between:
  - `PRJ-001 (Composite Vessel)`: Vessel construction WBS 1.0 - 4.0.
  - `PRJ-002 (Patrol Vessel)`: Autonomous patrol boat schedule.
  - `Multi-Project Portfolio View`: Side-by-side comparative timeline.
- **Tufte Features**: Vertical gridlines are removed for clear visual reading. Physical progress percentages (`97.5%`, `100.0%`) are labeled directly on bars.
- **Status Highlights**: Slate Blue (`#2c3e50`) indicates On-Track tasks; Crimson Red (`#e74c3c`) indicates Over-Budget tasks.

### C. Domain Analysis Tabs

- **📊 Project Controller (EVM & Forecasts)**: View detailed WBS performance matrix and run the **Dynamic EAC/VAC Forecast Simulator** using interactive target CPI sliders.
- **💼 CFO & Profitability Audit**: View Labor vs. Material cost split donut charts (71.8% labor share) and top resource hourly burn rates.
- **📜 Contract, Risk & Anomaly Audit**: Audit resource overtime (>45 hrs/wk), large purchases (>50k NOK), and active RAID log items.
- **🏗️ Production & Quality Control**: Inspect physical assembly completion bar charts per WBS element.

---

## 2. 👥 Stakeholder Reports View

Select **`👥 Stakeholder Reports`** in the sidebar to generate tailored executive summaries for specific roles:

| Stakeholder Persona                               | Key Information & Metrics Focus                                                                                                           |
| :------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **👑 Executive Steering Committee (CFO & Board)** | High-level financial risk, capital exposure, BAC vs EAC (1.86M NOK), VAC overrun (-359.5k NOK / 24%), and CFO margin mitigation guidance. |
| **🎯 Project Manager (Operational Control)**      | Physical progress %, Earned Value (EV), WBS matrix, critical path schedule, and active RAID log items.                                    |
| **📐 Engineering Lead (Design & Hours)**          | WBS 1.0 budget vs actuals (300k vs 419k NOK), design progress (97.5%), and resource-level engineering hours burn rates.                   |
| **🏗️ Yard & Production Manager**                  | Hull assembly (100%), Outfitting (100%), welder/electrician labor logs, and shop-floor overtime alerts.                                   |
| **📦 Procurement Lead**                           | Material spend breakdown (522k NOK), high-value supplier invoices (>50k NOK), and carbon sheet delivery risks.                            |
| **🛡️ Quality & Class Inspector (DNV)**            | DNV milestone verification, non-destructive weld testing results, and Sea Trials readiness (WBS 4.0).                                     |

---

## 3. 🔍 Individual Agent Skill Inspector

Select **`Individual Agent Skill Inspector`** in the sidebar to review the underlying system prompt, capabilities, and system rules for any of the **13 Agent Skills**:

- `project-controller-agent`
- `project-cfo-agent`
- `project-contract-manager-agent`
- `project-controlling-evm`
- `project-engineering-lead-agent`
- `project-evaluation-agent`
- `project-manager-agent`
- `project-procurement-agent`
- `project-production-agent`
- `project-quality-agent`
- `project-research-agent`
- `project-support-agent`
- `tufte-dashboard-designer`

---

## 4. 🤖 Live Crew Execution Console

Select **`Live Crew Execution`** to run live Python automated audit routines:

1. Click **`🚀 Run All 4 Agent Audits`**.
2. The app triggers `run_all_agents()` in the background and prints the live text audit report for Controller, CFO, Risk, and Quality agents directly on screen.

---

## 💡 Frequently Asked Questions & Troubleshooting

### Q: Why does the app display database error messages?

**A:** The database files (`project_controlling.db`) must be initialized first. Run:

```powershell
python AI_Controller/build_duckdb.py
python AI_Controller/build_sqlite.py
```

### Q: How do I change the target CPI in the EAC forecast simulator?

**A:** Go to the **Front Page -> 📊 Project Controller Tab** and adjust the **"Target Future Performance Index (CPI)"** slider. The simulated EAC and VAC waterfall chart will recalculate instantly.

### Q: How do I open the app from PowerShell?

From the project root folder, run:

```powershell
streamlit run AI_Controller/agent_skills_app.py
```

_Alternatively, run `./run_all.ps1` and select Option `[8]`._
