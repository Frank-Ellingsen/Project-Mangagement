# PBIP Conformance Review — 2026-08-02

Scope:

- `project_wessels.pbip`
- `project_wessels.Report`
- `project_wessels.SemanticModel`
- Markdown guidance in `Data/PowerBI_Project/*.md`

## 1) Package linkage

- [x] `.pbip` contains both required artifacts (`report`, `semanticModel`).
- [x] Report reference path points to local report folder.
- [x] Dataset reference in `definition.pbir` points to `../project_wessels.SemanticModel`.

## 2) Semantic model scope vs guidance

- [x] Core tables aligned with docs: `projects`, `wbs_elements`, `resources`, `timesheets`, `material_costs`, `physical_progress`, `ScenarioSelection`.
- [x] Measure table present: `_Measures`.
- [x] Relationships present for documented model grain.

## 3) EVM/DAX measure coverage vs guidance

- [x] Present: `BAC`, `AC`, `EV`, `PV`, `SV`, `CV`, `CPI`, `SPI`, `EAC (Typical)`, `VAC`, `Latest Percent Complete`, `Variance RAG`.
- [x] Scenario selector table and logic (`Conservative`, `Baseline`, `Aggressive`) present.

## 4) Hardening fixes applied in this pass

- [x] Fixed M type conversion syntax in generated artifact:
  - `project_wessels.SemanticModel/definition/tables/timesheets.tmdl`
  - `project_wessels.SemanticModel/definition/tables/_Measures.tmdl`

- [x] Made `Planned % Complete` safer by clamping to `[0,1]`:
  - `project_wessels.SemanticModel/definition/tables/_Measures.tmdl`

- [x] Persisted fixes in generator:
  - `AI_Controller/build_pbi_project.py`

## 5) Report implementation depth vs design markdown

- [x] Structure aligns (3 pages + expected themes/intent).
- [x] Financial Control blueprint now includes KPI row, scenario slicer, PV/EV/AC S-curve, WBS performance table, variance cards, and narrative guidance metadata.
- [x] Executive and Client pages now include expanded blueprint metadata (summary/matrix coverage) aligned with `financial_control_page_draft.md` and supporting markdown guidance.
- [~] Report remains `BlueprintPlus` (metadata-rich blueprint), not a full pixel-authored PBIR visual container export from Power BI Desktop.

Legend:

- `[x]` complete / aligned
- `[~]` partially aligned
- `[ ]` missing

## 6) Recommended next step

Open `project_wessels.pbip` in Power BI Desktop and validate semantic refresh. If needed, complete the final promotion step by saving a Desktop-authored PBIR export to generate full visual-container layout metadata.
