import os
import duckdb

# Define database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")

# Color constants for terminal highlighting (muted)
RED = "\033[91m"
RESET = "\033[0m"
AMBER = "\033[93m"

def format_cell(val, alignment, width, is_num=False, is_cpi=False):
    """Formats cell with alignment, widths and decimal positioning."""
    if val is None:
        return "N/A".rjust(width) if is_num else "N/A".ljust(width)
        
    if is_num:
        if is_cpi:
            text = f"{val:.2f}"
        else:
            text = f"{val:,.2f}"
        return text.rjust(width)
    else:
        text = str(val)
        if len(text) > width:
            text = text[:width-3] + "..."
        return text.ljust(width)

def print_tufte_dashboard():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Please run build_duckdb.py first.")
        return

    con = duckdb.connect(DB_PATH)
    try:
        # 1. Fetch WBS levels EVM Metrics
        wbs_data = con.execute("""
            SELECT WBS_Code, ElementName, BAC, AC, EV, CPI, PercentComplete, EAC_Typical 
            FROM v_wbs_evm_metrics
            ORDER BY WBS_Code
        """).fetchall()

        # 2. Fetch Project Summary
        summary = con.execute("SELECT Total_BAC, Total_AC, Total_EV, Total_CV, Project_CPI, Total_EAC_Typical, Total_VAC, Overall_Progress_Pct FROM v_project_evm_summary").fetchone()
        
        # 3. Print Title
        print("\n" + "=" * 98)
        print(" PROJECT CONTROLLING PERFORMANCE DASHBOARD (TUFTE-STYLE)")
        print("=" * 98)
        print("\nEVM Performance Matrix by WBS Element:")
        print("-" * 98)
        print(f"{'WBS':<6} | {'WBS Element Name':<28} | {'BAC (USD)':>12} | {'AC (USD)':>12} | {'EV (USD)':>12} | {'EAC (USD)':>12} | {'CPI':>5} | {'Status'}")
        print("-" * 98)
        
        for row in wbs_data:
            wbs_code, name, bac, ac, ev, cpi, pct, eac = row
            
            # Determine status and color highlighting
            status = "ON TRACK"
            color_start = ""
            color_end = ""
            if cpi < 0.95:
                status = "OVER BUDGET"
                color_start = RED
                color_end = RESET
            elif cpi > 1.05:
                status = "UNDER BUDGET"
                
            wbs_str = format_cell(wbs_code, "left", 6)
            name_str = format_cell(name, "left", 28)
            bac_str = format_cell(bac, "right", 12, is_num=True)
            ac_str = format_cell(ac, "right", 12, is_num=True)
            ev_str = format_cell(ev, "right", 12, is_num=True)
            eac_str = format_cell(eac, "right", 12, is_num=True)
            cpi_str = format_cell(cpi, "right", 5, is_num=True, is_cpi=True)
            
            print(f"{wbs_str} | {name_str} | {bac_str} | {ac_str} | {ev_str} | {eac_str} | {color_start}{cpi_str}{color_end} | {color_start}{status}{color_end}")

        print("-" * 98)
        
        # Project Summary Row
        tot_bac, tot_ac, tot_ev, tot_cv, proj_cpi, tot_eac, tot_vac, overall_pct = summary
        
        color_summary_start = ""
        color_summary_end = ""
        if proj_cpi < 0.95:
            color_summary_start = RED
            color_summary_end = RESET
            
        tot_bac_str = format_cell(tot_bac, "right", 12, is_num=True)
        tot_ac_str = format_cell(tot_ac, "right", 12, is_num=True)
        tot_ev_str = format_cell(tot_ev, "right", 12, is_num=True)
        tot_eac_str = format_cell(tot_eac, "right", 12, is_num=True)
        proj_cpi_str = format_cell(proj_cpi, "right", 5, is_num=True, is_cpi=True)
        
        print(f"{'TOTAL':<6} | {'Project Vessel Summary':<28} | {tot_bac_str} | {tot_ac_str} | {tot_ev_str} | {tot_eac_str} | {color_summary_start}{proj_cpi_str}{color_summary_end} |")
        print("-" * 98)
        
        # Bottom KPI Summary (Tufte style: large indicators, clear labels, minimal ink)
        print(f"\nProject Cost Variance (CV): {tot_cv:+,.2f} USD")
        print(f"Projected Variance at Completion (VAC): {tot_vac:+,.2f} USD (Typical EAC)")
        print(f"Overall Physical Progress: {overall_pct:.1f}%\n")
        
        # Additional analytical insight (Top resource consumers & Material overruns)
        print("Top Resource Cost Consumers (Timesheet Analysis, USD):")
        print("-" * 60)
        top_resources = con.execute("""
            SELECT r.ResourceName, r.Role, SUM(t.HoursWorked) as TotalHours, SUM(t.HoursWorked * r.HourlyRate) as TotalCost
            FROM timesheets t
            JOIN resources r ON t.ResourceID = r.ResourceID
            GROUP BY r.ResourceName, r.Role
            ORDER BY TotalCost DESC
            LIMIT 3
        """).fetchall()
        
        for rname, role, hours, cost in top_resources:
            print(f"  {rname:<20} ({role:<20}): {hours:>5.1f} hrs  |  {cost:>11,.2f} USD")
        print("-" * 60)
    finally:
        con.close()

if __name__ == "__main__":
    print_tufte_dashboard()
