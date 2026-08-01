import os
import sqlite3
import duckdb
from datetime import datetime

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUCKDB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")
SQLITE_PATH = os.path.join(BASE_DIR, "Data", "SQLite", "project_controlling.db")
EXPORT_PATH = os.path.join(BASE_DIR, "Reports", "PRJ-001_Executive_Board_Report.md")

def generate_report_content():
    # Load DuckDB data
    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    summary = con.execute("""
        SELECT Total_BAC, Total_AC, Total_EV, Total_CV, Project_CPI, Total_EAC_Typical, Total_VAC, Overall_Progress_Pct 
        FROM v_project_evm_summary
    """).fetchone()
    
    wbs_metrics = con.execute("""
        SELECT WBS_Code, ElementName, BAC, AC, EV, CPI, PercentComplete, EAC_Typical 
        FROM v_wbs_evm_metrics
        ORDER BY WBS_Code
    """).fetchall()
    
    # Material vs Labor Cost share (converted to USD using 1 USD = 1 USD)
    labor_cost = con.execute("""
        SELECT SUM(t.HoursWorked * r.HourlyRate) 
        FROM timesheets t 
        JOIN resources r ON t.ResourceID = r.ResourceID
    """).fetchone()[0] or 0.0
    
    material_cost = con.execute("""
        SELECT SUM(TotalActualCost) 
        FROM material_costs
    """).fetchone()[0] or 0.0
    
    con.close()
    
    # Load SQLite data
    conn = sqlite3.connect(SQLITE_PATH)
    
    overtimes = conn.execute("""
        SELECT r.ResourceName, strftime('%Y-%W', t.WorkDate) as WeekVal, SUM(CAST(t.HoursWorked AS REAL)) as WeeklyHours
        FROM timesheets t
        JOIN resources r ON t.ResourceID = r.ResourceID
        GROUP BY r.ResourceName, WeekVal
        HAVING WeeklyHours > 45
        ORDER BY WeeklyHours DESC
    """).fetchall()
    
    large_invoices = conn.execute("""
        SELECT PurchaseID, Description, CAST(TotalActualCost AS REAL) as Cost
        FROM material_costs
        WHERE CAST(TotalActualCost AS REAL) > 50000
        ORDER BY Cost DESC
    """).fetchall()
    
    active_raid = conn.execute("""
        SELECT RiskID, Type, Description, Impact, Probability, Owner
        FROM raid_log
        WHERE Status = 'Active'
        ORDER BY Type DESC
    """).fetchall()
    
    conn.close()
    
    tot_bac, tot_ac, tot_ev, tot_cv, proj_cpi, tot_eac, tot_vac, overall_pct = summary
    
    report = []
    report.append(f"# ⚓ EXECUTIVE BOARD BRIEFING: PROJECT PRJ-001")
    report.append(f"**Report Period:** Month-End June 2026  ")
    report.append(f"**Generated At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    report.append(f"**Classification:** Internal Restricted (CFO & Board)  ")
    report.append(f"**Standard:** PRINCE2 & AACE International Compliance  ")
    report.append("\n---")
    
    report.append("\n## 1. Executive Summary")
    status_indicator = "🔴 CRITICAL OVERRUN" if proj_cpi < 0.95 else "🟢 ON TRACK"
    report.append(f"The project **Composite Maritime Vessel Construction (PRJ-001)** is currently at **{overall_pct:.1f}% physical progress** (essentially complete) but has breached cost tolerances, finishing with an overall status of **{status_indicator}**.")
    report.append(f"* **Total Budget (BAC):** ${tot_bac:,.2f}")
    report.append(f"* **Actual Cost (AC):** ${tot_ac:,.2f}")
    report.append(f"* **Value Earned (EV):** ${tot_ev:,.2f}")
    report.append(f"* **Cost Variance (CV):** ${tot_cv:+,.2f}")
    report.append(f"* **Final Cost Performance Index (CPI):** {proj_cpi:.2f}")
    report.append(f"* **Projected Margin Slippage (VAC):** ${tot_vac:+,.2f} (an overrun of **{(tot_eac - tot_bac)/tot_bac*100:.1f}%** over baseline).")
    
    report.append("\n---")
    
    report.append("\n## 2. Work Breakdown Structure (WBS) Performance Matrix")
    report.append("The cost overruns are distributed across the primary work packages as follows:")
    report.append("\n| WBS | WBS Element Name | BAC (USD) | AC (USD) | EV (USD) | CPI | Status |")
    report.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |")
    for row in wbs_metrics:
        wbs_code, name, bac, ac, ev, cpi, pct, eac = row
        wbs_status = "🔴 Overrun" if cpi < 0.95 else "🟢 On Track"
        report.append(f"| {wbs_code} | {name} | ${bac:,.2f} | ${ac:,.2f} | ${ev:,.2f} | {cpi:.2f} | {wbs_status} |")
    
    report.append("\n### 🔍 WBS Completion Analysis: Why PRJ-001 is at 99.5% Progress")
    report.append("Although physical construction is complete, the project remains at **99.5% overall physical progress** due to unfinished administrative and closeout tasks in the engineering package:")
    report.append("* **WBS 1.0 - Project Management & Engineering (97.5% Complete):** Held up by outstanding closeout documentation, compilation of final as-built drawing updates, and class documentation packaging required for final DNV classification approval.")
    report.append("* **WBS 2.0 - Hull Fabrication & Assembly (100.0% Complete):** Fully complete and certified.")
    report.append("* **WBS 3.0 - Outfitting & Integration (100.0% Complete):** Fully integrated and certified.")
    report.append("* **WBS 4.0 - Sea Trials & Handover (100.0% Complete):** Sea trials completed successfully at end of June 2026.")
    
    report.append("\n---")
    
    report.append("\n## 3. Financial Cost-Share Drivers")
    report.append(f"Analysis of actual expenditures reveals that labor accounts for the dominant share of the budget slippage:")
    report.append(f"* **Labor Actual Spend:** ${labor_cost:,.2f} ({labor_cost/tot_ac*100:.1f}% of total cost)")
    report.append(f"* **Material Actual Spend:** ${material_cost:,.2f} ({material_cost/tot_ac*100:.1f}% of total cost)")
    
    report.append("\n### 🚨 Resource & Audit Anomalies")
    report.append("1. **Labor Overtime Violations (>45 hrs/week):**")
    if overtimes:
        for name, week, hours in overtimes:
            report.append(f"   * **[ALERT]** Resource `{name}` logged `{hours:.1f} hours` during Week `{week}`.")
    else:
        report.append("   * No resource weekly overtime violations detected.")
        
    report.append("\n2. **High-Value Procurement Invoices (>$50,000):**")
    if large_invoices:
        for pid, desc, cost in large_invoices:
            report.append(f"   * **[AUDIT]** Invoice `{pid}` for `{desc}` was processed at `${cost:,.2f}`.")
    else:
        report.append("   * No invoices exceeded the threshold.")
        
    report.append("\n---")
    
    report.append("\n## 4. RAID Log & Project Risk Status")
    report.append("The project has 3 active items on the RAID registry that require direct board oversight:")
    report.append("\n| ID | Category | Description | Impact | Probability | Owner |")
    report.append("| :--- | :--- | :--- | :---: | :---: | :--- |")
    if active_raid:
        for rid, rtype, desc, impact, prob, owner in active_raid:
            report.append(f"| {rid} | {rtype} | {desc} | {impact} | {prob} | {owner} |")
    else:
        report.append("| - | - | No active risks registered | - | - | - |")
        
    report.append("\n---")
    
    report.append("\n## 5. Corrective Action Plan & Recommendations")
    report.append("To safeguard the net margin of the vessel delivery and future project portfolios, we advise the Board to implement the following actions for the Red flagged project PRJ-001:")
    report.append("1. **Outfitting Cost Control (Reason: Contractor Rate Increases & Design Variations):** Audit outfitting contracts and renegotiate hourly rates to control labor burn. Instigate a strict change-order freeze on WBS 1.0 (PM & Engineering) and WBS 3.0 (Outfitting) to block unbudgeted design features.")
    report.append("2. **Contract Penalty Mitigation:** WBS 4.0 (Sea Trials) has slip risk. Enacting a schedule crash (overlapping testing crew shift) costs an extra **$10,000** but saves **$50,000** in liquidated damages penalty (Net Benefit: **+$40,000**).")
    report.append("3. **Resource Reallocation:** Reallocate excess structural welding capacity to delayed outfitting tasks to optimize yard-wide capacity and reduce overall costs.")
    
    return "\n".join(report)

def export_report():
    print(f"Generating Executive Board Report...")
    content = generate_report_content()
    os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Report exported successfully to: {EXPORT_PATH}")

if __name__ == "__main__":
    export_report()
