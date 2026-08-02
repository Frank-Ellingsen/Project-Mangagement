import os
import json

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

    # 2. Semantic Model definition
    pbidataset_content = {
        "version": "1.0",
        "dataset": {"path": "."}
    }
    write_json(os.path.join(SEM_MODEL_DIR, "definition.pbidataset"), pbidataset_content)

    # 3. Report target definition
    pbitarget_content = {
        "version": "1.0",
        "report": {"path": "."}
    }
    write_json(os.path.join(REPORT_DIR, "definition.pbitarget"), pbitarget_content)

    # 4. Richer report metadata
    report_json_content = {
        "version": "2.0",
        "displayName": "Project Controlling Control Tower",
        "description": "Executive EVM dashboard built for portfolio monitoring and delivery reporting.",
        "defaultPage": "overview",
        "theme": "Tufte"
    }
    write_json(os.path.join(REPORT_DIR, "definition", "report.json"), report_json_content)

    # 5. Dashboard layout blueprint and pages
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
        write_json(
            os.path.join(pdir, "page.json"),
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
                "name": page["id"],
                "displayName": page["displayName"],
                "displayOption": "FitToPage",
                "height": 720,
                "width": 1280,
                "description": page["description"]
            }
        )

    # 6. Semantic Model schema definition (model.bim)
    model_bim = {
        "name": PBI_NAME.replace("_", " ").title().replace(" ", "_"),
        "compatibilityLevel": 1570,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "PowerBI_V3",
            "sourceQueryCulture": "en-US",
            "tables": [
                {
                    "name": "_Measures",
                    "columns": [
                        {
                            "name": "MeasurePlaceholder",
                            "dataType": "int64",
                            "isHidden": True,
                            "sourceColumn": "MeasurePlaceholder"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "MeasuresPartition",
                            "source": {
                                "type": "m",
                                "expression": "let\n    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText(\"i44FAA==\", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasurePlaceholder = _t]),\n    Type = Table.TransformColumnTypes(Source,{{\"MeasurePlaceholder\", Int64.Type}})\nin\n    Type"
                            }
                        }
                    ],
                    "measures": [
                        {"name": "BAC", "expression": "SUM('wbs_elements'[PlannedCost])", "formatString": "$#,##0.00"},
                        {"name": "Actual Labor Cost", "expression": "SUM('timesheets'[LaborCost])", "formatString": "$#,##0.00"},
                        {"name": "Actual Material Cost", "expression": "SUM('material_costs'[TotalActualCost])", "formatString": "$#,##0.00"},
                        {"name": "AC", "expression": "[Actual Labor Cost] + [Actual Material Cost]", "formatString": "$#,##0.00"},
                        {"name": "Latest Percent Complete", "expression": "VAR SelectedDate = MAX('physical_progress'[RecordDate])\nRETURN\nSUMX(\n    VALUES('wbs_elements'[WBS_ID]),\n    VAR LatestWBSProgressDate = CALCULATE(MAX('physical_progress'[RecordDate]), 'physical_progress'[RecordDate] <= SelectedDate)\n    RETURN CALCULATE(MAX('physical_progress'[PercentComplete]), 'physical_progress'[RecordDate] = LatestWBSProgressDate)\n)", "formatString": "0.00%"},
                        {"name": "EV", "expression": "SUMX(VALUES('wbs_elements'[WBS_ID]), [BAC] * [Latest Percent Complete])", "formatString": "$#,##0.00"},
                        {"name": "CV", "expression": "[EV] - [AC]", "formatString": "$#,##0.00"},
                        {"name": "CPI", "expression": "DIVIDE([EV], [AC], 1.0)", "formatString": "0.00"},
                        {"name": "SPI", "expression": "DIVIDE([EV], [BAC], 1.0)", "formatString": "0.00"},
                        {"name": "EAC (Typical)", "expression": "DIVIDE([BAC], [CPI], [BAC])", "formatString": "$#,##0.00"},
                        {"name": "VAC", "expression": "[BAC] - [EAC (Typical)]", "formatString": "$#,##0.00"}
                    ]
                },
                {
                    "name": "projects",
                    "columns": [
                        {"name": "ProjectID", "dataType": "string", "sourceColumn": "ProjectID"},
                        {"name": "ProjectName", "dataType": "string", "sourceColumn": "ProjectName"},
                        {"name": "ProjectManager", "dataType": "string", "sourceColumn": "ProjectManager"},
                        {"name": "BudgetAtCompletion_BAC", "dataType": "double", "sourceColumn": "BudgetAtCompletion_BAC", "formatString": "$#,##0.00"},
                        {"name": "StartDate", "dataType": "dateTime", "sourceColumn": "StartDate"},
                        {"name": "EndDate", "dataType": "dateTime", "sourceColumn": "EndDate"},
                        {"name": "Status", "dataType": "string", "sourceColumn": "Status"}
                    ],
                    "partitions": [{"name": "projects-Partition", "source": {"type": "m", "expression": f'let\n    Source = Csv.Document(File.Contents("{os.path.join(BASE_DIR, "Data", "CSV", "projects.csv").replace("\\\\", "/")}"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])\nin\n    Headers'}}]
                },
                {
                    "name": "wbs_elements",
                    "columns": [
                        {"name": "WBS_ID", "dataType": "string", "sourceColumn": "WBS_ID"},
                        {"name": "ProjectID", "dataType": "string", "sourceColumn": "ProjectID"},
                        {"name": "WBS_Code", "dataType": "string", "sourceColumn": "WBS_Code"},
                        {"name": "ElementName", "dataType": "string", "sourceColumn": "ElementName"},
                        {"name": "PlannedCost", "dataType": "double", "sourceColumn": "PlannedCost", "formatString": "$#,##0.00"},
                        {"name": "PlannedHours", "dataType": "double", "sourceColumn": "PlannedHours"}
                    ],
                    "partitions": [{"name": "wbs_elements-Partition", "source": {"type": "m", "expression": f'let\n    Source = Csv.Document(File.Contents("{os.path.join(BASE_DIR, "Data", "CSV", "wbs_elements.csv").replace("\\\\", "/")}"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])\nin\n    Headers'}}]
                },
                {
                    "name": "resources",
                    "columns": [
                        {"name": "ResourceID", "dataType": "string", "sourceColumn": "ResourceID"},
                        {"name": "ResourceName", "dataType": "string", "sourceColumn": "ResourceName"},
                        {"name": "Role", "dataType": "string", "sourceColumn": "Role"},
                        {"name": "HourlyRate", "dataType": "double", "sourceColumn": "HourlyRate", "formatString": "$#,##0.00"}
                    ],
                    "partitions": [{"name": "resources-Partition", "source": {"type": "m", "expression": f'let\n    Source = Csv.Document(File.Contents("{os.path.join(BASE_DIR, "Data", "CSV", "resources.csv").replace("\\\\", "/")}"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])\nin\n    Headers'}}]
                },
                {
                    "name": "timesheets",
                    "columns": [
                        {"name": "TimesheetID", "dataType": "string", "sourceColumn": "TimesheetID"},
                        {"name": "ResourceID", "dataType": "string", "sourceColumn": "ResourceID"},
                        {"name": "WBS_ID", "dataType": "string", "sourceColumn": "WBS_ID"},
                        {"name": "WorkDate", "dataType": "dateTime", "sourceColumn": "WorkDate"},
                        {"name": "HoursWorked", "dataType": "double", "sourceColumn": "HoursWorked"},
                        {"name": "ApprovalStatus", "dataType": "string", "sourceColumn": "ApprovalStatus"},
                        {"name": "LaborCost", "dataType": "double", "sourceColumn": "LaborCost", "formatString": "$#,##0.00"}
                    ],
                    "partitions": [{"name": "timesheets-Partition", "source": {"type": "m", "expression": f'let\n    Source = Csv.Document(File.Contents("{os.path.join(BASE_DIR, "Data", "CSV", "timesheets.csv").replace("\\\\", "/")}"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),\n    Types = Table.TransformColumnTypes(Headers, {{"HoursWorked", type number}}),\n    MergeRes = Table.NestedJoin(Types, {{"ResourceID"}}, resources, {{"ResourceID"}}, "res", JoinKind.LeftOuter),\n    ExpandRes = Table.ExpandTableColumn(MergeRes, "res", {{"HourlyRate"}}, {{"HourlyRate"}}),\n    TypeRate = Table.TransformColumnTypes(ExpandRes, {{"HourlyRate", type number}}),\n    AddLabor = Table.AddColumn(TypeRate, "LaborCost", each [HoursWorked] * [HourlyRate], type number)\nin\n    AddLabor'}}]
                },
                {
                    "name": "material_costs",
                    "columns": [
                        {"name": "PurchaseID", "dataType": "string", "sourceColumn": "PurchaseID"},
                        {"name": "WBS_ID", "dataType": "string", "sourceColumn": "WBS_ID"},
                        {"name": "PurchaseDate", "dataType": "dateTime", "sourceColumn": "PurchaseDate"},
                        {"name": "Description", "dataType": "string", "sourceColumn": "Description"},
                        {"name": "Quantity", "dataType": "int64", "sourceColumn": "Quantity"},
                        {"name": "UnitPrice", "dataType": "double", "sourceColumn": "UnitPrice", "formatString": "$#,##0.00"},
                        {"name": "TotalActualCost", "dataType": "double", "sourceColumn": "TotalActualCost", "formatString": "$#,##0.00"}
                    ],
                    "partitions": [{"name": "material_costs-Partition", "source": {"type": "m", "expression": f'let\n    Source = Csv.Document(File.Contents("{os.path.join(BASE_DIR, "Data", "CSV", "material_costs.csv").replace("\\\\", "/")}"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])\nin\n    Headers'}}]
                },
                {
                    "name": "physical_progress",
                    "columns": [
                        {"name": "ProgressID", "dataType": "string", "sourceColumn": "ProgressID"},
                        {"name": "WBS_ID", "dataType": "string", "sourceColumn": "WBS_ID"},
                        {"name": "RecordDate", "dataType": "dateTime", "sourceColumn": "RecordDate"},
                        {"name": "PercentComplete", "dataType": "double", "sourceColumn": "PercentComplete"},
                        {"name": "ReportedBy", "dataType": "string", "sourceColumn": "ReportedBy"}
                    ],
                    "partitions": [{"name": "physical_progress-Partition", "source": {"type": "m", "expression": f'let\n    Source = Csv.Document(File.Contents("{os.path.join(BASE_DIR, "Data", "CSV", "physical_progress.csv").replace("\\\\", "/")}"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])\nin\n    Headers'}}]
                }
            ],
            "relationships": [
                {"name": "rel_project_wbs", "fromTable": "wbs_elements", "fromColumn": "ProjectID", "toTable": "projects", "toColumn": "ProjectID"},
                {"name": "rel_wbs_timesheets", "fromTable": "timesheets", "fromColumn": "WBS_ID", "toTable": "wbs_elements", "toColumn": "WBS_ID"},
                {"name": "rel_resources_timesheets", "fromTable": "timesheets", "fromColumn": "ResourceID", "toTable": "resources", "toColumn": "ResourceID"},
                {"name": "rel_wbs_material_costs", "fromTable": "material_costs", "fromColumn": "WBS_ID", "toTable": "wbs_elements", "toColumn": "WBS_ID"},
                {"name": "rel_wbs_physical_progress", "fromTable": "physical_progress", "fromColumn": "WBS_ID", "toTable": "wbs_elements", "toColumn": "WBS_ID"}
            ]
        }
    }
    write_json(os.path.join(SEM_MODEL_DIR, "model.bim"), model_bim)

    # 7. Dashboard blueprint for future report authoring
    dashboard_blueprint = {
        "reportName": PBI_NAME,
        "designPrinciples": [
            "Tufte-inspired minimalism",
            "Direct labels and clear KPI thresholds",
            "Executive narrative over decoration"
        ],
        "pages": page_specs,
        "coreMeasures": ["BAC", "AC", "EV", "CV", "CPI", "SPI", "EAC (Typical)", "VAC", "Latest Percent Complete"],
        "dataSources": ["projects", "wbs_elements", "timesheets", "material_costs", "physical_progress", "resources"]
    }
    write_json(os.path.join(PBI_DIR, "dashboard_structure.json"), dashboard_blueprint)

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
    with open(os.path.join(PBI_DIR, "README.md"), "w", encoding="utf-8") as handle:
        handle.write(readme_content)

    print(f"Power BI Project compiled successfully at: {os.path.join(PBI_DIR, f'{PBI_NAME}.pbip')}")


if __name__ == "__main__":
    build_project_files()
