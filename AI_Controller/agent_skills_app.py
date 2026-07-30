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
def render_tufte_gantt_chart(project_selection="PRJ-001 (Composite Vessel)"):
    # Generate schedule datasets
    tasks_prj001 = [
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "1.0", "Task": "1.0 PM & Engineering", "Start": "2026-01-01", "Finish": "2026-06-30", "Type": "Actual Schedule", "Status": "⚠️ Over Budget", "Progress": 97.5, "BAC": 300000, "AC": 419230},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "2.0", "Task": "2.0 Hull Fabrication", "Start": "2026-02-01", "Finish": "2026-04-20", "Type": "Actual Schedule", "Status": "✅ On Track", "Progress": 100.0, "BAC": 600000, "AC": 620450},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "3.0", "Task": "3.0 Outfitting & Integration", "Start": "2026-04-01", "Finish": "2026-05-25", "Type": "Actual Schedule", "Status": "⚠️ Over Budget", "Progress": 100.0, "BAC": 400000, "AC": 540445},
        {"Project": "PRJ-001 (Vessel Construction)", "WBS": "4.0", "Task": "4.0 Sea Trials & Handover", "Start": "2026-06-01", "Finish": "2026-06-30", "Type": "Actual Schedule", "Status": "⚠️ Over Budget", "Progress": 100.0, "BAC": 200000, "AC": 268685},
    ]
    
    tasks_prj002 = [
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "1.0", "Task": "1.0 Hull Design & CFD", "Start": "2026-05-01", "Finish": "2026-08-15", "Type": "Actual Schedule", "Status": "✅ On Track", "Progress": 75.0, "BAC": 450000, "AC": 320000},
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "2.0", "Task": "2.0 Carbon Fiber Molding", "Start": "2026-07-01", "Finish": "2026-10-30", "Type": "Actual Schedule", "Status": "✅ On Track", "Progress": 20.0, "BAC": 850000, "AC": 170000},
        {"Project": "PRJ-002 (Autonomous Patrol Vessel)", "WBS": "3.0", "Task": "3.0 Autonomous Avionics", "Start": "2026-09-01", "Finish": "2026-12-15", "Type": "Planned Schedule", "Status": "✅ On Track", "Progress": 0.0, "BAC": 650000, "AC": 0},
    ]
    
    if "PRJ-001" in project_selection:
        df_gantt = pd.DataFrame(tasks_prj001)
    elif "PRJ-002" in project_selection:
        df_gantt = pd.DataFrame(tasks_prj002)
    else:
        df_gantt = pd.DataFrame(tasks_prj001 + tasks_prj002)
        
    df_gantt["Start"] = pd.to_datetime(df_gantt["Start"])
    df_gantt["Finish"] = pd.to_datetime(df_gantt["Finish"])
    
    # Plotly Timeline Gantt adhering to Tufte Principles:
    # - No vertical gridlines (showgrid=False)
    # - High-contrast clean color palette (#2c3e50 for On Track, #e74c3c for Over Budget)
    # - Direct labeling showing physical progress % on bars
    fig_gantt = px.timeline(
        df_gantt,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Status",
        text=df_gantt["Progress"].apply(lambda x: f"{x:.1f}%"),
        hover_data=["Project", "BAC", "AC", "Progress"],
        color_discrete_map={
            "✅ On Track": "#2c3e50",
            "⚠️ Over Budget": "#e74c3c"
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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
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
    
    # --- Top KPI Row (Tufte Style) ---
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Budget at Completion", f"{bac:,.0f} NOK")
    with col2:
        st.metric("Actual Cost (AC)", f"{ac:,.0f} NOK", delta=f"{ac - bac:,.0f} NOK over BAC", delta_color="inverse")
    with col3:
        st.metric("Earned Value (EV)", f"{ev:,.0f} NOK")
    with col4:
        st.metric("Project CPI", f"{cpi:.2f}", delta=f"{'ON TRACK' if cpi >= 0.95 else 'COST OVERRUN'}", delta_color="normal" if cpi >= 0.95 else "inverse")
    with col5:
        st.metric("Physical Progress", f"{progress:.1f}%")
        
    st.write("---")

    # --- INTERACTIVE GANTT CHART SECTION (FRONT PAGE) ---
    st.subheader("📅 Interactive Schedule & WBS Gantt Chart")
    
    gantt_col1, gantt_col2 = st.columns([3, 1])
    with gantt_col2:
        project_select = st.selectbox(
            "Select Project Context",
            ["PRJ-001 (Composite Vessel)", "PRJ-002 (Patrol Vessel)", "Multi-Project Portfolio View"]
        )
        st.caption("🔍 **Tufte Rule Check:** Vertical gridlines removed for maximum data-ink ratio. Progress percentages displayed directly on bars.")
        
    with gantt_col1:
        fig_gantt = render_tufte_gantt_chart(project_select)
        st.plotly_chart(fig_gantt, use_container_width=True)

    st.write("---")

    # --- Agent Domains Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Project Controller (EVM & Forecasts)",
        "💼 CFO & Profitability Audit",
        "📜 Contract, Risk & Anomaly Audit",
        "🏗️ Production & Quality Control"
    ])
    
    with tab1:
        st.subheader("WBS Element Performance Matrix")
        wbs_display = wbs_df.copy()
        wbs_display['Status'] = wbs_display['CPI'].apply(lambda x: "⚠️ OVER BUDGET" if x < 0.95 else "✅ ON TRACK")
        wbs_display['BAC (NOK)'] = wbs_display['BAC'].apply(lambda x: f"{x:,.2f}")
        wbs_display['AC (NOK)'] = wbs_display['AC'].apply(lambda x: f"{x:,.2f}")
        wbs_display['EV (NOK)'] = wbs_display['EV'].apply(lambda x: f"{x:,.2f}")
        wbs_display['EAC Typical (NOK)'] = wbs_display['EAC_Typical'].apply(lambda x: f"{x:,.2f}")
        wbs_display['CPI'] = wbs_display['CPI'].apply(lambda x: f"{x:.2f}")
        wbs_display['Progress %'] = wbs_display['PercentComplete'].apply(lambda x: f"{x:.1f}%")
        
        st.table(wbs_display[['WBS_Code', 'ElementName', 'BAC (NOK)', 'AC (NOK)', 'EV (NOK)', 'EAC Typical (NOK)', 'CPI', 'Progress %', 'Status']])
        
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
            st.metric("WBS Status", "1 On Track / 3 Over Budget")
            
        st.subheader("Critical Path & WBS Performance")
        st.table(wbs_df[['WBS_Code', 'ElementName', 'BAC', 'AC', 'EV', 'CPI', 'PercentComplete']])
        
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
