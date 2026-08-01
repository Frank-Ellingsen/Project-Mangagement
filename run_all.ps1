# Project Controlling Workspace Master Launcher
Clear-Host

Write-Host "=========================================================================" -ForegroundColor Cyan
Write-Host "  PROJECT CONTROLLING WORKSPACE MASTER LAUNCHER (TUFTE STYLE)" -ForegroundColor Cyan
Write-Host "=========================================================================" -ForegroundColor Cyan

function Show-Menu {
    Write-Host ""
    Write-Host "  [1] Build Databases (DuckDB & SQLite)"
    Write-Host "  [2] Run EVM Data Verification check"
    Write-Host "  [3] Print Tufte CLI Performance Dashboard"
    Write-Host "  [4] Run Excel Reports Agent"
    Write-Host "  [5] Compile Power BI Project (.pbip)"
    Write-Host "  [6] Run Agentic Control Crew Audits"
    Write-Host "  [7] Run Executive Board Report Exporters (MD & PDF)"
    Write-Host "  [8] Start Interactive Streamlit Dashboard"
    Write-Host "  [9] Run Pipeline (All steps 1 to 7 in sequence)"
    Write-Host "  [10] Exit"
    Write-Host ""
}

do {
    Show-Menu
    $choice = Read-Host "Select an option [1-10]"
    Write-Host ""

    switch ($choice) {
        "1" {
            Write-Host "--- Compiling DuckDB & SQLite Databases ---" -ForegroundColor Yellow
            python AI_Controller/build_duckdb.py
            python AI_Controller/build_sqlite.py
        }
        "2" {
            Write-Host "--- Executing Verification Checks ---" -ForegroundColor Yellow
            python AI_Controller/verify_dataset.py
        }
        "3" {
            Write-Host "--- Launching Tufte CLI Dashboard ---" -ForegroundColor Yellow
            python AI_Controller/tufte_cli_dashboard.py
        }
        "4" {
            Write-Host "--- Executing Excel Reports Agent ---" -ForegroundColor Yellow
            python AI_Controller/excel_report_agent.py
        }
        "5" {
            Write-Host "--- Compiling Power BI Project ---" -ForegroundColor Yellow
            python AI_Controller/build_pbi_project.py
        }
        "6" {
            Write-Host "--- Running Agentic Control Crew Audits ---" -ForegroundColor Yellow
            python AI_Controller/run_agents.py
        }
        "7" {
            Write-Host "--- Running Executive Board Report Exporters (MD & PDF) ---" -ForegroundColor Yellow
            python AI_Controller/export_executive_report.py
            python AI_Controller/export_pdf_report.py
        }
        "8" {
            Write-Host "--- Starting Agent Control Tower Streamlit App ---" -ForegroundColor Yellow
            streamlit run AI_Controller/agent_skills_app.py
        }
        "9" {
            Write-Host "==============================================" -ForegroundColor Green
            Write-Host " STARTING SYSTEM PIPELINE SEQUENCE" -ForegroundColor Green
            Write-Host "==============================================" -ForegroundColor Green
            
            Write-Host "`n[Step 1/7] Building Databases..." -ForegroundColor Cyan
            python AI_Controller/build_duckdb.py
            python AI_Controller/build_sqlite.py
            
            Write-Host "`n[Step 2/7] Running Data Verification..." -ForegroundColor Cyan
            python AI_Controller/verify_dataset.py
            
            Write-Host "`n[Step 3/7] Displaying CLI Dashboard..." -ForegroundColor Cyan
            python AI_Controller/tufte_cli_dashboard.py
            
            Write-Host "`n[Step 4/7] Compiling Excel Reports..." -ForegroundColor Cyan
            python AI_Controller/excel_report_agent.py
            
            Write-Host "`n[Step 5/7] Compiling Power BI Project..." -ForegroundColor Cyan
            python AI_Controller/build_pbi_project.py
            
            Write-Host "`n[Step 6/7] Executing Agent Crew..." -ForegroundColor Cyan
            python AI_Controller/run_agents.py
            
            Write-Host "`n[Step 7/7] Exporting Board Reports (MD & PDF)..." -ForegroundColor Cyan
            python AI_Controller/export_executive_report.py
            python AI_Controller/export_pdf_report.py
            
            Write-Host "`n==============================================" -ForegroundColor Green
            Write-Host " PIPELINE SEQUENCE COMPLETED SUCCESSFULLY" -ForegroundColor Green
            Write-Host "==============================================" -ForegroundColor Green
        }
        "10" {
            Write-Host "Exiting Master Launcher. Goodbye!" -ForegroundColor Green
            break
        }
        default {
            Write-Host "Invalid choice. Please select 1-10." -ForegroundColor Red
        }
    }
    
    if ($choice -ne "10") {
        Write-Host ""
        Read-Host "Press Enter to return to menu"
        Clear-Host
        Write-Host "=========================================================================" -ForegroundColor Cyan
        Write-Host "  PROJECT CONTROLLING WORKSPACE MASTER LAUNCHER (TUFTE STYLE)" -ForegroundColor Cyan
        Write-Host "=========================================================================" -ForegroundColor Cyan
    }
} while ($choice -ne "10")
