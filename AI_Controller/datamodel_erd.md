# Project Controlling Data Model (ERD)

This document describes a highly granular, relational database schema designed for modern project controlling and Earned Value Management (EVM). It is semantic-agnostic, meaning it is designed at the raw relational database level (SQL/CSV) and can be mapped to any semantic layer (like Power BI, Microsoft Dataverse, or DuckDB views).

## Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    PROJECTS ||--o{ WBS_ELEMENTS : contains
    RESOURCES ||--o{ RESOURCE_ASSIGNMENTS : allocated-to
    WBS_ELEMENTS ||--o{ RESOURCE_ASSIGNMENTS : assigns
    WBS_ELEMENTS ||--o{ TIMESHEETS : tracks-labor
    RESOURCES ||--o{ TIMESHEETS : logs-hours
    WBS_ELEMENTS ||--o{ MATERIAL_COSTS : consumes
    WBS_ELEMENTS ||--o{ PHYSICAL_PROGRESS : records-completion
    
    PROJECTS {
        string ProjectID PK "Unique identifier for the project"
        string ProjectName "Name of the project"
        string ProjectManager "Name of the project manager"
        double BudgetAtCompletion_BAC "Total budgeted cost of the project"
        date StartDate "Project start date"
        date EndDate "Project target end date"
        string Status "Project status (Active, Completed, On Hold)"
    }

    WBS_ELEMENTS {
        string WBS_ID PK "Unique identifier for the WBS element"
        string ProjectID FK "Associated Project ID"
        string WBS_Code "Work Breakdown Structure code (e.g., 1.1, 1.1.2)"
        string ElementName "Name of the work package or phase"
        double PlannedCost "Allocated budget for this specific element"
        double PlannedHours "Allocated labor hours for this specific element"
    }

    RESOURCES {
        string ResourceID PK "Unique identifier for the resource"
        string ResourceName "Name of the employee or contractor"
        string Role "Role / Job title (e.g., Senior Engineer, Welder)"
        double HourlyRate "Cost rate per hour"
    }

    RESOURCE_ASSIGNMENTS {
        string AssignmentID PK "Unique assignment ID"
        string WBS_ID FK "Associated WBS Element ID"
        string ResourceID FK "Associated Resource ID"
        double AllocatedHours "Planned hours for this resource on this WBS element"
    }

    TIMESHEETS {
        string TimesheetID PK "Unique identifier for the timesheet log"
        string ResourceID FK "Associated Resource ID"
        string WBS_ID FK "Associated WBS Element ID"
        date WorkDate "Date when the work was done"
        double HoursWorked "Number of actual hours logged"
        string ApprovalStatus "Status of the timesheet (Approved, Pending)"
    }

    MATERIAL_COSTS {
        string PurchaseID PK "Unique identifier for the purchase transaction"
        string WBS_ID FK "Associated WBS Element ID"
        date PurchaseDate "Date of purchase/invoice"
        string Description "Description of materials purchased"
        int Quantity "Quantity purchased"
        double UnitPrice "Unit cost of the item"
        double TotalActualCost "Total purchase cost (Quantity * UnitPrice)"
    }

    PHYSICAL_PROGRESS {
        string ProgressID PK "Unique progress entry ID"
        string WBS_ID FK "Associated WBS Element ID"
        date RecordDate "Date of progress measurement"
        double PercentComplete "Estimated physical completion percentage (0.0 to 1.0)"
        string ReportedBy "Person who assessed/entered progress"
    }

    RAID_LOG {
        string RiskID PK "Unique risk/issue identifier"
        string Type "RAID category (Risk, Assumption, Issue, Dependency)"
        string Description "Description of the RAID item"
        string Impact "Impact level (High, Medium, Low)"
        string Probability "Probability level (High, Medium, Low)"
        string MitigationStrategy "Mitigation actions or strategy"
        string Owner "Assigned owner of the RAID entry"
        string Status "Status of RAID item (Active, Closed)"
    }
```

## Relational Rules & Integrity

1. **`PROJECTS` to `WBS_ELEMENTS`**: One-to-Many (`1:N`). A project contains multiple tasks or work packages structured hierarchically via the WBS code.
2. **`RESOURCES` to `RESOURCE_ASSIGNMENTS`**: One-to-Many (`1:N`). A resource can be assigned to multiple WBS elements.
3. **`WBS_ELEMENTS` to `RESOURCE_ASSIGNMENTS`**: One-to-Many (`1:N`). A WBS element can have multiple resource assignments (forming an `M:N` relationship between resources and WBS elements).
4. **`TIMESHEETS` (Granular Labor Costs)**: Tracks daily actual hours logged.
   - **Hourly Cost Calculation**: `Actual Labor Cost = HoursWorked * RESOURCES.HourlyRate`.
5. **`MATERIAL_COSTS` (Granular Materials)**: Captures non-labor actual costs invoiced directly to specific WBS elements.
6. **`PHYSICAL_PROGRESS` (EVM Driver)**: Periodic records of physical completion. Used to calculate **Earned Value (EV)** at any given date:
   - `EV = WBS_ELEMENTS.PlannedCost * PHYSICAL_PROGRESS.PercentComplete`.
