import os
import duckdb

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "Data", "CSV")
DB_DIR = os.path.join(BASE_DIR, "Data", "DuckDB")
DB_PATH = os.path.join(DB_DIR, "project_controlling.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

print(f"Connecting to DuckDB database at: {DB_PATH}")
con = duckdb.connect(DB_PATH)

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

# Import CSVs into tables
for table_name, csv_file in csv_files.items():
    csv_path = os.path.join(CSV_DIR, csv_file).replace('\\', '/')
    print(f"Loading {csv_file} into table '{table_name}'...")
    con.execute(f"DROP TABLE IF EXISTS {table_name};")
    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}');")

# Create views for EVM metrics calculation
print("Creating analytical views...")

# 1. Latest physical progress per WBS
con.execute("""
CREATE OR REPLACE VIEW v_wbs_latest_progress AS
WITH ranked_progress AS (
    SELECT 
        WBS_ID, 
        PercentComplete, 
        RecordDate,
        ROW_NUMBER() OVER(PARTITION BY WBS_ID ORDER BY RecordDate DESC) as rn
    FROM physical_progress
)
SELECT WBS_ID, PercentComplete, RecordDate
FROM ranked_progress
WHERE rn = 1;
""")

# 2. Labor actual costs per WBS
con.execute("""
CREATE OR REPLACE VIEW v_wbs_labor_actuals AS
SELECT 
    t.WBS_ID,
    SUM(t.HoursWorked * r.HourlyRate) as LaborCost,
    SUM(t.HoursWorked) as HoursWorked
FROM timesheets t
JOIN resources r ON t.ResourceID = r.ResourceID
GROUP BY t.WBS_ID;
""")

# 3. Material actual costs per WBS
con.execute("""
CREATE OR REPLACE VIEW v_wbs_material_actuals AS
SELECT 
    WBS_ID,
    SUM(TotalActualCost) as MaterialCost
FROM material_costs
GROUP BY WBS_ID;
""")

# 4. Master EVM metrics per WBS element
con.execute("""
CREATE OR REPLACE VIEW v_wbs_evm_metrics AS
SELECT 
    w.WBS_ID,
    w.WBS_Code,
    w.ElementName,
    w.PlannedCost as BAC,
    COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0) as AC,
    w.PlannedCost * COALESCE(p.PercentComplete, 0.0) as EV,
    (w.PlannedCost * COALESCE(p.PercentComplete, 0.0)) - (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) as CV,
    -- CPI = EV / AC
    CASE 
        WHEN (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) > 0 
        THEN (w.PlannedCost * COALESCE(p.PercentComplete, 0.0)) / (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0))
        ELSE 1.0 
    END as CPI,
    COALESCE(p.PercentComplete, 0.0) as PercentComplete,
    -- EAC Typical = BAC / CPI
    CASE 
        WHEN (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) > 0 AND (w.PlannedCost * COALESCE(p.PercentComplete, 0.0)) > 0
        THEN w.PlannedCost / (
            (w.PlannedCost * COALESCE(p.PercentComplete, 0.0)) / (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0))
        )
        ELSE w.PlannedCost
    END as EAC_Typical,
    -- EAC Atypical = AC + (BAC - EV)
    (COALESCE(l.LaborCost, 0.0) + COALESCE(m.MaterialCost, 0.0)) + (w.PlannedCost - (w.PlannedCost * COALESCE(p.PercentComplete, 0.0))) as EAC_Atypical
FROM wbs_elements w
LEFT JOIN v_wbs_labor_actuals l ON w.WBS_ID = l.WBS_ID
LEFT JOIN v_wbs_material_actuals m ON w.WBS_ID = m.WBS_ID
LEFT JOIN v_wbs_latest_progress p ON w.WBS_ID = p.WBS_ID;
""")

# 5. Project-level summary
con.execute("""
CREATE OR REPLACE VIEW v_project_evm_summary AS
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

print("DuckDB database setup successfully!")
con.close()
