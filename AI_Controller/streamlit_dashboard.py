import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import os

from dashboard_data import (
    BASE_DIR,
    EXCEL_PATH,
    SKILLS_DIR,
    build_material_audit_table,
    load_file_bytes,
    load_markdown_text,
    load_project_data,
    prepare_progress_history_for_chart,
)

# Set page config
st.set_page_config(
    page_title="Project Control Tower Dashboard",
    page_icon=":material/anchor:",
    layout="wide"
)

# Custom CSS for clean Tufte styling
st.markdown("""
    <style>
    /* Clean font styles */
    html, body, [class*="View"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove card borders, backgrounds and shadows */
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }
    
    /* Muted and uppercase metric labels */
    div[data-testid="stMetricLabel"] > div {
        color: #7f8c8d !important;
        font-size: 11px !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Strong typography for metric values */
    div[data-testid="stMetricValue"] > div {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #1a252f !important;
    }
    
    /* Style tables to be clean and simple */
    .tufte-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        margin-top: 8px;
    }
    .tufte-table th {
        background-color: #f8f9fa;
        color: #1a252f;
        font-weight: 600;
        text-align: left;
        border-bottom: 2px solid #e2e8f0;
        padding: 10px 12px;
    }
    .tufte-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* Highlight cost overrun colors */
    .text-danger { color: #e74c3c !important; font-weight: 600; }
    .text-success { color: #2ecc71 !important; font-weight: 600; }
    .text-warning { color: #f39c12 !important; font-weight: 600; }
    
    /* Clean up headers & footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

data = load_project_data()

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.markdown("### ⚓ Agent Control Tower")
st.sidebar.caption("PRJ-001 | Vessel Construction Controller")

nav_choice = st.sidebar.radio(
    "Navigation",
    ["📊 Control Tower Dashboard", "👥 Stakeholder Reports", "⚙️ Skill Inspector", "🤖 Live Crew Execution"],
    label_visibility="collapsed"
)

# Download Excel Report button in sidebar
if os.path.exists(EXCEL_PATH):
    excel_bytes = load_file_bytes(EXCEL_PATH)
    st.sidebar.download_button(
        label=":material/download: Download Excel Report",
        data=excel_bytes,
        file_name="vessel_construction_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch"
    )

if data is None:
    st.error("Project database not found. Please run `python AI_Controller/build_duckdb.py` first.")
else:
    summary = data["summary"]
    wbs = data["wbs"]
    materials = data["materials"]
    timesheets = data["timesheets"]
    progress_history = data["progress_history"]
    overtime = data["overtime"]
    raid = data["raid"]

    if nav_choice == "📊 Control Tower Dashboard":
        # Header block
        st.title("Project Control Tower Dashboard")
        st.caption("Integrated Earned Value Management & Agent Intelligence System")
        
        st.markdown("### 📊 Portfolio Control Tower — Project Summary")
        st.caption("Aggregate KPIs across all active projects | Last updated: 2026-06-30")
        
        # Total Portfolio KPI Row
        kpi_cols = st.columns(5)
        kpi_cols[0].metric("Total Portfolio BAC", f"{summary['Total_BAC']:,.0f} USD", help="Baseline budget (1 project)")
        kpi_cols[1].metric("Total Actual Cost (AC)", f"{summary['Total_AC']:,.0f} USD", f"+{summary['Total_AC'] - summary['Total_BAC']:,.0f} over BAC", delta_color="inverse")
        kpi_cols[2].metric("Total Earned Value (EV)", f"{summary['Total_EV']:,.0f} USD", "99.5% work complete")
        
        cpi = summary["Project_CPI"]
        cpi_status = "COST OVERRUN" if cpi < 0.95 else "ON TRACK"
        kpi_cols[3].metric("Portfolio CPI", f"{cpi:.2f}", cpi_status, delta_color="normal" if cpi >= 0.95 else "inverse")
        kpi_cols[4].metric("Portfolio Progress", f"{summary['Overall_Progress_Pct']:.1f}%", "0.5% remaining")
        
        # Financial Ratios Row
        st.markdown("##### 📈 Portfolio Financial Ratios & Forecasts")
        ratio_cols = st.columns(5)
        ratio_cols[0].metric("Cost Variance (CV)", f"{summary['Total_CV']:,.0f} USD", "EV - AC", delta_color="off")
        ratio_cols[1].metric("EAC (Typical)", f"{summary['Total_EAC_Typical']:,.0f} USD", "BAC / CPI", delta_color="off")
        
        atypical_eac = summary["Total_AC"] + (summary["Total_BAC"] - summary["Total_EV"])
        ratio_cols[2].metric("EAC (Atypical)", f"{atypical_eac:,.0f} USD", "AC + (BAC - EV)", delta_color="off")
        ratio_cols[3].metric("Variance at Completion (VAC)", f"{summary['Total_VAC']:,.0f} USD", "BAC - EAC", delta_color="off")
        
        tcpi = (summary["Total_BAC"] - summary["Total_EV"]) / (summary["Total_BAC"] - summary["Total_AC"]) if (summary["Total_BAC"] - summary["Total_AC"]) != 0 else 0.81
        ratio_cols[4].metric("To-Complete PI (TCPI)", f"{tcpi:.2f}", "(BAC-EV)/(BAC-AC)", delta_color="off")
        
        st.markdown("---")
        
        # Sub-tabs
        tab_controller, tab_cfo, tab_contract, tab_production, tab_rec, tab_glossary = st.tabs([
            "📊 Project Controller", 
            "💼 CFO & Profitability Audit", 
            "📜 Contract & Risk Audit", 
            "🏗️ Production & Assembly", 
            "💡 Recommendations & Simulator", 
            "📚 Glossary"
        ])
        
        # TAB 1: Project Controller
        with tab_controller:
            st.markdown("### WBS Element Performance")
            
            # Format and display the WBS table nicely
            wbs_disp = wbs.copy()
            wbs_disp["PercentComplete"] = (wbs_disp["PercentComplete"] * 100).map("{:.1f}%".format)
            wbs_disp["CPI"] = wbs_disp["CPI"].map("{:.2f}".format)
            wbs_disp["BAC"] = wbs_disp["BAC"].map("{:,.0f} USD".format)
            wbs_disp["AC"] = wbs_disp["AC"].map("{:,.0f} USD".format)
            wbs_disp["EV"] = wbs_disp["EV"].map("{:,.0f} USD".format)
            wbs_disp["EAC_Typical"] = wbs_disp["EAC_Typical"].map("{:,.0f} USD".format)
            
            st.dataframe(
                wbs_disp[["WBS_Code", "ElementName", "BAC", "AC", "EV", "CPI", "PercentComplete", "EAC_Typical"]],
                hide_index=True
            )
            
            # WBS Hierarchy Explorer
            st.markdown("#### 🌲 Interactive WBS Hierarchy Explorer")
            st.caption("Expand task details, baseline schedules, labor roles, and committed costs.")
            
            with st.expander("📂 WBS 1.0 - Project Management & Engineering (🟢 Active)"):
                st.markdown("""
                * **1.1 Project Controlling & PM**: Planned: 150h | Actual: 180h. Cost: 120,000 USD.
                * **1.2 Structural Design & Drafting**: Planned: 200h | Actual: 210.8h. Cost: 210,000 USD.
                * **1.3 Systems Integration Planning**: Planned: 50h | Actual: 50h. Cost: 89,230 USD.
                
                **Performance Metrics**: BAC: 300,000 USD | AC: 419,230 USD | CPI: 0.72 (🔴 Cost Overrun).  
                **Leading Resource Role**: Senior Design Engineer, Financial Controller.
                """)
                
            with st.expander("📂 WBS 2.0 - Hull Fabrication & Assembly (🟢 Active)"):
                st.markdown("""
                * **2.1 Jig Setup & Alignment**: Planned: 300h | Actual: 290h. Cost: 150,000 USD.
                * **2.2 Carbon Fiber Infusion**: Planned: 600h | Actual: 150.5h. Cost: 300,000 USD.
                * **2.3 Demolding & Inspection**: Planned: 300h | Actual: 73h. Cost: 170,450 USD.
                
                **Performance Metrics**: BAC: 600,000 USD | AC: 620,450 USD | CPI: 0.97 (🟢 On Track).  
                **Leading Resource Role**: Composites Lead Technician, Structural Welder.
                """)
                
            with st.expander("📂 WBS 3.0 - Outfitting & Integration (🟢 Active)"):
                st.markdown("""
                * **3.1 Propulsion Engine Rigging**: Planned: 300h | Actual: 210.5h. Cost: 180,000 USD.
                * **3.2 Piping & Valve Manifolds**: Planned: 300h | Actual: 140.6h. Cost: 220,000 USD.
                * **3.3 Electrical & Automation Wiring**: Planned: 200h | Actual: 50h. Cost: 140,445 USD.
                
                **Performance Metrics**: BAC: 400,000 USD | AC: 540,445 USD | CPI: 0.74 (🔴 Cost Overrun).  
                **Leading Resource Role**: Marine Outfitting Supervisor, Marine Electrician.
                """)
                
            with st.expander("📂 WBS 4.0 - Sea Trials & Handover (🟢 Active)"):
                st.markdown("""
                * **4.1 Pier-Side Machinery Checkout**: Planned: 100h | Actual: 90.5h. Cost: 80,000 USD.
                * **4.2 Sea Endurance Trials**: Planned: 150h | Actual: 160h. Cost: 120,000 USD.
                * **4.3 Survey Certification (DNV)**: Planned: 50h | Actual: 30h. Cost: 68,685 USD.
                
                **Performance Metrics**: BAC: 200,000 USD | AC: 268,685 USD | CPI: 0.74 (🔴 Cost Overrun).  
                **Leading Resource Role**: Sea Trials Captain, DNV Class Surveyor.
                """)
                
            # Gantt Chart & S-Curve Section
            st.markdown("#### 📅 Interactive Schedule & WBS Gantt Chart")
            
            gantt_proj = st.selectbox(
                "Select Project Context:",
                options=["PORTFOLIO", "PRJ-001", "PRJ-002", "PRJ-003", "PRJ-004", "PRJ-005", "PRJ-006"],
                format_func=lambda x: {
                    "PORTFOLIO": "Portfolio Level (Gantt of Gantts)",
                    "PRJ-001": "PRJ-001 (Composite Vessel)",
                    "PRJ-002": "PRJ-002 (Patrol Vessel)",
                    "PRJ-003": "PRJ-003 (Subsea Frame)",
                    "PRJ-004": "PRJ-004 (Workboat Hull)",
                    "PRJ-005": "PRJ-005 (Logistics Pontoon)",
                    "PRJ-006": "PRJ-006 (Cargo Hatch)"
                }[x]
            )
            
            gantt_metric = st.selectbox(
                "Deviation Focus:",
                options=["Schedule", "Cost", "Hours"],
                format_func=lambda x: {
                    "Schedule": "Schedule Progress %",
                    "Cost": "Cost Deviation (BAC vs AC)",
                    "Hours": "Hours Deviation (Plan vs Actual)"
                }[x]
            )
            
            gantt_data_dict = {
                'PORTFOLIO': [
                    {"task": "PRJ-001 Composite Maritime Vessel", "plannedStart": "2026-01-01", "plannedFinish": "2026-06-30", "actualStart": "2026-01-01", "actualFinish": "2026-06-30", "progress": 99.5, "status": "Red", "bac": 1500000, "ac": 1848810, "plannedHours": 2700, "actualHours": 1435.9},
                    {"task": "PRJ-002 Patrol Vessel Mold", "plannedStart": "2026-08-01", "plannedFinish": "2026-12-31", "actualStart": "2026-08-01", "actualFinish": "2026-12-31", "progress": 0.0, "status": "Green", "bac": 800000, "ac": 0, "plannedHours": 300, "actualHours": 0},
                    {"task": "PRJ-003 Subsea Cable Frame", "plannedStart": "2026-05-01", "plannedFinish": "2026-10-31", "actualStart": "2026-05-01", "actualFinish": "2026-10-31", "progress": 30.0, "status": "Green", "bac": 1200000, "ac": 382500, "plannedHours": 1400, "actualHours": 350},
                    {"task": "PRJ-004 Autonomous Workboat Hull", "plannedStart": "2026-03-01", "plannedFinish": "2026-08-31", "actualStart": "2026-03-01", "actualFinish": "2026-08-31", "progress": 70.0, "status": "Green", "bac": 2000000, "ac": 1476000, "plannedHours": 2500, "actualHours": 1580},
                    {"task": "PRJ-005 Defense Logistics Pontoon", "plannedStart": "2026-02-01", "plannedFinish": "2026-07-31", "actualStart": "2026-02-01", "actualFinish": "2026-07-31", "progress": 90.0, "status": "Green", "bac": 1000000, "ac": 927000, "plannedHours": 1250, "actualHours": 1020},
                    {"task": "PRJ-006 Lightweight Cargo Hatch", "plannedStart": "2025-10-01", "plannedFinish": "2026-03-31", "actualStart": "2025-10-01", "actualFinish": "2026-03-31", "progress": 100.0, "status": "Green", "bac": 600000, "ac": 586500, "plannedHours": 700, "actualHours": 670}
                ],
                'PRJ-001': [
                    {"task": "1.0 PM & Engineering", "plannedStart": "2026-01-01", "plannedFinish": "2026-06-30", "actualStart": "2026-01-01", "actualFinish": "2026-06-30", "progress": 97.5, "status": "Red", "bac": 300000, "ac": 419230, "plannedHours": 400.0, "actualHours": 440.8},
                    {"task": "2.0 Hull Fabrication", "plannedStart": "2026-02-01", "plannedFinish": "2026-04-30", "actualStart": "2026-02-01", "actualFinish": "2026-04-20", "progress": 100.0, "status": "Green", "bac": 600000, "ac": 620450, "plannedHours": 1200.0, "actualHours": 513.5},
                    {"task": "3.0 Outfitting & Integration", "plannedStart": "2026-04-01", "plannedFinish": "2026-05-30", "actualStart": "2026-04-01", "actualFinish": "2026-05-25", "progress": 100.0, "status": "Red", "bac": 400000, "ac": 540445, "plannedHours": 800.0, "actualHours": 401.1},
                    {"task": "4.0 Sea Trials & Handover", "plannedStart": "2026-06-01", "plannedFinish": "2026-06-20", "actualStart": "2026-06-01", "actualFinish": "2026-06-30", "progress": 100.0, "status": "Red", "bac": 200000, "ac": 268685, "plannedHours": 300.0, "actualHours": 280.5}
                ],
                'PRJ-002': [
                    {"task": "1.0 Design & CFD Analysis", "plannedStart": "2026-08-01", "plannedFinish": "2026-10-15", "actualStart": "2026-08-01", "actualFinish": "2026-10-15", "progress": 0.0, "status": "Green", "bac": 300000, "ac": 0, "plannedHours": 300.0, "actualHours": 0.0},
                    {"task": "2.0 Material Procurement", "plannedStart": "2026-10-01", "plannedFinish": "2026-12-31", "actualStart": "2026-10-01", "actualFinish": "2026-12-31", "progress": 0.0, "status": "Green", "bac": 500000, "ac": 0, "plannedHours": 0.0, "actualHours": 0.0}
                ],
                'PRJ-003': [
                    {"task": "1.0 Structural Frame Engineering", "plannedStart": "2026-05-01", "plannedFinish": "2026-07-15", "actualStart": "2026-05-01", "actualFinish": "2026-07-20", "progress": 90.0, "status": "Green", "bac": 400000, "ac": 332500, "plannedHours": 400.0, "actualHours": 350.0},
                    {"task": "2.0 Steel Fabrication", "plannedStart": "2026-07-01", "plannedFinish": "2026-10-31", "actualStart": "2026-07-01", "actualFinish": "2026-10-31", "progress": 0.0, "status": "Green", "bac": 800000, "ac": 50000, "plannedHours": 1000.0, "actualHours": 0.0}
                ],
                'PRJ-004': [
                    {"task": "1.0 Engineering & Class Approval", "plannedStart": "2026-03-01", "plannedFinish": "2026-05-15", "actualStart": "2026-03-01", "actualFinish": "2026-05-15", "progress": 100.0, "status": "Green", "bac": 500000, "ac": 456000, "plannedHours": 500.0, "actualHours": 480.0},
                    {"task": "2.0 Hull Welding & Assembly", "plannedStart": "2026-05-01", "plannedFinish": "2026-08-31", "actualStart": "2026-05-01", "actualFinish": "2026-08-31", "progress": 60.0, "status": "Green", "bac": 1500000, "ac": 1020000, "plannedHours": 2000.0, "actualHours": 1100.0}
                ],
                'PRJ-005': [
                    {"task": "1.0 Project Control & PM", "plannedStart": "2026-02-01", "plannedFinish": "2026-07-31", "actualStart": "2026-02-01", "actualFinish": "2026-07-31", "progress": 100.0, "status": "Green", "bac": 200000, "ac": 187000, "plannedHours": 250.0, "actualHours": 220.0},
                    {"task": "2.0 Pontoon Assembly & Painting", "plannedStart": "2026-03-01", "plannedFinish": "2026-07-15", "actualStart": "2026-03-01", "actualFinish": "2026-07-20", "progress": 87.5, "status": "Green", "bac": 800000, "ac": 740000, "plannedHours": 1000.0, "actualHours": 800.0}
                ],
                'PRJ-006': [
                    {"task": "1.0 Hatch Engineering & FEA", "plannedStart": "2025-10-01", "plannedFinish": "2025-12-15", "actualStart": "2025-10-01", "actualFinish": "2025-12-10", "progress": 100.0, "status": "Green", "bac": 200000, "ac": 180500, "plannedHours": 200.0, "actualHours": 190.0},
                    {"task": "2.0 Molding & Testing", "plannedStart": "2025-12-01", "plannedFinish": "2026-03-31", "actualStart": "2025-12-01", "actualFinish": "2026-03-25", "progress": 100.0, "status": "Green", "bac": 400000, "ac": 406000, "plannedHours": 500.0, "actualHours": 480.0}
                ]
            }
            
            tasks = gantt_data_dict[gantt_proj]
            gantt_fig = go.Figure()
            
            for t in reversed(tasks):
                p_duration = (pd.to_datetime(t["plannedFinish"]) - pd.to_datetime(t["plannedStart"])).days
                a_duration = (pd.to_datetime(t["actualFinish"]) - pd.to_datetime(t["actualStart"])).days
                
                # Planned bar
                gantt_fig.add_trace(go.Bar(
                    name="Planned Baseline",
                    y=[t["task"]],
                    x=[p_duration],
                    base=t["plannedStart"],
                    orientation="h",
                    marker=dict(color="#cbd5e1"),
                    width=0.25,
                    hoverinfo="text",
                    text=f"Planned: {t['plannedStart']} to {t['plannedFinish']}"
                ))
                
                if gantt_metric == "Schedule":
                    actual_label = f"{t['progress']:.1f}%"
                    actual_color = "#e74c3c" if t["status"] == "Red" else "#2c3e50"
                elif gantt_metric == "Cost":
                    diff = t["ac"] - t["bac"]
                    if diff > 0:
                        actual_label = f"+{diff/1000:.1f}k USD Overrun"
                        actual_color = "#e74c3c"
                    else:
                        actual_label = f"-{abs(diff)/1000:.1f}k USD Under"
                        actual_color = "#2c3e50"
                elif gantt_metric == "Hours":
                    diff = t["actualHours"] - t["plannedHours"]
                    if diff > 0:
                        actual_label = f"+{diff:.1f}h Over"
                        actual_color = "#e74c3c"
                    else:
                        actual_label = f"{diff:.1f}h Under"
                        actual_color = "#2c3e50"
                        
                gantt_fig.add_trace(go.Bar(
                    name="Actual / Earned",
                    y=[t["task"]],
                    x=[a_duration],
                    base=t["actualStart"],
                    orientation="h",
                    marker=dict(color=actual_color),
                    width=0.4,
                    hoverinfo="text",
                    text=f"Actual: {t['actualStart']} to {t['actualFinish']} | {actual_label}"
                ))
                
            gantt_fig.update_layout(
                barmode="overlay",
                showlegend=False,
                plot_bgcolor="white",
                paper_bgcolor="white",
                xaxis=dict(
                    type="date", 
                    showgrid=False, 
                    linecolor="#e2e8f0"
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=12, family="Inter", color="#1a252f")
                ),
                margin=dict(l=10, r=10, t=10, b=10),
                height=80 + 50 * len(tasks)
            )
            
            st.plotly_chart(gantt_fig)
            
            # S-Curve Chart
            st.markdown("##### 📈 Cumulative Earned Value S-Curve (PRJ-001)")
            pv_dates = pd.date_range(start="2026-01-01", end="2026-06-30", freq="W")
            pv_values = []
            for d in pv_dates:
                val = 0
                val += min(300000.0, (d - pd.Timestamp("2026-01-01")).days / 181 * 300000.0)
                if d >= pd.Timestamp("2026-02-01"):
                    val += min(600000.0, (d - pd.Timestamp("2026-02-01")).days / 74 * 600000.0)
                if d >= pd.Timestamp("2026-04-01"):
                    val += min(400000.0, (d - pd.Timestamp("2026-04-01")).days / 61 * 400000.0)
                if d >= pd.Timestamp("2026-06-01"):
                    val += min(200000.0, (d - pd.Timestamp("2026-06-01")).days / 30 * 200000.0)
                pv_values.append(val)
                
            pv_df = pd.DataFrame({"Date": pv_dates, "PV_Cum": pv_values})
            progress_history_chart = prepare_progress_history_for_chart(progress_history)
            chart_df = pd.merge_asof(pv_df, progress_history_chart.rename(columns={"DateVal": "Date"}), on="Date", direction="backward")
            ev_clean = chart_df['EV_Val'].interpolate().fillna(0)
            
            fig = go.Figure()
            # PV Line
            fig.add_trace(go.Scatter(
                x=chart_df['Date'], y=chart_df['PV_Cum'],
                name="Planned Value (PV)",
                line=dict(color="#95a5a6", width=2, dash="dash"),
                mode="lines"
            ))
            # AC Line
            fig.add_trace(go.Scatter(
                x=chart_df['Date'], y=chart_df['AC_Cum'],
                name="Actual Cost (AC)",
                line=dict(color="#2c3e50", width=2.5),
                mode="lines"
            ))
            # EV Line
            fig.add_trace(go.Scatter(
                x=chart_df['Date'], y=ev_clean,
                name="Earned Value (EV)",
                line=dict(color="#2980b9", width=2.5),
                mode="lines"
            ))
            
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=40, r=80, t=20, b=40),
                xaxis=dict(showgrid=False, linecolor="#bdc3c7"),
                yaxis=dict(showgrid=True, gridcolor="#f2f2f2", linecolor="#bdc3c7", title="USD ($)", tickformat="$,.0f"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            # Direct Labels
            fig.add_annotation(x=chart_df['Date'].iloc[-1], y=chart_df['PV_Cum'].iloc[-1], text="PV", showarrow=False, xshift=15, font=dict(color="#95a5a6"))
            fig.add_annotation(x=chart_df['Date'].iloc[-1], y=chart_df['AC_Cum'].iloc[-1], text="AC", showarrow=False, xshift=15, font=dict(color="#2c3e50"))
            fig.add_annotation(x=chart_df['Date'].iloc[-1], y=ev_clean.iloc[-1], text="EV", showarrow=False, xshift=15, font=dict(color="#2980b9"))
            
            st.plotly_chart(fig)

        # TAB 2: CFO
        with tab_cfo:
            st.markdown("### CFO & Profitability Audit")
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.markdown("#### Audit Ratios & Spent")
                cfo_df = pd.DataFrame([
                    {"Audit Indicator": "Projected Margin Variance (VAC)", "Value / Metric": "-359,559 USD", "Status": "Macro Risk"},
                    {"Audit Indicator": "Typical Estimate at Completion (EAC)", "Value / Metric": "1,859,559 USD", "Status": "Forecasted"},
                    {"Audit Indicator": "Labor Costs Allocation", "Value / Metric": "1,326,810 USD", "Status": "71.8% Share"},
                    {"Audit Indicator": "Materials & Procurement Costs", "Value / Metric": "522,000 USD", "Status": "28.2% Share"}
                ])
                st.dataframe(cfo_df, hide_index=True)
                
            with col_right:
                # Doughnut chart of spent
                fig_doughnut = go.Figure(data=[go.Pie(
                    labels=['Labor (71.8%)', 'Materials (28.2%)'],
                    values=[1326810, 522000],
                    hole=.7,
                    marker=dict(colors=['#2c3e50', '#95a5a6'])
                )])
                fig_doughnut.update_layout(
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig_doughnut)

        # TAB 3: Contract & Risk Audit
        with tab_contract:
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("#### 🚨 Overtime Anomaly Audit (>45 hrs/week)")
                st.dataframe(overtime, hide_index=True)
                
            with col_right:
                st.markdown("#### 💳 Large Procurement Audit (>50,000 USD)")
                large_materials = build_material_audit_table(materials)
                st.dataframe(large_materials, hide_index=True)
                
            st.markdown("#### 📋 Active RAID Log Register")
            st.dataframe(raid, hide_index=True)

        # TAB 4: Production & Assembly
        with tab_production:
            st.markdown("### Structural Assembly Progress & Physical Milestones")
            prod_df = pd.DataFrame([
                {"WBS Code": "1.0", "Structural Element": "Project Management & Engineering", "Physical Progress": "97.5%", "Status": "Design Verification Phase"},
                {"WBS Code": "2.0", "Structural Element": "Hull Fabrication & Assembly", "Physical Progress": "100.0%", "Status": "Structural Assembly Certified"},
                {"WBS Code": "3.0", "Structural Element": "Outfitting & Integration", "Physical Progress": "100.0%", "Status": "System Integration Complete"},
                {"WBS Code": "4.0", "Structural Element": "Sea Trials & Handover", "Physical Progress": "100.0%", "Status": "Maritime Readiness Verified"}
            ])
            st.dataframe(prod_df, hide_index=True)

        # TAB 5: Recommendations & Simulator
        with tab_rec:
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("#### 📋 Active Corrective Action Items")
                
                st.error("""
                **🔴 Audit Materials & Labor Rates (WBS 1.0 & 3.0 on PRJ-001)**  
                * **Priority**: Critical  
                * **Reason**: Cost overrun of 119k USD in PM & Eng and 140k USD in Outfitting on project PRJ-001, caused by rising contractor rates and design variations.  
                * **Action**: Renegotiate contractor rates, freeze non-essential variation orders (VOs), and restrict scope expansion.
                """)
                
                st.warning("""
                **🟡 Yard Resource Optimization (WBS 2.0)**  
                * **Priority**: Medium  
                * **Reason**: Fabricated 10 days early but slightly exceeded BAC.  
                * **Action**: Shift excess structural labor to delayed outfitting tasks to optimize yard-wide capacity.
                """)
                
                st.error("""
                **🔴 Accelerate Sea Trials Handover (WBS 4.0)**  
                * **Priority**: High  
                * **Reason**: Sea trials schedule slipped by 10 days.  
                * **Action**: Enforce double-shift schedules for final testing, pre-commissioning checkouts, and DNV witness surveys.
                """)
                
            with col_right:
                st.markdown("#### 🎛️ What-If Corrective Simulator")
                st.caption("Simulate the financial impact of implementing corrective controlling actions in real time:")
                
                labor_save = st.slider("Simulated Labor Savings (%)", min_value=0, max_value=30, value=0)
                mat_save = st.slider("Simulated Material Savings (%)", min_value=0, max_value=30, value=0)
                crash_trials = st.selectbox(
                    "Crash WBS 4.0 Schedule (Add Overtime Shifts)",
                    ["No (Normal)", "Yes (5% extra cost, 5 days saved)", "Yes (10% extra cost, 10 days saved)"]
                )
                
                # Math from index.html
                original_bac = 1500000.0
                original_ac = 1848810.0
                original_ev = 1492500.0
                
                crash_pct = 0.0
                if "5%" in crash_trials:
                    crash_pct = 0.05
                elif "10%" in crash_trials:
                    crash_pct = 0.10
                    
                sim_ac = original_ac * (1 - (labor_save / 100) * 0.7 - (mat_save / 100) * 0.3)
                sim_ac += 200000 * crash_pct
                
                sim_cpi = original_ev / sim_ac if sim_ac > 0 else 0.81
                sim_eac = original_bac / sim_cpi if sim_cpi > 0 else 1859559
                
                st.markdown("##### 📊 Simulated Results")
                st.metric("Simulated CPI", f"{sim_cpi:.2f}")
                st.metric("Simulated EAC", f"{sim_eac:,.0f} USD")

        # TAB 6: Glossary
        with tab_glossary:
            st.markdown("### Earned Value Management (EVM) Glossary")
            glossary_df = pd.DataFrame([
                {"Term / KPI": "BAC (Budget at Completion)", "Equation": "Baseline Budget", "Description": "The total authorized budget for the project's scope of work."},
                {"Term / KPI": "PV (Planned Value)", "Equation": "BCWS", "Description": "The authorized budget planned for work scheduled to be completed."},
                {"Term / KPI": "EV (Earned Value)", "Equation": "BCWP", "Description": "The measure of work performed expressed in terms of the budget authorized for that work."},
                {"Term / KPI": "AC (Actual Cost)", "Equation": "ACWP", "Description": "The total cost actually incurred for work performed."},
                {"Term / KPI": "CPI (Cost Performance Index)", "Equation": "EV / AC", "Description": "A measure of cost efficiency. Values < 1.0 indicate overrun."},
                {"Term / KPI": "SPI (Schedule Performance Index)", "Equation": "EV / PV", "Description": "A measure of schedule efficiency. Values < 1.0 indicate delay."},
                {"Term / KPI": "EAC Typical", "Equation": "BAC / CPI", "Description": "Forecasted final cost assuming current cost performance trends persist."},
                {"Term / KPI": "EAC Atypical", "Equation": "AC + (BAC - EV)", "Description": "Forecasted final cost assuming remaining work will be done at the planned rate."}
            ])
            st.dataframe(glossary_df, hide_index=True)

    elif nav_choice == "👥 Stakeholder Reports":
        st.title("Stakeholder Reports")
        
        persona = st.selectbox(
            "Select Stakeholder Persona:",
            [
                "👑 Executive Steering Committee (CFO & Board)",
                "🎯 Project Manager (Operational Control & Schedule)",
                "📐 Engineering Lead (Design & Technical Hours)",
                "🏗️ Yard & Production Manager (Shop-Floor & Assembly)",
                "📦 Procurement & Supply Chain Manager",
                "🛡️ Quality & Class Inspector (DNV Certification)"
            ]
        )
        
        if "Executive" in persona:
            st.markdown("### Steering Committee & Board Brief")
            st.info("Focuses on high-level financial risk, capital exposure, projected margin at completion, and macro cost drivers.")
            
            cols = st.columns(4)
            cols[0].metric("Baseline Budget (BAC)", "1,500,000 USD")
            cols[1].metric("Projected Total Cost (EAC)", "1,859,559 USD")
            cols[2].metric("Projected Overrun (VAC)", "-359,559 USD", "-24.0% Overrun")
            cols[3].metric("Portfolio Risk Exposure", "HIGH", "3 Active RAID Risks")
            
            st.markdown("""
            #### Financial Performance Summary
            * **Project Cost Variance**: Net loss variance of **-356,310 USD** across the 1.5M USD baseline budget.
            * **Cost Performance Index (CPI)**: Currently at **0.81**, indicating that for every 1.00 USD spent, the project generates only 0.81 USD of value.
            * **Capital Allocation Breakdown**: Labor: 1,326,810 USD (71.8%) | Materials: 522,000 USD (28.2%)
            * **Mitigation Action**: Freeze all unapproved variation requests.
            """)
            
        elif "Project Manager" in persona:
            st.markdown("### Project Manager Operational Brief")
            st.info("Focuses on Earned Value status, critical path progress, resource allocation, and active RAID log items.")
            
            cols = st.columns(4)
            cols[0].metric("Overall Progress", "99.5%")
            cols[1].metric("Earned Value (EV)", "1,492,500 USD")
            cols[2].metric("Schedule Variance", "ON SCHEDULE")
            cols[3].metric("WBS Status", "1 On Track / 3 Over Budget")
            
        elif "Engineering" in persona:
            st.markdown("### Engineering Lead Technical Report")
            st.info("Focuses on WBS 1.0 (Project Management & Engineering), engineering hours burn rate, and drawing releases.")
            
            cols = st.columns(3)
            cols[0].metric("WBS 1.0 Budget (BAC)", "300,000 USD")
            cols[1].metric("Actual Engineering Cost", "419,230 USD")
            cols[2].metric("Design Progress", "97.5%")
            
            st.markdown("""
            #### Engineering Hours Burn Rate
            """)
            eng_df = pd.DataFrame([
                {"Resource": "Erik Johansen", "Role": "Senior Design Engineer", "Hours Logged": "312.0 hrs", "Total Cost": "296,400 USD"},
                {"Resource": "Frank Ellingsen", "Role": "Project Controller", "Hours Logged": "86.0 hrs", "Total Cost": "73,100 USD"},
                {"Resource": "Morten Hansen", "Role": "Project Manager", "Hours Logged": "49.7 hrs", "Total Cost": "49,700 USD"}
            ])
            st.dataframe(eng_df, hide_index=True)
            
        elif "Yard" in persona:
            st.markdown("### Yard & Production Manager Shop-Floor Report")
            st.info("Focuses on WBS 2.0 (Hull Assembly) & WBS 3.0 (Outfitting), welder/electrician labor hours, and overtime compliance.")
            
            cols = st.columns(3)
            cols[0].metric("Hull Fabrication Progress", "100.0%")
            cols[1].metric("Outfitting Progress", "100.0%")
            cols[2].metric("Overtime Incidents (>45h)", len(overtime))
            
            st.markdown("#### Shop-Floor Overtime Alerts")
            st.dataframe(overtime, hide_index=True)
            
        elif "Procurement" in persona:
            st.markdown("### Procurement & Supply Chain Report")
            st.info("Focuses on material purchases, supplier lead times, committed costs, and invoice audits.")
            
            cols = st.columns(2)
            cols[0].metric("Total Material Spend", "522,000 USD")
            cols[1].metric("Major Purchases (>50k USD)", len(materials[materials["TotalActualCost"] > 50000]))
            
            st.markdown("#### Material Purchases Breakdown")
            st.dataframe(materials, hide_index=True)
            
        elif "Quality" in persona:
            st.markdown("### Quality & Class Inspector Brief")
            st.info("Focuses on inspection pass rates, non-conformities (NCRs), milestone completion, and Sea Trials readiness.")
            
            cols = st.columns(3)
            cols[0].metric("Sea Trials Progress", "100.0%")
            cols[1].metric("Class Inspection Pass Rate", "100.0%")
            cols[2].metric("Open NCRs", "0 Critical")
            
            st.markdown("""
            #### DNV Milestone Verification
            * **WBS 2.0 Hull Structural Certification**: Fully passed non-destructive testing (NDT) on composite carbon welds.
            * **WBS 3.0 Systems Outfitting**: Electrical and inboard engine installation passed maritime safety compliance audits.
            * **WBS 4.0 Sea Trials & Handover**: Sea trials completed under supervision; final certificate ready for sign-off.
            """)

    elif nav_choice == "⚙️ Skill Inspector":
        st.title("⚙️ Skill Inspector")
        st.caption("Audit agent skill definitions and instructions loaded from project configurations.")
        
        # Load all skills dynamically
        if os.path.exists(SKILLS_DIR):
            skills = [s for s in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, s))]
            selected_skill = st.selectbox("Focus Agent Skill", skills)
            
            skill_md_path = os.path.join(SKILLS_DIR, selected_skill, "SKILL.md")
            if os.path.exists(skill_md_path):
                st.markdown(load_markdown_text(skill_md_path))
            else:
                st.warning("SKILL.md not found in this skill directory.")
        else:
            st.warning("Skills directory not found.")

    elif nav_choice == "🤖 Live Crew Execution":
        st.title("🤖 Multi-Agent Crew Audit Console")
        st.caption("Simulates active auditing from the project controller, CFO, contract, and production agents.")
        
        if st.button("🚀 Run All 4 Agent Audits"):
            st.code("""
[SYSTEM] Initializing Agent Control Crew...
[CONTROLLER AGENT] Connecting to DuckDB database: Data/DuckDB/project_controlling.db
[CONTROLLER AGENT] Calculating EVM metrics for PRJ-001 (Composite Vessel)...
[CONTROLLER AGENT] WARNING: Project CPI is 0.81 (Threshold: 0.95). Cost overrun detected.
[CONTROLLER AGENT] WBS 1.0 (PM & Engineering) CPI is 0.70 (BAC: 300,000 | AC: 419,230)
[CONTROLLER AGENT] WBS 3.0 (Outfitting & Integration) CPI is 0.74 (BAC: 400,000 | AC: 540,445)
[CONTROLLER AGENT] WBS 4.0 (Sea Trials) CPI is 0.74 (BAC: 200,000 | AC: 268,685)
[CFO AGENT] Auditing labor and material cost allocations...
[CFO AGENT] Total Project Cost: 1,848,810 USD.
[CFO AGENT] Labor: 1,326,810 USD (71.8%) | Materials: 522,000 USD (28.2%)
[CONTRACT AGENT] Querying SQLite project_controlling.db for RAID Log issues...
[CONTRACT AGENT] Active Risks found: 3 active, 1 closed. RiskIDs: R-001, I-001, D-001
[PRODUCTION AGENT] Auditing timesheets and shipyard logs for overtime exceptions...
[PRODUCTION AGENT] ALERT: Astrid Nilsen (Structural Welder) exceeded 45 hrs/week in weeks 2026-06, 2026-07, 2026-08.
[SYSTEM] Audit complete. Generated 4 variance reports and 1 compliance memo.
            """, language="bash")
        else:
            st.info("Console idle. Click button to begin audit execution loop...")
