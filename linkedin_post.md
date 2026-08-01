# ⚓ Can you manage a 7,100,000 NOK engineering portfolio with ZERO licensing costs—100% locally?

I am excited to share a major update to a project I’ve been building: the **Agentic Project Controlling Control Tower**. Originally a single-vessel controller, it has now scaled into a fully automated, local-first **Multi-Project Portfolio Ecosystem**!

Designed specifically for engineering, maritime, and defense sector projects, this platform bridges the gap between raw data transactions and executive-level decision-making.

---

### 📊 The Portfolio Scope (7.1M NOK Under Control)
The Control Tower now tracks **6 distinct projects** in different stages of completion:
1. **PRJ-001 (Composite Vessel Construction):** 99.5% complete, facing a 🔴 24.0% cost overrun driven by labor burn rates.
2. **PRJ-002 (Patrol Vessel Carbon Mold Design):** 0.0% complete (Planned & ready for launch).
3. **PRJ-003 (Subsea Cable Frame):** 30.0% complete (Active engineering phase).
4. **PRJ-004 (Autonomous Workboat Hull):** 70.0% complete (Active fabrication phase).
5. **PRJ-005 (Defense Logistics Pontoon):** 90.0% complete (Active outfitting phase).
6. **PRJ-006 (Lightweight Cargo Hatch):** 100.0% completed, delivered 🟢 **under budget** (CPI = 1.02) and fully audited.

---

### 🤖 Premium Features Built for Project Controls

Here is what makes this system unique and why it's generating interest in project controlling circles:

* **Local LLM Executive Narration:** An offline AI agent (**Ollama + qwen2.5:latest**) runs locally to analyze multi-agent audit logs and generate concise, plain English board summaries on the dashboard. (No external APIs, no data leaks, no licensing costs).
* **Interactive Crashing & Delay Simulator:** Upgraded the Streamlit app and the Excel sheets with a schedule-crashing trade-off calculator. It computes the direct cost of adding overtime shifts vs. contract liquidated damages saved to find the net financial benefit.
* **AI-Guardrailed Write-Back Forms:** Interactive forms let users write RAID log entries directly back to SQLite and source CSVs, with guardrails that block invalid entries (e.g. flagging a high-impact risk without a mitigation strategy).
* **Post-Project Evaluation (Etterkalkyle):** Unlocked a close-out audit for PRJ-006 detailing how a **12% material saving** was achieved during composite carbon mold fabrication using advanced nesting software.
* **Tufte-Style Visualization:** Replaced generic dashboards with borderless metric cards and Gantt charts with **zero vertical gridlines**, maximizing the **Data-Ink Ratio** for rapid interpretation.

---

### 🛠️ The Local-First Architecture

* **Analytical Layer (DuckDB):** Handles high-speed EVM aggregations and compiles SQL views in milliseconds.
* **Transactional Layer (SQLite):** Manages audit logs, RAID history, and write-back persistence.
* **Visual Layer (Streamlit & Plotly):** Houses S-Curves, Gantt charts, and what-if simulators.
* **Excel Layer (OpenPyXL):** Automatically replicates the entire dashboard layout into a formula-driven, macro-free Excel workbook.
* **Semantic Layer (Power BI):** A star schema structure with relative M queries and robust DAX measures.

---

### 💡 Curiosity Builders: How does it work under the hood?
* How did laser nesting software save 12% in shipyard structural assembly?
* How does the Project Controller Agent automatically flag welder overtime limit breaches and cost variance slips?
* How can you dynamically simulate schedule-crashing (overtime vs. liquidated damages saved) using target CPI sliders directly in a web UI?

👉 Explore the full open-source repository here: https://github.com/Frank-Ellingsen/Project-Mangagement

Whether you are in project controls, financial controlling, maritime engineering, or building local-first AI systems, I would love to hear your feedback!

#ProjectManagement #EarnedValueManagement #EVM #DataAnalytics #MaritimeEngineering #PowerBI #Streamlit #Python #DuckDB #SQLite #PRINCE2 #Tufte #DataVisualization #ProjectControls #Engineering #Automation #OpenSource #ChrisCroft #AACE #PMI #ControlTower #ProjectAuditing #MultiAgentSystem #Ollama #LocalLLM #AIinProjectManagement #Etterkalkyle
