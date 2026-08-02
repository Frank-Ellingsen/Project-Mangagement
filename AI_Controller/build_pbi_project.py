import os
import json
import shutil

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PBI_DIR = os.path.join(BASE_DIR, "Data", "PowerBI_Project")
PBI_NAME = "project_wessels"
SEM_MODEL_DIR = os.path.join(PBI_DIR, f"{PBI_NAME}.SemanticModel")
REPORT_DIR = os.path.join(PBI_DIR, f"{PBI_NAME}.Report")

# Ensure directories exist
for folder in [PBI_DIR, SEM_MODEL_DIR, REPORT_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def build_project_files():
    print("Generating Power BI Project (.pbip) configuration files...")

    # 1. Main .pbip file
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {"report": {"path": f"{PBI_NAME}.Report"}},
            {"semanticModel": {"path": f"{PBI_NAME}.SemanticModel"}}
        ],
        "settings": {
            "enableAutoRecovery": True,
            "reportRegistry": {
                f"{PBI_NAME}.Report": {
                    "reportId": "00000000-0000-0000-0000-000000000000"
                }
            }
        }
    }
    write_json(os.path.join(PBI_DIR, f"{PBI_NAME}.pbip"), pbip_content)

    # 2. Semantic Model definition pointing to TMDL format
    pbidataset_content = {
        "version": "1.0",
        "dataset": {"path": "."}
    }
    write_json(os.path.join(SEM_MODEL_DIR, "definition.pbidataset"), pbidataset_content)

    # Clean legacy model.bim if it exists to avoid conflicts
    model_bim_path = os.path.join(SEM_MODEL_DIR, "model.bim")
    if os.path.exists(model_bim_path):
        os.remove(model_bim_path)
        print("Removed legacy model.bim file.")

    # 3. Report target definition
    pbitarget_content = {
        "version": "1.0",
        "report": {"path": "."}
    }
    write_json(os.path.join(REPORT_DIR, "definition.pbitarget"), pbitarget_content)

    # 4. Report metadata
    page_specs = [
        {
            "id": "49e7f05a2a176419458c",
            "displayName": "Executive Overview",
            "description": "Portfolio health, KPI cards and milestone status"
        },
        {
            "id": "6b41b695c9024ef09170c164e6d39b9f",
            "displayName": "Financial Control",
            "description": "CPI, CV, EAC and S-curve trend analysis"
        },
        {
            "id": "8ed314e6a2da43fdaf1b63ef8e4f52d9c",
            "displayName": "Client Delivery",
            "description": "Progress, milestones and delivery narrative"
        }
    ]
    page_blueprints = [
        {
            "pageId": page_specs[0]["id"],
            "displayName": page_specs[0]["displayName"],
            "visuals": [
                {"type": "kpi-card", "title": "Budget at Completion", "measure": "BAC"},
                {"type": "kpi-card", "title": "Actual Cost", "measure": "AC"},
                {"type": "kpi-card", "title": "Earned Value", "measure": "EV"},
                {"type": "kpi-card", "title": "Percent Complete", "measure": "Latest Percent Complete"},
                {"type": "bar-chart", "title": "Project status by status", "category": "projects[Status]", "value": "Latest Percent Complete"}
            ]
        },
        {
            "pageId": page_specs[1]["id"],
            "displayName": page_specs[1]["displayName"],
            "visuals": [
                {"type": "line-chart", "title": "Cost and value trend", "xAxis": "physical_progress[RecordDate]", "value": "EV"},
                {"type": "variance-card", "title": "Cost Variance", "measure": "CV"},
                {"type": "variance-card", "title": "Schedule Variance", "measure": "SV"},
                {"type": "variance-card", "title": "Overall RAG", "measure": "Variance RAG"},
                {"type": "slicer", "title": "Scenario selector", "field": "ScenarioSelection[Scenario]", "placement": "top-right", "style": "button-group", "compact": True},
                {"type": "variance-card", "title": "Cost Performance Index", "measure": "CPI"},
                {"type": "variance-card", "title": "Schedule Performance Index", "measure": "SPI"}
            ]
        },
        {
            "pageId": page_specs[2]["id"],
            "displayName": page_specs[2]["displayName"],
            "visuals": [
                {"type": "progress-table", "title": "WBS delivery status", "category": "wbs_elements[ElementName]", "value": "Latest Percent Complete"},
                {"type": "stacked-bar", "title": "Milestone completion", "category": "projects[ProjectName]", "value": "Latest Percent Complete"},
                {"type": "narrative-card", "title": "Delivery narrative", "text": "Focus on late or at-risk work packages and highlight recovery actions."}
            ]
        }
    ]
    report_json_content = {
        "version": "2.0",
        "displayName": "Project Controlling Control Tower",
        "description": "Executive EVM dashboard built for portfolio monitoring and delivery reporting.",
        "defaultPage": page_specs[0]["id"],
        "theme": "Tufte",
        "pageBlueprints": page_blueprints
    }
    os.makedirs(os.path.join(REPORT_DIR, "definition"), exist_ok=True)
    write_json(os.path.join(REPORT_DIR, "definition", "report.json"), report_json_content)

    # 5. Dashboard layout blueprint and pages
    os.makedirs(os.path.join(REPORT_DIR, "definition", "pages"), exist_ok=True)
    write_json(
        os.path.join(REPORT_DIR, "definition", "pages", "pages.json"),
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
            "pageOrder": [page["id"] for page in page_specs],
            "activePageName": page_specs[0]["id"]
        }
    )
    for page in page_specs:
        pdir = os.path.join(REPORT_DIR, "definition", "pages", page["id"])
        os.makedirs(pdir, exist_ok=True)
        page_blueprint = next(item for item in page_blueprints if item["pageId"] == page["id"])
        write_json(
            os.path.join(pdir, "page.json"),
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
                "name": page["id"],
                "displayName": page["displayName"],
                "displayOption": "FitToPage",
                "height": 720,
                "width": 1280,
                "description": page["description"],
                "visualBlueprint": page_blueprint["visuals"]
            }
        )

    # 6. Generate TMDL Semantic Model definition folder
    definition_dir = os.path.join(SEM_MODEL_DIR, "definition")
    tables_dir = os.path.join(definition_dir, "tables")

    # Clean existing definition directory to ensure no old files exist
    if os.path.exists(definition_dir):
        shutil.rmtree(definition_dir)
    os.makedirs(tables_dir, exist_ok=True)

    # Write database.tmdl
    write_file(os.path.join(definition_dir, "database.tmdl"), f"database {PBI_NAME}\n")

    # Write model.tmdl
    model_tmdl_content = """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US

\tref table _Measures
\tref table ScenarioSelection
\tref table projects
\tref table wbs_elements
\tref table resources
\tref table timesheets
\tref table material_costs
\tref table physical_progress

\tref cultureInfo en-US
"""
    write_file(os.path.join(definition_dir, "model.tmdl"), model_tmdl_content)

    # Write relationships.tmdl
    relationships_tmdl_content = """relationship rel_project_wbs
\tfromColumn: wbs_elements.ProjectID
\ttoColumn: projects.ProjectID

relationship rel_wbs_timesheets
\tfromColumn: timesheets.WBS_ID
\ttoColumn: wbs_elements.WBS_ID

relationship rel_resources_timesheets
\tfromColumn: timesheets.ResourceID
\ttoColumn: resources.ResourceID

relationship rel_wbs_material_costs
\tfromColumn: material_costs.WBS_ID
\ttoColumn: wbs_elements.WBS_ID

relationship rel_wbs_physical_progress
\tfromColumn: physical_progress.WBS_ID
\ttoColumn: wbs_elements.WBS_ID
"""
    write_file(os.path.join(definition_dir, "relationships.tmdl"), relationships_tmdl_content)

    # CSV path helper
    def get_csv_path(filename):
        return os.path.join(BASE_DIR, "Data", "CSV", filename).replace("\\", "/")

    # Table: _Measures
    measures_tmdl = f"""table _Measures

\tmeasure BAC = SUM('wbs_elements'[PlannedCost])
\t\tformatString: "$#,##0.00"

\tmeasure 'Actual Labor Cost' = SUM('timesheets'[LaborCost])
\t\tformatString: "$#,##0.00"

\tmeasure 'Actual Material Cost' = SUM('material_costs'[TotalActualCost])
\t\tformatString: "$#,##0.00"

\tmeasure AC = [Actual Labor Cost] + [Actual Material Cost]
\t\tformatString: "$#,##0.00"

\tmeasure 'Latest Percent Complete' = 
\t\t\tVAR SelectedDate = MAX('physical_progress'[RecordDate])
\t\t\tRETURN
\t\t\tSUMX(
\t\t\t    VALUES('wbs_elements'[WBS_ID]),
\t\t\t    VAR LatestWBSProgressDate = CALCULATE(MAX('physical_progress'[RecordDate]), 'physical_progress'[RecordDate] <= SelectedDate)
\t\t\t    RETURN CALCULATE(MAX('physical_progress'[PercentComplete]), 'physical_progress'[RecordDate] = LatestWBSProgressDate)
\t\t\t)
\t\tformatString: "0.00%"

\tmeasure 'Planned % Complete' = 
\t\t\tVAR StartDate = MIN('projects'[StartDate])
\t\t\tVAR EndDate = MAX('projects'[EndDate])
\t\t\tVAR CurrentDate = MAX('physical_progress'[RecordDate])
\t\t\tRETURN
\t\t\tIF(
\t\t\t    EndDate <= StartDate,
\t\t\t    0,
\t\t\t    DIVIDE(DATEDIFF(StartDate, CurrentDate, DAY), DATEDIFF(StartDate, EndDate, DAY), 0)
\t\t\t)
\t\tformatString: "0.00%"

\tmeasure EV = SUMX(VALUES('wbs_elements'[WBS_ID]), [BAC] * [Latest Percent Complete])
\t\tformatString: "$#,##0.00"

\tmeasure PV = [BAC] * [Planned % Complete]
\t\tformatString: "$#,##0.00"

\tmeasure SV = [EV] - [PV]
\t\tformatString: "$#,##0.00"

\tmeasure CV = [EV] - [AC]
\t\tformatString: "$#,##0.00"

\tmeasure 'Variance RAG' = 
\t\t\tVAR Scenario = SELECTEDVALUE(ScenarioSelection[Scenario], "Baseline")
\t\t\tVAR CostVariancePct = DIVIDE([CV], [BAC], 0)
\t\t\tVAR ScheduleVariancePct = DIVIDE([SV], [BAC], 0)
\t\t\tVAR CostAmberThreshold = SWITCH(Scenario, "Conservative", 0.08, "Baseline", 0.12, "Aggressive", 0.18, 0.12)
\t\t\tVAR CostRedThreshold = SWITCH(Scenario, "Conservative", 0.15, "Baseline", 0.20, "Aggressive", 0.30, 0.20)
\t\t\tVAR ScheduleAmberThreshold = SWITCH(Scenario, "Conservative", 0.05, "Baseline", 0.10, "Aggressive", 0.15, 0.10)
\t\t\tVAR ScheduleRedThreshold = SWITCH(Scenario, "Conservative", 0.10, "Baseline", 0.15, "Aggressive", 0.25, 0.15)
\t\t\tRETURN
\t\t\tSWITCH(
\t\t\t    TRUE(),
\t\t\t    ABS(CostVariancePct) >= CostRedThreshold || ABS(ScheduleVariancePct) >= ScheduleRedThreshold, "Red",
\t\t\t    ABS(CostVariancePct) >= CostAmberThreshold || ABS(ScheduleVariancePct) >= ScheduleAmberThreshold, "Amber",
\t\t\t    "Green"
\t\t\t)
\t\tformatString: "@"

\tmeasure CPI = DIVIDE([EV], [AC], 1.0)
\t\tformatString: "0.00"

\tmeasure SPI = DIVIDE([EV], [PV], 1.0)
\t\tformatString: "0.00"

\tmeasure 'EAC (Typical)' = DIVIDE([BAC], [CPI], [BAC])
\t\tformatString: "$#,##0.00"

\tmeasure 'EAC (Atypical)' = [AC] + ([BAC] - [EV])
\t\tformatString: "$#,##0.00"

\tmeasure ETC = [EAC (Typical)] - [AC]
\t\tformatString: "$#,##0.00"

\tmeasure VAC = [BAC] - [EAC (Typical)]
\t\tformatString: "$#,##0.00"

\tcolumn MeasurePlaceholder
\t\tdataType: int64
\t\tisHidden
\t\tsourceColumn: MeasurePlaceholder

\tpartition MeasuresPartition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasurePlaceholder = _t]),
\t\t\t\t    Type = Table.TransformColumnTypes(Source,{{"MeasurePlaceholder", Int64.Type}})
\t\t\t\tin
\t\t\t\t    Type
"""
    write_file(os.path.join(tables_dir, "_Measures.tmdl"), measures_tmdl)

    # Table: ScenarioSelection
    scenarios_tmdl = """table ScenarioSelection

\tcolumn Scenario
\t\tdataType: string
\t\tsourceColumn: Scenario

\tpartition ScenarioSelection-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = #table({"Scenario"}, {{"Conservative"}, {"Baseline"}, {"Aggressive"}})
\t\t\t\tin
\t\t\t\t    Source
"""
    write_file(os.path.join(tables_dir, "ScenarioSelection.tmdl"), scenarios_tmdl)

    # Table: projects
    projects_tmdl = f"""table projects

\tcolumn ProjectID
\t\tdataType: string
\t\tsourceColumn: ProjectID

\tcolumn ProjectName
\t\tdataType: string
\t\tsourceColumn: ProjectName

\tcolumn ProjectManager
\t\tdataType: string
\t\tsourceColumn: ProjectManager

\tcolumn BudgetAtCompletion_BAC
\t\tdataType: double
\t\tformatString: "$#,##0.00"
\t\tsourceColumn: BudgetAtCompletion_BAC

\tcolumn StartDate
\t\tdataType: dateTime
\t\tformatString: "yyyy-MM-dd"
\t\tsourceColumn: StartDate

\tcolumn EndDate
\t\tdataType: dateTime
\t\tformatString: "yyyy-MM-dd"
\t\tsourceColumn: EndDate

\tcolumn Status
\t\tdataType: string
\t\tsourceColumn: Status

\tpartition projects-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('projects.csv')}"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])
\t\t\t\tin
\t\t\t\t    Headers
"""
    write_file(os.path.join(tables_dir, "projects.tmdl"), projects_tmdl)

    # Table: wbs_elements
    wbs_tmdl = f"""table wbs_elements

\tcolumn WBS_ID
\t\tdataType: string
\t\tsourceColumn: WBS_ID

\tcolumn ProjectID
\t\tdataType: string
\t\tsourceColumn: ProjectID

\tcolumn WBS_Code
\t\tdataType: string
\t\tsourceColumn: WBS_Code

\tcolumn ElementName
\t\tdataType: string
\t\tsourceColumn: ElementName

\tcolumn PlannedCost
\t\tdataType: double
\t\tformatString: "$#,##0.00"
\t\tsourceColumn: PlannedCost

\tcolumn PlannedHours
\t\tdataType: double
\t\tsourceColumn: PlannedHours

\tpartition wbs_elements-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('wbs_elements.csv')}"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])
\t\t\t\tin
\t\t\t\t    Headers
"""
    write_file(os.path.join(tables_dir, "wbs_elements.tmdl"), wbs_tmdl)

    # Table: resources
    resources_tmdl = f"""table resources

\tcolumn ResourceID
\t\tdataType: string
\t\tsourceColumn: ResourceID

\tcolumn ResourceName
\t\tdataType: string
\t\tsourceColumn: ResourceName

\tcolumn Role
\t\tdataType: string
\t\tsourceColumn: Role

\tcolumn HourlyRate
\t\tdataType: double
\t\tformatString: "$#,##0.00"
\t\tsourceColumn: HourlyRate

\tpartition resources-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('resources.csv')}"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])
\t\t\t\tin
\t\t\t\t    Headers
"""
    write_file(os.path.join(tables_dir, "resources.tmdl"), resources_tmdl)

    # Table: timesheets
    timesheets_tmdl = f"""table timesheets

\tcolumn TimesheetID
\t\tdataType: string
\t\tsourceColumn: TimesheetID

\tcolumn ResourceID
\t\tdataType: string
\t\tsourceColumn: ResourceID

\tcolumn WBS_ID
\t\tdataType: string
\t\tsourceColumn: WBS_ID

\tcolumn WorkDate
\t\tdataType: dateTime
\t\tformatString: "yyyy-MM-dd"
\t\tsourceColumn: WorkDate

\tcolumn HoursWorked
\t\tdataType: double
\t\tsourceColumn: HoursWorked

\tcolumn ApprovalStatus
\t\tdataType: string
\t\tsourceColumn: ApprovalStatus

\tcolumn LaborCost
\t\tdataType: double
\t\tformatString: "$#,##0.00"
\t\tsourceColumn: LaborCost

\tpartition timesheets-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('timesheets.csv')}"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
\t\t\t\t    Types = Table.TransformColumnTypes(Headers, {{"HoursWorked", type number}}),
\t\t\t\t    MergeRes = Table.NestedJoin(Types, {{"ResourceID"}}, resources, {{"ResourceID"}}, "res", JoinKind.LeftOuter),
\t\t\t\t    ExpandRes = Table.ExpandTableColumn(MergeRes, "res", {{"HourlyRate"}}, {{"HourlyRate"}}),
\t\t\t\t    TypeRate = Table.TransformColumnTypes(ExpandRes, {{"HourlyRate", type number}}),
\t\t\t\t    AddLabor = Table.AddColumn(TypeRate, "LaborCost", each [HoursWorked] * [HourlyRate], type number)
\t\t\t\tin
\t\t\t\t    AddLabor
"""
    write_file(os.path.join(tables_dir, "timesheets.tmdl"), timesheets_tmdl)

    # Table: material_costs
    material_tmdl = f"""table material_costs

\tcolumn PurchaseID
\t\tdataType: string
\t\tsourceColumn: PurchaseID

\tcolumn WBS_ID
\t\tdataType: string
\t\tsourceColumn: WBS_ID

\tcolumn PurchaseDate
\t\tdataType: dateTime
\t\tformatString: "yyyy-MM-dd"
\t\tsourceColumn: PurchaseDate

\tcolumn Description
\t\tdataType: string
\t\tsourceColumn: Description

\tcolumn Quantity
\t\tdataType: int64
\t\tsourceColumn: Quantity

\tcolumn UnitPrice
\t\tdataType: double
\t\tformatString: "$#,##0.00"
\t\tsourceColumn: UnitPrice

\tcolumn TotalActualCost
\t\tdataType: double
\t\tformatString: "$#,##0.00"
\t\tsourceColumn: TotalActualCost

\tpartition material_costs-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('material_costs.csv')}"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])
\t\t\t\tin
\t\t\t\t    Headers
"""
    write_file(os.path.join(tables_dir, "material_costs.tmdl"), material_tmdl)

    # Table: physical_progress
    progress_tmdl = f"""table physical_progress

\tcolumn ProgressID
\t\tdataType: string
\t\tsourceColumn: ProgressID

\tcolumn WBS_ID
\t\tdataType: string
\t\tsourceColumn: WBS_ID

\tcolumn RecordDate
\t\tdataType: dateTime
\t\tformatString: "yyyy-MM-dd"
\t\tsourceColumn: RecordDate

\tcolumn PercentComplete
\t\tdataType: double
\t\tformatString: "0.00%"
\t\tsourceColumn: PercentComplete

\tcolumn ReportedBy
\t\tdataType: string
\t\tsourceColumn: ReportedBy

\tpartition physical_progress-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('physical_progress.csv')}"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])
\t\t\t\tin
\t\t\t\t    Headers
"""
    write_file(os.path.join(tables_dir, "physical_progress.tmdl"), progress_tmdl)

    readme_content = """# Power BI project package

This folder now contains a richer Power BI project package aligned with the overall project guidelines for the Control Tower.

## What is included
- A three-page report structure for executive, financial and delivery audiences.
- A semantic model blueprint based on the project portfolio CSV files.
- Core EVM measures for BAC, AC, EV, CV, CPI, SPI, EAC and VAC.
- A dashboard blueprint ready for further report authoring in Power BI Desktop.

## Recommended visuals
1. Executive Overview: KPI cards, overall progress bar and milestone health.
2. Financial Control: S-curve, variance cards and WBS breakdown table.
3. Client Delivery: Milestone trend, delivery narrative and completion status.
"""
    write_file(os.path.join(PBI_DIR, "README.md"), readme_content)

    print(f"Power BI Project TMDL compiled successfully at: {os.path.join(PBI_DIR, f'{PBI_NAME}.pbip')}")


if __name__ == "__main__":
    build_project_files()
