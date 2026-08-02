# Financial Control Page — Dashboard View Layout Draft

This document outlines the wireframe, components, field mappings, and specific visual formatting settings required to implement the **Financial Control** page in Power BI Desktop according to Edward Tufte's Data-Ink ratio principles.

---

## 1. Visual Layout Wireframe

```
+-------------------------------------------------------------------------------------------------------------+
|  PROJECT CONTROL TOWER  |  Financial Control                                    [Scenario: Baseline | v ]   |
+-------------------------------------------------------------------------------------------------------------+
|                                                                                                             |
|  [ BAC ]              [ AC ]              [ EV ]              [ CV ]              [ SV ]                    |
|  $1,240,000           $945,000            $910,000            -$35,000 (Amber)    -$45,000 (Amber)          |
|                                                                                                             |
|  +--------------------------------------------------+  +-------------------------------------------------+  |
|  | CUMULATIVE S-CURVE (PV vs EV vs AC)              |  | WBS ELEMENT PERFORMANCE                         |  |
|  |                                                  |  |                                                 |  |
|  | Value ($)                                        |  | WBS   Element Name     Planned      Actual   CPI  |  |
|  |   ^                                       -- AC  |  | ----- ---------------- ------------ -------- ---  |  |
|  |   |                             ------           |  | 1.1   Hull Fab          $400,000  $415,000 0.96  |  |
|  |   |                       ------   EV            |  | 1.2   Outfitting        $350,000  $340,000 1.02  |  |
|  |   |                 ------                       |  | 1.3   Commissioning     $200,000  $190,000 1.05  |  |
|  |   |           ------   PV                        |  | 2.1   Propulsion        $290,000  $290,000 1.00  |  |
|  |   +------------------------------------------->  |  | ----- ---------------- ------------ -------- ---  |  |
|  |                                    Record Date   |  | Total                   $1,240,000  $945,000 0.96  |  |
|  +--------------------------------------------------+  +-------------------------------------------------+  |
|                                                                                                             |
|  +-------------------------------------------------------------------------------------------------------+  |
|  | CONTROL NARRATIVE & VARIANCE HIGHLIGHTS                                                                |  |
|  | Under the "Baseline" risk scenario, Hull Fabrication (WBS 1.1) exhibits an active cost overrun of 3.8%  |  |
|  | (CPI = 0.96). Action required: Audit timesheet allocations and adjust upcoming resource levels.       |  |
|  +-------------------------------------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------------------------------------+
```

---

## 2. Component Design & Field Mapping

### 2.1 Page Settings
* **Size**: Standard 16:9 (`1280 x 720` px).
* **Background Color**: Light gray/white (`#F8F9FA`) to maintain a clean workspace. No background images or wallpapers.

### 2.2 Slicer: Scenario Selector (Top Right)
* **Visual Type**: Slicer (Orientation: Horizontal / Button-group tile style).
* **Data Field**: `ScenarioSelection[Scenario]` (Values: `Conservative`, `Baseline`, `Aggressive`).
* **Tufte Styling**:
  * **Slicer Header**: 9pt Semibold, left-aligned, muted grey text. Title: *"Select Risk Scenario Thresholds"*.
  * **Tile/Buttons**: No border outline. Default background color: Light gray (`#E9ECEF`), selected button background color: Muted steel blue (`#495057`) with white text.
  * **Layout**: Multi-select off, Single-select on.

### 2.3 Row of KPI Cards (Upper Section)
Five KPI cards aligned horizontally:
1. **Budget at Completion (BAC)**
   * **Field**: `[BAC]` (Measure)
   * **Formatting**: Value: 24pt bold, `#212529`. Label: 9pt, `#6C757D` bottom-positioned.
2. **Actual Cost (AC)**
   * **Field**: `[AC]` (Measure)
   * **Formatting**: Value: 24pt bold, `#212529`.
3. **Earned Value (EV)**
   * **Field**: `[EV]` (Measure)
   * **Formatting**: Value: 24pt bold, `#212529`.
4. **Cost Variance (CV)**
   * **Field**: `[CV]` (Measure)
   * **Conditional Color**: If `[Variance RAG]` = *"Red"*, value font color is `#DC3545` (Bright Red). If *"Amber"*, `#D97706` (Amber/Dark Yellow). If *"Green"*, `#198754` (Muted Green).
5. **Schedule Variance (SV)**
   * **Field**: `[SV]` (Measure)
   * **Conditional Color**: Color matches `[Variance RAG]` using conditional formatting rule mapping to Red/Amber/Green.

* **Tufte Card Styling**:
  * **Borders & Shadows**: Turn off "Visual Border" and "Shadow" in the formatting pane.
  * **Background**: Transparent or matching the page background (`#F8F9FA`).
  * **Icons**: Completely disabled.

### 2.4 Cumulative S-Curve (Left Visual)
* **Visual Type**: Line Chart.
* **X-Axis**: `physical_progress[RecordDate]` (Continuous timeline).
* **Y-Axis**: `[PV]`, `[EV]`, `[AC]` (Measures plotted together).
* **Tufte Line Styling**:
  * **Gridlines**: Vertical gridlines: **Off**. Horizontal gridlines: **On (subtle dotted, `#DEE2E6`)**.
  * **Lines**:
    * `[PV]`: Thin dotted slate line (`#6C757D`).
    * `[EV]`: Solid steel-blue line (`#4A6B82`, stroke width 3).
    * `[AC]`: Solid dark gray line (`#343A40`, stroke width 2).
  * **Legend**: **Disabled**. Direct labels enabled on the end of each line (Power BI > Series Labels > On).
  * **Title**: Left-aligned, 11pt bold, `#212529`. Title: *"Cumulative S-Curve: Value & Cost Progress ($)"*.

### 2.5 WBS Element Performance Table (Right Visual)
* **Visual Type**: Table.
* **Fields**:
  1. `wbs_elements[WBS_Code]` (WBS ID/Code)
  2. `wbs_elements[ElementName]` (Work package)
  3. `[BAC]` (Planned budget)
  4. `[AC]` (Actual spent)
  5. `[EV]` (Earned value)
  6. `[CPI]` (Cost Performance Index)
* **Tufte Table Formatting**:
  * **Style Preset**: None (removes thick headers and background colors).
  * **Gridlines**: Vertical gridlines: **Off**. Horizontal gridlines: **On (subtle gray `#E9ECEF`)**.
  * **Alignment**:
    * WBS Code & Element Name: **Left-aligned**.
    * BAC, AC, EV, CPI: **Right-aligned**.
  * **Font**: UI Font (Segoe UI or Inter), 9pt. Headers 10pt Bold, text color `#212529`.
  * **Alternating Row Background**: Disabled (no alternating colored bars; keep background white/transparent for high text contrast).
  * **Total Row**: Muted top divider line, 10pt bold values.

### 2.6 Control Narrative & Action Box (Bottom Panel)
* **Visual Type**: Multi-row card or custom HTML/text card.
* **Field**: Dynamic measure reporting status.
* **Formatting**: Font 10pt, left-aligned. Minimal frame, `#F1F3F5` light background box with no border.
