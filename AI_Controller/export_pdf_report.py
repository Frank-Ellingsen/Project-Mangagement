import os
import sqlite3
import duckdb
from datetime import datetime
from fpdf import FPDF

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUCKDB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")
SQLITE_PATH = os.path.join(BASE_DIR, "Data", "SQLite", "project_controlling.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "Reports")
PDF_PATH = os.path.join(OUTPUT_DIR, "PRJ-001_Executive_Board_Report.pdf")

class TufteReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 110, 120)
            self.cell(0, 10, "EXECUTIVE BOARD BRIEFING: PROJECT PRJ-001", ln=1, align="L")
            self.set_draw_color(220, 225, 230)
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 145, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}  |  Confidential  |  PRINCE2 & AACE Compliant", align="C")

def generate_pdf():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Fetch data from DuckDB
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
    
    # 2. Fetch data from SQLite
    conn = sqlite3.connect(SQLITE_PATH)
    overtimes = conn.execute("""
        SELECT r.ResourceName, r.Role, strftime('%Y-%W', t.WorkDate) as WeekVal, SUM(CAST(t.HoursWorked AS REAL)) as WeeklyHours
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

    # Build PDF Document
    pdf = TufteReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Title & Metadata block
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(26, 37, 47) # Sleek Navy
    pdf.cell(0, 10, "EXECUTIVE BOARD BRIEFING: PROJECT PRJ-001", ln=1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(0, 5, f"Report Period: Month-End June 2026", ln=1)
    pdf.cell(0, 5, f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    pdf.cell(0, 5, f"Classification: Internal Restricted (CFO & Board)", ln=1)
    pdf.cell(0, 5, f"Standard: PRINCE2 & AACE International Compliance", ln=1)
    
    pdf.ln(5)
    pdf.set_draw_color(226, 232, 240)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # 1. Executive Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 37, 47)
    pdf.cell(0, 8, "1. Executive Summary", ln=1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    status_str = "CRITICAL OVERRUN" if proj_cpi < 0.95 else "ON TRACK"
    
    pdf.multi_cell(0, 5, 
        f"The project Composite Maritime Vessel Construction (PRJ-001) is currently at {overall_pct:.1f}% physical progress "
        f"but has breached cost tolerances, finishing with an overall status of {status_str}."
    )
    pdf.ln(3)

    # KPI Table (Tufte style - no vertical gridlines)
    col_w = 47
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100, 110, 120)
    # Header Line
    pdf.cell(col_w, 6, "Metric Name", border="B", align="L")
    pdf.cell(col_w, 6, "Value (USD)", border="B", align="R")
    pdf.cell(col_w, 6, "Metric Name", border="B", align="L")
    pdf.cell(col_w, 6, "Value (USD)", border="B", align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    
    kpis = [
        ("Total Budget (BAC)", f"${tot_bac:,.2f}", "Actual Cost (AC)", f"${tot_ac:,.2f}"),
        ("Value Earned (EV)", f"${tot_ev:,.2f}", "Cost Variance (CV)", f"${tot_cv:+,.2f}"),
        ("Cost Performance Index (CPI)", f"{proj_cpi:.2f}", "Projected Overrun (VAC)", f"${tot_vac:+,.2f}")
    ]
    
    for left_lbl, left_val, right_lbl, right_val in kpis:
        pdf.cell(col_w, 6, left_lbl, align="L")
        # Bold warning CPI or CV
        if "CPI" in left_lbl and proj_cpi < 0.95:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(231, 76, 60) # Muted Red
        pdf.cell(col_w, 6, left_val, align="R")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(51, 65, 85)
        
        pdf.cell(col_w, 6, right_lbl, align="L")
        if "VAC" in right_lbl and tot_vac < 0:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(231, 76, 60)
        pdf.cell(col_w, 6, right_val, align="R")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(51, 65, 85)
        pdf.ln()
    
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # 2. WBS Performance Matrix Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 37, 47)
    pdf.cell(0, 8, "2. Work Breakdown Structure (WBS) Performance Matrix", ln=1)
    pdf.ln(1)

    # Table Header (Tufte style)
    # WBS (15), Name (50), BAC (30), AC (30), EV (30), CPI (15), Status (20)
    w_wbs, w_name, w_bac, w_ac, w_ev, w_cpi, w_stat = 15, 60, 25, 25, 25, 15, 25
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(w_wbs, 6, "WBS", border="B", align="L")
    pdf.cell(w_name, 6, "WBS Element Name", border="B", align="L")
    pdf.cell(w_bac, 6, "BAC", border="B", align="R")
    pdf.cell(w_ac, 6, "AC", border="B", align="R")
    pdf.cell(w_ev, 6, "EV", border="B", align="R")
    pdf.cell(w_cpi, 6, "CPI", border="B", align="R")
    pdf.cell(w_stat, 6, "Status", border="B", align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(51, 65, 85)
    for row in wbs_metrics:
        wbs_code, name, bac, ac, ev, cpi, pct, eac = row
        wbs_status = "Overrun" if cpi < 0.95 else "On Track"
        
        pdf.cell(w_wbs, 6, str(wbs_code), align="L")
        pdf.cell(w_name, 6, name[:35], align="L")
        pdf.cell(w_bac, 6, f"${bac:,.0f}", align="R")
        pdf.cell(w_ac, 6, f"${ac:,.0f}", align="R")
        pdf.cell(w_ev, 6, f"${ev:,.0f}", align="R")
        
        # Color warning CPI
        if cpi < 0.95:
            pdf.set_font("Helvetica", "B", 8.5)
            pdf.set_text_color(231, 76, 60)
        pdf.cell(w_cpi, 6, f"{cpi:.2f}", align="R")
        pdf.cell(w_stat, 6, wbs_status, align="R")
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(51, 65, 85)
        pdf.ln()
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # 3. Financial Cost-Share Drivers
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 37, 47)
    pdf.cell(0, 8, "3. Financial Cost-Share Drivers", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 5, 
        f"Analysis of actual expenditures reveals that labor accounts for the dominant share of the budget slippage:\n"
        f"  * Labor Actual Spend: ${labor_cost:,.2f} ({labor_cost/tot_ac*100:.1f}% of total cost)\n"
        f"  * Material Actual Spend: ${material_cost:,.2f} ({material_cost/tot_ac*100:.1f}% of total cost)"
    )
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 37, 47)
    pdf.cell(0, 6, "Resource & Audit Anomalies", ln=1)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    
    # Overtime
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, "Labor Overtime Violations (>45 hrs/week):", ln=1)
    pdf.set_font("Helvetica", "", 9)
    if overtimes:
        for name, role, week, hours in overtimes:
            pdf.cell(0, 5, f"  * [ALERT] Resource {name} ({role}) logged {hours:.1f} hours during Week {week}.", ln=1)
    else:
        pdf.cell(0, 5, "  * No resource weekly overtime violations detected.", ln=1)
    pdf.ln(2)

    # High Value Invoices
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 5, "High-Value Procurement Invoices (>$50,000):", ln=1)
    pdf.set_font("Helvetica", "", 9)
    if large_invoices:
        for pid, desc, cost in large_invoices:
            pdf.cell(0, 5, f"  * [AUDIT] Invoice {pid} for '{desc}' was processed at ${cost:,.2f}.", ln=1)
    else:
        pdf.cell(0, 5, "  * No invoices exceeded the threshold.", ln=1)
    
    pdf.ln(4)

    # 4. RAID Log & Project Risk Status
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 37, 47)
    pdf.cell(0, 8, "4. RAID Log & Project Risk Status", ln=1)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "Active items on the RAID registry requiring direct board oversight:", ln=1)
    pdf.ln(2)

    # Table: ID, Category, Description, Impact, Probability, Owner
    w_id, w_cat, w_desc, w_imp, w_prob, w_owner = 15, 25, 85, 20, 20, 25
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(100, 110, 120)
    pdf.cell(w_id, 6, "ID", border="B", align="L")
    pdf.cell(w_cat, 6, "Category", border="B", align="L")
    pdf.cell(w_desc, 6, "Description", border="B", align="L")
    pdf.cell(w_imp, 6, "Impact", border="B", align="R")
    pdf.cell(w_prob, 6, "Probability", border="B", align="R")
    pdf.cell(w_owner, 6, "Owner", border="B", align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(51, 65, 85)
    if active_raid:
        for rid, rtype, desc, impact, prob, owner in active_raid:
            pdf.cell(w_id, 6, str(rid), align="L")
            pdf.cell(w_cat, 6, rtype, align="L")
            pdf.cell(w_desc, 6, desc[:48], align="L")
            pdf.cell(w_imp, 6, impact, align="R")
            pdf.cell(w_prob, 6, prob, align="R")
            pdf.cell(w_owner, 6, owner, align="R")
            pdf.ln()
    else:
        pdf.cell(0, 6, "No active risks registered", align="C")
        pdf.ln()
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # 5. Corrective Action Plan & Recommendations
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 37, 47)
    pdf.cell(0, 8, "5. Corrective Action Plan & Recommendations", ln=1)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(51, 65, 85)
    
    recs = [
        "1. Outfitting Cost Control (Reason: Contractor Rate Increases & Design Variations): Audit outfitting contracts and renegotiate hourly rates to control labor burn. Instigate a strict change-order freeze on WBS 1.0 (PM & Engineering) and WBS 3.0 (Outfitting) to block unbudgeted design features.",
        "2. Contract Penalty Mitigation: WBS 4.0 (Sea Trials) has slip risk. Enacting a schedule crash (overlapping testing crew shift) costs an extra $10,000 but saves $50,000 in liquidated damages penalty (Net Benefit: +$40,000).",
        "3. Resource Reallocation: Reallocate excess structural welding capacity to delayed outfitting tasks to optimize yard-wide capacity and reduce overall costs."
    ]
    
    for rec in recs:
        pdf.multi_cell(0, 5, rec)
        pdf.ln(2)

    pdf.output(PDF_PATH)
    print(f"PDF report generated successfully at: {PDF_PATH}")

if __name__ == "__main__":
    generate_pdf()
