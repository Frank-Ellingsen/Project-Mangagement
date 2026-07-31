# 🚢 Project Controlling Control Tower — Multi-Project EVM & Agentic Auditing Ecosystem

I'm excited to share a major upgrade to a project I've been building: an **automated, interactive Project Controlling & Earned Value Management (EVM) Control Tower** designed for engineering, maritime, and defense sector projects. 

Originally built as a single-vessel controller, it has now scaled into a full **Multi-Project Portfolio Ecosystem**!

## 🎯 What It Is

A complete, local-first data pipeline that transforms raw transactional project logs into actionable portfolio intelligence — spanning **analytical databases, automated agentic audits, Excel reporting, Power BI compilation, and a Streamlit web dashboard** — all governed by **Edward Tufte's Data-Ink Ratio** principles, **PRINCE2** standards, and **AACE International** methodologies.

## 📊 Scale of the New Portfolio Ecosystem

The Control Tower now tracks a portfolio of **6 projects** representing different stages of physical completion:

1. **PRJ-001 (Composite Vessel Construction):** 99.5% complete, facing a 🔴 24.0% cost overrun driven by labor burn rates.
2. **PRJ-002 (Patrol Vessel Carbon Mold Design):** 0.0% complete, budgeted, and ready for initiation.
3. **PRJ-003 (Subsea Cable Installation Frame):** 30.0% complete, engineering design active.
4. **PRJ-004 (Autonomous Workboat Hull Weldments):** 70.0% complete, fabrication phase active.
5. **PRJ-005 (Defense Logistics Pontoon Build):** 90.0% complete, outfitting phase finishing.
6. **PRJ-006 (Lightweight Composite Cargo Hatch):** 100.0% completed, delivered 🟢 **under budget** (CPI = 1.02) and fully evaluated.

## 🤖 Premium Features Just Added

* **Local LLM Narration & Fallback:** Integrated a local LLM agent (**Ollama qwen2.5:latest**) directly in the dashboard to synthesize multi-agent audit logs into concise executive narratives. If Ollama is offline, it automatically falls back to a rule-based deterministic narrator.
* **Interactive Crashing & Delay Simulator:** Upgraded the Streamlit app and the Excel sheets with a schedule-crashing trade-off calculator. It computes the direct cost of adding overtime shifts vs. contract liquidated damages saved to find the net financial benefit.
* **AI-Guardrailed Write-Back Forms:** Added interactive entry forms in the Streamlit app to log new RAID items. Built-in guardrails block entries that violate project rules (e.g., issues must have high probability; high-impact risks require detailed mitigation strategies), writing data back to both the SQLite database and the source CSV files.
* **Post-Project Evaluation (Etterkalkyle):** Created a comprehensive close-out audit for PRJ-006 detailing final reconciliations, material nesting software efficiency savings (laser nesting saved 12%), and recommendations.
* **Interactive Excel Replication:** Replicated all dashboard views (KPIs, Gantt, Cost-Share, RAID logs, and simulators) inside a formula-driven, macro-free Excel workbook.

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Analytical DB** | DuckDB | High-speed EVM aggregations & portfolio SQL views |
| **Transactional DB** | SQLite | Transaction logs, RAID audit trails, write-back persistence |
| **Web Dashboard** | Streamlit + Plotly | Portfolio timelines, interactive Gantt charts, S-Curves, and What-If simulators |
| **Excel Reports** | OpenPyXL | Multi-tab interactive sheets reproducing the Streamlit dashboard using cell formulas |
| **BI Platform** | Power BI (.pbip) | Developer-mode star schema, relative M queries, DAX measures |
| **Agent Framework** | 13 specialized agents + Ollama | Automated audits across finance, risk, quality, engineering, and narrative generation |

## 📈 Standards Compliance

* **AACE International Practice Standard 10S-90** (EVM)
* **PMI Practice Standard for Earned Value Management**
* **PRINCE2** project management methodology
* **Edward Tufte's Data-Ink Ratio** principles for visual design
* **Chris Croft's** critical path scheduling methodology

## 🔗 Get Involved

The entire workspace is open-source on GitHub:
👉 https://github.com/Frank-Ellingsen/Project-Mangagement

Whether you're in project controls, maritime engineering, or just interested in data-driven project management, I'd love to hear your thoughts!

#ProjectManagement #EarnedValueManagement #EVM #DataAnalytics #MaritimeEngineering #PowerBI #Streamlit #Python #DuckDB #SQLite #PRINCE2 #Tufte #DataVisualization #ProjectControls #Engineering #Automation #OpenSource #ChrisCroft #AACE #PMI #ControlTower #ProjectAuditing #MultiAgentSystem #Ollama #LocalLLM #AIinProjectManagement #Etterkalkyle
