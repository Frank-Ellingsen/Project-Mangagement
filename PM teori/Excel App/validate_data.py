import os
import csv

csv_dir = r"c:\Users\frank\Desktop\Project Mng\PM teori\Excel App\CSV"

def load_csv(filename):
    path = os.path.join(csv_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        return header, [row for row in reader]

print("Running validation of Star Schema CSV files...")

# Load tables
wbs_header, wbs_rows = load_csv("Dim_WBS.csv")
pv_header, pv_rows = load_csv("Fact_Baseline_PV.csv")
ac_header, ac_rows = load_csv("Fact_Actual_Costs.csv")
progress_header, progress_rows = load_csv("Fact_Physical_Progress.csv")

# 1. Verify WBS Total Budget
wbs_budgets = {row[0]: float(row[4]) for row in wbs_rows}
total_bac = sum(wbs_budgets.values())
print(f"Total BAC from Dim_WBS: {total_bac:.2f} NOK (Expected: 268650.00 NOK)")
assert abs(total_bac - 268650.00) < 0.01, "BAC mismatch!"

# 2. Verify Planned Value (PV) sums to BAC
total_pv = sum(float(row[2]) for row in pv_rows)
print(f"Total Planned Value from Fact_Baseline_PV: {total_pv:.2f} NOK (Expected: 268650.00 NOK)")
assert abs(total_pv - 268650.00) < 0.01, "Planned Value total mismatch!"

# 3. Verify actual costs roll up correctly to spreadsheet weekly values
# Weekly AC expected cumulative:
# Week 1: 16,295.04
# Week 2: 38,949.12
# Week 3: 61,603.20
# Week 4: 86,509.44
# Week 5: 115,986.24
# Week 6: 141,985.44
expected_ac_cum = {
    1: 16295.04,
    2: 38949.12,
    3: 61603.20,
    4: 86509.44,
    5: 115986.24,
    6: 141985.44
}

# Determine week numbers for AC records from Dim_Calendar
cal_header, cal_rows = load_csv("Dim_Calendar.csv")
date_to_week = {row[0]: int(row[5]) for row in cal_rows}

weekly_ac = {}
for row in ac_rows:
    dt = row[0]
    cost = float(row[3])
    wk = date_to_week[dt]
    weekly_ac[wk] = weekly_ac.get(wk, 0.0) + cost

cum_ac = 0.0
for wk in sorted(expected_ac_cum.keys()):
    cum_ac += weekly_ac.get(wk, 0.0)
    expected = expected_ac_cum[wk]
    print(f"Week {wk} Cumulative AC: {cum_ac:.2f} NOK (Expected: {expected:.2f} NOK)")
    assert abs(cum_ac - expected) < 0.05, f"Week {wk} AC mismatch! Got {cum_ac:.2f}, expected {expected:.2f}"

# 4. Verify Earned Value (EV) rolls up correctly
# EV of a WBS element in a week = WBS_Budget * progress_percent.
# Progress is reported weekly.
# Week EV cumulative expected:
# Week 1: 15,088
# Week 2: 36,064
# Week 3: 57,040
# Week 4: 80,101.33
# Week 5: 107,394.67
# Week 6: 131,468.00
expected_ev_cum = {
    1: 15088.00,
    2: 36064.00,
    3: 57040.00,
    4: 80101.33,
    5: 107394.67,
    6: 131468.00
}

# Group progress reports by week
weekly_progress = {}
for row in progress_rows:
    dt = row[0]
    wbs = row[1]
    pct = float(row[2])
    wk = date_to_week[dt]
    if wk not in weekly_progress:
        weekly_progress[wk] = {}
    weekly_progress[wk][wbs] = pct

for wk in sorted(expected_ev_cum.keys()):
    prog_at_wk = weekly_progress.get(wk, {})
    # For a week W, we calculate EV. Note that physical progress is recorded as cumulative percent complete.
    # So EV for task T in week W is simply budget(T) * pct(T, W).
    ev_total = 0.0
    for wbs, budget in wbs_budgets.items():
        # Find the latest progress for this WBS up to week wk
        latest_pct = 0.0
        for w_chk in range(1, wk + 1):
            if w_chk in weekly_progress and wbs in weekly_progress[w_chk]:
                latest_pct = weekly_progress[w_chk][wbs]
        ev_total += budget * latest_pct
    
    expected = expected_ev_cum[wk]
    print(f"Week {wk} Cumulative EV: {ev_total:.2f} NOK (Expected: {expected:.2f} NOK)")
    assert abs(ev_total - expected) < 1.0, f"Week {wk} EV mismatch! Got {ev_total:.2f}, expected {expected:.2f}"

print("All validations PASSED successfully!")
