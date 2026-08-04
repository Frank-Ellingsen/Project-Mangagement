import os
import win32com.client

def test_excel_formulas():
    filepath = r"c:\Users\frank\Desktop\Project Mng\PM teori\Excel App\Project_Controlling_App.xlsx"
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    print("Launching Microsoft Excel via COM...")
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    
    try:
        print(f"Opening workbook: {filepath}")
        wb = excel.Workbooks.Open(filepath)
        
        # Force a full recalculation of all formulas
        print("Triggering Excel formula recalculation...")
        excel.Calculate()
        
        ws = wb.Sheets("EVM Dashboard")
        
        # Read KPI Cards
        # Set 1 (Row 7)
        bac = ws.Range("A7").Value
        pv = ws.Range("D7").Value
        ac = ws.Range("G7").Value
        ev = ws.Range("J7").Value
        
        # Set 2 (Row 10)
        cv = ws.Range("A10").Value
        sv = ws.Range("D10").Value
        cpi = ws.Range("G10").Value
        spi = ws.Range("J10").Value
        
        # Set 3 (Row 13)
        eac = ws.Range("A13").Value
        etc = ws.Range("D13").Value
        vac = ws.Range("G13").Value
        progress = ws.Range("J13").Value
        
        print("\n" + "="*50)
        print("EXCEL EVALUATED EVM DASHBOARD KPI RESULTS")
        print("="*50)
        print(f"BAC:      {bac}")
        print(f"PV:       {pv}")
        print(f"AC:       {ac}")
        print(f"EV:       {ev}")
        print(f"CV:       {cv}")
        print(f"SV:       {sv}")
        print(f"CPI:      {cpi:.3f}" if isinstance(cpi, float) else f"CPI:      {cpi}")
        print(f"SPI:      {spi:.3f}" if isinstance(spi, float) else f"SPI:      {spi}")
        print(f"EAC:      {eac}")
        print(f"ETC:      {etc}")
        print(f"VAC:      {vac}")
        print(f"Progress: {progress*100:.2f}%" if isinstance(progress, float) else f"Progress: {progress}")
        print("="*50)
        
        # WBS Table Row 18
        print("\nFirst WBS Element (WBS-01 - Project Management) evaluation:")
        wbs_id = ws.Range("A18").Value
        wbs_name = ws.Range("B18").Value
        wbs_bac = ws.Range("D18").Value
        wbs_pv = ws.Range("E18").Value
        wbs_ac = ws.Range("F18").Value
        wbs_prog = ws.Range("G18").Value
        wbs_ev = ws.Range("H18").Value
        wbs_cpi = ws.Range("K18").Value
        wbs_status = ws.Range("P18").Value
        
        safe_status = str(wbs_status).replace("🔴", "[RED]").replace("🟡", "[YELLOW]").replace("🟢", "[GREEN]")
        print(f"ID: {wbs_id} | Name: {wbs_name}")
        print(f"BAC: {wbs_bac} | PV: {wbs_pv} | AC: {wbs_ac} | Progress: {wbs_prog*100:.1f}% | EV: {wbs_ev} | CPI: {wbs_cpi:.3f} | Status: {safe_status}")
        
        # Weekly Trend Table Row 36 (Week 1)
        print("\nWeekly Cumulative Trend (Week 1):")
        wk_num = ws.Range("A36").Value
        wk_date = ws.Range("B36").Value
        wk_pv = ws.Range("C36").Value
        wk_cum_pv = ws.Range("D36").Value
        wk_cum_ac = ws.Range("F36").Value
        wk_cum_ev = ws.Range("G36").Value
        
        print(f"Week {wk_num} ({wk_date}) | Weekly PV: {wk_pv} | Cum PV: {wk_cum_pv} | Cum AC: {wk_cum_ac} | Cum EV: {wk_cum_ev:.2f}")
        
        # Run assertions to check accuracy
        assert abs(bac - 268650.00) < 0.01, "BAC mismatch!"
        assert abs(pv - 142900.00) < 0.01, "PV mismatch!"
        assert abs(ac - 141985.44) < 0.01, "AC mismatch!"
        assert abs(ev - 131468.00) < 0.01, "EV mismatch!"
        assert abs(cv - -10517.44) < 0.05, "CV mismatch!"
        assert abs(sv - -11432.00) < 0.05, "SV mismatch!"
        
        print("\nAll Excel-recalculated formulas matches exactly with expected mathematical results! Test PASSED.")
        
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")
        raise e
    finally:
        wb.Close(SaveChanges=False)
        excel.Quit()

if __name__ == "__main__":
    test_excel_formulas()
