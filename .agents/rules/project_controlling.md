# Workspace Rules: Project Controlling & EVM

This rule file applies specifically to the `Project Mng` workspace directory.

## 1. Directory Structure Organization

All agents must respect the organized directory layout:

- **docs/personal/**: Resumes, CV matching, and study syllabus.
- **docs/methodology/**: Project management theory and glossaries.
- **docs/templates/**: Project management documents and templates.
- **docs/visuals/**: Visual assets and diagram source material.
- **AI_Controller/**: Technical code, database schemas, and data pipelines.
- **Data/**: Relational CSVs plus generated analytical databases.

## 2. Mock Data & Database Relational Rules

- Relational database tables are stored as standard CSVs in [`Data/CSV/`](../../Data/CSV).
- Semicolon-separated CSV versions for Excel are stored in [`Data/CSV/excel_friendly/`](../../Data/CSV/excel_friendly).
- Always reference [`AI_Controller/datamodel_erd.md`](../../AI_Controller/datamodel_erd.md) when generating queries, Python scripts, or schema explanations.

## 3. EVM Formula Standardisation

When calculating project performance metrics, always use the following formulas:

- **Earned Value (EV)**: `BAC * Physical Progress %`
- **Cost Variance (CV)**: `EV - AC`
- **Schedule Variance (SV)**: `EV - PV`
- **Cost Performance Index (CPI)**: `EV / AC` (Favorable if > 1.0)
- **Schedule Performance Index (SPI)**: `EV / PV` (Favorable if > 1.0)
- **Estimate at Completion (EAC)**: `BAC / CPI` (For typical variances) or `AC + (BAC - EV)` (For atypical variances)
