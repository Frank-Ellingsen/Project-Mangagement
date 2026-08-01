import os
import sqlite3

import duckdb
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUCKDB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")
SQLITE_PATH = os.path.join(BASE_DIR, "Data", "SQLite", "project_controlling.db")
EXCEL_PATH = os.path.join(BASE_DIR, "Reports", "vessel_construction_report.xlsx")
SKILLS_DIR = os.path.join(BASE_DIR, ".agents", "skills")


@st.cache_data(ttl=60)
def load_duckdb_data():
    if not os.path.exists(DUCKDB_PATH):
        return None, None, None, None

    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    try:
        summary = con.execute("SELECT * FROM v_project_evm_summary").df().iloc[0]
        wbs = con.execute(
            "SELECT WBS_Code, ElementName, BAC, AC, EV, CPI, PercentComplete, EAC_Typical FROM v_wbs_evm_metrics ORDER BY WBS_Code"
        ).df()

        timesheets = con.execute(
            """
            SELECT t.WorkDate, t.WBS_ID, w.ElementName, r.ResourceName, r.Role, r.HourlyRate, t.HoursWorked,
                   (t.HoursWorked * r.HourlyRate) as LaborCost
            FROM timesheets t
            JOIN resources r ON t.ResourceID = r.ResourceID
            JOIN wbs_elements w ON t.WBS_ID = w.WBS_ID
            ORDER BY t.WorkDate
            """
        ).df()

        materials = con.execute(
            """
            SELECT m.PurchaseDate, m.WBS_ID, w.ElementName, m.Description as ItemDescription, m.PurchaseID as InvoiceNumber, m.TotalActualCost
            FROM material_costs m
            JOIN wbs_elements w ON m.WBS_ID = w.WBS_ID
            ORDER BY m.PurchaseDate
            """
        ).df()
    finally:
        con.close()

    return summary, wbs, timesheets, materials


@st.cache_data(ttl=60)
def load_progress_history():
    if not os.path.exists(DUCKDB_PATH):
        return None

    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    try:
        progress_history = con.execute(
            """
            WITH wbs_dates AS (
                SELECT DISTINCT RecordDate as DateVal FROM physical_progress
                UNION
                SELECT DISTINCT WorkDate as DateVal FROM timesheets
                UNION
                SELECT DISTINCT PurchaseDate as DateVal FROM material_costs
            ),
            daily_labor AS (
                SELECT t.WorkDate, SUM(t.HoursWorked * r.HourlyRate) as DailyLabor
                FROM timesheets t
                JOIN resources r ON t.ResourceID = r.ResourceID
                GROUP BY t.WorkDate
            ),
            daily_material AS (
                SELECT PurchaseDate, SUM(TotalActualCost) as DailyMat
                FROM material_costs
                GROUP BY PurchaseDate
            ),
            daily_progress AS (
                SELECT p.RecordDate, SUM(w.PlannedCost * p.PercentComplete) as ProgressValue
                FROM physical_progress p
                JOIN wbs_elements w ON p.WBS_ID = w.WBS_ID
                GROUP BY p.RecordDate
            ),
            dates_filled AS (
                SELECT 
                    d.DateVal,
                    COALESCE(l.DailyLabor, 0.0) as Labor,
                    COALESCE(m.DailyMat, 0.0) as Mat,
                    COALESCE(p.ProgressValue, 0.0) as EV_Val
                FROM wbs_dates d
                LEFT JOIN daily_labor l ON d.DateVal = l.WorkDate
                LEFT JOIN daily_material m ON d.DateVal = m.PurchaseDate
                LEFT JOIN daily_progress p ON d.DateVal = p.RecordDate
            )
            SELECT 
                DateVal,
                SUM(Labor + Mat) OVER(ORDER BY DateVal) as AC_Cum,
                EV_Val
            FROM dates_filled
            ORDER BY DateVal
            """
        ).df()
    finally:
        con.close()

    return progress_history


@st.cache_data(ttl=60)
def load_sqlite_data():
    if not os.path.exists(SQLITE_PATH):
        return None, None

    con = sqlite3.connect(SQLITE_PATH)
    try:
        raid = pd.read_sql_query(
            "SELECT RiskID as RAID_ID, Type as Category, Description, Impact, Probability, MitigationStrategy, Owner, Status FROM raid_log ORDER BY RiskID DESC",
            con,
        )
        overtime = pd.read_sql_query(
            """
            SELECT strftime('%Y-%W', t.WorkDate) as WorkWeek, r.ResourceName, r.Role, SUM(CAST(t.HoursWorked AS REAL)) as TotalHours
            FROM timesheets t
            JOIN resources r ON t.ResourceID = r.ResourceID
            GROUP BY WorkWeek, r.ResourceName, r.Role
            HAVING TotalHours > 45
            ORDER BY WorkWeek DESC, TotalHours DESC
            """,
            con,
        )
    finally:
        con.close()

    return raid, overtime


@st.cache_data(ttl=60)
def load_project_data():
    summary, wbs, timesheets, materials = load_duckdb_data()
    raid, overtime = load_sqlite_data()
    progress_history = load_progress_history()

    return {
        "summary": summary,
        "wbs": wbs,
        "materials": materials,
        "timesheets": timesheets,
        "progress_history": progress_history,
        "raid": raid,
        "overtime": overtime,
    }


def _format_currency(value, decimals=0):
    if pd.isna(value):
        return ""
    return f"{value:,.{decimals}f}"


@st.cache_data(ttl=900)
def build_wbs_display_table(wbs_df, currency_decimals=2):
    if wbs_df is None:
        return None

    display = wbs_df.copy()
    display["Status"] = display["CPI"].apply(lambda x: "🟢 Green" if x >= 0.98 else "🟡 Amber" if x >= 0.90 else "🔴 Red")

    display["BAC (USD)"] = display["BAC"].apply(lambda x: _format_currency(x, currency_decimals))
    display["AC (USD)"] = display["AC"].apply(lambda x: _format_currency(x, currency_decimals))
    display["EV (USD)"] = display["EV"].apply(lambda x: _format_currency(x, currency_decimals))
    if "EAC_Typical" in display.columns:
        display["EAC Typical (USD)"] = display["EAC_Typical"].apply(lambda x: _format_currency(x, currency_decimals))
    display["CPI"] = display["CPI"].apply(lambda x: f"{x:.2f}")
    display["Progress %"] = display["PercentComplete"].apply(lambda x: f"{x:.1f}%")

    columns = ["WBS_Code", "ElementName", "BAC (USD)", "AC (USD)", "EV (USD)", "CPI", "Progress %", "Status"]
    if "EAC Typical (USD)" in display.columns:
        columns.insert(5, "EAC Typical (USD)")

    return display[columns]


@st.cache_data(ttl=900)
def build_material_audit_table(material_df, threshold=50000):
    if material_df is None:
        return None

    large_materials = material_df[material_df["TotalActualCost"] > threshold].sort_values(by="TotalActualCost", ascending=False).copy()
    large_materials["Cost (USD)"] = large_materials["TotalActualCost"].apply(lambda x: _format_currency(x, 2))
    return large_materials[["PurchaseDate", "InvoiceNumber", "ItemDescription", "Cost (USD)"]]


@st.cache_data(ttl=900)
def prepare_progress_history_for_chart(progress_history):
    if progress_history is None:
        return None

    history = progress_history.copy()
    history["DateVal"] = pd.to_datetime(history["DateVal"])
    return history.sort_values("DateVal")


@st.cache_data(ttl=900)
def load_file_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()


@st.cache_data(ttl=900)
def load_markdown_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    return content


@st.cache_data(ttl=900)
def load_skill_markdown(relative_skill_path):
    full_skill_path = os.path.join(BASE_DIR, relative_skill_path.replace("/", os.sep))
    if not os.path.exists(full_skill_path):
        return None
    return load_markdown_text(full_skill_path)
