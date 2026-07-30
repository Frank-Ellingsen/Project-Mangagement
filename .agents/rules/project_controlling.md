# Workspace Rules: Project Controlling & EVM

This rule file applies specifically to the `Project Mng` workspace directory.

## 1. Directory Structure Organization
All agents must respect the organized directory layout:
* **Career/**: Resumes, CV matching, and study syllabus.
* **Methodology/**: Project management theory and glossaries.
* **Templates/**: Project management documents and charts.
* **AI_Controller/**: Technical code, database schemas, and data pipelines.
* **Visuals/**: Architecture maps and visual figures.

## 2. Mock Data & Database Relational Rules
* Relational database tables are stored as standard CSVs in [AI_Controller/mock_data/](file:///c:/Users/frank/Desktop/Project%20Mng/AI_Controller/mock_data).
* Semicolon-separated CSV versions for Excel are stored in [AI_Controller/mock_data/excel_friendly/](file:///c:/Users/frank/Desktop/Project%20Mng/AI_Controller/mock_data/excel_friendly).
* Always reference [datamodel_erd.md](file:///c:/Users/frank/Desktop/Project%20Mng/AI_Controller/datamodel_erd.md) when generating queries, Python scripts, or schema explanations.

## 3. EVM Formula Standardisation
When calculating project performance metrics, always use the following formulas:
* **Earned Value (EV)**: `BAC * Physical Progress %`
* **Cost Variance (CV)**: `EV - AC`
* **Schedule Variance (SV)**: `EV - PV`
* **Cost Performance Index (CPI)**: `EV / AC` (Favorable if > 1.0)
* **Schedule Performance Index (SPI)**: `EV / PV` (Favorable if > 1.0)
* **Estimate at Completion (EAC)**: `BAC / CPI` (For typical variances) or `AC + (BAC - EV)` (For atypical variances)
