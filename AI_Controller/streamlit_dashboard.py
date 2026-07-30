import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import os

# Set page config
st.set_page_config(page_title="Project controlling Dashboard", layout="wide")

# Custom CSS to enforce Tufte's principles (Erase card shadows, borders, standard gray themes)
st.markdown("""
    <style>
    /* Clean background and fonts */
    html, body, [class*="View"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove borders/shadows from cards */
    div[data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }
    
    /* Mute metrics labels */
    div[data-testid="stMetricLabel"] > div {
        color: #7f8c8d !important;
        font-size: 11px !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Large clean typography for numbers */
    div[data-testid="stMetricValue"] > div {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
    }
    
    /* Hide default Streamlit decoration */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Define DB path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")

@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        return None, None, None
    con = duckdb.connect(DB_PATH)
    
    # 1. Project Summary
    summary = con.execute("SELECT * FROM v_project_evm_summary").df().iloc[0]
    
    # 2. WBS Table
    wbs = con.execute("SELECT WBS_Code, ElementName, BAC, AC, EV, CPI, PercentComplete, EAC_Typical FROM v_wbs_evm_metrics ORDER BY WBS_Code").df()
    
    # 3. Time Series for S-Curve
    # Fetch cumulative AC (labor + material) and EV over time
    progress_history = con.execute("""
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
            -- For EV, we fetch the latest progress value
            EV_Val
        FROM dates_filled
        ORDER BY DateVal
    """).df()
    
    con.close()
    return summary, wbs, progress_history

summary, wbs, time_data = load_data()

if summary is None:
    st.error("Project database not found. Please run `python AI_Controller/build_duckdb.py` first.")
else:
    st.title("Project Controlling Workspace")
    st.caption("Composite Maritime Vessel Construction (PRJ-001) Dashboard")
    
    # --- Top Row: Tufte-Style KPI Cards ---
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Budget at Completion", value=f"{summary['Total_BAC']:,.0f} NOK")
    with col2:
        st.metric(label="Actual Cost (AC)", value=f"{summary['Total_AC']:,.0f} NOK")
    with col3:
        st.metric(label="Earned Value (EV)", value=f"{summary['Total_EV']:,.0f} NOK")
    with col4:
        # Highlight CPI variance if < 0.95 (unfavorable)
        cpi = summary['Project_CPI']
        cpi_color = "red" if cpi < 0.95 else "green"
        st.metric(label="Project CPI", value=f"{cpi:.2f}")
    with col5:
        st.metric(label="Overall Progress", value=f"{summary['Overall_Progress_Pct']:.1f}%")
        
    st.write("---")
    
    # --- Main Section: S-Curve & WBS Performance ---
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("Performance S-Curve (Cumulative PV, EV, AC)")
        
        # Build synthetic PV line for visualization (weekly interpolation)
        pv_dates = pd.date_range(start="2026-01-01", end="2026-06-30", freq="W")
        # WBS plans: WBS-001 (300k, 6 months), WBS-002 (600k, Feb-Apr), WBS-003 (400k, Apr-May), WBS-004 (200k, Jun)
        pv_values = []
        for d in pv_dates:
            val = 0
            # WBS-001: 300k over 181 days
            val += min(300000.0, (d - pd.Timestamp("2026-01-01")).days / 181 * 300000.0)
            # WBS-002: Feb 1 to Apr 15 (74 days)
            if d >= pd.Timestamp("2026-02-01"):
                val += min(600000.0, (d - pd.Timestamp("2026-02-01")).days / 74 * 600000.0)
            # WBS-003: Apr 1 to May 31 (61 days)
            if d >= pd.Timestamp("2026-04-01"):
                val += min(400000.0, (d - pd.Timestamp("2026-04-01")).days / 61 * 400000.0)
            # WBS-004: Jun 1 to Jun 30 (30 days)
            if d >= pd.Timestamp("2026-06-01"):
                val += min(200000.0, (d - pd.Timestamp("2026-06-01")).days / 30 * 200000.0)
            pv_values.append(val)
            
        pv_df = pd.DataFrame({"Date": pv_dates, "PV_Cum": pv_values})
        
        # Format time_data for plotting
        time_data['DateVal'] = pd.to_datetime(time_data['DateVal'])
        
        # Merge time_data with cumulative progress
        chart_df = pd.merge_asof(pv_df, time_data.rename(columns={"DateVal": "Date"}), on="Date", direction="backward")
        chart_df['EV_Cum'] = chart_df['EV_Val'] # In a real system, we accumulate progress values or fetch cumulative EV.
        # Since EV is cumulative BAC * %Complete of active WBS elements:
        # WBS-002 is 100% complete (600k), WBS-003 is 100% complete (400k), WBS-004 is 100% complete (200k), WBS-001 is 97.5% complete (292.5k)
        # We can construct a cleaner cumulative EV by multiplying current date WBS progress by BAC.
        # For simplicity, we interpolate cumulative EV using the DB physical_progress logs.
        
        # Plotly chart using Edward Tufte principles:
        # - Dash/gray for PV, solid blue for EV, solid black for AC
        # - No vertical gridlines
        # - Direct labeling at the end of the curves
        fig = go.Figure()
        
        # Planned Value (PV)
        fig.add_trace(go.Scatter(
            x=chart_df['Date'], y=chart_df['PV_Cum'],
            name="Planned Value (PV)",
            line=dict(color="#95a5a6", width=2, dash="dash"),
            mode="lines"
        ))
        
        # Actual Cost (AC)
        fig.add_trace(go.Scatter(
            x=chart_df['Date'], y=chart_df['AC_Cum'],
            name="Actual Cost (AC)",
            line=dict(color="#2c3e50", width=2.5),
            mode="lines"
        ))
        
        # Earned Value (EV) - Interpolate to fill gaps
        ev_clean = chart_df['EV_Val'].interpolate().fillna(0)
        fig.add_trace(go.Scatter(
            x=chart_df['Date'], y=ev_clean,
            name="Earned Value (EV)",
            line=dict(color="#2980b9", width=2.5),
            mode="lines"
        ))
        
        # Style layout
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=40, r=80, t=20, b=40),
            xaxis=dict(
                showgrid=False,
                linecolor="#bdc3c7",
                ticks="outside"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#f2f2f2",
                linecolor="#bdc3c7",
                title="NOK (in Thousands)",
                tickformat=",.0f"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Annotations for Direct Labeling (Tufte style)
        fig.add_annotation(x=chart_df['Date'].iloc[-1], y=chart_df['PV_Cum'].iloc[-1], text="PV", showarrow=False, xshift=15, font=dict(color="#95a5a6"))
        fig.add_annotation(x=chart_df['Date'].iloc[-1], y=chart_df['AC_Cum'].iloc[-1], text="AC", showarrow=False, xshift=15, font=dict(color="#2c3e50"))
        fig.add_annotation(x=chart_df['Date'].iloc[-1], y=ev_clean.iloc[-1], text="EV", showarrow=False, xshift=15, font=dict(color="#2980b9"))
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.subheader("Performance Anomalies & Variance")
        # Calculate CV
        tot_cv = summary['Total_CV']
        tot_vac = summary['Total_VAC']
        
        if tot_cv < 0:
            st.error(f"**Current Cost Variance (CV):** {tot_cv:+,.2f} NOK (Over Budget)")
        else:
            st.success(f"**Current Cost Variance (CV):** {tot_cv:+,.2f} NOK (Under Budget)")
            
        if tot_vac < 0:
            st.warning(f"**Projected Variance at Completion (VAC):** {tot_vac:+,.2f} NOK (Typical EAC)")
        else:
            st.info(f"**Projected Variance at Completion (VAC):** {tot_vac:+,.2f} NOK")
            
        # Quick table showing WBS Status (Highlighting red for low CPI)
        st.write("WBS Health Status:")
        wbs_disp = wbs.copy()
        wbs_disp['PercentComplete'] = (wbs_disp['PercentComplete'] * 100).map("{:.1f}%".format)
        wbs_disp['CPI'] = wbs_disp['CPI'].map("{:.2f}".format)
        wbs_disp['BAC'] = wbs_disp['BAC'].map("{:,.0f}".format)
        wbs_disp['AC'] = wbs_disp['AC'].map("{:,.0f}".format)
        
        st.dataframe(
            wbs_disp[['WBS_Code', 'ElementName', 'BAC', 'AC', 'CPI', 'PercentComplete']],
            hide_index=True,
            use_container_width=True
        )

    # --- Lower Row: Resource Allocation Analysis ---
    st.write("---")
    st.subheader("Resource Allocation & Utilization (Tufte Style Histogram)")
    
    con = duckdb.connect(DB_PATH)
    res_load = con.execute("""
        SELECT r.ResourceName, SUM(t.HoursWorked) as ActualHours, COALESCE(SUM(a.AllocatedHours), 0) as PlannedHours
        FROM resources r
        LEFT JOIN timesheets t ON r.ResourceID = t.ResourceID
        LEFT JOIN resource_assignments a ON r.ResourceID = a.ResourceID
        GROUP BY r.ResourceName
    """).df()
    con.close()
    
    # Render clean comparison bar chart
    fig_res = go.Figure()
    fig_res.add_trace(go.Bar(
        x=res_load['ResourceName'], y=res_load['PlannedHours'],
        name="Planned Allocation (Hours)",
        marker_color="#bdc3c7"
    ))
    fig_res.add_trace(go.Bar(
        x=res_load['ResourceName'], y=res_load['ActualHours'],
        name="Actual Logged (Hours)",
        marker_color="#2c3e50"
    ))
    fig_res.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f2f2f2", title="Hours"),
        bgroupmode="group"
    )
    st.plotly_chart(fig_res, use_container_width=True)
