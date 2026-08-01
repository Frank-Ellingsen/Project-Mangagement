import os
import csv
import sqlite3

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "Data", "CSV")
DB_DIR = os.path.join(BASE_DIR, "Data", "SQLite")
DB_PATH = os.path.join(DB_DIR, "project_controlling.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

print(f"Connecting to SQLite database at: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# List of CSV files to import
csv_files = {
    "projects": "projects.csv",
    "wbs_elements": "wbs_elements.csv",
    "resources": "resources.csv",
    "resource_assignments": "resource_assignments.csv",
    "timesheets": "timesheets.csv",
    "material_costs": "material_costs.csv",
    "physical_progress": "physical_progress.csv",
    "raid_log": "raid_log.csv"
}

# Helper to read CSV rows
def read_csv(file_name):
    filepath = os.path.join(CSV_DIR, file_name)
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
        return header, rows

# Load data into SQLite
for table_name, csv_file in csv_files.items():
    print(f"Loading {csv_file} into SQLite table '{table_name}'...")
    header, rows = read_csv(csv_file)
    
    # Drop existing table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    
    # Create table dynamically
    col_defs = ", ".join([f"{col} TEXT" for col in header]) # Simplistic type allocation for simplicity, SQLite will handle conversions
    cursor.execute(f"CREATE TABLE {table_name} ({col_defs});")
    
    # Insert rows
    placeholders = ", ".join(["?" for _ in header])
    cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders});", rows)

# Create EVM views in SQLite
print("Creating SQLite analytical views...")

# 1. Latest physical progress per WBS (SQLite syntax using subquery or ROW_NUMBER if supported, SQLite 3.25+ supports window functions)
cursor.execute("DROP VIEW IF EXISTS v_wbs_latest_progress;")
cursor.execute("""
CREATE VIEW v_wbs_latest_progress AS
WITH ranked_progress AS (
    SELECT 
        WBS_ID, 
        CAST(PercentComplete AS REAL) as PercentComplete, 
        RecordDate,
        ROW_NUMBER() OVER(PARTITION BY WBS_ID ORDER BY RecordDate DESC) as rn
    FROM physical_progress
)
SELECT WBS_ID, PercentComplete, RecordDate
FROM ranked_progress
WHERE rn = 1;
""")

# 2. Labor actual costs per WBS
cursor.execute("DROP VIEW IF EXISTS v_wbs_labor_actuals;")
cursor.execute("""
CREATE VIEW v_wbs_labor_actuals AS
SELECT 
    t.WBS_ID,
    SUM(CAST(t.HoursWorked AS REAL) * CAST(r.HourlyRate AS REAL)) as LaborCost,
    SUM(CAST(t.HoursWorked AS REAL)) as HoursWorked
FROM timesheets t
JOIN resources r ON t.ResourceID = r.ResourceID
GROUP BY t.WBS_ID;
""")

# 3. Material actual costs per WBS
cursor.execute("DROP VIEW IF EXISTS v_wbs_material_actuals;")
cursor.execute("""
CREATE VIEW v_wbs_material_actuals AS
SELECT 
    WBS_ID,
    SUM(CAST(TotalActualCost AS REAL)) as MaterialCost
FROM material_costs
GROUP BY WBS_ID;
""")

# 4. Master EVM metrics per WBS element
cursor.execute("DROP VIEW IF EXISTS v_wbs_evm_metrics;")
cursor.execute("""
CREATE VIEW v_wbs_evm_metrics AS
SELECT 
    w.WBS_ID,
    w.WBS_Code,
    w.ElementName,
    CAST(w.PlannedCost AS REAL) as BAC,
    COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0) as AC,
    CAST(w.PlannedCost AS REAL) * COALESCE(p.PercentComplete, 0.0) as EV,
    (CAST(w.PlannedCost AS REAL) * COALESCE(p.PercentComplete, 0.0)) - (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) as CV,
    CASE 
        WHEN (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) > 0 
        THEN (CAST(w.PlannedCost AS REAL) * COALESCE(p.PercentComplete, 0.0)) / (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0))
        ELSE 1.0 
    END as CPI,
    COALESCE(p.PercentComplete, 0.0) as PercentComplete,
    CASE 
        WHEN (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) > 0 AND (CAST(w.PlannedCost AS REAL) * COALESCE(p.PercentComplete, 0.0)) > 0
        THEN CAST(w.PlannedCost AS REAL) / (
            (CAST(w.PlannedCost AS REAL) * COALESCE(p.PercentComplete, 0.0)) / (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0))
        )
        ELSE CAST(w.PlannedCost AS REAL)
    END as EAC_Typical,
    (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) + (CAST(w.PlannedCost AS REAL) - (CAST(w.PlannedCost AS REAL) * COALESCE(p.PercentComplete, 0.0))) as EAC_Atypical
FROM wbs_elements w
LEFT JOIN v_wbs_labor_actuals l ON w.WBS_ID = l.WBS_ID
LEFT JOIN v_wbs_material_actuals m ON w.WBS_ID = m.WBS_ID
LEFT JOIN v_wbs_latest_progress p ON w.WBS_ID = p.WBS_ID;
""")

# 5. Project-level summary
cursor.execute("DROP VIEW IF EXISTS v_project_evm_summary;")
cursor.execute("""
CREATE VIEW v_project_evm_summary AS
SELECT 
    SUM(BAC) as Total_BAC,
    SUM(AC) as Total_AC,
    SUM(EV) as Total_EV,
    SUM(CV) as Total_CV,
    CASE WHEN SUM(AC) > 0 THEN SUM(EV) / SUM(AC) ELSE 1.0 END as Project_CPI,
    SUM(EAC_Typical) as Total_EAC_Typical,
    SUM(BAC) - SUM(EAC_Typical) as Total_VAC,
    (SUM(EV) / SUM(BAC)) * 100 as Overall_Progress_Pct
FROM v_wbs_evm_metrics;
""")

conn.commit()
print("SQLite database setup successfully!")
conn.close()
