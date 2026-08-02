import os
import json
import shutil

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PBI_DIR = os.path.join(BASE_DIR, "Reports")
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
            {"report": {"path": f"{PBI_NAME}.Report"}}
        ],
        "settings": {
            "enableAutoRecovery": True
        }
    }
    write_json(os.path.join(PBI_DIR, f"{PBI_NAME}.pbip"), pbip_content)

    # 2. Clean legacy/conflicting semantic model descriptors
    pbidataset_path = os.path.join(SEM_MODEL_DIR, "definition.pbidataset")
    if os.path.exists(pbidataset_path):
        os.remove(pbidataset_path)
        print("Removed conflicting definition.pbidataset file.")

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

    # 3b. Report definition properties
    definition_pbir_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {
            "byPath": {
                "path": f"../{PBI_NAME}.SemanticModel"
            }
        }
    }
    write_json(os.path.join(REPORT_DIR, "definition.pbir"), definition_pbir_content)

    # 4. Report metadata
    page_specs = [
        {
            "id": "ReportSection",
            "displayName": "Executive Overview",
            "description": "Portfolio health, KPI cards and milestone status"
        },
        {
            "id": "ReportSection1",
            "displayName": "Financial Control",
            "description": "CPI, CV, EAC and S-curve trend analysis"
        },
        {
            "id": "ReportSection2",
            "displayName": "Client Delivery",
            "description": "Progress, milestones and delivery narrative"
        },
        {
            "id": "ReportSection3",
            "displayName": "Risk & Issues (RAID)",
            "description": "Risk matrix, Kanban status flow, and mitigation log"
        }
    ]
    report_json_content = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json",
        "themeCollection": {
            "baseTheme": {
                "name": "CY26SU07",
                "reportVersionAtImport": {
                    "visual": "2.11.0",
                    "report": "3.4.0",
                    "page": "2.3.1"
                },
                "type": "SharedResources"
            }
        },
        "objects": {
            "section": [
                {
                    "properties": {
                        "verticalAlignment": {
                            "expr": {
                                "Literal": {
                                    "Value": "'Top'"
                                }
                            }
                        }
                    }
                }
            ]
        },
        "resourcePackages": [
            {
                "name": "SharedResources",
                "type": "SharedResources",
                "items": [
                    {
                        "name": "CY26SU07",
                        "path": "BaseThemes/CY26SU07.json",
                        "type": "BaseTheme"
                    }
                ]
            }
        ],
        "settings": {
            "useStylableVisualContainerHeader": True,
            "exportDataMode": "AllowSummarized",
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True
        }
    }
    os.makedirs(os.path.join(REPORT_DIR, "definition"), exist_ok=True)
    write_json(
        os.path.join(REPORT_DIR, "definition", "version.json"),
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
            "version": "2.0.0"
        }
    )
    write_json(os.path.join(REPORT_DIR, "definition", "report.json"), report_json_content)

    # 5. Dashboard layout blueprint and pages
    pages_root = os.path.join(REPORT_DIR, "definition", "pages")
    if os.path.exists(pages_root):
        shutil.rmtree(pages_root)
    os.makedirs(pages_root, exist_ok=True)
    write_json(
        os.path.join(pages_root, "pages.json"),
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
            "pageOrder": [page["id"] for page in page_specs],
            "activePageName": page_specs[0]["id"]
        }
    )

    def measure_projection(measure_name):
        return {
            "field": {
                "Measure": {
                    "Expression": {
                        "SourceRef": {
                            "Entity": "_Measures"
                        }
                    },
                    "Property": measure_name
                }
            },
            "queryRef": f"_Measures.{measure_name}",
            "nativeQueryRef": measure_name
        }

    def column_projection(entity, column_name, active=False):
        projection = {
            "field": {
                "Column": {
                    "Expression": {
                        "SourceRef": {
                            "Entity": entity
                        }
                    },
                    "Property": column_name
                }
            },
            "queryRef": f"{entity}.{column_name}",
            "nativeQueryRef": column_name
        }
        if active:
            projection["active"] = True
        return projection

    def textbox_visual(visual_id, x, y, width, height, text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "textbox",
                "objects": {
                    "general": [
                        {
                            "properties": {
                                "paragraphs": [
                                    {
                                        "textRuns": [
                                            {
                                                "value": text,
                                                "textStyle": {
                                                    "fontFamily": "Segoe UI Semibold",
                                                    "fontSize": "18px",
                                                    "color": "#1F2937"
                                                }
                                            }
                                        ],
                                        "horizontalTextAlignment": "left"
                                    }
                                ]
                            }
                        }
                    ]
                },
                "visualContainerObjects": {
                    "background": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "false"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "border": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "false"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def card_visual(visual_id, x, y, width, height, measure_names, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "cardVisual",
                "query": {
                    "queryState": {
                        "Data": {
                            "projections": [measure_projection(name) for name in measure_names]
                        }
                    }
                }
            }
        }

    def clustered_bar_visual(visual_id, x, y, width, height, category_entity, category_column, measure_name, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "clusteredBarChart",
                "query": {
                    "queryState": {
                        "Category": {
                            "projections": [column_projection(category_entity, category_column, True)]
                        },
                        "Y": {
                            "projections": [measure_projection(measure_name)]
                        }
                    }
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                },
                                "text": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{title_text}'"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def line_visual(visual_id, x, y, width, height, category_entity, category_column, measure_names, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "lineChart",
                "query": {
                    "queryState": {
                        "Category": {
                            "projections": [column_projection(category_entity, category_column, True)]
                        },
                        "Y": {
                            "projections": [measure_projection(name) for name in measure_names]
                        }
                    }
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                },
                                "text": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{title_text}'"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def table_visual(visual_id, x, y, width, height, fields, title_text, tab_order, z_order):
        projections = []
        for field in fields:
            if field["kind"] == "column":
                projections.append(column_projection(field["entity"], field["name"]))
            else:
                projections.append(measure_projection(field["name"]))

        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "tableEx",
                "query": {
                    "queryState": {
                        "Values": {
                            "projections": projections
                        }
                    }
                },
                "objects": {
                    "columnHeaders": [
                        {
                            "properties": {
                                "columnAdjustment": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'growToFit'"
                                        }
                                    }
                                },
                                "autoSizeColumnWidth": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                },
                                "text": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{title_text}'"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def pivot_visual(visual_id, x, y, width, height, row_field, column_field, measure_name, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "pivotTable",
                "query": {
                    "queryState": {
                        "Rows": {
                            "projections": [column_projection(row_field["entity"], row_field["name"])]
                        },
                        "Columns": {
                            "projections": [column_projection(column_field["entity"], column_field["name"])]
                        },
                        "Values": {
                            "projections": [measure_projection(measure_name)]
                        }
                    }
                },
                "objects": {
                    "columnHeaders": [
                        {
                            "properties": {
                                "columnAdjustment": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'growToFit'"
                                        }
                                    }
                                },
                                "autoSizeColumnWidth": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                },
                                "text": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{title_text}'"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def slicer_dropdown_visual(visual_id, x, y, width, height, entity, column_name, header_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "slicer",
                "query": {
                    "queryState": {
                        "Values": {
                            "projections": [column_projection(entity, column_name)]
                        }
                    }
                },
                "objects": {
                    "data": [
                        {
                            "properties": {
                                "mode": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'Dropdown'"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "header": [
                        {
                            "properties": {
                                "show": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "true"
                                        }
                                    }
                                },
                                "text": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{header_text}'"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                },
                "visualContainerObjects": {
                    "padding": [
                        {
                            "properties": {
                                "top": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "8D"
                                        }
                                    }
                                },
                                "bottom": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "8D"
                                        }
                                    }
                                },
                                "left": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "8D"
                                        }
                                    }
                                },
                                "right": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "8D"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

    def donut_visual(visual_id, x, y, width, height, category_entity, category_column, measure_name, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "donutChart",
                "query": {
                    "queryState": {
                        "Legend": {
                            "projections": [column_projection(category_entity, category_column, True)]
                        },
                        "Y": {
                            "projections": [measure_projection(measure_name)]
                        }
                    }
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": { "expr": { "Literal": { "Value": "true" } } },
                                "text": { "expr": { "Literal": { "Value": f"'{title_text}'" } } }
                            }
                        }
                    ]
                }
            }
        }

    def waterfall_visual(visual_id, x, y, width, height, category_entity, category_column, measure_name, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "waterfallChart",
                "query": {
                    "queryState": {
                        "Category": {
                            "projections": [column_projection(category_entity, category_column, True)]
                        },
                        "Y": {
                            "projections": [measure_projection(measure_name)]
                        }
                    }
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": { "expr": { "Literal": { "Value": "true" } } },
                                "text": { "expr": { "Literal": { "Value": f"'{title_text}'" } } }
                            }
                        }
                    ]
                }
            }
        }

    def matrix_visual(visual_id, x, y, width, height, row_fields, measure_names, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "matrix",
                "query": {
                    "queryState": {
                        "Rows": {
                            "projections": [column_projection(field["entity"], field["name"]) for field in row_fields]
                        },
                        "Values": {
                            "projections": [measure_projection(name) for name in measure_names]
                        }
                    }
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": { "expr": { "Literal": { "Value": "true" } } },
                                "text": { "expr": { "Literal": { "Value": f"'{title_text}'" } } }
                            }
                        }
                    ]
                }
            }
        }

    def gantt_visual(visual_id, x, y, width, height, task_entity, task_column, start_column, end_column, percent_complete_measure, title_text, tab_order, z_order):
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json",
            "name": visual_id,
            "position": {
                "x": x,
                "y": y,
                "z": z_order,
                "height": height,
                "width": width,
                "tabOrder": tab_order
            },
            "visual": {
                "visualType": "gantt",
                "query": {
                    "queryState": {
                        "Task": {
                            "projections": [column_projection(task_entity, task_column)]
                        },
                        "StartDate": {
                            "projections": [column_projection(task_entity, start_column)]
                        },
                        "EndDate": {
                            "projections": [column_projection(task_entity, end_column)]
                        },
                        "PercentComplete": {
                            "projections": [measure_projection(percent_complete_measure)]
                        }
                    }
                },
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": { "expr": { "Literal": { "Value": "true" } } },
                                "text": { "expr": { "Literal": { "Value": f"'{title_text}'" } } }
                            }
                        }
                    ]
                }
            }
        }

    page_visuals = {
        page_specs[0]["id"]: [
            textbox_visual("49e7f05a2a1764190001", 20, 16, 900, 56, "Executive Overview", 0, 1000),
            card_visual("49e7f05a2a1764190002", 20, 84, 300, 110, ["BAC"], 1, 1001),
            card_visual("49e7f05a2a1764190003", 340, 84, 300, 110, ["AC"], 2, 1002),
            card_visual("49e7f05a2a1764190004", 660, 84, 300, 110, ["EV"], 3, 1003),
            card_visual("49e7f05a2a1764190005", 980, 84, 280, 110, ["Latest Percent Complete"], 4, 1004),
            clustered_bar_visual("49e7f05a2a1764190006", 20, 214, 620, 300, "projects", "ProjectName", "Latest Percent Complete", "Project status completion", 5, 1005),
            table_visual(
                "49e7f05a2a1764190007",
                660,
                214,
                600,
                300,
                [
                    {"kind": "column", "entity": "projects", "name": "ProjectName"},
                    {"kind": "measure", "name": "Latest Percent Complete"},
                    {"kind": "measure", "name": "Variance RAG"}
                ],
                "Milestone delivery snapshot",
                6,
                1006
            ),
            gantt_visual(
                "49e7f05a2a1764190008",
                20,
                530,
                620,
                180,
                "projects",
                "ProjectName",
                "StartDate",
                "EndDate",
                "Latest Percent Complete",
                "Gantt of Gantts (Project Timeline Overview)",
                7,
                1007
            ),
            donut_visual(
                "49e7f05a2a1764190009",
                660,
                530,
                600,
                180,
                "projects",
                "ProjectName",
                "Latest Percent Complete",
                "Donut chart of % completion by Project",
                8,
                1008
            )
        ],
        page_specs[1]["id"]: [
            textbox_visual("6b41b695c9024ef00001", 20, 16, 900, 56, "Financial Control", 0, 1000),
            card_visual("6b41b695c9024ef00002", 20, 84, 900, 110, ["BAC", "AC", "EV", "CV", "SV"], 1, 1001),
            slicer_dropdown_visual("6b41b695c9024ef00003", 940, 84, 320, 80, "ScenarioSelection", "Scenario", "Scenario selector", 2, 1002),
            line_visual("6b41b695c9024ef00004", 20, 214, 760, 260, "physical_progress", "RecordDate", ["PV", "EV", "AC"], "Cost and value trend", 3, 1003),
            table_visual(
                "6b41b695c9024ef00005",
                800,
                214,
                460,
                420,
                [
                    {"kind": "column", "entity": "wbs_elements", "name": "WBS_Code"},
                    {"kind": "column", "entity": "wbs_elements", "name": "ElementName"},
                    {"kind": "measure", "name": "BAC"},
                    {"kind": "measure", "name": "AC"},
                    {"kind": "measure", "name": "EV"},
                    {"kind": "measure", "name": "CPI"}
                ],
                "WBS element performance",
                4,
                1004
            ),
            waterfall_visual(
                "6b41b695c9024ef00007",
                20,
                490,
                760,
                210,
                "projects",
                "ProjectName",
                "CV",
                "Cost Variance (CV) Waterfall",
                6,
                1006
            ),
            textbox_visual("6b41b695c9024ef00006", 800, 650, 460, 50, "Control narrative: review CV/SV trend and apply corrective actions.", 5, 1005)
        ],
        page_specs[2]["id"]: [
            textbox_visual("8ed314e6a2da43fd0001", 20, 16, 900, 56, "Client Delivery", 0, 1000),
            clustered_bar_visual("8ed314e6a2da43fd0002", 20, 84, 620, 250, "wbs_elements", "ElementName", "Latest Percent Complete", "WBS delivery status", 1, 1001),
            pivot_visual(
                "8ed314e6a2da43fd0003",
                660,
                84,
                600,
                250,
                {"entity": "resources", "name": "Role"},
                {"entity": "projects", "name": "ProjectName"},
                "AC",
                "Resource utilization",
                2,
                1002
            ),
            table_visual(
                "8ed314e6a2da43fd0004",
                20,
                350,
                620,
                200,
                [
                    {"kind": "column", "entity": "projects", "name": "ProjectName"},
                    {"kind": "column", "entity": "projects", "name": "Status"},
                    {"kind": "measure", "name": "Latest Percent Complete"},
                    {"kind": "measure", "name": "Variance RAG"}
                ],
                "Project delivery status",
                3,
                1003
            ),
            gantt_visual(
                "8ed314e6a2da43fd0007",
                660,
                350,
                600,
                200,
                "projects",
                "ProjectName",
                "StartDate",
                "EndDate",
                "Latest Percent Complete",
                "WBS Gantt Timeline View",
                6,
                1006
            ),
            matrix_visual(
                "8ed314e6a2da43fd0006",
                20,
                565,
                940,
                140,
                [
                    {"entity": "projects", "name": "ProjectName"},
                    {"entity": "wbs_elements", "name": "WBS_Code"},
                    {"entity": "wbs_elements", "name": "ElementName"}
                ],
                ["BAC", "AC", "Latest Percent Complete", "Variance RAG"],
                "Hierarchical WBS breakdown from Projects",
                5,
                1005
            ),
            textbox_visual("8ed314e6a2da43fd0005", 980, 565, 280, 140, "Delivery narrative: focus on late packages and resource bottlenecks.", 4, 1004)
        ],
        page_specs[3]["id"]: [
            textbox_visual("8ed314e6a2da43fd0008", 20, 16, 900, 56, "Risk & Issues (RAID) Management", 0, 1000),
            donut_visual("8ed314e6a2da43fd0010", 20, 84, 400, 200, "raid_log", "Type", "Risk Count", "RAID Items by Type", 1, 1001),
            pivot_visual(
                "8ed314e6a2da43fd0011",
                440,
                84,
                820,
                200,
                {"entity": "raid_log", "name": "Impact"},
                {"entity": "raid_log", "name": "Probability"},
                "Risk Count",
                "Risk Matrix (Severity vs Probability)",
                2,
                1002
            ),
            table_visual(
                "8ed314e6a2da43fd0012",
                20,
                300,
                1240,
                400,
                [
                    {"kind": "column", "entity": "raid_log", "name": "Status"},
                    {"kind": "column", "entity": "raid_log", "name": "Type"},
                    {"kind": "column", "entity": "raid_log", "name": "RiskID"},
                    {"kind": "column", "entity": "raid_log", "name": "Description"},
                    {"kind": "column", "entity": "raid_log", "name": "MitigationStrategy"},
                    {"kind": "column", "entity": "raid_log", "name": "Owner"}
                ],
                "RAID Item Mitigation & Assumptions Log",
                3,
                1003
            )
        ]
    }

    for page in page_specs:
        pdir = os.path.join(REPORT_DIR, "definition", "pages", page["id"])
        if os.path.exists(pdir):
            shutil.rmtree(pdir)
        os.makedirs(pdir, exist_ok=True)
        write_json(
            os.path.join(pdir, "page.json"),
            {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
                "name": page["id"],
                "displayName": page["displayName"],
                "displayOption": "FitToPage",
                "height": 720,
                "width": 1280
            }
        )
        visuals_dir = os.path.join(pdir, "visuals")
        os.makedirs(visuals_dir, exist_ok=True)

        for visual in page_visuals[page["id"]]:
            visual_dir = os.path.join(visuals_dir, visual["name"])
            os.makedirs(visual_dir, exist_ok=True)
            write_json(os.path.join(visual_dir, "visual.json"), visual)

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

ref table _Measures
ref table ScenarioSelection
ref table projects
ref table wbs_elements
ref table resources
ref table timesheets
ref table material_costs
ref table physical_progress
ref table raid_log

ref cultureInfo en-US
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

	measure 'Latest Percent Complete' = 
			VAR SelectedDate = MAX('physical_progress'[RecordDate])
			RETURN
			SUMX(
			    VALUES('wbs_elements'[WBS_ID]),
			    VAR LatestWBSProgressDate = CALCULATE(MAX('physical_progress'[RecordDate]), 'physical_progress'[RecordDate] <= SelectedDate)
			    VAR LatestWBSProgress = CALCULATE(MAX('physical_progress'[PercentComplete]), 'physical_progress'[RecordDate] = LatestWBSProgressDate)
			    RETURN COALESCE(VALUE(LatestWBSProgress), 0)
			)
\t\tformatString: "0.00%"

\tmeasure 'Planned % Complete' = 
\t\t\tVAR StartDate = MIN('projects'[StartDate])
\t\t\tVAR EndDate = MAX('projects'[EndDate])
			VAR CurrentDate = MAX('physical_progress'[RecordDate])
			VAR RawProgress = DIVIDE(DATEDIFF(StartDate, CurrentDate, DAY), DATEDIFF(StartDate, EndDate, DAY), 0)
\t\t\tRETURN
\t\t\tIF(
\t\t\t    EndDate <= StartDate,
\t\t\t    0,
			    MIN(1, MAX(0, RawProgress))
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

\tmeasure 'Risk Count' = COUNTROWS('raid_log')
\t\tformatString: "#,##0"

\tmeasure 'Actual Hours' = SUM('timesheets'[HoursWorked])
\t\tformatString: "#,##0"

\tmeasure 'Planned Hours' = SUM('wbs_elements'[PlannedHours])
\t\tformatString: "#,##0"

\tmeasure 'Manpower Count' = DISTINCTCOUNT('timesheets'[ResourceID])
\t\tformatString: "#,##0"

\tmeasure 'Crew Utilization %' = DIVIDE([Actual Hours], [Planned Hours])
\t\tformatString: "0.00%"

\tmeasure 'Productivity Index' = DIVIDE([Latest Percent Complete], [Actual Hours])
\t\tformatString: "0.00%"

\tmeasure 'Total Risks' = CALCULATE(COUNTROWS('raid_log'), 'raid_log'[Type] = "Risk")
\t\tformatString: "#,##0"

\tmeasure 'High Risks' = CALCULATE(COUNTROWS('raid_log'), 'raid_log'[Type] = "Risk" && 'raid_log'[Impact] = "High")
\t\tformatString: "#,##0"

\tmeasure 'Open Issues' = CALCULATE(COUNTROWS('raid_log'), 'raid_log'[Type] = "Issue" && 'raid_log'[Status] = "Active")
\t\tformatString: "#,##0"

\tmeasure 'Project Health Score' = ([Latest Percent Complete] * 0.6) + ([SPI] * 0.2) + ([CPI] * 0.2)
\t\tformatString: "0.00%"

\tmeasure 'Overall Status' = SWITCH(TRUE(), [Project Health Score] >= 0.85, "On Track", [Project Health Score] >= 0.70, "At Risk", "Delayed")
\t\tformatString: "@"

\tcolumn MeasurePlaceholder
\t\tdataType: int64
\t\tisHidden
\t\tsourceColumn: MeasurePlaceholder

\tpartition MeasuresPartition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasurePlaceholder = _t]),
                    Type = Table.TransformColumnTypes(Source,{{{{"MeasurePlaceholder", Int64.Type}}}})
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
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
\t\t\t\t    Typed = Table.TransformColumnTypes(Headers, {{{{"BudgetAtCompletion_BAC", type number}}, {{"StartDate", type datetime}}, {{"EndDate", type datetime}}}}, "en-US")
\t\t\t\tin
\t\t\t\t    Typed
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
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
\t\t\t\t    Typed = Table.TransformColumnTypes(Headers, {{{{"PlannedCost", type number}}, {{"PlannedHours", type number}}}}, "en-US")
\t\t\t\tin
\t\t\t\t    Typed
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
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
\t\t\t\t    Typed = Table.TransformColumnTypes(Headers, {{{{"HourlyRate", type number}}}}, "en-US")
\t\t\t\tin
\t\t\t\t    Typed
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
\t\tformatString: "0.00"
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
				    Types = Table.TransformColumnTypes(Headers, {{{{"HoursWorked", type number}}}}, "en-US"),
\t\t\t\t    MergeRes = Table.NestedJoin(Types, {{"ResourceID"}}, resources, {{"ResourceID"}}, "res", JoinKind.LeftOuter),
\t\t\t\t    ExpandRes = Table.ExpandTableColumn(MergeRes, "res", {{"HourlyRate"}}, {{"HourlyRate"}}),
				    TypeRate = Table.TransformColumnTypes(ExpandRes, {{{{"HourlyRate", type number}}}}, "en-US"),
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
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
\t\t\t\t    Typed = Table.TransformColumnTypes(Headers, {{{{"Quantity", Int64.Type}}, {{"UnitPrice", type number}}, {{"TotalActualCost", type number}}}}, "en-US")
\t\t\t\tin
\t\t\t\t    Typed
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
                        Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
                        Typed = Table.TransformColumnTypes(Headers, {{{{"ProgressID", type text}}, {{"WBS_ID", type text}}, {{"RecordDate", type datetime}}, {{"PercentComplete", type number}}, {{"ReportedBy", type text}}}}, "en-US")
\t\t\t\tin
                        Typed
"""
    write_file(os.path.join(tables_dir, "physical_progress.tmdl"), progress_tmdl)

    # Table: raid_log
    raid_tmdl = f"""table raid_log

\tcolumn RiskID
\t\tdataType: string
\t\tsourceColumn: RiskID

\tcolumn Type
\t\tdataType: string
\t\tsourceColumn: Type

\tcolumn Description
\t\tdataType: string
\t\tsourceColumn: Description

\tcolumn Impact
\t\tdataType: string
\t\tsourceColumn: Impact

\tcolumn Probability
\t\tdataType: string
\t\tsourceColumn: Probability

\tcolumn MitigationStrategy
\t\tdataType: string
\t\tsourceColumn: MitigationStrategy

\tcolumn Owner
\t\tdataType: string
\t\tsourceColumn: Owner

\tcolumn Status
\t\tdataType: string
\t\tsourceColumn: Status

\tpartition raid_log-Partition = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents("{get_csv_path('raid_log.csv')}"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    Headers = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true])
\t\t\t\tin
\t\t\t\t    Headers
"""
    write_file(os.path.join(tables_dir, "raid_log.tmdl"), raid_tmdl)

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
