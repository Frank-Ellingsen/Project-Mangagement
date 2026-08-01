import os
import csv
import subprocess

# Define directory references
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "Data", "CSV")

def append_rows_if_missing(filename, key_col, rows_to_add):
    filepath = os.path.join(CSV_DIR, filename)
    
    # Read existing keys
    existing_keys = set()
    headers = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for row in reader:
                existing_keys.add(row[key_col])
                
    # Filter rows to add
    filtered_rows = [r for r in rows_to_add if r[key_col] not in existing_keys]
    
    if filtered_rows:
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerows(filtered_rows)
        print(f"Added {len(filtered_rows)} rows to {filename}.")
    else:
        print(f"No new rows needed for {filename} (already up-to-date).")

def add_mockup_projects():
    print("Injecting new mockup projects into source CSV files...")
    
    # 1. Projects
    projects = [
        {
            "ProjectID": "PRJ-002",
            "ProjectName": "PRJ-002: Patrol Vessel Carbon Mold Design",
            "ProjectManager": "Morten Hansen",
            "BudgetAtCompletion_BAC": "800000.00",
            "StartDate": "2026-08-01",
            "EndDate": "2026-12-31",
            "Status": "Planned"
        },
        {
            "ProjectID": "PRJ-003",
            "ProjectName": "PRJ-003: Subsea Cable Installation Frame",
            "ProjectManager": "Erik Johansen",
            "BudgetAtCompletion_BAC": "1200000.00",
            "StartDate": "2026-05-01",
            "EndDate": "2026-10-31",
            "Status": "Active"
        },
        {
            "ProjectID": "PRJ-004",
            "ProjectName": "PRJ-004: Autonomous Workboat Hull Weldments",
            "ProjectManager": "Astrid Nilsen",
            "BudgetAtCompletion_BAC": "2000000.00",
            "StartDate": "2026-03-01",
            "EndDate": "2026-08-31",
            "Status": "Active"
        },
        {
            "ProjectID": "PRJ-005",
            "ProjectName": "PRJ-005: Defense Logistics Pontoon Build",
            "ProjectManager": "Frank Ellingsen",
            "BudgetAtCompletion_BAC": "1000000.00",
            "StartDate": "2026-02-01",
            "EndDate": "2026-07-31",
            "Status": "Active"
        },
        {
            "ProjectID": "PRJ-006",
            "ProjectName": "PRJ-006: Lightweight Composite Cargo Hatch",
            "ProjectManager": "Morten Hansen",
            "BudgetAtCompletion_BAC": "600000.00",
            "StartDate": "2025-10-01",
            "EndDate": "2026-03-31",
            "Status": "Completed"
        }
    ]
    append_rows_if_missing("projects.csv", "ProjectID", projects)
    
    # 2. WBS Elements
    wbs = [
        # PRJ-002
        {"WBS_ID": "WBS-005", "ProjectID": "PRJ-002", "WBS_Code": "1.0", "ElementName": "Design & CFD Analysis", "PlannedCost": "300000.00", "PlannedHours": "300.0"},
        {"WBS_ID": "WBS-006", "ProjectID": "PRJ-002", "WBS_Code": "2.0", "ElementName": "Material Procurement", "PlannedCost": "500000.00", "PlannedHours": "0.0"},
        # PRJ-003
        {"WBS_ID": "WBS-007", "ProjectID": "PRJ-003", "WBS_Code": "1.0", "ElementName": "Structural Frame Engineering", "PlannedCost": "400000.00", "PlannedHours": "400.0"},
        {"WBS_ID": "WBS-008", "ProjectID": "PRJ-003", "WBS_Code": "2.0", "ElementName": "Steel Fabrication", "PlannedCost": "800000.00", "PlannedHours": "1000.0"},
        # PRJ-004
        {"WBS_ID": "WBS-009", "ProjectID": "PRJ-004", "WBS_Code": "1.0", "ElementName": "Engineering Drawings & Class Approval", "PlannedCost": "500000.00", "PlannedHours": "500.0"},
        {"WBS_ID": "WBS-010", "ProjectID": "PRJ-004", "WBS_Code": "2.0", "ElementName": "Hull Welding & Assembly", "PlannedCost": "1500000.00", "PlannedHours": "2000.0"},
        # PRJ-005
        {"WBS_ID": "WBS-011", "ProjectID": "PRJ-005", "WBS_Code": "1.0", "ElementName": "Project Control & PM", "PlannedCost": "200000.00", "PlannedHours": "250.0"},
        {"WBS_ID": "WBS-012", "ProjectID": "PRJ-005", "WBS_Code": "2.0", "ElementName": "Pontoon Assembly & Painting", "PlannedCost": "800000.00", "PlannedHours": "1000.0"},
        # PRJ-006
        {"WBS_ID": "WBS-013", "ProjectID": "PRJ-006", "WBS_Code": "1.0", "ElementName": "Hatch Engineering & FEA", "PlannedCost": "200000.00", "PlannedHours": "200.0"},
        {"WBS_ID": "WBS-014", "ProjectID": "PRJ-006", "WBS_Code": "2.0", "ElementName": "Molding & Testing", "PlannedCost": "400000.00", "PlannedHours": "500.0"}
    ]
    append_rows_if_missing("wbs_elements.csv", "WBS_ID", wbs)
    
    # 3. Resource Assignments
    asg = [
        {"AssignmentID": "ASG-009", "WBS_ID": "WBS-005", "ResourceID": "RES-003", "AllocatedHours": "300.0"},
        {"AssignmentID": "ASG-010", "WBS_ID": "WBS-007", "ResourceID": "RES-003", "AllocatedHours": "400.0"},
        {"AssignmentID": "ASG-011", "WBS_ID": "WBS-008", "ResourceID": "RES-004", "AllocatedHours": "1000.0"},
        {"AssignmentID": "ASG-012", "WBS_ID": "WBS-009", "ResourceID": "RES-003", "AllocatedHours": "500.0"},
        {"AssignmentID": "ASG-013", "WBS_ID": "WBS-010", "ResourceID": "RES-004", "AllocatedHours": "2000.0"},
        {"AssignmentID": "ASG-014", "WBS_ID": "WBS-011", "ResourceID": "RES-001", "AllocatedHours": "250.0"},
        {"AssignmentID": "ASG-015", "WBS_ID": "WBS-012", "ResourceID": "RES-004", "AllocatedHours": "1000.0"},
        {"AssignmentID": "ASG-016", "WBS_ID": "WBS-013", "ResourceID": "RES-003", "AllocatedHours": "200.0"},
        {"AssignmentID": "ASG-017", "WBS_ID": "WBS-014", "ResourceID": "RES-004", "AllocatedHours": "500.0"}
    ]
    append_rows_if_missing("resource_assignments.csv", "AssignmentID", asg)
    
    # 4. Timesheets (Actual Hours)
    # PRJ-002: Not started, no timesheets.
    # PRJ-003 (30% Complete): 350 hours engineering.
    # PRJ-004 (70% Complete): 480 hours engineering, 1100 hours welding.
    # PRJ-005 (90% Complete): 220 hours PM/Controlling, 800 hours welding.
    # PRJ-006 (100% Complete): 190 hours engineering, 480 hours welding.
    ts = [
        # PRJ-003
        {"TimesheetID": "TS-3001", "ResourceID": "RES-003", "WBS_ID": "WBS-007", "WorkDate": "2026-05-15", "HoursWorked": "350.0", "ApprovalStatus": "Approved"},
        # PRJ-004
        {"TimesheetID": "TS-4001", "ResourceID": "RES-003", "WBS_ID": "WBS-009", "WorkDate": "2026-03-20", "HoursWorked": "480.0", "ApprovalStatus": "Approved"},
        {"TimesheetID": "TS-4002", "ResourceID": "RES-004", "WBS_ID": "WBS-010", "WorkDate": "2026-04-10", "HoursWorked": "1100.0", "ApprovalStatus": "Approved"},
        # PRJ-005
        {"TimesheetID": "TS-5001", "ResourceID": "RES-001", "WBS_ID": "WBS-011", "WorkDate": "2026-02-28", "HoursWorked": "220.0", "ApprovalStatus": "Approved"},
        {"TimesheetID": "TS-5002", "ResourceID": "RES-004", "WBS_ID": "WBS-012", "WorkDate": "2026-03-15", "HoursWorked": "800.0", "ApprovalStatus": "Approved"},
        # PRJ-006
        {"TimesheetID": "TS-6001", "ResourceID": "RES-003", "WBS_ID": "WBS-013", "WorkDate": "2025-10-25", "HoursWorked": "190.0", "ApprovalStatus": "Approved"},
        {"TimesheetID": "TS-6002", "ResourceID": "RES-004", "WBS_ID": "WBS-014", "WorkDate": "2025-11-20", "HoursWorked": "480.0", "ApprovalStatus": "Approved"}
    ]
    append_rows_if_missing("timesheets.csv", "TimesheetID", ts)
    
    # 5. Material Costs (Actual Material)
    # PRJ-003: 50,000 USD steel frame pre-payment.
    # PRJ-004: 250,000 USD welding raw materials.
    # PRJ-005: 180,000 USD paint and plates.
    # PRJ-006: 70,000 USD composite fibers.
    mats = [
        {"PurchaseID": "MAT-3001", "WBS_ID": "WBS-008", "PurchaseDate": "2026-05-10", "Description": "Steel Frame Pre-payment Deposit", "Quantity": "1", "UnitPrice": "50000.00", "TotalActualCost": "50000.00"},
        {"PurchaseID": "MAT-4001", "WBS_ID": "WBS-010", "PurchaseDate": "2026-03-25", "Description": "Consumables & Steel Plates", "Quantity": "1", "UnitPrice": "250000.00", "TotalActualCost": "250000.00"},
        {"PurchaseID": "MAT-5001", "WBS_ID": "WBS-012", "PurchaseDate": "2026-03-01", "Description": "Paint & Marine Alloy Plates", "Quantity": "1", "UnitPrice": "180000.00", "TotalActualCost": "180000.00"},
        {"PurchaseID": "MAT-6001", "WBS_ID": "WBS-014", "PurchaseDate": "2025-11-01", "Description": "Composite Cutting Fiber", "Quantity": "1", "UnitPrice": "70000.00", "TotalActualCost": "70000.00"}
    ]
    append_rows_if_missing("material_costs.csv", "PurchaseID", mats)
    
    # 6. Physical Progress
    # PRJ-002 (Planned / 0% complete)
    # PRJ-003 (30% complete): WBS 1.0 is 90% (0.90) complete, WBS 2.0 is 0% complete. Average weighted = (400k * 0.9 + 800k * 0) / 1.2M = 30%.
    # PRJ-004 (70% complete): WBS 1.0 is 100% (1.00) complete, WBS 2.0 is 60% (0.60) complete. Average weighted = (500k * 1.0 + 1500k * 0.6) / 2M = 70%.
    # PRJ-005 (90% complete): WBS 1.0 is 100% (1.00) complete, WBS 2.0 is 87.5% (0.875) complete. Average weighted = (200k * 1.0 + 800k * 0.875) / 1M = 90%.
    # PRJ-006 (100% complete): WBS 1.0 and 2.0 are 100% complete.
    prog = [
        # PRJ-002
        {"ProgressID": "PRG-2001", "WBS_ID": "WBS-005", "RecordDate": "2026-07-31", "PercentComplete": "0.00", "ReportedBy": "Frank Ellingsen"},
        {"ProgressID": "PRG-2002", "WBS_ID": "WBS-006", "RecordDate": "2026-07-31", "PercentComplete": "0.00", "ReportedBy": "Frank Ellingsen"},
        # PRJ-003
        {"ProgressID": "PRG-3001", "WBS_ID": "WBS-007", "RecordDate": "2026-05-30", "PercentComplete": "0.90", "ReportedBy": "Frank Ellingsen"},
        {"ProgressID": "PRG-3002", "WBS_ID": "WBS-008", "RecordDate": "2026-05-30", "PercentComplete": "0.00", "ReportedBy": "Frank Ellingsen"},
        # PRJ-004
        {"ProgressID": "PRG-4001", "WBS_ID": "WBS-009", "RecordDate": "2026-04-15", "PercentComplete": "1.00", "ReportedBy": "Frank Ellingsen"},
        {"ProgressID": "PRG-4002", "WBS_ID": "WBS-010", "RecordDate": "2026-04-15", "PercentComplete": "0.60", "ReportedBy": "Frank Ellingsen"},
        # PRJ-005
        {"ProgressID": "PRG-5001", "WBS_ID": "WBS-011", "RecordDate": "2026-04-30", "PercentComplete": "1.00", "ReportedBy": "Frank Ellingsen"},
        {"ProgressID": "PRG-5002", "WBS_ID": "WBS-012", "RecordDate": "2026-04-30", "PercentComplete": "0.875", "ReportedBy": "Frank Ellingsen"},
        # PRJ-006
        {"ProgressID": "PRG-6001", "WBS_ID": "WBS-013", "RecordDate": "2026-03-31", "PercentComplete": "1.00", "ReportedBy": "Frank Ellingsen"},
        {"ProgressID": "PRG-6002", "WBS_ID": "WBS-014", "RecordDate": "2026-03-31", "PercentComplete": "1.00", "ReportedBy": "Frank Ellingsen"}
    ]
    append_rows_if_missing("physical_progress.csv", "ProgressID", prog)
    
    # Recompile databases
    print("Re-compiling DuckDB analytical views...")
    subprocess.run(["python", "AI_Controller/build_duckdb.py"], check=True)
    
    print("Re-compiling SQLite relational databases...")
    subprocess.run(["python", "AI_Controller/build_sqlite.py"], check=True)
    
    print("All databases successfully re-compiled with the 5 new mockup projects!")

if __name__ == "__main__":
    add_mockup_projects()
