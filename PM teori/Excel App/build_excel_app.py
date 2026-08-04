import csv
import os
from datetime import date, datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# Define directories
BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "CSV"
OUTPUT_PATH = BASE_DIR / "Project_Controlling_App.xlsx"


def _coerce_value(value: str):
    if value is None:
        return None

    text = value.strip()
    if not text:
        return None

    try:
        if len(text) == 10 and text[4] == "-" and text[7] == "-":
            return datetime.strptime(text, "%Y-%m-%d").date()
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def build_workbook():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    font_family = "Segoe UI"
    title_font = Font(name=font_family, size=16, bold=True, color="2C3E50")
    subtitle_font = Font(name=font_family, size=10, italic=True, color="7F8C8D")
    section_font = Font(name=font_family, size=12, bold=True, color="2C3E50")
    header_font = Font(name=font_family, size=10, bold=True, color="333333")
    data_font = Font(name=font_family, size=10, color="000000")
    bold_data_font = Font(name=font_family, size=10, bold=True, color="000000")

    header_fill = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")
    total_fill = PatternFill(start_color="FBFCFC", end_color="FBFCFC", fill_type="solid")

    thin_gray = Side(style="thin", color="E5E7E9")
    medium_dark = Side(style="thin", color="BDC3C7")
    double_dark = Side(style="double", color="2C3E50")

    border_header = Border(bottom=medium_dark, top=thin_gray)
    border_data = Border(bottom=thin_gray)
    border_total = Border(top=medium_dark, bottom=double_dark)

    csv_files = [
        ("Dim_Project.csv", "Dim_Project"),
        ("Dim_WBS.csv", "Dim_WBS"),
        ("Dim_Resource.csv", "Dim_Resource"),
        ("Dim_Calendar.csv", "Dim_Calendar"),
        ("Fact_Baseline_PV.csv", "Fact_Baseline_PV"),
        ("Fact_Actual_Costs.csv", "Fact_Actual_Costs"),
        ("Fact_Physical_Progress.csv", "Fact_Physical_Progress"),
    ]

    for filename, sheetname in csv_files:
        filepath = CSV_DIR / filename
        ws = wb.create_sheet(title=sheetname)
        ws.views.sheetView[0].showGridLines = True

        with open(filepath, "r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            for row_idx, row in enumerate(reader, start=1):
                for col_idx, value in enumerate(row, start=1):
                    typed_val = _coerce_value(value)
                    cell = ws.cell(row=row_idx, column=col_idx, value=typed_val)
                    cell.font = data_font

                    if isinstance(typed_val, (date, datetime)):
                        cell.number_format = "yyyy-mm-dd"

                    if row_idx == 1:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.border = border_header

        for column in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in column)
            col_letter = get_column_letter(column[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 10)

    ws_dash = wb.create_sheet(title="EVM Dashboard")
    ws_dash.views.sheetView[0].showGridLines = False
    ws_dash.freeze_panes = "A17"

    ws_dash["A1"] = "OFFICE FIT-OUT - PROJECT CONTROLLING DASHBOARD"
    ws_dash["A1"].font = title_font
    ws_dash["A2"] = "EVM Performance Status | Tufte-Compliant Design | Data-Ink Maximized"
    ws_dash["A2"].font = subtitle_font
    ws_dash.row_dimensions[1].height = 24
    ws_dash.row_dimensions[2].height = 18

    ws_dash["A4"] = "Status Date:"
    ws_dash["A4"].font = bold_data_font
    ws_dash["B4"] = datetime.strptime("2026-06-12", "%Y-%m-%d").date()
    ws_dash["B4"].font = data_font
    ws_dash["B4"].number_format = "yyyy-mm-dd"
    ws_dash["B4"].alignment = Alignment(horizontal="left")

    ws_dash["D4"] = "Status Week:"
    ws_dash["D4"].font = bold_data_font
    ws_dash["E4"] = 6
    ws_dash["E4"].font = data_font
    ws_dash["E4"].alignment = Alignment(horizontal="left")

    ws_dash["G4"] = "Sector:"
    ws_dash["G4"].font = bold_data_font
    ws_dash["H4"] = "Corporate Real Estate"
    ws_dash["H4"].font = data_font

    ws_dash["A6"] = "Executive Metrics Summary"
    ws_dash["A6"].font = section_font

    kpis = [
        ("Budget at Completion (BAC)", "=D30", "#,##0.00\" NOK\"", "A", 7),
        ("Planned Value (PV)", "=E30", "#,##0.00\" NOK\"", "D", 7),
        ("Actual Cost (AC)", "=F30", "#,##0.00\" NOK\"", "G", 7),
        ("Earned Value (EV)", "=H30", "#,##0.00\" NOK\"", "J", 7),
        ("Cost Variance (CV)", "=I30", "#,##0.00\" NOK\"", "A", 10),
        ("Schedule Variance (SV)", "=J30", "#,##0.00\" NOK\"", "D", 10),
        ("CPI (Cost Index)", "=K30", "0.00", "G", 10),
        ("SPI (Schedule Index)", "=L30", "0.00", "J", 10),
        ("Estimate at Completion (EAC)", "=M30", "#,##0.00\" NOK\"", "A", 13),
        ("Estimate to Complete (ETC)", "=N30", "#,##0.00\" NOK\"", "D", 13),
        ("Variance at Completion (VAC)", "=O30", "#,##0.00\" NOK\"", "G", 13),
        ("Project Progress %", "=G30", "0.0%", "J", 13),
    ]

    for label, formula, num_format, col, row_idx in kpis:
        next_col = chr(ord(col) + 2)
        lbl_cell = ws_dash[f"{col}{row_idx - 1}"]
        lbl_cell.value = label.upper()
        lbl_cell.font = Font(name=font_family, size=9, bold=True, color="7F8C8D")

        val_cell = ws_dash[f"{col}{row_idx}"]
        val_cell.value = formula
        val_cell.font = Font(name=font_family, size=12, bold=True, color="2C3E50")
        val_cell.number_format = num_format
        val_cell.alignment = Alignment(horizontal="left", vertical="center")
        val_cell.border = Border(bottom=thin_gray)
        val_cell.fill = total_fill
        ws_dash.merge_cells(f"{col}{row_idx}:{next_col}{row_idx}")

    ws_dash.row_dimensions[7].height = 24
    ws_dash.row_dimensions[10].height = 24
    ws_dash.row_dimensions[13].height = 24

    ws_dash["A15"] = "WBS Element Performance Breakdown"
    ws_dash["A15"].font = section_font

    headers = [
        "WBS ID",
        "Activity Name",
        "Type",
        "Budget (BAC)",
        "Planned Value (PV)",
        "Actual Cost (AC)",
        "Progress %",
        "Earned Value (EV)",
        "CV",
        "SV",
        "CPI",
        "SPI",
        "EAC",
        "ETC",
        "VAC",
        "Status",
    ]

    for idx, header in enumerate(headers, start=1):
        cell = ws_dash.cell(row=17, column=idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border_header
        cell.alignment = Alignment(horizontal="left" if idx in [1, 2, 3] else ("center" if idx == 16 else "right"))

    wbs_activities = [
        ("WBS-01", "Project Management", "Labor"),
        ("WBS-02", "Site Survey & Mobilization", "Labor"),
        ("WBS-03", "Design & Engineering", "Labor"),
        ("WBS-04", "Procurement - Materials", "Material"),
        ("WBS-05", "Demolition & Prep", "Labor"),
        ("WBS-06", "Electrical Rough-In", "Labor"),
        ("WBS-07", "HVAC Installation", "Subcontractor"),
        ("WBS-08", "Partitions & Drywall", "Subcontractor"),
        ("WBS-09", "Flooring", "Material"),
        ("WBS-10", "Fixtures & Furniture", "Material"),
        ("WBS-11", "Testing / Commissioning", "Labor"),
        ("WBS-12", "Handover & Closeout", "Labor"),
    ]

    for row_idx, (wbs_id, name, w_type) in enumerate(wbs_activities, start=18):
        ws_dash.cell(row=row_idx, column=1, value=wbs_id).alignment = Alignment(horizontal="left")
        ws_dash.cell(row=row_idx, column=2, value=name).alignment = Alignment(horizontal="left")
        ws_dash.cell(row=row_idx, column=3, value=w_type).alignment = Alignment(horizontal="left")

        ws_dash.cell(row=row_idx, column=4, value=f"=VLOOKUP(A{row_idx}, Dim_WBS!$A:$E, 5, FALSE)").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=5, value=f"=SUMIFS(Fact_Baseline_PV!$C:$C, Fact_Baseline_PV!$B:$B, A{row_idx}, Fact_Baseline_PV!$A:$A, "<="&$B$4)").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=6, value=f"=SUMIFS(Fact_Actual_Costs!$D:$D, Fact_Actual_Costs!$B:$B, A{row_idx})").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=7, value=f"=IFERROR(MAXIFS(Fact_Physical_Progress!$C:$C, Fact_Physical_Progress!$B:$B, A{row_idx}, Fact_Physical_Progress!$A:$A, "<="&$B$4), 0)").number_format = "0.0%"
        ws_dash.cell(row=row_idx, column=8, value=f"=D{row_idx}*G{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=9, value=f"=H{row_idx}-F{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=10, value=f"=H{row_idx}-E{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=11, value=f"=IF(F{row_idx}>0, H{row_idx}/F{row_idx}, 1.00)").number_format = "0.00"
        ws_dash.cell(row=row_idx, column=12, value=f"=IF(E{row_idx}>0, H{row_idx}/E{row_idx}, 1.00)").number_format = "0.00"
        ws_dash.cell(row=row_idx, column=13, value=f"=IF(K{row_idx}>0, D{row_idx}/K{row_idx}, D{row_idx})").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=14, value=f"=M{row_idx}-F{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=15, value=f"=D{row_idx}-M{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=16, value=f"=IF(K{row_idx}<0.95, \"Overrun\", IF(K{row_idx}<1.0, \"Warning\", \"On Track\"))").alignment = Alignment(horizontal="center")

        for col_idx in range(1, 17):
            cell = ws_dash.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_data
            if col_idx not in [1, 2, 3, 16]:
                cell.alignment = Alignment(horizontal="right")

    tot_row = 30
    ws_dash.cell(row=tot_row, column=1, value="Total / Project Portfolio").font = bold_data_font
    ws_dash.cell(row=tot_row, column=1).alignment = Alignment(horizontal="left")
    ws_dash.cell(row=tot_row, column=4, value="=SUM(D18:D29)").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=5, value="=SUM(E18:E29)").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=6, value="=SUM(F18:F29)").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=7, value="=H30/D30").number_format = "0.0%"
    ws_dash.cell(row=tot_row, column=8, value="=SUM(H18:H29)").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=9, value="=H30-F30").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=10, value="=H30-E30").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=11, value="=IF(F30>0, H30/F30, 1.00)").number_format = "0.00"
    ws_dash.cell(row=tot_row, column=12, value="=IF(E30>0, H30/E30, 1.00)").number_format = "0.00"
    ws_dash.cell(row=tot_row, column=13, value="=IF(K30>0, D30/K30, D30)").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=14, value="=M30-F30").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=15, value="=D30-M30").number_format = "#,##0.00"
    ws_dash.cell(row=tot_row, column=16, value="=IF(K30<0.95, \"Overrun\", IF(K30<1.0, \"Warning\", \"On Track\"))").alignment = Alignment(horizontal="center")

    for col_idx in range(1, 17):
        cell = ws_dash.cell(row=tot_row, column=col_idx)
        cell.font = bold_data_font
        cell.fill = total_fill
        cell.border = border_total
        if col_idx not in [1, 2, 3, 16]:
            cell.alignment = Alignment(horizontal="right")

    ws_dash["A33"] = "Weekly Cumulative Performance Trends"
    ws_dash["A33"].font = section_font

    trend_headers = [
        "Week",
        "Week Date",
        "Weekly PV",
        "Cum PV",
        "Weekly AC",
        "Cum AC",
        "Cum EV",
        "CV",
        "SV",
        "CPI",
        "SPI",
    ]

    for idx, header in enumerate(trend_headers, start=1):
        cell = ws_dash.cell(row=35, column=idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border_header
        cell.alignment = Alignment(horizontal="left" if idx == 2 else "right")

    weeks_dates = [
        (1, "2026-05-04"),
        (2, "2026-05-11"),
        (3, "2026-05-18"),
        (4, "2026-05-25"),
        (5, "2026-06-01"),
        (6, "2026-06-08"),
        (7, "2026-06-15"),
        (8, "2026-06-22"),
        (9, "2026-06-29"),
        (10, "2026-07-06"),
        (11, "2026-07-13"),
        (12, "2026-07-20"),
    ]

    for row_idx, (week_num, date_str) in enumerate(weeks_dates, start=36):
        ws_dash.cell(row=row_idx, column=1, value=week_num).alignment = Alignment(horizontal="right")
        date_cell = ws_dash.cell(row=row_idx, column=2, value=datetime.strptime(date_str, "%Y-%m-%d").date())
        date_cell.alignment = Alignment(horizontal="left")
        date_cell.number_format = "yyyy-mm-dd"

        ws_dash.cell(row=row_idx, column=3, value=f"=SUMIFS(Fact_Baseline_PV!$C:$C, Fact_Baseline_PV!$A:$A, B{row_idx})").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=4, value=f"=SUM(C$36:C{row_idx})").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=5, value=f"=SUMIFS(Fact_Actual_Costs!$D:$D, Fact_Actual_Costs!$A:$A, ">="&B{row_idx}, Fact_Actual_Costs!$A:$A, "<="&B{row_idx}+6)").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=6, value=f"=SUM(E$36:E{row_idx})").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=7, value=f"=SUMPRODUCT(Dim_WBS!$E$2:$E$13, SUMIFS(Fact_Physical_Progress!$C$2:$C$100, Fact_Physical_Progress!$B$2:$B$100, Dim_WBS!$A$2:$A$13, Fact_Physical_Progress!$A$2:$A$100, "<="&B{row_idx}+4))").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=8, value=f"=G{row_idx}-F{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=9, value=f"=G{row_idx}-D{row_idx}").number_format = "#,##0.00"
        ws_dash.cell(row=row_idx, column=10, value=f"=IF(F{row_idx}>0, G{row_idx}/F{row_idx}, 1.00)").number_format = "0.00"
        ws_dash.cell(row=row_idx, column=11, value=f"=IF(D{row_idx}>0, G{row_idx}/D{row_idx}, 1.00)").number_format = "0.00"

        for col_idx in range(1, 12):
            cell = ws_dash.cell(row=row_idx, column=col_idx)
            cell.font = data_font
            cell.border = border_data

    ws_dash["A50"] = "Workbook Notes"
    ws_dash["A50"].font = section_font
    ws_dash["A51"] = "This workbook links the CSV star schema tables to the dashboard via Excel formulas."
    ws_dash["A51"].font = Font(name=font_family, size=9, italic=True, color="555555")

    for column_letter, width in {
        "A": 12,
        "B": 28,
        "C": 15,
        "D": 16,
        "E": 20,
        "F": 16,
        "G": 14,
        "H": 18,
        "I": 14,
        "J": 14,
        "K": 10,
        "L": 10,
        "M": 16,
        "N": 16,
        "O": 16,
        "P": 14,
    }.items():
        ws_dash.column_dimensions[column_letter].width = width

    wb.properties.creator = "Project Controlling Workspace"
    wb.properties.title = "Project Controlling App"
    wb.properties.subject = "Earned Value Management Dashboard"

    wb.save(OUTPUT_PATH)
    print(f"Workbook successfully saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_workbook()
