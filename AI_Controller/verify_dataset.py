import os
import csv

# Directory references
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "Data", "CSV")

def load_csv(filename):
    filepath = os.path.join(CSV_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# Load data
projects = load_csv("projects.csv")
wbs_elements = load_csv("wbs_elements.csv")
resources = load_csv("resources.csv")
assignments = load_csv("resource_assignments.csv")
timesheets = load_csv("timesheets.csv")
material_costs = load_csv("material_costs.csv")
physical_progress = load_csv("physical_progress.csv")

print("--- DATASET VERIFICATION (MEMORY-JOINED) ---")
print(f"Projects: {len(projects)}")
print(f"WBS Elements: {len(wbs_elements)}")
print(f"Resources: {len(resources)}")
print(f"Timesheet Logs: {len(timesheets)}")
print(f"Material Purchase Records: {len(material_costs)}")
print(f"Physical Progress Logs: {len(physical_progress)}")
print("--------------------------------------------\n")

# Map resource hourly rates for calculation
rates = {r["ResourceID"]: float(r["HourlyRate"]) for r in resources}

# Join and calculate Actual Costs (AC) per WBS Element
actual_costs_by_wbs = {}
labor_hours_by_wbs = {}

# Labor Actual Cost = HoursWorked * HourlyRate
for ts in timesheets:
    wbs_id = ts["WBS_ID"]
    res_id = ts["ResourceID"]
    hours = float(ts["HoursWorked"])
    rate = rates.get(res_id, 0.0)
    cost = hours * rate
    
    actual_costs_by_wbs[wbs_id] = actual_costs_by_wbs.get(wbs_id, 0.0) + cost
    labor_hours_by_wbs[wbs_id] = labor_hours_by_wbs.get(wbs_id, 0.0) + hours

# Material Actual Cost = TotalActualCost
for mat in material_costs:
    wbs_id = mat["WBS_ID"]
    cost = float(mat["TotalActualCost"])
    actual_costs_by_wbs[wbs_id] = actual_costs_by_wbs.get(wbs_id, 0.0) + cost

# Get the latest physical progress (PercentComplete) for each WBS Element
latest_progress = {}
for prg in physical_progress:
    wbs_id = prg["WBS_ID"]
    date_str = prg["RecordDate"]
    percent = float(prg["PercentComplete"])
    
    # If not recorded yet, or this date is later, update
    if wbs_id not in latest_progress or date_str > latest_progress[wbs_id]["Date"]:
        latest_progress[wbs_id] = {"Date": date_str, "Percent": percent}

# Print EVM Report by WBS Element
# Print EVM Report by WBS Element (reported in USD)
total_bac = 0.0
total_ac = 0.0
total_ev = 0.0

print(f"{'WBS':<8} | {'WBS Element Name':<30} | {'BAC (USD)':<12} | {'AC (USD)':<12} | {'EV (USD)':<12} | {'CPI':<6} | {'Status'}")
print("-" * 95)

for wbs in wbs_elements:
    wbs_id = wbs["WBS_ID"]
    name = wbs["ElementName"]
    bac = float(wbs["PlannedCost"])
    ac = actual_costs_by_wbs.get(wbs_id, 0.0)
    
    # Earned Value = BAC * Percent Complete
    progress_info = latest_progress.get(wbs_id, {"Percent": 0.0})
    percent_complete = progress_info["Percent"]
    ev = bac * percent_complete
    
    cpi = ev / ac if ac > 0 else 1.0
    
    total_bac += bac
    total_ac += ac
    total_ev += ev
    
    # Status evaluation
    status = "ON TRACK"
    if cpi < 0.95:
        status = "OVER BUDGET (WARN)"
    elif cpi > 1.05:
        status = "UNDER BUDGET (SAVING)"
        
    print(f"{wbs['WBS_Code']:<8} | {name:<30} | {bac:<11,.2f} USD | {ac:<11,.2f} USD | {ev:<11,.2f} USD | {cpi:<6.2f} | {status}")

# Project Summary
project_cpi = total_ev / total_ac if total_ac > 0 else 1.0
print("-" * 95)
print(f"{'PROJECT':<8} | {'Total Project Vessel':<30} | {total_bac:<11,.2f} USD | {total_ac:<11,.2f} USD | {total_ev:<11,.2f} USD | {project_cpi:<6.2f} |")
print("-" * 95)
print(f"Project Cost Variance (CV): {total_ev - total_ac:+,.2f} USD")
print(f"Overall Physical Progress: {total_ev / total_bac * 100:.1f}%")
print("\n")

# Verify against DuckDB database if available
try:
    import duckdb
    db_path = os.path.join(BASE_DIR, "Data", "DuckDB", "project_controlling.db")
    if os.path.exists(db_path):
        print("--- DUCKDB ANALYTICAL VIEW VERIFICATION ---")
        con = duckdb.connect(db_path)
        db_summary = con.execute("SELECT Total_BAC, Total_AC, Total_EV, Total_CV, Project_CPI, Overall_Progress_Pct FROM v_project_evm_summary").fetchone()
        
        db_bac, db_ac, db_ev, db_cv, db_cpi, db_progress = db_summary
        print(f"DuckDB Total BAC : {db_bac:,.2f} USD (Mismatch: {abs(db_bac - total_bac):.2f} USD)")
        print(f"DuckDB Total AC  : {db_ac:,.2f} USD (Mismatch: {abs(db_ac - total_ac):.2f} USD)")
        print(f"DuckDB Total EV  : {db_ev:,.2f} USD (Mismatch: {abs(db_ev - total_ev):.2f} USD)")
        print(f"DuckDB Total CV  : {db_cv:,.2f} USD (Mismatch: {abs(db_cv - (total_ev - total_ac)):.2f} USD)")
        print(f"DuckDB CPI       : {db_cpi:.2f} (Mismatch: {abs(db_cpi - project_cpi):.4f})")
        print(f"DuckDB Progress  : {db_progress:.1f}% (Mismatch: {abs(db_progress - (total_ev / total_bac * 100)):.2f}%)")
        print("-------------------------------------------")
        con.close()
    else:
        print("[Notice] DuckDB project_controlling.db database file not found. Run build_duckdb.py first to enable SQL verification.")
except ImportError:
    print("[Notice] duckdb python package not installed. SQL-based verification skipped.")
