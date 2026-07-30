import os
import csv
import random
from datetime import datetime, timedelta

# Create output folder
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "mock_data")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Set random seed for reproducibility
random.seed(42)

# Date Helper
def get_workdays(start_date, end_date):
    """Returns a list of datetime dates between start and end (excluding weekends)."""
    curr = start_date
    workdays = []
    while curr <= end_date:
        if curr.weekday() < 5:  # Monday to Friday
            workdays.append(curr)
        curr += timedelta(days=1)
    return workdays

# Project Timeline: 2026-01-01 to 2026-06-30
start_dt = datetime(2026, 1, 1)
end_dt = datetime(2026, 6, 30)

# 1. PROJECTS
projects = [
    {
        "ProjectID": "PRJ-001",
        "ProjectName": "Composite Maritime Vessel Construction",
        "ProjectManager": "Morten Hansen",
        "BudgetAtCompletion_BAC": 1500000.00,
        "StartDate": "2026-01-01",
        "EndDate": "2026-06-30",
        "Status": "Completed"
    }
]

# 2. WBS_ELEMENTS
wbs_elements = [
    {
        "WBS_ID": "WBS-001",
        "ProjectID": "PRJ-001",
        "WBS_Code": "1.0",
        "ElementName": "Project Management & Engineering",
        "PlannedCost": 300000.00,
        "PlannedHours": 400.0
    },
    {
        "WBS_ID": "WBS-002",
        "ProjectID": "PRJ-001",
        "WBS_Code": "2.0",
        "ElementName": "Hull Fabrication & Assembly",
        "PlannedCost": 600000.00,
        "PlannedHours": 1200.0
    },
    {
        "WBS_ID": "WBS-003",
        "ProjectID": "PRJ-001",
        "WBS_Code": "3.0",
        "ElementName": "Outfitting & Integration",
        "PlannedCost": 400000.00,
        "PlannedHours": 800.0
    },
    {
        "WBS_ID": "WBS-004",
        "ProjectID": "PRJ-001",
        "WBS_Code": "4.0",
        "ElementName": "Sea Trials & Handover",
        "PlannedCost": 200000.00,
        "PlannedHours": 300.0
    }
]

# 3. RESOURCES
resources = [
    {"ResourceID": "RES-001", "ResourceName": "Frank Ellingsen", "Role": "Project Controller", "HourlyRate": 850.00},
    {"ResourceID": "RES-002", "ResourceName": "Morten Hansen", "Role": "Project Manager", "HourlyRate": 1000.00},
    {"ResourceID": "RES-003", "ResourceName": "Erik Johansen", "Role": "Senior Design Engineer", "HourlyRate": 950.00},
    {"ResourceID": "RES-004", "ResourceName": "Astrid Nilsen", "Role": "Structural Welder", "HourlyRate": 700.00},
    {"ResourceID": "RES-005", "ResourceName": "Lars Olsen", "Role": "Marine Electrician", "HourlyRate": 750.00}
]

# 4. RESOURCE_ASSIGNMENTS
assignments = [
    # WBS-001 (PM & Eng)
    {"AssignmentID": "ASG-001", "WBS_ID": "WBS-001", "ResourceID": "RES-001", "AllocatedHours": 100.0},
    {"AssignmentID": "ASG-002", "WBS_ID": "WBS-001", "ResourceID": "RES-002", "AllocatedHours": 200.0},
    {"AssignmentID": "ASG-003", "WBS_ID": "WBS-001", "ResourceID": "RES-003", "AllocatedHours": 100.0},
    # WBS-002 (Hull Fabrication)
    {"AssignmentID": "ASG-004", "WBS_ID": "WBS-002", "ResourceID": "RES-004", "AllocatedHours": 1000.0},
    {"AssignmentID": "ASG-005", "WBS_ID": "WBS-002", "ResourceID": "RES-003", "AllocatedHours": 200.0},
    # WBS-003 (Outfitting)
    {"AssignmentID": "ASG-006", "WBS_ID": "WBS-003", "ResourceID": "RES-005", "AllocatedHours": 600.0},
    {"AssignmentID": "ASG-007", "WBS_ID": "WBS-003", "ResourceID": "RES-004", "AllocatedHours": 200.0},
    # WBS-004 (Sea Trials)
    {"AssignmentID": "ASG-008", "WBS_ID": "WBS-004", "ResourceID": "RES-002", "AllocatedHours": 100.0},
    {"AssignmentID": "ASG-009", "WBS_ID": "WBS-004", "ResourceID": "RES-005", "AllocatedHours": 150.0},
    {"AssignmentID": "ASG-010", "WBS_ID": "WBS-004", "ResourceID": "RES-001", "AllocatedHours": 50.0}
]

# 5. TIMESHEETS (Granular labor logs)
timesheets = []
timesheet_id_counter = 1

# Work schedule helper to generate realistic hours
# WBS-001: Run full project period (2026-01-01 to 2026-06-30)
wbs001_days = get_workdays(datetime(2026, 1, 1), datetime(2026, 6, 30))
# Frank (RES-001) logs ~4h/week (mostly on Fridays)
for d in wbs001_days:
    if d.weekday() == 4: # Friday
        h = round(random.uniform(3.5, 4.5), 1)
        timesheets.append({
            "TimesheetID": f"TS-{timesheet_id_counter:04d}",
            "ResourceID": "RES-001",
            "WBS_ID": "WBS-001",
            "WorkDate": d.strftime("%Y-%m-%d"),
            "HoursWorked": h,
            "ApprovalStatus": "Approved"
        })
        timesheet_id_counter += 1

# Morten (RES-002) logs ~8h/week (mostly on Mondays)
for d in wbs001_days:
    if d.weekday() == 0: # Monday
        h = round(random.uniform(7.5, 9.0), 1)
        timesheets.append({
            "TimesheetID": f"TS-{timesheet_id_counter:04d}",
            "ResourceID": "RES-002",
            "WBS_ID": "WBS-001",
            "WorkDate": d.strftime("%Y-%m-%d"),
            "HoursWorked": h,
            "ApprovalStatus": "Approved"
        })
        timesheet_id_counter += 1

# Erik (RES-003) logs early in design phase (Jan-Feb: ~15h/week, 3h/day)
wbs001_erik_days = get_workdays(datetime(2026, 1, 1), datetime(2026, 2, 28))
for d in wbs001_erik_days:
    h = round(random.uniform(2.5, 3.5), 1)
    timesheets.append({
        "TimesheetID": f"TS-{timesheet_id_counter:04d}",
        "ResourceID": "RES-003",
        "WBS_ID": "WBS-001",
        "WorkDate": d.strftime("%Y-%m-%d"),
        "HoursWorked": h,
        "ApprovalStatus": "Approved"
    })
    timesheet_id_counter += 1


# WBS-002 (Hull Fabrication): 2026-02-01 to 2026-04-15
# Welders (RES-004) log full-time (7.5-8.5 h/day)
# Note: To create an overrun, we will log slightly more hours than planned.
wbs002_days = get_workdays(datetime(2026, 2, 1), datetime(2026, 4, 15))
for d in wbs002_days:
    h = round(random.uniform(8.0, 9.0), 1) # Overrun: average is 8.5h
    timesheets.append({
        "TimesheetID": f"TS-{timesheet_id_counter:04d}",
        "ResourceID": "RES-004",
        "WBS_ID": "WBS-002",
        "WorkDate": d.strftime("%Y-%m-%d"),
        "HoursWorked": h,
        "ApprovalStatus": "Approved"
    })
    timesheet_id_counter += 1

# Design Engineer (RES-003) logs quality control hours on WBS-002 (2h/day)
for d in wbs002_days:
    if d.weekday() % 2 == 0: # Every other day
        h = round(random.uniform(1.5, 2.5), 1)
        timesheets.append({
            "TimesheetID": f"TS-{timesheet_id_counter:04d}",
            "ResourceID": "RES-003",
            "WBS_ID": "WBS-002",
            "WorkDate": d.strftime("%Y-%m-%d"),
            "HoursWorked": h,
            "ApprovalStatus": "Approved"
        })
        timesheet_id_counter += 1


# WBS-003 (Outfitting): 2026-04-01 to 2026-05-31
# Electrician (RES-005) logs 7.5-8.5 h/day
wbs003_days = get_workdays(datetime(2026, 4, 1), datetime(2026, 5, 31))
for d in wbs003_days:
    h = round(random.uniform(7.2, 8.2), 1) # Completes efficiently
    timesheets.append({
        "TimesheetID": f"TS-{timesheet_id_counter:04d}",
        "ResourceID": "RES-005",
        "WBS_ID": "WBS-003",
        "WorkDate": d.strftime("%Y-%m-%d"),
        "HoursWorked": h,
        "ApprovalStatus": "Approved"
    })
    timesheet_id_counter += 1

# Welder (RES-004) logs assembly hours on WBS-003 (~4h/day, alternate days)
for d in wbs003_days:
    if d.weekday() % 2 == 1:
        h = round(random.uniform(3.5, 4.5), 1)
        timesheets.append({
            "TimesheetID": f"TS-{timesheet_id_counter:04d}",
            "ResourceID": "RES-004",
            "WBS_ID": "WBS-003",
            "WorkDate": d.strftime("%Y-%m-%d"),
            "HoursWorked": h,
            "ApprovalStatus": "Approved"
        })
        timesheet_id_counter += 1


# WBS-004 (Sea Trials & Handover): 2026-06-01 to 2026-06-30
wbs004_days = get_workdays(datetime(2026, 6, 1), datetime(2026, 6, 30))
# Morten (RES-002) - PM oversight (4h/day)
for d in wbs004_days:
    h = round(random.uniform(3.5, 4.5), 1)
    timesheets.append({
        "TimesheetID": f"TS-{timesheet_id_counter:04d}",
        "ResourceID": "RES-002",
        "WBS_ID": "WBS-004",
        "WorkDate": d.strftime("%Y-%m-%d"),
        "HoursWorked": h,
        "ApprovalStatus": "Approved"
    })
    timesheet_id_counter += 1

# Electrician (RES-005) - Trials support (7.5h/day)
for d in wbs004_days:
    h = round(random.uniform(7.0, 8.0), 1)
    timesheets.append({
        "TimesheetID": f"TS-{timesheet_id_counter:04d}",
        "ResourceID": "RES-005",
        "WBS_ID": "WBS-004",
        "WorkDate": d.strftime("%Y-%m-%d"),
        "HoursWorked": h,
        "ApprovalStatus": "Approved"
    })
    timesheet_id_counter += 1

# Frank (RES-001) - Closeout auditing (3h/day on select days)
for d in wbs004_days:
    if d.weekday() in [1, 3]: # Tuesday & Thursday
        h = round(random.uniform(2.5, 3.5), 1)
        timesheets.append({
            "TimesheetID": f"TS-{timesheet_id_counter:04d}",
            "ResourceID": "RES-001",
            "WBS_ID": "WBS-004",
            "WorkDate": d.strftime("%Y-%m-%d"),
            "HoursWorked": h,
            "ApprovalStatus": "Approved"
        })
        timesheet_id_counter += 1


# 6. MATERIAL_COSTS
# Invoices associated with raw materials and components
material_costs = [
    # WBS-002 (Hull Fab: Composite fiber, epoxy resins, structural steel)
    {"PurchaseID": "INV-001", "WBS_ID": "WBS-002", "PurchaseDate": "2026-02-05", "Description": "Structural Composite Carbon Sheets", "Quantity": 10, "UnitPrice": 15000.00},
    {"PurchaseID": "INV-002", "WBS_ID": "WBS-002", "PurchaseDate": "2026-02-12", "Description": "Epoxy Resin Infusion Kit", "Quantity": 20, "UnitPrice": 2500.00},
    {"PurchaseID": "INV-003", "WBS_ID": "WBS-002", "PurchaseDate": "2026-02-28", "Description": "Steel Support Beam Frames", "Quantity": 4, "UnitPrice": 8000.00},
    {"PurchaseID": "INV-004", "WBS_ID": "WBS-002", "PurchaseDate": "2026-03-10", "Description": "Additional Epoxies (Overrun material)", "Quantity": 5, "UnitPrice": 2700.00},
    # WBS-003 (Outfitting: Cabling, engines, instruments, dashboard displays)
    {"PurchaseID": "INV-005", "WBS_ID": "WBS-003", "PurchaseDate": "2026-04-05", "Description": "Marine Cabin Electrical Wiring", "Quantity": 2, "UnitPrice": 12000.00},
    {"PurchaseID": "INV-006", "WBS_ID": "WBS-003", "PurchaseDate": "2026-04-20", "Description": "Simrad Integrated Marine Dashboard", "Quantity": 1, "UnitPrice": 45000.00},
    {"PurchaseID": "INV-007", "WBS_ID": "WBS-003", "PurchaseDate": "2026-05-02", "Description": "Twin Electric Inboard Engines", "Quantity": 2, "UnitPrice": 65000.00},
    {"PurchaseID": "INV-008", "WBS_ID": "WBS-003", "PurchaseDate": "2026-05-18", "Description": "Battery Storage Bank Lithium 10kWh", "Quantity": 2, "UnitPrice": 22000.00},
    # WBS-004 (Trials: Fuel, safety equipment, certifications)
    {"PurchaseID": "INV-009", "WBS_ID": "WBS-004", "PurchaseDate": "2026-06-05", "Description": "DNV Safety & Compliance Certification", "Quantity": 1, "UnitPrice": 25000.00},
    {"PurchaseID": "INV-010", "WBS_ID": "WBS-004", "PurchaseDate": "2026-06-15", "Description": "Test Trial Bio-Fuel & Supplies", "Quantity": 1, "UnitPrice": 8500.00}
]
# Add TotalActualCost to invoices
for inv in material_costs:
    inv["TotalActualCost"] = inv["Quantity"] * inv["UnitPrice"]


# 7. PHYSICAL_PROGRESS (Weekly records for EVM tracking)
# Generates weekly progress updates for each WBS Element
physical_progress = []
progress_id_counter = 1

def generate_weekly_progress(wbs_id, start_date, end_date, normal_rate, lag_weeks=None, catchup_rate=None):
    global progress_id_counter
    curr = start_date
    progress = 0.0
    week_num = 0
    while curr <= end_date:
        # Check for simulated lag
        rate = normal_rate
        if lag_weeks and week_num in lag_weeks:
            rate = normal_rate * 0.3  # Slower progress during lag
        elif catchup_rate and lag_weeks and week_num > max(lag_weeks):
            rate = catchup_rate  # Slower progress was caught up later

        progress = min(1.0, progress + rate)
        
        physical_progress.append({
            "ProgressID": f"PRG-{progress_id_counter:04d}",
            "WBS_ID": wbs_id,
            "RecordDate": curr.strftime("%Y-%m-%d"),
            "PercentComplete": round(progress, 3),
            "ReportedBy": "Frank Ellingsen"
        })
        progress_id_counter += 1
        if progress >= 1.0:
            break
        curr += timedelta(days=7)
        week_num += 1

# Generate WBS Weekly records
# WBS-001 (Management/Design) - Starts Jan 1, completed Jun 30 (26 weeks). Rate ~3.9% per week.
generate_weekly_progress("WBS-001", datetime(2026, 1, 7), datetime(2026, 6, 30), 0.039)

# WBS-002 (Hull Fabrication) - Starts Feb 1, completed Apr 15 (11 weeks). Target rate ~9.1% per week.
# Simulate a lag in weeks 4, 5, 6 due to material delay, then catchup.
generate_weekly_progress(
    "WBS-002", 
    datetime(2026, 2, 7), 
    datetime(2026, 4, 15), 
    0.095, 
    lag_weeks=[4, 5, 6], 
    catchup_rate=0.18  # Rush job to finish on time
)

# WBS-003 (Outfitting) - Starts Apr 1, completed May 31 (9 weeks). Target rate ~11% per week.
# Completed ahead of schedule by mid-May! Rate ~14% per week.
generate_weekly_progress("WBS-003", datetime(2026, 4, 7), datetime(2026, 5, 31), 0.13)

# WBS-004 (Trials & Handover) - Starts Jun 1, completed Jun 30 (4 weeks). Target rate ~25% per week.
generate_weekly_progress("WBS-004", datetime(2026, 6, 7), datetime(2026, 6, 30), 0.25)


# HELPER FUNCTION TO WRITE CSV
def write_csv(filename, data, headers):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated {filename} with {len(data)} rows.")

# Write CSV files
write_csv("projects.csv", projects, ["ProjectID", "ProjectName", "ProjectManager", "BudgetAtCompletion_BAC", "StartDate", "EndDate", "Status"])
write_csv("wbs_elements.csv", wbs_elements, ["WBS_ID", "ProjectID", "WBS_Code", "ElementName", "PlannedCost", "PlannedHours"])
write_csv("resources.csv", resources, ["ResourceID", "ResourceName", "Role", "HourlyRate"])
write_csv("resource_assignments.csv", assignments, ["AssignmentID", "WBS_ID", "ResourceID", "AllocatedHours"])
write_csv("timesheets.csv", timesheets, ["TimesheetID", "ResourceID", "WBS_ID", "WorkDate", "HoursWorked", "ApprovalStatus"])
write_csv("material_costs.csv", material_costs, ["PurchaseID", "WBS_ID", "PurchaseDate", "Description", "Quantity", "UnitPrice", "TotalActualCost"])
write_csv("physical_progress.csv", physical_progress, ["ProgressID", "WBS_ID", "RecordDate", "PercentComplete", "ReportedBy"])

print("Data generation complete! All files saved in: " + OUTPUT_DIR)
