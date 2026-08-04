import os
import csv
from datetime import datetime, timedelta

# Create CSV folder
csv_dir = r"c:\Users\frank\Desktop\Project Mng\PM teori\Excel App\CSV"
os.makedirs(csv_dir, exist_ok=True)

# 1. Dim_Project.csv
project_file = os.path.join(csv_dir, "Dim_Project.csv")
project_data = [
    ["Project_ID", "Project_Name", "Start_Date", "End_Date", "BAC", "Sector"],
    ["P101", "Office Fit-Out", "2026-05-04", "2026-07-26", 268650.00, "Corporate Real Estate"]
]
with open(project_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(project_data)

# 2. Dim_WBS.csv
wbs_file = os.path.join(csv_dir, "Dim_WBS.csv")
wbs_data = [
    ["WBS_ID", "WBS_Code", "Activity_Name", "Type", "Total_Budget"],
    ["WBS-01", "1.0", "Project Management", "Labor", 18000.00],
    ["WBS-02", "2.0", "Site Survey & Mobilization", "Labor", 8500.00],
    ["WBS-03", "3.0", "Design & Engineering", "Labor", 19200.00],
    ["WBS-04", "4.0", "Procurement - Materials", "Material", 42000.00],
    ["WBS-05", "5.0", "Demolition & Prep", "Labor", 13200.00],
    ["WBS-06", "6.0", "Electrical Rough-In", "Labor", 26000.00],
    ["WBS-07", "7.0", "HVAC Installation", "Subcontractor", 36000.00],
    ["WBS-08", "8.0", "Partitions & Drywall", "Subcontractor", 28000.00],
    ["WBS-09", "9.0", "Flooring", "Material", 35750.00],
    ["WBS-10", "10.0", "Fixtures & Furniture", "Material", 30000.00],
    ["WBS-11", "11.0", "Testing / Commissioning", "Labor", 8400.00],
    ["WBS-12", "12.0", "Handover & Closeout", "Labor", 3600.00]
]
with open(wbs_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(wbs_data)

# 3. Dim_Resource.csv
resource_file = os.path.join(csv_dir, "Dim_Resource.csv")
resource_data = [
    ["Resource_ID", "Resource_Name", "Role", "Hourly_Rate"],
    ["R01", "Project Manager", "Management", 1500.00],
    ["R02", "Lead Engineer", "Engineering", 2400.00],
    ["R03", "Electrician", "Trades", 2600.00],
    ["R04", "Demolition Crew", "Labor", 2200.00],
    ["R05", "Testing Engineer", "QA", 2100.00],
    ["R06", "Closeout Specialist", "QA", 1800.00],
    ["R07", "Materials Vendor", "Vendor", 0.00],
    ["R08", "HVAC Contractor", "Contractor", 0.00],
    ["R09", "Drywall Contractor", "Contractor", 0.00],
    ["R10", "Flooring Supplier", "Vendor", 0.00],
    ["R11", "Furniture Supplier", "Vendor", 0.00]
]
with open(resource_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(resource_data)

# 4. Dim_Calendar.csv
calendar_file = os.path.join(csv_dir, "Dim_Calendar.csv")
start_date = datetime.strptime("2026-05-04", "%Y-%m-%d") # Monday of Wk1
end_date = datetime.strptime("2026-07-26", "%Y-%m-%d") # Sunday of Wk12
calendar_data = [["Date", "Year", "Month", "Month_Name", "Quarter", "Week_Number", "Is_Weekday"]]
curr = start_date
while curr <= end_date:
    days_diff = (curr - start_date).days
    week_num = (days_diff // 7) + 1
    is_weekday = 1 if curr.weekday() < 5 else 0
    calendar_data.append([
        curr.strftime("%Y-%m-%d"),
        curr.year,
        curr.month,
        curr.strftime("%B"),
        (curr.month - 1) // 3 + 1,
        week_num,
        is_weekday
    ])
    curr += timedelta(days=1)
with open(calendar_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(calendar_data)

# 5. Fact_Baseline_PV.csv
# Scheduled weeks and weekly PV allocations per activity (using Monday dates)
# Week dates:
# Wk1: 2026-05-04, Wk2: 2026-05-11, Wk3: 2026-05-18, Wk4: 2026-05-25, Wk5: 2026-06-01, Wk6: 2026-06-08
# Wk7: 2026-06-15, Wk8: 2026-06-22, Wk9: 2026-06-29, Wk10: 2026-07-06, Wk11: 2026-07-13, Wk12: 2026-07-20
weeks_dates = {
    1: "2026-05-04", 2: "2026-05-11", 3: "2026-05-18", 4: "2026-05-25",
    5: "2026-06-01", 6: "2026-06-08", 7: "2026-06-15", 8: "2026-06-22",
    9: "2026-06-29", 10: "2026-07-06", 11: "2026-07-13", 12: "2026-07-20"
}
pv_allocations = {
    "WBS-01": {w: 1500.00 for w in range(1, 13)},
    "WBS-02": {1: 8500.00},
    "WBS-03": {1: 6400.00, 2: 6400.00, 3: 6400.00},
    "WBS-04": {2: 10500.00, 3: 10500.00, 4: 10500.00, 5: 10500.00},
    "WBS-05": {2: 4400.00, 3: 4400.00, 4: 4400.00},
    "WBS-06": {4: 8666.67, 5: 8666.67, 6: 8666.66},
    "WBS-07": {5: 9000.00, 6: 9000.00, 7: 9000.00, 8: 9000.00},
    "WBS-08": {6: 7000.00, 7: 7000.00, 8: 7000.00, 9: 7000.00},
    "WBS-09": {8: 11916.67, 9: 11916.67, 10: 11916.66},
    "WBS-10": {9: 10000.00, 10: 10000.00, 11: 10000.00},
    "WBS-11": {11: 4200.00, 12: 4200.00},
    "WBS-12": {12: 3600.00}
}
pv_file = os.path.join(csv_dir, "Fact_Baseline_PV.csv")
pv_data = [["Date", "WBS_ID", "Planned_Value"]]
for wbs, allocs in pv_allocations.items():
    for w, val in allocs.items():
        pv_data.append([weeks_dates[w], wbs, round(val, 2)])
with open(pv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(pv_data)

# 6. Fact_Actual_Costs.csv
# Weekly increments of AC matching spreadsheet:
# Week 1: 16,295.04
# Week 2: 22,654.08
# Week 3: 22,654.08
# Week 4: 24,906.24
# Week 5: 29,476.80
# Week 6: 25,999.20
ac_weekly_postings = [
    # Week 1
    {"week": 1, "wbs": "WBS-01", "resource": "R01", "cost": 1600.00, "is_labor": True},
    {"week": 1, "wbs": "WBS-02", "resource": "R04", "cost": 8700.00, "is_labor": True},
    {"week": 1, "wbs": "WBS-03", "resource": "R02", "cost": 5995.04, "is_labor": True},
    # Week 2
    {"week": 2, "wbs": "WBS-01", "resource": "R01", "cost": 1600.00, "is_labor": True},
    {"week": 2, "wbs": "WBS-03", "resource": "R02", "cost": 6000.00, "is_labor": True},
    {"week": 2, "wbs": "WBS-04", "resource": "R07", "cost": 10500.00, "is_labor": False},
    {"week": 2, "wbs": "WBS-05", "resource": "R04", "cost": 4554.08, "is_labor": True},
    # Week 3
    {"week": 3, "wbs": "WBS-01", "resource": "R01", "cost": 1600.00, "is_labor": True},
    {"week": 3, "wbs": "WBS-03", "resource": "R02", "cost": 6200.00, "is_labor": True},
    {"week": 3, "wbs": "WBS-04", "resource": "R07", "cost": 10200.00, "is_labor": False},
    {"week": 3, "wbs": "WBS-05", "resource": "R04", "cost": 4654.08, "is_labor": True},
    # Week 4
    {"week": 4, "wbs": "WBS-01", "resource": "R01", "cost": 1600.00, "is_labor": True},
    {"week": 4, "wbs": "WBS-04", "resource": "R07", "cost": 10200.00, "is_labor": False},
    {"week": 4, "wbs": "WBS-05", "resource": "R04", "cost": 4200.00, "is_labor": True},
    {"week": 4, "wbs": "WBS-06", "resource": "R03", "cost": 8906.24, "is_labor": True},
    # Week 5
    {"week": 5, "wbs": "WBS-01", "resource": "R01", "cost": 1600.00, "is_labor": True},
    {"week": 5, "wbs": "WBS-04", "resource": "R07", "cost": 10400.00, "is_labor": False},
    {"week": 5, "wbs": "WBS-06", "resource": "R03", "cost": 8800.00, "is_labor": True},
    {"week": 5, "wbs": "WBS-07", "resource": "R08", "cost": 8676.80, "is_labor": True},
    # Week 6
    {"week": 6, "wbs": "WBS-01", "resource": "R01", "cost": 1600.00, "is_labor": True},
    {"week": 6, "wbs": "WBS-06", "resource": "R03", "cost": 8500.00, "is_labor": True},
    {"week": 6, "wbs": "WBS-07", "resource": "R08", "cost": 8800.00, "is_labor": True},
    {"week": 6, "wbs": "WBS-08", "resource": "R09", "cost": 7099.20, "is_labor": True}
]

ac_file = os.path.join(csv_dir, "Fact_Actual_Costs.csv")
ac_data = [["Date", "WBS_ID", "Resource_ID", "Actual_Cost", "Hours_Worked"]]

resource_rates = {"R01": 1500.00, "R02": 2400.00, "R03": 2600.00, "R04": 2200.00, "R05": 2100.00, "R06": 1800.00}

for posting in ac_weekly_postings:
    w = posting["week"]
    wbs = posting["wbs"]
    res = posting["resource"]
    total_c = posting["cost"]
    is_lab = posting["is_labor"]
    
    w_start = start_date + timedelta(days=(w - 1) * 7)
    
    if not is_lab:
        p_date = (w_start + timedelta(days=2)).strftime("%Y-%m-%d")
        ac_data.append([p_date, wbs, res, round(total_c, 2), 0.0])
    else:
        daily_c = round(total_c / 5.0, 2)
        last_day_c = round(total_c - (daily_c * 4), 2)
        rate = resource_rates.get(res, 0.0)
        daily_h = round(daily_c / rate, 2) if rate > 0 else 0.0
        last_day_h = round(last_day_c / rate, 2) if rate > 0 else 0.0
        
        for d in range(5):
            p_date = (w_start + timedelta(days=d)).strftime("%Y-%m-%d")
            c = daily_c if d < 4 else last_day_c
            h = daily_h if d < 4 else last_day_h
            ac_data.append([p_date, wbs, res, c, h])

with open(ac_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(ac_data)

# 7. Fact_Physical_Progress.csv
# Weekly cumulative physical progress per WBS element.
progress_postings = {
    1: {"WBS-01": 1/12, "WBS-02": 1.0, "WBS-03": 0.265},
    2: {"WBS-01": 2/12, "WBS-02": 1.0, "WBS-03": 0.60, "WBS-04": 0.20, "WBS-05": 0.351818},
    3: {"WBS-01": 3/12, "WBS-02": 1.0, "WBS-03": 1.00, "WBS-04": 0.45, "WBS-05": 0.45},
    4: {"WBS-01": 4/12, "WBS-02": 1.0, "WBS-03": 1.00, "WBS-04": 0.70, "WBS-05": 0.85, "WBS-06": 0.2223588},
    5: {"WBS-01": 5/12, "WBS-02": 1.0, "WBS-03": 1.00, "WBS-04": 1.00, "WBS-05": 1.00, "WBS-06": 0.50, "WBS-07": 0.110963},
    6: {"WBS-01": 6/12, "WBS-02": 1.0, "WBS-03": 1.00, "WBS-04": 1.00, "WBS-05": 1.00, "WBS-06": 0.70, "WBS-07": 0.40, "WBS-08": 0.2488571}
}

progress_file = os.path.join(csv_dir, "Fact_Physical_Progress.csv")
progress_data = [["Date", "WBS_ID", "Physical_Progress_Pct"]]
for w, wbs_progress in progress_postings.items():
    w_start = start_date + timedelta(days=(w - 1) * 7)
    report_date = (w_start + timedelta(days=4)).strftime("%Y-%m-%d")
    for wbs, pct in wbs_progress.items():
        progress_data.append([report_date, wbs, round(pct, 6)])

with open(progress_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(progress_data)

print("Mock data generation successfully completed.")
