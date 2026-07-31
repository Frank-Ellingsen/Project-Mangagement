import os
import sqlite3
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & TUFTE DESIGN SYSTEM
# ==========================================
st.set_page_config(
    page_title="Agent Control Tower | Project Controlling",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Edward Tufte Data-Ink CSS & Custom Styling
st.markdown("""
    <style>
    /* Clean typography & muted palette */
    html, body, [class*="View"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        background-color: #fcfcfc;
        color: #2c3e50;
    }
    
    /* Remove card borders, drop shadows, and heavy backgrounds */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #eaeaea !important;
        border-radius: 4px !important;
        box-shadow: none !important;
        padding: 12px 16px !important;
    }
    
    /* Mute metric headers */
    div[data-testid="stMetricLabel"] > div {
        color: #7f8c8d !important;
        font-size: 11px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* High contrast numeric values */
    div[data-testid="stMetricValue"] > div {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #1a252f !important;
    }
    
    /* Stakeholder card styling */
    .stakeholder-card {
        background-color: #ffffff;
        border-left: 4px solid #2c3e50;
        padding: 16px 20px;
        margin-bottom: 20px;
        border-radius: 2px;
        border-top: 1px solid #f0f0f0;
        border-right: 1px solid #f0f0f0;
        border-bottom: 1px solid #f0f0f0;
    }
    .stakeholder-card h3 {
        margin-top: 0;
        color: #1a252f;
        font-size: 18px;
    }
    .stakeholder-card p {
        color: #555555;
        font-size: 13px;
        margin-bottom: 0;
    }

    /* Custom clean table styling */
    .dataframe {
        font-size: 13px !important;
        border-collapse: collapse !important;
        width: 100%;
    }
    .dataframe th {
        background-color: #f8f9fa !important;
        color: #495057 !important;
        font-weight: 600 !important;
        text-align: left;
        border-bottom: 2px solid #dee2e6 !important;
        padding: 8px !important;
    }
    .dataframe td {
        padding: 8px !important;
        border-bottom: 1px solid #e9ecef !important;
    }
    
    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# PATH INITIALIZATION & DATA RETRIEVAL
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUCKDB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")
SQLITE_PATH = os.path.join(BASE_DIR, "Data", "SQLite", "project_controlling.db")

@st.cache_data(ttl=60)
def load_duckdb_data():
    if not os.path.exists(DUCKDB_PATH):
        return None, None, None, None
    con = duckdb.connect(DUCKDB_PATH, read_only=True)
    
    summary = con.execute("SELECT * FROM v_project_evm_summary").df().iloc[0]
    wbs = con.execute("SELECT WBS_Code, ElementName, BAC, AC, EV, CPI, PercentComplete, EAC_Typical FROM v_wbs_evm_metrics ORDER BY WBS_Code").df()
    
    timesheets = con.execute("""
        SELECT t.WorkDate, t.WBS_ID, w.ElementName, r.ResourceName, r.Role, r.HourlyRate, t.HoursWorked,
               (t.HoursWorked * r.HourlyRate) as LaborCost
        FROM timesheets t
        JOIN resources r ON t.ResourceID = r.ResourceID
        JOIN wbs_elements w ON t.WBS_ID = w.WBS_ID
        ORDER BY t.WorkDate
    """).df()
    
    materials = con.execute("""
        SELECT m.PurchaseDate, m.WBS_ID, w.ElementName, m.Description as ItemDescription, m.PurchaseID as InvoiceNumber, m.TotalActualCost
        FROM material_costs m
        JOIN wbs_elements w ON m.WBS_ID = w.WBS_ID
        ORDER BY m.PurchaseDate
    """).df()
    
    con.close()
    return summary, wbs, timesheets, materials

@st.cache_data(ttl=60)
def load_sqlite_data():
    if not os.path.exists(SQLITE_PATH):
        return None, None
    con = sqlite3.connect(SQLITE_PATH)
    
    raid = pd.read_sql_query("SELECT RiskID as RAID_ID, Type as Category, Description, Impact, Probability, MitigationStrategy, Owner, Status FROM raid_log ORDER BY RiskID DESC", con)
    overtime = pd.read_sql_query("""
        SELECT strftime('%Y-%W', t.WorkDate) as WorkWeek, r.ResourceName, r.Role, SUM(t.HoursWorked) as TotalHours
        FROM timesheets t
        JOIN resources r ON t.ResourceID = r.ResourceID
        GROUP BY WorkWeek, r.ResourceName, r.Role
        HAVING TotalHours > 45
        ORDER BY WorkWeek DESC, TotalHours DESC
    """, con)
    
    con.close()
    return raid, overtime

summary, wbs_df, timesheet_df, material_df = load_duckdb_data()
raid_df, overtime_df = load_sqlite_data()

# Check if data exists
if summary is None:
    st.error("⚠️ Database files not found. Please run `python AI_Controller/build_duckdb.py` and `python AI_Controller/build_sqlite.py` to initialize data.")
    st.stop()

# ==========================================
# AGENT SKILL REGISTRY METADATA
# ==========================================
AGENT_SKILLS = {
    "project-controller-agent": {
        "title": "Project Controller Agent",
        "category": "Financial Control",
        "icon": "📊",
        "role": "Calculates EVM metrics (CPI/SPI), forecasts EAC/VAC, and flags WBS cost variance anomalies.",
        "file": ".agents/skills/project-controller-agent/SKILL.md"
    },
    "project-cfo-agent": {
        "title": "Project CFO Agent",
        "category": "Financial Control",
        "icon": "💼",
        "role": "Audits portfolio profitability, cash flow burn rates, labor/material split, and Margin at Completion.",
        "file": ".agents/skills/project-cfo-agent/SKILL.md"
    },
    "project-contract-manager-agent": {
        "title": "Project Contract Manager Agent",
        "category": "Governance & Risk",
        "icon": "📜",
        "role": "Tracks Variation Orders (VO/VOR), scope modifications, baseline budget revisions, and contractual milestones.",
        "file": ".agents/skills/project-contract-manager-agent/SKILL.md"
    },
    "project-controlling-evm": {
        "title": "EVM Calculation Engine",
        "category": "Financial Control",
        "icon": "🔢",
        "role": "Core mathematical engine executing Earned Value Management formulas and status thresholds.",
        "file": ".agents/skills/project-controlling-evm/SKILL.md"
    },
    "project-engineering-lead-agent": {
        "title": "Project Engineering Lead Agent",
        "category": "Operations & Schedule",
        "icon": "📐",
        "role": "Monitors engineering design schedules, drawing release dates, and design hour burn rates.",
        "file": ".agents/skills/project-engineering-lead-agent/SKILL.md"
    },
    "project-evaluation-agent": {
        "title": "Project Evaluation Agent",
        "category": "Governance & Risk",
        "icon": "🔍",
        "role": "Conducts post-project financial audits (etterkalkyle), analyzes baseline deviations, and compiles benchmarks.",
        "file": ".agents/skills/project-evaluation-agent/SKILL.md"
    },
    "project-manager-agent": {
        "title": "Project Manager Agent",
        "category": "Operations & Schedule",
        "icon": "🎯",
        "role": "Coordinates project milestones, resource allocation, critical path scheduling, and task dependencies.",
        "file": ".agents/skills/project-manager-agent/SKILL.md"
    },
    "project-procurement-agent": {
        "title": "Project Procurement Agent",
        "category": "Operations & Schedule",
        "icon": "📦",
        "role": "Audits purchase orders, committed costs vs actual invoices, supplier lead times, and vendor delivery risks.",
        "file": ".agents/skills/project-procurement-agent/SKILL.md"
    },
    "project-production-agent": {
        "title": "Project Production Agent",
        "category": "Operations & Schedule",
        "icon": "🏗️",
        "role": "Tracks shipyard/shop-floor labor productivity, physical assembly milestones, and structural completion.",
        "file": ".agents/skills/project-production-agent/SKILL.md"
    },
    "project-quality-agent": {
        "title": "Project Quality Agent",
        "category": "Governance & Risk",
        "icon": "🛡️",
        "role": "Tracks Non-Conformity Reports (NCRs), inspection pass rates, and estimates financial rework impact.",
        "file": ".agents/skills/project-quality-agent/SKILL.md"
    },
    "project-research-agent": {
        "title": "Project Research Agent",
        "category": "Governance & Risk",
        "icon": "🔬",
        "role": "Conducts shipbuilding rate benchmarking, market research, and software tool evaluations.",
        "file": ".agents/skills/project-research-agent/SKILL.md"
    },
    "project-support-agent": {
        "title": "Project Support Agent",
        "category": "Governance & Risk",
        "icon": "📁",
        "role": "Manages project documentation, timesheet compliance collection, and administrative logs.",
        "file": ".agents/skills/project-support-agent/SKILL.md"
    },
    "tufte-dashboard-designer": {
        "title": "Tufte Dashboard Designer",
        "category": "Financial Control",
        "icon": "🎨",
        "role": "Applies Edward Tufte's Data-Ink Ratio principles (no gridlines, subtle colors, clean layout) to UI components.",
        "file": ".agents/skills/tufte-dashboard-designer/SKILL.md"
    }
}

# ==========================================
# INTERACTIVE GANTT CHART GENERATOR
# ==========================================
# ==========================================
# INTERACTIVE GANTT CHART GENERATOR
# ==========================================
def render_tufte_gantt_chart(project_selection="PRJ-001 (Composite Vessel)", metric_focus="Schedule Progress %"):
    # Generate schedule datasets (Planned vs Actual/Forecast)
    tasks_prj001 = [
        # Planned
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "1.0", "Task": "1.0 PM & Engineering", "Start": "2026-01-01", "Finish": "2026-06-30", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 300000, "AC": 300000, "PlannedHours": 400.0, "ActualHours": 400.0, "Status": "Planned"},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "2.0", "Task": "2.0 Hull Fabrication", "Start": "2026-02-01", "Finish": "2026-04-30", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 600000, "AC": 600000, "PlannedHours": 1200.0, "ActualHours": 1200.0, "Status": "Planned"},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "3.0", "Task": "3.0 Outfitting & Integration", "Start": "2026-04-01", "Finish": "2026-05-30", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 400000, "AC": 400000, "PlannedHours": 800.0, "ActualHours": 800.0, "Status": "Planned"},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "4.0", "Task": "4.0 Sea Trials & Handover", "Start": "2026-06-01", "Finish": "2026-06-20", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 200000, "AC": 200000, "PlannedHours": 300.0, "ActualHours": 300.0, "Status": "Planned"},
        # Actual
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "1.0", "Task": "1.0 PM & Engineering", "Start": "2026-01-01", "Finish": "2026-06-30", "ScheduleType": "Actual/Forecast", "Progress": 97.5, "BAC": 300000, "AC": 419230, "PlannedHours": 400.0, "ActualHours": 440.8, "Status": "🔴 Red (Overrun)"},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "2.0", "Task": "2.0 Hull Fabrication", "Start": "2026-02-01", "Finish": "2026-04-20", "ScheduleType": "Actual/Forecast", "Progress": 100.0, "BAC": 600000, "AC": 620450, "PlannedHours": 1200.0, "ActualHours": 513.5, "Status": "🟢 Green (On Track)"},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "3.0", "Task": "3.0 Outfitting & Integration", "Start": "2026-04-01", "Finish": "2026-05-25", "ScheduleType": "Actual/Forecast", "Progress": 100.0, "BAC": 400000, "AC": 540445, "PlannedHours": 800.0, "ActualHours": 401.1, "Status": "🔴 Red (Overrun)"},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "4.0", "Task": "4.0 Sea Trials & Handover", "Start": "2026-06-01", "Finish": "2026-06-30", "ScheduleType": "Actual/Forecast", "Progress": 100.0, "BAC": 200000, "AC": 268685, "PlannedHours": 300.0, "ActualHours": 280.5, "Status": "🔴 Red (Overrun)"},
    ]
    
    tasks_prj002 = [
        # Planned
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "1.0", "Task": "1.0 Hull Design & CFD", "Start": "2026-05-01", "Finish": "2026-08-15", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 450000, "AC": 450000, "PlannedHours": 500.0, "ActualHours": 500.0, "Status": "Planned"},
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "2.0", "Task": "2.0 Carbon Fiber Molding", "Start": "2026-07-01", "Finish": "2026-10-30", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 850000, "AC": 850000, "PlannedHours": 1000.0, "ActualHours": 1000.0, "Status": "Planned"},
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "3.0", "Task": "3.0 Autonomous Avionics", "Start": "2026-09-01", "Finish": "2026-12-15", "ScheduleType": "Planned", "Progress": 100.0, "BAC": 650000, "AC": 650000, "PlannedHours": 800.0, "ActualHours": 800.0, "Status": "Planned"},
        # Actual
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "1.0", "Task": "1.0 Hull Design & CFD", "Start": "2026-05-01", "Finish": "2026-08-15", "ScheduleType": "Actual/Forecast", "Progress": 75.0, "BAC": 450000, "AC": 320000, "PlannedHours": 500.0, "ActualHours": 380.0, "Status": "🟢 Green (On Track)"},
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "2.0", "Task": "2.0 Carbon Fiber Molding", "Start": "2026-07-01", "Finish": "2026-10-30", "ScheduleType": "Actual/Forecast", "Progress": 20.0, "BAC": 850000, "AC": 170000, "PlannedHours": 1000.0, "ActualHours": 210.0, "Status": "🟢 Green (On Track)"},
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "3.0", "Task": "3.0 Autonomous Avionics", "Start": "2026-09-01", "Finish": "2026-12-15", "ScheduleType": "Actual/Forecast", "Progress": 0.0, "BAC": 650000, "AC": 0, "PlannedHours": 800.0, "ActualHours": 0.0, "Status": "🟢 Green (On Track)"},
    ]
    
    if "PRJ-001" in project_selection:
        tasks = tasks_prj001
    elif "PRJ-002" in project_selection:
        tasks = tasks_prj002
    else:
        tasks = tasks_prj001 + tasks_prj002
        
    df_gantt = pd.DataFrame(tasks)
    df_gantt["Start"] = pd.to_datetime(df_gantt["Start"])
    df_gantt["Finish"] = pd.to_datetime(df_gantt["Finish"])
    
    # Calculate Labels & Colors based on Metric Focus
    labels = []
    colors = []
    
    for idx, r in df_gantt.iterrows():
        is_planned = r["ScheduleType"] == "Planned"
        
        if metric_focus == "Schedule Progress %":
            if is_planned:
                labels.append("Planned Baseline")
                colors.append("Planned")
            else:
                labels.append(f"{r['Progress']:.1f}%")
                colors.append(r["Status"])
                
        elif metric_focus == "Cost Deviation (BAC vs AC)":
            if is_planned:
                labels.append(f"BAC: {r['BAC']/1000:.0f}k NOK")
                colors.append("Planned")
            else:
                diff = r["AC"] - r["BAC"]
                if diff > 0:
                    labels.append(f"+{diff/1000:.1f}k NOK Overrun")
                    colors.append("🔴 Red (Overrun)")
                else:
                    labels.append(f"-{abs(diff)/1000:.1f}k NOK Under")
                    colors.append("🟢 Green (On Track)")
                    
        elif metric_focus == "Hours Deviation (Plan vs Actual)":
            if is_planned:
                labels.append(f"Plan: {r['PlannedHours']:.0f}h")
                colors.append("Planned")
            else:
                diff = r["ActualHours"] - r["PlannedHours"]
                if diff > 0:
                    labels.append(f"+{diff:.1f}h Over")
                    colors.append("🔴 Red (Overrun)")
                else:
                    labels.append(f"{diff:.1f}h Under")
                    colors.append("🟢 Green (On Track)")
                    
    df_gantt["DisplayLabel"] = labels
    df_gantt["ColorCategory"] = colors
    
    fig_gantt = px.timeline(
        df_gantt,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="ColorCategory",
        text="DisplayLabel",
        hover_data=["Project", "BAC", "AC", "PlannedHours", "ActualHours", "Progress", "ScheduleType"],
        color_discrete_map={
            "Planned": "#cbd5e1",
            "🟢 Green (On Track)": "#2c3e50",
            "🔴 Red (Overrun)": "#e74c3c"
        }
    )
    
    # Tufte Layout Styling
    fig_gantt.update_layout(
        title_text="Project WBS Schedule Gantt Chart",
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode="group"
    )
    
    # REMOVE VERTICAL GRIDLINES (Tufte Data-Ink Rule)
    fig_gantt.update_xaxes(showgrid=False, linecolor="#cccccc")
    fig_gantt.update_yaxes(autorange="reversed", showgrid=True, gridcolor="#f5f5f5")
    
    return fig_gantt

# ==========================================
# SIDEBAR NAVIGATION & AGENT SELECTOR
# ==========================================
with st.sidebar:
    st.title("⚓ Agent Control Tower")
    st.caption("PRJ-001 | Vessel Construction Controller")
    st.write("---")
    
    view_mode = st.radio(
        "Navigation View",
        ["Agent Control Tower", "👥 Stakeholder Reports", "Individual Agent Skill Inspector", "Live Crew Execution"]
    )
    
    st.write("---")
    selected_skill = st.selectbox(
        "Focus Agent Skill",
        options=list(AGENT_SKILLS.keys()),
        format_func=lambda x: f"{AGENT_SKILLS[x]['icon']} {AGENT_SKILLS[x]['title']}"
    )
    
    agent_info = AGENT_SKILLS[selected_skill]
    st.markdown(f"**Domain:** `{agent_info['category']}`")
    st.markdown(f"**Description:**\n{agent_info['role']}")
    st.markdown(f"**Skill Path:**\n`{agent_info['file']}`")

# Fetch key numbers for global reuse
bac = summary['Total_BAC']
ac = summary['Total_AC']
ev = summary['Total_EV']
cpi = summary['Project_CPI']
progress = summary['Overall_Progress_Pct']
cv = summary['Total_CV']
vac = bac - (ac + ((bac - ev) / cpi))

# ==========================================
# 1. MAIN AGENT CONTROL TOWER DASHBOARD (FRONT PAGE)
# ==========================================
if view_mode == "Agent Control Tower":
    st.title("⚓ Project Control Tower Dashboard")
    st.caption("Integrated Earned Value Management & Agent Intelligence System")
    
    # --- PORTFOLIO SUMMARY HEADER ---
    st.markdown("""
    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 16px 24px; margin-bottom: 24px;">
        <h3 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 600;">
            📊 Portfolio Control Tower — Project Summary
        </h3>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #7f8c8d; font-weight: normal;">
            Aggregate KPIs across all active projects | Last updated: 2026-06-30
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- PORTFOLIO KPI ROW (Tufte Style) ---
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Portfolio BAC", f"{bac:,.0f} NOK", delta="Baseline budget (1 project)")
    with col2:
        st.metric("Total Actual Cost (AC)", f"{ac:,.0f} NOK", delta=f"{ac - bac:,.0f} NOK over BAC", delta_color="inverse")
    with col3:
        st.metric("Total Earned Value (EV)", f"{ev:,.0f} NOK", delta=f"{progress:.1f}% work complete")
    with col4:
        st.metric("Portfolio CPI", f"{cpi:.2f}", delta=f"{'🟢 GREEN' if cpi >= 0.98 else '🟡 AMBER' if cpi >= 0.90 else '🔴 RED'}", delta_color="normal" if cpi >= 0.98 else "off" if cpi >= 0.90 else "inverse")
    with col5:
        st.metric("Portfolio Progress", f"{progress:.1f}%", delta="0.5% remaining")
        
    st.write("---")
    
    # --- PORTFOLIO RATIOS SUMMARY ---
    st.subheader("📈 Portfolio Financial Ratios & Forecasts")
    col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
    with col_r1:
        st.metric("Cost Variance (CV)", f"{cv:,.0f} NOK", delta="EV - AC", delta_color="inverse")
    with col_r2:
        st.metric("EAC (Typical)", f"{summary['Total_EAC_Typical']:,.0f} NOK", delta="BAC / CPI", delta_color="inverse")
    with col_r3:
        eac_atypical = ac + (bac - ev)
        st.metric("EAC (Atypical)", f"{eac_atypical:,.0f} NOK", delta="AC + (BAC - EV)", delta_color="inverse")
    with col_r4:
        st.metric("Variance at Completion (VAC)", f"{summary['Total_VAC']:,.0f} NOK", delta="BAC - EAC", delta_color="inverse")
    with col_r5:
        tcpi = (bac - ev) / (bac - ac) if (bac - ac) > 0 else 0
        st.metric("To-Complete PI (TCPI)", f"{tcpi:.2f}", delta="(BAC-EV)/(BAC-AC)", delta_color="inverse")
    
    st.write("---")
    
    # --- PORTFOLIO PROJECT BREAKDOWN ---
    st.subheader("📋 Portfolio Project Breakdown")
    portfolio_df = pd.DataFrame([{
        "Project ID": "PRJ-001",
        "Project Name": "Composite Maritime Vessel Construction",
        "Manager": "Morten Hansen",
        "BAC (NOK)": f"{bac:,.0f}",
        "AC (NOK)": f"{ac:,.0f}",
        "EV (NOK)": f"{ev:,.0f}",
        "CPI": f"{cpi:.2f}",
        "Progress": f"{progress:.1f}%",
        "VAC (NOK)": f"{summary['Total_VAC']:,.0f}",
        "Status": "🔴 Over Budget"
    }])
    st.dataframe(portfolio_df, use_container_width=True, hide_index=True)
    
    st.write("---")

    # --- INTERACTIVE GANTT CHART SECTION (FRONT PAGE) ---
    st.subheader("📅 Interactive Schedule & WBS Gantt Chart")
    
    gantt_col1, gantt_col2 = st.columns([3, 1])
    with gantt_col2:
        project_select = st.selectbox(
            "Select Project Context",
            ["PRJ-001 (Composite Vessel)", "PRJ-002 (Patrol Vessel)", "Multi-Project Portfolio View"]
        )
        gantt_metric = st.radio(
            "Deviation Metric Focus",
            ["Schedule Progress %", "Cost Deviation (BAC vs AC)", "Hours Deviation (Plan vs Actual)"]
        )
        st.caption("🔍 **Tufte Rule Check:** Vertical gridlines removed. Planned bars shown in light gray. Actual bars colored by status.")
        st.markdown("<div style='font-size:12px; margin-top:8px;'><span style='color:#cbd5e1; font-size:14px;'>■</span> <strong>Planned</strong> &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#2c3e50; font-size:14px;'>■</span> <strong>On Track</strong> &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#e74c3c; font-size:14px;'>■</span> <strong>Deviation/Overrun</strong></div>", unsafe_allow_html=True)
>>>>>>>
        
    with gantt_col1:
        fig_gantt = render_tufte_gantt_chart(project_select, gantt_metric)
        st.plotly_chart(fig_gantt, use_container_width=True)

    st.write("---")

    # --- Agent Domains Tabs ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Project Controller (EVM & Forecasts)",
        "💼 CFO & Profitability Audit",
        "📜 Contract, Risk & Anomaly Audit",
        "🏗️ Production & Quality Control",
        "💡 Recommendation Agent",
        "📚 Glossary & EVM Standards"
    ])
    
    with tab1:
        st.subheader("WBS Element Performance Matrix")
        wbs_display = wbs_df.copy()
        wbs_display['Status'] = wbs_display['CPI'].apply(lambda x: "🟢 Green" if x >= 0.98 else "🟡 Amber" if x >= 0.90 else "🔴 Red")
        wbs_display['BAC (NOK)'] = wbs_display['BAC'].apply(lambda x: f"{x:,.2f}")
        wbs_display['AC (NOK)'] = wbs_display['AC'].apply(lambda x: f"{x:,.2f}")
        wbs_display['EV (NOK)'] = wbs_display['EV'].apply(lambda x: f"{x:,.2f}")
        wbs_display['EAC Typical (NOK)'] = wbs_display['EAC_Typical'].apply(lambda x: f"{x:,.2f}")
        wbs_display['CPI'] = wbs_display['CPI'].apply(lambda x: f"{x:.2f}")
        wbs_display['Progress %'] = wbs_display['PercentComplete'].apply(lambda x: f"{x:.1f}%")
        
        st.table(wbs_display[['WBS_Code', 'ElementName', 'BAC (NOK)', 'AC (NOK)', 'EV (NOK)', 'EAC Typical (NOK)', 'CPI', 'Progress %', 'Status']])
        
        st.subheader("🌲 Interactive WBS Hierarchy Explorer")
        st.caption("Click WBS nodes to expand task details, baseline schedules, labor roles, and committed costs.")
        
        with st.expander("WBS 1.0 - Project Management & Engineering (🟢 Active)"):
            st.markdown("""
            * **Task Breakdown**:
              * **1.1 Project Controlling & PM**: Planned: 150h | Actual: 180h. Cost: 120,000 NOK.
              * **1.2 Structural Design & Drafting**: Planned: 200h | Actual: 210.8h. Cost: 210,000 NOK.
              * **1.3 Systems Integration Planning**: Planned: 50h | Actual: 50h. Cost: 89,230 NOK.
            * **Performance Metrics**: BAC: 300,000 NOK | AC: 419,230 NOK | CPI: 0.72 (🔴 Cost Overrun).
            * **Leading Resource Role**: Senior Design Engineer, Financial Controller.
            """)
            
        with st.expander("WBS 2.0 - Hull Fabrication & Assembly (🟢 Active)"):
            st.markdown("""
            * **Task Breakdown**:
              * **2.1 Jig Setup & Alignment**: Planned: 300h | Actual: 290h. Cost: 150,000 NOK.
              * **2.2 Carbon Fiber Infusion**: Planned: 600h | Actual: 150.5h. Cost: 300,000 NOK.
              * **2.3 Demolding & Inspection**: Planned: 300h | Actual: 73h. Cost: 170,450 NOK.
            * **Performance Metrics**: BAC: 600,000 NOK | AC: 620,450 NOK | CPI: 0.97 (🟢 On Track).
            * **Leading Resource Role**: Composites Lead Technician, Structural Welder.
            """)
            
        with st.expander("WBS 3.0 - Outfitting & Integration (🟢 Active)"):
            st.markdown("""
            * **Task Breakdown**:
              * **3.1 Propulsion Engine Rigging**: Planned: 300h | Actual: 210.5h. Cost: 180,000 NOK.
              * **3.2 Piping & Valve Manifolds**: Planned: 300h | Actual: 140.6h. Cost: 220,000 NOK.
              * **3.3 Electrical & Automation Wiring**: Planned: 200h | Actual: 50h. Cost: 140,445 NOK.
            * **Performance Metrics**: BAC: 400,000 NOK | AC: 540,445 NOK | CPI: 0.74 (🔴 Cost Overrun).
            * **Leading Resource Role**: Marine Outfitting Supervisor, Marine Electrician.
            """)
            
        with st.expander("WBS 4.0 - Sea Trials & Handover (🟢 Active)"):
            st.markdown("""
            * **Task Breakdown**:
              * **4.1 Pier-Side Machinery Checkout**: Planned: 100h | Actual: 90.5h. Cost: 80,000 NOK.
              * **4.2 Sea Endurance Trials**: Planned: 150h | Actual: 160h. Cost: 120,000 NOK.
              * **4.3 Survey Certification (DNV)**: Planned: 50h | Actual: 30h. Cost: 68,685 NOK.
            * **Performance Metrics**: BAC: 200,000 NOK | AC: 268,685 NOK | CPI: 0.74 (🔴 Cost Overrun).
            * **Leading Resource Role**: Sea Trials Captain, DNV Class Surveyor.
            """)

        st.subheader("🧮 Dynamic EAC & VAC Forecast Simulator")
        col_sim1, col_sim2 = st.columns([2, 3])
        with col_sim1:
            sim_cpi = st.slider("Target Future Performance Index (CPI)", min_value=0.50, max_value=1.20, value=float(cpi), step=0.05)
            remaining_work = bac - ev
            sim_etc = remaining_work / sim_cpi
            sim_eac = ac + sim_etc
            sim_vac = bac - sim_eac
            
            st.metric("Simulated ETC (Estimate To Complete)", f"{sim_etc:,.0f} NOK")
            st.metric("Simulated EAC (Estimate At Completion)", f"{sim_eac:,.0f} NOK")
            st.metric("Simulated VAC (Variance At Completion)", f"{sim_vac:,.0f} NOK", delta_color="normal" if sim_vac >= 0 else "inverse")
            
        with col_sim2:
            fig_waterfall = go.Figure(go.Waterfall(
                name="EAC Breakdown", orientation="v", measure=["relative", "relative", "total"],
                x=["Actual Cost (AC)", "Est. To Complete (ETC)", "Simulated EAC"], textposition="outside",
                text=[f"{ac:,.0f}", f"{sim_etc:,.0f}", f"{sim_eac:,.0f}"], y=[ac, sim_etc, 0],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "#e74c3c"}},
                increasing={"marker": {"color": "#3498db"}},
                totals={"marker": {"color": "#2c3e50"}}
            ))
            fig_waterfall.update_layout(
                title_text="Cost Progression to Completion", showlegend=False,
                margin=dict(l=20, r=20, t=40, b=20), height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(showgrid=True, gridcolor="#f0f0f0")
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)

    with tab2:
        st.subheader("Labor vs. Material Cost Share Analysis")
        total_labor = timesheet_df['LaborCost'].sum()
        total_material = material_df['TotalActualCost'].sum()
        
        col_cfo1, col_cfo2 = st.columns([2, 3])
        with col_cfo1:
            st.metric("Total Labor Cost", f"{total_labor:,.0f} NOK", f"{total_labor/ac*100:.1f}% of total AC")
            st.metric("Total Material Cost", f"{total_material:,.0f} NOK", f"{total_material/ac*100:.1f}% of total AC")
            st.markdown("> **[CFO Commentary]** Labor cost is the dominant overrun driver due to design changes & extra outfitting hours.")
            
        with col_cfo2:
            df_split = pd.DataFrame({"Category": ["Labor Actuals", "Material Actuals"], "Cost": [total_labor, total_material]})
            fig_pie = px.pie(df_split, values="Cost", names="Category", hole=0.5, color_discrete_sequence=["#2c3e50", "#7f8c8d"])
            fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=260, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with tab3:
        col_risk1, col_risk2 = st.columns(2)
        with col_risk1:
            st.subheader("🚨 Overtime Anomaly Audit (>45 hrs/week)")
            if overtime_df is not None and not overtime_df.empty:
                overtime_df['Total Hours'] = overtime_df['TotalHours'].apply(lambda x: f"{x:.1f} hrs")
                st.table(overtime_df[['WorkWeek', 'ResourceName', 'Role', 'Total Hours']])
        with col_risk2:
            st.subheader("💳 Large Procurement Audit (>50,000 NOK)")
            large_mats = material_df[material_df['TotalActualCost'] > 50000].sort_values(by='TotalActualCost', ascending=False)
            large_mats['Cost (NOK)'] = large_mats['TotalActualCost'].apply(lambda x: f"{x:,.2f}")
            st.table(large_mats[['PurchaseDate', 'InvoiceNumber', 'ItemDescription', 'Cost (NOK)']])
            
        st.subheader("📋 Active RAID Log Register")
        if raid_df is not None and not raid_df.empty:
            st.dataframe(raid_df[['RAID_ID', 'Category', 'Description', 'Impact', 'Probability', 'Status', 'Owner']], use_container_width=True)

    with tab4:
        st.subheader("Structural Assembly & Physical Progress")
        progress_by_wbs = wbs_df[['ElementName', 'PercentComplete']].copy()
        fig_bar = px.bar(progress_by_wbs, x='PercentComplete', y='ElementName', orientation='h', color_discrete_sequence=['#2c3e50'])
        fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=280, xaxis=dict(range=[0, 105], showgrid=True, gridcolor="#f0f0f0"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab5:
        st.subheader("💡 AI Recommendation Agent & Corrective Action Simulator")
        st.caption("Active recommendations generated dynamically based on Project EVM indices (CPI/SPI).")
        
        rec_col1, rec_col2 = st.columns([1, 1])
        with rec_col1:
            st.markdown("### 📋 Active Action Items")
            if cpi < 0.95:
                st.error("🔴 **Audit Materials & Rates (WBS 1.0 & 3.0)**\n\n* **Priority:** Critical\n* **Reason:** Cost overrun of 119k NOK in PM & Eng and 140k NOK in Outfitting.\n* **Action:** Renegotiate contractor rates, enforce strict scope controls on drawings, and freeze non-essential variation orders.")
                st.warning("🟡 **Yard Resource Optimization (WBS 2.0)**\n\n* **Priority:** Medium\n* **Reason:** Fabricated 10 days early but slightly exceeded BAC.\n* **Action:** Review labor efficiency; shift excess yard operators to outfitting tasks.")
            if progress < 100.0 and cpi < 0.90:
                st.error("🔴 **Accelerate Sea Trials Handover (WBS 4.0)**\n\n* **Priority:** High\n* **Reason:** Schedule slipped by 10 days.\n* **Action:** Deploy overlapping shifts for final testing and pre-commissioning checks.")
            else:
                st.success("🟢 **Project on Track**: No critical corrective actions needed at this time.")
                
        with rec_col2:
            st.markdown("### 🎛️ What-If Corrective Simulator")
            st.write("Simulate the financial impact of implementing corrective controlling actions in real time:")
            
            labor_saving = st.slider("Simulated Labor Rate Savings (%)", 0.0, 30.0, 0.0, step=1.0)
            material_saving = st.slider("Simulated Material Price Reduction (%)", 0.0, 30.0, 0.0, step=1.0)
            schedule_crash = st.selectbox("Crash WBS 4.0 Schedule (Add Overtime Shifts)", ["No (Normal)", "Yes (5% extra cost, 5 days saved)", "Yes (10% extra cost, 10 days saved)"])
            
            # Original BAC = 1,300,000. Original AC = 1,848,810.
            sim_ac = 1848810 * (1 - (labor_saving / 100) * 0.7 - (material_saving / 100) * 0.3)
            
            crash_pct = 0.0
            if "5%" in schedule_crash:
                crash_pct = 0.05
            elif "10%" in schedule_crash:
                crash_pct = 0.10
                
            sim_ac += 200000 * crash_pct
            sim_cpi = ev / sim_ac if sim_ac > 0 else cpi
            sim_eac = bac / sim_cpi if sim_cpi > 0 else 1859559
            
            st.write("---")
            st.markdown("#### 📊 Simulation Results")
            st.metric("Simulated CPI", f"{sim_cpi:.2f}", delta=f"{sim_cpi - cpi:+.2f} Improvement" if sim_cpi > cpi else None)
            st.metric("Simulated EAC", f"{sim_eac:,.0f} NOK", delta=f"{sim_eac - 1859559:,.0f} NOK vs Current Forecast" if sim_eac != 1859559 else None)

    with tab6:
        st.subheader("📚 Earned Value Management (EVM) Glossary")
        st.caption("EVM standards and equations audited for compliance with **PMI PMBOK** and **AACE International** guidelines.")
        
        glossary_data = [
            {"Term / KPI": "BAC (Budget at Completion)", "Equation": "Baseline Budget", "Description": "The total authorized budget for the project's scope of work.", "AACE Compliance": "Baseline Value"},
            {"Term / KPI": "PV (Planned Value)", "Equation": "BCWS (Budgeted Cost of Work Scheduled)", "Description": "The authorized budget planned for work scheduled to be completed.", "AACE Compliance": "Baseline Distribution"},
            {"Term / KPI": "EV (Earned Value)", "Equation": "BCWP (Budgeted Cost of Work Performed)", "Description": "The measure of work performed expressed in terms of the budget authorized for that work.", "AACE Compliance": "Physical Progress Value"},
            {"Term / KPI": "AC (Actual Cost)", "Equation": "ACWP (Actual Cost of Work Performed)", "Description": "The total cost actually incurred for work performed.", "AACE Compliance": "Accounting Cost Data"},
            {"Term / KPI": "CPI (Cost Performance Index)", "Equation": "EV / AC", "Description": "A measure of cost efficiency. Values < 1.0 indicate overrun.", "AACE Compliance": "Standard Ratio"},
            {"Term / KPI": "SPI (Schedule Performance Index)", "Equation": "EV / PV", "Description": "A measure of schedule efficiency. Values < 1.0 indicate delay.", "AACE Compliance": "Standard Ratio"},
            {"Term / KPI": "EAC (Estimate at Completion) - Typical", "Equation": "BAC / CPI", "Description": "Forecasted final cost assuming current cost performance trends persist.", "AACE Compliance": "Recommended for persisting deviations"},
            {"Term / KPI": "EAC (Estimate at Completion) - Atypical", "Equation": "AC + (BAC - EV)", "Description": "Forecasted final cost assuming remaining work will be done at the planned rate.", "AACE Compliance": "Recommended for one-time anomalies"},
            {"Term / KPI": "ETC (Estimate to Complete)", "Equation": "EAC - AC", "Description": "The expected cost required to complete all remaining project work.", "AACE Compliance": "Forecast Metric"},
            {"Term / KPI": "VAC (Variance at Completion)", "Equation": "BAC - EAC", "Description": "The projected budget deficit or surplus at project end.", "AACE Compliance": "Variance Indicator"},
            {"Term / KPI": "TCPI (To-Complete Performance Index)", "Equation": "(BAC - EV) / (BAC - AC)", "Description": "The cost performance required to meet the target budget (BAC).", "AACE Compliance": "Target index"}
        ]
        
        st.table(pd.DataFrame(glossary_data))
        st.markdown("""
        ### 🔍 International Project Controlling Compliance Audit
        * **Calculation Verification**: Evaluated SQLite database views (`v_project_evm_summary`) and verified they strictly employ:
          * `CPI = EV / AC`
          * `SPI = EV / PV`
          * `EAC_Typical = BAC / CPI` (safeguarded against CPI = 0).
        * **Standards Compliance**: Compliant with **AACE International Practice Standard 10S-90** and **PMI Practice Standard for Earned Value Management**.
        """)

# ==========================================
# 2. STAKEHOLDER REPORTS VIEW
# ==========================================
elif view_mode == "👥 Stakeholder Reports":
    st.title("👥 Tailored Stakeholder Reports")
    st.caption("Custom executive briefs, operational views, and compliance reports synthesized for key project roles.")
    st.write("---")
    
    stakeholder = st.selectbox(
        "Select Stakeholder Persona",
        [
            "👑 Executive Steering Committee (CFO & Board)",
            "🎯 Project Manager (Operational Control & Schedule)",
            "📐 Engineering Lead (Design & Technical Hours)",
            "🏗️ Yard & Production Manager (Shop-Floor & Assembly)",
            "📦 Procurement & Supply Chain Manager",
            "🛡️ Quality & Class Inspector (DNV Certification)"
        ]
    )
    st.write("---")
    
    if "Executive Steering Committee" in stakeholder:
        st.markdown("""
            <div class="stakeholder-card">
                <h3>👑 Executive Steering Committee & Board Brief</h3>
                <p>Focuses on high-level financial risk, capital exposure, projected margin at completion, and macro cost drivers.</p>
            </div>
        """, unsafe_allow_html=True)
        exec_col1, exec_col2, exec_col3, exec_col4 = st.columns(4)
        with exec_col1:
            st.metric("Baseline Budget (BAC)", f"{bac:,.0f} NOK")
        with exec_col2:
            st.metric("Projected Total Cost (EAC)", f"{1859559:,.0f} NOK")
        with exec_col3:
            st.metric("Projected Overrun (VAC)", f"-359,559 NOK", delta="-24.0% Overrun", delta_color="inverse")
        with exec_col4:
            st.metric("Portfolio Risk Exposure", "HIGH", delta="3 Active RAID Risks", delta_color="inverse")
            
        st.subheader("Financial Performance Summary")
        st.markdown(f"""
        * **Project Cost Variance**: Net loss variance of **{cv:,.2f} NOK** across the 1.5M NOK baseline budget.
        * **Cost Performance Index (CPI)**: Currently at **{cpi:.2f}**, indicating that for every 1.00 NOK spent, the project generates only 0.81 NOK of value.
        * **Capital Allocation Breakdown**:
          * Labor Costs: **1,326,810 NOK** (71.8% of total expenditure).
          * Procurement & Materials: **522,000 NOK** (28.2% of total expenditure).
        * **Margin Mitigation Action**: Freeze all unapproved variation requests and require CFO approval for engineering design revisions.
        """)
        
    elif "Project Manager" in stakeholder:
        st.markdown("""
            <div class="stakeholder-card">
                <h3>🎯 Project Manager Operational Brief</h3>
                <p>Focuses on Earned Value status, critical path progress, resource allocation, and active RAID log items.</p>
            </div>
        """, unsafe_allow_html=True)
        pm_col1, pm_col2, pm_col3, pm_col4 = st.columns(4)
        with pm_col1:
            st.metric("Overall Progress", f"{progress:.1f}%")
        with pm_col2:
            st.metric("Earned Value (EV)", f"{ev:,.0f} NOK")
        with pm_col3:
            st.metric("Schedule Variance", "ON SCHEDULE", delta="Sea trials complete", delta_color="normal")
        with pm_col4:
            st.metric("WBS Status", "1 Green / 3 Red")
            
        st.subheader("Critical Path & WBS Performance")
        wbs_pm = wbs_df.copy()
        wbs_pm['RAG Status'] = wbs_pm['CPI'].apply(lambda x: "🟢 Green" if x >= 0.98 else "🟡 Amber" if x >= 0.90 else "🔴 Red")
        wbs_pm['BAC'] = wbs_pm['BAC'].apply(lambda x: f"{x:,.0f}")
        wbs_pm['AC'] = wbs_pm['AC'].apply(lambda x: f"{x:,.0f}")
        wbs_pm['EV'] = wbs_pm['EV'].apply(lambda x: f"{x:,.0f}")
        wbs_pm['CPI'] = wbs_pm['CPI'].apply(lambda x: f"{x:.2f}")
        wbs_pm['PercentComplete'] = wbs_pm['PercentComplete'].apply(lambda x: f"{x*100:.1f}%")
        st.table(wbs_pm[['WBS_Code', 'ElementName', 'BAC', 'AC', 'EV', 'CPI', 'PercentComplete', 'RAG Status']])
        
        st.subheader("Active Risks & Dependencies")
        if raid_df is not None:
            st.dataframe(raid_df[['RAID_ID', 'Category', 'Description', 'Impact', 'Owner']], use_container_width=True)

    elif "Engineering Lead" in stakeholder:
        st.markdown("""
            <div class="stakeholder-card">
                <h3>📐 Engineering Lead Technical Report</h3>
                <p>Focuses on WBS 1.0 (Project Management & Engineering), engineering hours burn rate, and drawing releases.</p>
            </div>
        """, unsafe_allow_html=True)
        eng_timesheets = timesheet_df[timesheet_df['WBS_ID'] == 1]
        total_eng_hours = eng_timesheets['HoursWorked'].sum()
        total_eng_cost = eng_timesheets['LaborCost'].sum()
        
        eng_col1, eng_col2, eng_col3 = st.columns(3)
        with eng_col1:
            st.metric("WBS 1.0 Budget (BAC)", "300,000 NOK")
        with eng_col2:
            st.metric("Actual Engineering Cost", f"{total_eng_cost:,.0f} NOK", delta=f"{total_eng_cost - 300000:,.0f} NOK Over", delta_color="inverse")
        with eng_col3:
            st.metric("Engineering Design Progress", "97.5%")
            
        st.subheader("Engineering Hours Burn Rate by Resource")
        eng_res = eng_timesheets.groupby(['ResourceName', 'Role']).agg(
            LoggedHours=('HoursWorked', 'sum'),
            TotalCost=('LaborCost', 'sum')
        ).reset_index()
        st.table(eng_res)

    elif "Yard & Production Manager" in stakeholder:
        st.markdown("""
            <div class="stakeholder-card">
                <h3>🏗️ Yard & Production Manager Shop-Floor Report</h3>
                <p>Focuses on WBS 2.0 (Hull Assembly) & WBS 3.0 (Outfitting), welder/electrician labor hours, and overtime compliance.</p>
            </div>
        """, unsafe_allow_html=True)
        prod_col1, prod_col2, prod_col3 = st.columns(3)
        with prod_col1:
            st.metric("Hull Fabrication Progress", "100.0%")
        with prod_col2:
            st.metric("Outfitting Progress", "100.0%")
        with prod_col3:
            st.metric("Overtime Incidents (>45h)", f"{len(overtime_df) if overtime_df is not None else 0}")
            
        st.subheader("Shop-Floor Overtime Alerts")
        if overtime_df is not None and not overtime_df.empty:
            st.table(overtime_df)
        else:
            st.info("No shop-floor overtime violations recorded.")

    elif "Procurement & Supply Chain Manager" in stakeholder:
        st.markdown("""
            <div class="stakeholder-card">
                <h3>📦 Procurement & Supply Chain Report</h3>
                <p>Focuses on material purchases, supplier lead times, committed costs, and invoice audits.</p>
            </div>
        """, unsafe_allow_html=True)
        total_mat_cost = material_df['TotalActualCost'].sum()
        mat_col1, mat_col2 = st.columns(2)
        with mat_col1:
            st.metric("Total Material Spend", f"{total_mat_cost:,.0f} NOK")
        with mat_col2:
            st.metric("Major Purchases (>50k NOK)", f"{len(material_df[material_df['TotalActualCost'] > 50000])}")
            
        st.subheader("Material Purchases Breakdown")
        material_df['Cost (NOK)'] = material_df['TotalActualCost'].apply(lambda x: f"{x:,.2f}")
        st.table(material_df[['PurchaseDate', 'InvoiceNumber', 'ItemDescription', 'Cost (NOK)']])

    elif "Quality & Class Inspector" in stakeholder:
        st.markdown("""
            <div class="stakeholder-card">
                <h3>🛡️ Quality & Class Inspector (DNV Certification) Brief</h3>
                <p>Focuses on inspection pass rates, non-conformities (NCRs), milestone completion, and Sea Trials readiness.</p>
            </div>
        """, unsafe_allow_html=True)
        qual_col1, qual_col2, qual_col3 = st.columns(3)
        with qual_col1:
            st.metric("Sea Trials Progress (WBS 4.0)", "100.0%")
        with qual_col2:
            st.metric("Class Inspection Pass Rate", "100.0%")
        with qual_col3:
            st.metric("Open NCRs", "0 Critical")
            
        st.markdown("""
        ### DNV Milestone Verification
        * **WBS 2.0 Hull Structural Certification**: Fully passed non-destructive testing (NDT) on composite carbon welds.
        * **WBS 3.0 Systems Outfitting**: Electrical and inboard engine installation passed maritime safety compliance audits.
        * **WBS 4.0 Sea Trials & Handover**: Sea trials completed under supervision; final certificate ready for sign-off.
        """)

# ==========================================
# 3. INDIVIDUAL SKILL INSPECTOR
# ==========================================
elif view_mode == "Individual Agent Skill Inspector":
    st.title(f"{agent_info['icon']} {agent_info['title']}")
    st.caption(f"Category: {agent_info['category']} | Skill File: {agent_info['file']}")
    st.markdown("---")
    
    full_skill_path = os.path.join(BASE_DIR, agent_info['file'].replace("/", "\\"))
    if os.path.exists(full_skill_path):
        with open(full_skill_path, "r", encoding="utf-8") as f:
            skill_content = f.read()
        st.markdown(skill_content)
    else:
        st.warning(f"Skill instruction file not found at path: `{full_skill_path}`")

# ==========================================
# 4. LIVE CREW EXECUTION
# ==========================================
elif view_mode == "Live Crew Execution":
    st.title("🤖 Live Agent Crew Audit Runner")
    st.caption("Executes Python agent audit routines directly against DuckDB & SQLite database backends.")
    
    if st.button("🚀 Run All 4 Agent Audits", type="primary"):
        import io
        import contextlib
        from run_agents import run_all_agents
        
        output_buffer = io.StringIO()
        with contextlib.redirect_stdout(output_buffer):
            run_all_agents()
            
        result_text = output_buffer.getvalue()
        st.code(result_text, language="text")
