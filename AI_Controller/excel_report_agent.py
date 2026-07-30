import os
import duckdb
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")
REPORT_PATH = os.path.join(BASE_DIR, "Data", "vessel_construction_report.xlsx")

def create_excel_report():
    print(f"Loading EVM data from DuckDB...")
    con = duckdb.connect(DB_PATH)
    wbs_metrics = con.execute("""
        SELECT WBS_Code, ElementName, BAC, AC, EV, CPI, PercentComplete, EAC_Typical 
        FROM v_wbs_evm_metrics
        ORDER BY WBS_Code
    """).fetchall()
    
    summary = con.execute("""
        SELECT Total_BAC, Total_AC, Total_EV, Total_CV, Project_CPI, Total_EAC_Typical, Total_VAC, Overall_Progress_Pct 
        FROM v_project_evm_summary
    """).fetchone()
    con.close()
    
    # Initialize OpenPyXL workbook
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # TAB 1: EVM Dashboard
    # ----------------------------------------------------
    ws_dash = wb.active
    ws_dash.title = "EVM Dashboard"
    ws_dash.views.sheetView[0].showGridLines = True
    
    # Styles
    title_font = Font(name="Segoe UI", size=16, bold=True, color="2C3E50")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Segoe UI", size=11, bold=True, color="2C3E50")
    regular_font = Font(name="Segoe UI", size=11, color="333333")
    muted_font = Font(name="Segoe UI", size=10, italic=True, color="7F8C8D")
    
    header_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
    accent_fill = PatternFill(start_color="ECF0F1", end_color="ECF0F1", fill_type="solid")
    alert_fill = PatternFill(start_color="FADBD8", end_color="FADBD8", fill_type="solid")
    
    thin_bottom = Border(bottom=Side(style='thin', color='BDC3C7'))
    double_bottom = Border(bottom=Side(style='double', color='2C3E50'), top=Side(style='thin', color='BDC3C7'))
    
    # Title
    ws_dash["A1"] = "PROJECT VESSEL PERFORMANCE DASHBOARD (EVM)"
    ws_dash["A1"].font = title_font
    ws_dash.row_dimensions[1].height = 30
    
    # Metadata
    ws_dash["A2"] = "Report Generated: 2026-07-29 | Method: DuckDB Analytical Integration"
    ws_dash["A2"].font = muted_font
    
    # KPI Cards (Tufte style: large values, clean labels, no borders)
    kpis = [
        ("BUDGET (BAC)", summary[0], "$#,##0.00"),
        ("ACTUAL COST (AC)", summary[1], "$#,##0.00"),
        ("EARNED VALUE (EV)", summary[2], "$#,##0.00"),
        ("CPI", summary[4], "0.00"),
        ("PROGRESS", summary[7] / 100, "0.0%")
    ]
    
    for i, (label, val, fmt) in enumerate(kpis):
        col_idx = i * 2 + 1
        ws_dash.cell(row=4, column=col_idx, value=label).font = muted_font
        val_cell = ws_dash.cell(row=5, column=col_idx, value=val)
        val_cell.font = Font(name="Segoe UI", size=18, bold=True, color="2C3E50")
        val_cell.number_format = fmt
        if label == "CPI" and val < 0.95:
            val_cell.fill = alert_fill
            
    # WBS Table Headers
    headers = ["WBS", "WBS Element Name", "Planned Cost (BAC)", "Actual Cost (AC)", "Earned Value (EV)", "CPI", "Progress", "EAC (Typical)", "Status"]
    for col_idx, header in enumerate(headers, start=1):
        cell = ws_dash.cell(row=8, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center" if col_idx == 1 or col_idx == 9 else ("left" if col_idx == 2 else "right"))
    ws_dash.row_dimensions[8].height = 24
    
    # WBS Table Rows
    start_row = 9
    for i, row in enumerate(wbs_metrics):
        r = start_row + i
        wbs_code, name, bac, ac, ev, cpi, pct, eac = row
        
        ws_dash.cell(row=r, column=1, value=wbs_code).alignment = Alignment(horizontal="center")
        ws_dash.cell(row=r, column=2, value=name).alignment = Alignment(horizontal="left")
        
        ws_dash.cell(row=r, column=3, value=bac).number_format = "$#,##0.00"
        ws_dash.cell(row=r, column=4, value=ac).number_format = "$#,##0.00"
        ws_dash.cell(row=r, column=5, value=ev).number_format = "$#,##0.00"
        
        # Use Excel Formulas for indices to make it interactive!
        cpi_cell = ws_dash.cell(row=r, column=6, value=f"=E{r}/D{r}")
        cpi_cell.number_format = "0.00"
        cpi_cell.alignment = Alignment(horizontal="right")
        
        ws_dash.cell(row=r, column=7, value=pct).number_format = "0.0%"
        
        eac_cell = ws_dash.cell(row=r, column=8, value=f"=C{r}/F{r}")
        eac_cell.number_format = "$#,##0.00"
        
        status_cell = ws_dash.cell(row=r, column=9, value=f'=IF(F{r}<0.95, "OVER BUDGET", "ON TRACK")')
        status_cell.alignment = Alignment(horizontal="center")
        
        # Formatting rows
        for c in range(1, 10):
            cell = ws_dash.cell(row=r, column=c)
            cell.font = regular_font
            cell.border = thin_bottom
            if cpi < 0.95 and c in [6, 9]:
                cell.fill = alert_fill
                
    # Total Row
    tot_row = start_row + len(wbs_metrics)
    ws_dash.cell(row=tot_row, column=1, value="TOTAL").alignment = Alignment(horizontal="center")
    ws_dash.cell(row=tot_row, column=2, value="Project Vessel Summary")
    ws_dash.cell(row=tot_row, column=3, value=f"=SUM(C9:C{tot_row-1})").number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row, column=4, value=f"=SUM(D9:D{tot_row-1})").number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row, column=5, value=f"=SUM(E9:E{tot_row-1})").number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row, column=6, value=f"=E{tot_row}/D{tot_row}").number_format = "0.00"
    ws_dash.cell(row=tot_row, column=7, value=f"=E{tot_row}/C{tot_row}").number_format = "0.0%"
    ws_dash.cell(row=tot_row, column=8, value=f"=SUM(H9:H{tot_row-1})").number_format = "$#,##0.00"
    
    for c in range(1, 10):
        cell = ws_dash.cell(row=tot_row, column=c)
        cell.font = bold_font
        cell.border = double_bottom
        cell.fill = accent_fill

    # ----------------------------------------------------
    # TAB 2: Gantt & Critical Path (Chris Croft Method)
    # ----------------------------------------------------
    ws_gantt = wb.create_sheet(title="Gantt & Critical Path")
    ws_gantt.views.sheetView[0].showGridLines = True
    
    ws_gantt["A1"] = "VESSEL CONSTRUCTION SCHEDULE & CRITICAL PATH"
    ws_gantt["A1"].font = title_font
    ws_gantt["A2"] = "Chris Croft Method: Duration, Predecessors, Float & Critical Path Identification"
    ws_gantt["A2"].font = muted_font
    
    # Gantt Headers
    gantt_headers = [
        "WBS", "Task Description", "Start Date", "End Date", 
        "Duration (Days)", "Predecessors", "Total Float", "Critical?", 
        "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026", "Jun 2026"
    ]
    
    for col_idx, header in enumerate(gantt_headers, start=1):
        cell = ws_gantt.cell(row=5, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
    ws_gantt.row_dimensions[5].height = 24
    
    # Project schedule data (Chris Croft style metrics)
    tasks = [
        ("1.0", "Project Management & Eng.", "2026-01-01", "2026-06-30", 181, "None", 0, "Yes", [1, 1, 1, 1, 1, 1]),
        ("2.0", "Hull Fabrication & Assembly", "2026-02-01", "2026-04-15", 74, "1.0 (Design)", 0, "Yes", [0, 1, 1, 1, 0, 0]),
        ("3.0", "Outfitting & Integration", "2026-04-01", "2026-05-31", 61, "2.0", 0, "Yes", [0, 0, 0, 1, 1, 0]),
        ("4.0", "Sea Trials & Handover", "2026-06-01", "2026-06-30", 30, "3.0", 0, "Yes", [0, 0, 0, 0, 0, 1]),
    ]
    
    critical_fill = PatternFill(start_color="F5B7B1", end_color="F5B7B1", fill_type="solid") # soft red
    pm_fill = PatternFill(start_color="D6DBDF", end_color="D6DBDF", fill_type="solid") # soft gray
    
    for i, task in enumerate(tasks):
        r = 6 + i
        wbs_code, name, start, end, duration, pred, float_val, is_crit, months = task
        
        ws_gantt.cell(row=r, column=1, value=wbs_code).alignment = Alignment(horizontal="center")
        ws_gantt.cell(row=r, column=2, value=name).alignment = Alignment(horizontal="left")
        ws_gantt.cell(row=r, column=3, value=start).alignment = Alignment(horizontal="center")
        ws_gantt.cell(row=r, column=4, value=end).alignment = Alignment(horizontal="center")
        ws_gantt.cell(row=r, column=5, value=duration).alignment = Alignment(horizontal="right")
        ws_gantt.cell(row=r, column=6, value=pred).alignment = Alignment(horizontal="center")
        ws_gantt.cell(row=r, column=7, value=float_val).alignment = Alignment(horizontal="right")
        
        crit_cell = ws_gantt.cell(row=r, column=8, value=is_crit)
        crit_cell.alignment = Alignment(horizontal="center")
        if is_crit == "Yes":
            crit_cell.font = Font(name="Segoe UI", bold=True, color="C0392B")
            
        # Draw Gantt bars using background fills
        for m_idx, active in enumerate(months):
            col = 9 + m_idx
            bar_cell = ws_gantt.cell(row=r, column=col, value="" if not active else "■")
            bar_cell.alignment = Alignment(horizontal="center")
            if active:
                if wbs_code == "1.0":
                    bar_cell.fill = pm_fill
                    bar_cell.font = Font(color="7F8C8D")
                else:
                    bar_cell.fill = critical_fill
                    bar_cell.font = Font(color="C0392B")
                    
        # Apply standard row styling
        for c in range(1, 15):
            cell = ws_gantt.cell(row=r, column=c)
            if c <= 8:
                cell.font = bold_font if c == 8 else regular_font
                cell.border = thin_bottom
            else:
                # Gantt cells borders
                cell.border = Border(left=Side(style='thin', color='E5E7E9'), right=Side(style='thin', color='E5E7E9'), bottom=Side(style='thin', color='E5E7E9'))

    # Auto-adjust column widths
    for ws in [ws_dash, ws_gantt]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if val_str.startswith('='): # Don't size based on formulas
                    val_str = "100,000.00"
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 10)
            
    # Save Workbook
    wb.save(REPORT_PATH)
    print(f"Excel report successfully generated and saved to: {REPORT_PATH}")

if __name__ == "__main__":
    create_excel_report()
