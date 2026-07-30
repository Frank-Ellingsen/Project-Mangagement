import os
import csv

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "Data", "CSV")
EXCEL_DIR = os.path.join(CSV_DIR, "excel_friendly")

if not os.path.exists(EXCEL_DIR):
    os.makedirs(EXCEL_DIR)

def load_csv(filename):
    filepath = os.path.join(CSV_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# Load the source relational data
projects = load_csv("projects.csv")
wbs_elements = load_csv("wbs_elements.csv")
resources = load_csv("resources.csv")
timesheets = load_csv("timesheets.csv")
material_costs = load_csv("material_costs.csv")
physical_progress = load_csv("physical_progress.csv")

# Create lookup dictionaries for joining
res_lookup = {r["ResourceID"]: r for r in resources}
wbs_lookup = {w["WBS_ID"]: w for w in wbs_elements}
prj_lookup = {p["ProjectID"]: p for p in projects}

# 1. Denormalized Timesheets Flat File
timesheets_flat = []
for ts in timesheets:
    res = res_lookup.get(ts["ResourceID"], {"ResourceName": "Unknown", "Role": "Unknown", "HourlyRate": "0"})
    wbs = wbs_lookup.get(ts["WBS_ID"], {"WBS_Code": "N/A", "ElementName": "Unknown", "ProjectID": "N/A"})
    prj = prj_lookup.get(wbs["ProjectID"], {"ProjectName": "Unknown"})
    
    hours = float(ts["HoursWorked"])
    rate = float(res["HourlyRate"])
    labor_cost = hours * rate
    
    timesheets_flat.append({
        "TimesheetID": ts["TimesheetID"],
        "WorkDate": ts["WorkDate"],
        "ProjectName": prj["ProjectName"],
        "WBS_Code": wbs["WBS_Code"],
        "WBS_Name": wbs["ElementName"],
        "ResourceName": res["ResourceName"],
        "Role": res["Role"],
        "HourlyRate": str(rate).replace(".", ","), # Excel European decimal format
        "HoursWorked": str(hours).replace(".", ","),
        "LaborCost": str(round(labor_cost, 2)).replace(".", ",")
    })

# 2. Denormalized Material Costs Flat File
materials_flat = []
for mat in material_costs:
    wbs = wbs_lookup.get(mat["WBS_ID"], {"WBS_Code": "N/A", "ElementName": "Unknown", "ProjectID": "N/A"})
    prj = prj_lookup.get(wbs["ProjectID"], {"ProjectName": "Unknown"})
    
    qty = int(mat["Quantity"])
    unit_price = float(mat["UnitPrice"])
    total_cost = float(mat["TotalActualCost"])
    
    materials_flat.append({
        "PurchaseID": mat["PurchaseID"],
        "PurchaseDate": mat["PurchaseDate"],
        "ProjectName": prj["ProjectName"],
        "WBS_Code": wbs["WBS_Code"],
        "WBS_Name": wbs["ElementName"],
        "Description": mat["Description"],
        "Quantity": qty,
        "UnitPrice": str(unit_price).replace(".", ","),
        "TotalActualCost": str(total_cost).replace(".", ",")
    })

# 3. Denormalized Progress Flat File
progress_flat = []
for prg in physical_progress:
    wbs = wbs_lookup.get(prg["WBS_ID"], {"WBS_Code": "N/A", "ElementName": "Unknown", "ProjectID": "N/A", "PlannedCost": "0"})
    prj = prj_lookup.get(wbs["ProjectID"], {"ProjectName": "Unknown"})
    
    percent = float(prg["PercentComplete"])
    bac = float(wbs["PlannedCost"])
    ev = bac * percent
    
    progress_flat.append({
        "ProgressID": prg["ProgressID"],
        "RecordDate": prg["RecordDate"],
        "ProjectName": prj["ProjectName"],
        "WBS_Code": wbs["WBS_Code"],
        "WBS_Name": wbs["ElementName"],
        "PlannedCost_BAC": str(bac).replace(".", ","),
        "PercentComplete": str(percent).replace(".", ","),
        "EarnedValue_EV": str(round(ev, 2)).replace(".", ","),
        "ReportedBy": prg["ReportedBy"]
    })

# Helper function to write semicolon-separated CSVs (Excel-friendly in Europe)
def write_excel_csv(filename, data, headers):
    filepath = os.path.join(EXCEL_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f: # utf-8-sig adds BOM so Excel opens it as UTF-8
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=";")
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated Excel-friendly: {filename} with {len(data)} rows.")

# Write the Excel-friendly flat files
write_excel_csv("excel_timesheets_flat.csv", timesheets_flat, 
                ["TimesheetID", "WorkDate", "ProjectName", "WBS_Code", "WBS_Name", "ResourceName", "Role", "HourlyRate", "HoursWorked", "LaborCost"])

write_excel_csv("excel_material_costs_flat.csv", materials_flat, 
                ["PurchaseID", "PurchaseDate", "ProjectName", "WBS_Code", "WBS_Name", "Description", "Quantity", "UnitPrice", "TotalActualCost"])

write_excel_csv("excel_progress_flat.csv", progress_flat, 
                ["ProgressID", "RecordDate", "ProjectName", "WBS_Code", "WBS_Name", "PlannedCost_BAC", "PercentComplete", "EarnedValue_EV", "ReportedBy"])

print("Excel files generation complete! Saved in: " + EXCEL_DIR)
