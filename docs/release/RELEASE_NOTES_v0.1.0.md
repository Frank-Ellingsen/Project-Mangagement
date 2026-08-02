# Project Controlling Control Tower — v0.1.0

## Highlights

- Introduced a complete **Project Controlling + EVM Control Tower** workflow for a 6-project portfolio.
- Added deterministic local pipeline orchestration via `run_all.ps1`.
- Delivered dual-database backend architecture:
  - DuckDB for analytical views
  - SQLite for transactional and audit workflows
- Included interactive reporting surfaces:
  - Streamlit control tower app (`AI_Controller/agent_skills_app.py`)
  - Tufte-style CLI dashboard (`AI_Controller/tufte_cli_dashboard.py`)
  - Power BI project compiler (`AI_Controller/build_pbi_project.py`)
  - Excel board-style reporting (`AI_Controller/excel_report_agent.py`)
- Added AI/agent audit execution flow via `AI_Controller/run_agents.py`.

## Documentation & Release Quality Improvements

- Corrected launcher guidance in Streamlit user docs:
  - Fixed code block format for PowerShell command
  - Corrected menu option for Streamlit launch from `[7]` to `[8]`
- Updated README pipeline references:
  - Corrected full pipeline option to `[9]`
  - Corrected full pipeline step range to `1–7`
- Added an explicit **Pre-publication Quality Gate** section in `README.md`.
- Added GitHub Actions CI smoke workflow at `.github/workflows/ci.yml` to validate core scripts on push/PR.

## Validation Performed

The following release smoke workflow was executed successfully:

1. `python -m compileall -q AI_Controller`
2. `python AI_Controller/build_duckdb.py`
3. `python AI_Controller/build_sqlite.py`
4. `python AI_Controller/verify_dataset.py`
5. `python AI_Controller/tufte_cli_dashboard.py`
6. `python AI_Controller/excel_report_agent.py`
7. `python AI_Controller/build_pbi_project.py`
8. `python AI_Controller/run_agents.py`
9. `python AI_Controller/export_executive_report.py`

## Notes

- Data is simulated/mock for demonstration and learning purposes.
- CI is configured to run smoke checks using Python 3.10.
- Recommended next hardening step: add a repository `LICENSE` file before broad public distribution.
