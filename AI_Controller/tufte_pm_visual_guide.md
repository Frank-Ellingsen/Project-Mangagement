# Visual Guide: Project Management Dashboards & Edward Tufte's Data-Ink Ratio

Edward Tufte, a pioneer in statistical graphics, introduced the **Data-Ink Ratio**: the proportion of a graphic's ink (or pixels) devoted to the non-redundant display of data-information. 

$$\text{Data-Ink Ratio} = \frac{\text{Data-Ink}}{\text{Total Ink used to print the graphic}}$$

Tufte's core directive is: **Maximize the data-ink ratio.** Erase chart junk (decorations, heavy borders, redundant grids) so that nothing competes with the data. 

This guide translates Tufte's principles into practical rules for project controlling visuals (S-Curves, Gantt charts, Histograms, Tables, and KPI Cards).

---

## 1. S-Curves (PV, EV, AC over Time)

S-Curves are notorious for visual clutter: gridlines, markers, legends, and heavy colors distract from the performance gaps.

| Standard BI Practice (Low Data-Ink) | Tufte Best Practice (Max Data-Ink) |
| :--- | :--- |
| **Gridlines**: Dense horizontal and vertical gridlines. | **No Gridlines**: Remove background grids. Let the lines stand on clean whitespace. |
| **Markers**: Dots or circles on every single weekly data point. | **Line Only**: The line itself carries the trend. Individual dots are redundant ink. |
| **Legend**: A separate box containing color keys (forcing eyes to jump back and forth). | **Direct Labeling**: Place labels (*Planned*, *Earned*, *Actual*) directly at the end of the curves. |
| **Axis Scales**: 10+ tick marks and vertical grid lines. | **Micro-Axes**: Keep axis ticks minimal. Only label key points: Start, Current Date, End. |

### S-Curve Visual Design Blueprint:
* **Planned Value (PV)**: Thin, dashed, medium-grey line (sets the background target context).
* **Earned Value (EV)**: Solid, medium-blue line (stands out as the physical progress made).
* **Actual Cost (AC)**: Solid, dark-grey or black line (draws attention to spending).
* **Direct Labels**: Place the text `Planned`, `Earned`, and `Actual` directly next to the lines at the right edge of the chart.

---

## 2. Gantt Charts

Traditional Gantt charts are packed with "chart junk": 3D bars, drop shadows, icons, and massive grid matrices.

```
[Standard: Low Ratio]                      [Tufte: High Ratio]
|---Task A---|   (Heavy grids)            Task A     ════════
  |---Task B---| (Icons, colors)          Task B             ════════
```

### Clean Gantt Principles:
1. **Erase Vertical Grids**: Use thin, light-grey tick marks on the time axis at the top. Remove all vertical lines crossing the chart.
2. **Remove Task Icons**: Icons of folder structures, calendars, or checklists represent non-data-ink. Indentation is sufficient to represent hierarchy.
3. **Use Muted Colors for Status**: Do not color-code every bar with a unique color. 
   * Use **light grey** for the baseline schedule.
   * Use **dark grey** for actual progress.
   * Use a **muted red** only on tasks that are on the critical path and currently delayed.
4. **Direct Task Labeling**: If space permits, write the name of the task directly to the left of the bar. Avoid forcing the user to map a table row to a bar far across the page.

---

## 3. Resource Histograms (Allocation over Time)

Histograms are used to spot over-allocation, but they are often cluttered with thick bars, borders, and legends.

### Clean Histogram Principles:
* **Remove Bar Borders**: Let the color fill speak for itself. Black borders around columns add useless ink.
* **Remove Y-Axis if Labeled**: If you write the numbers (e.g. `8h`, `10h`) inside or on top of the bars, delete the Y-axis entirely. Keeping both is redundant.
* **Highlight Variances Only**: Instead of a solid line representing max resource capacity:
  * Draw a very thin, dotted horizontal line for capacity.
  * Keep the bars below capacity a neutral grey.
  * Highlight the portion of the bar *above* capacity in a single accent color (e.g., muted amber). This draws the eyes instantly to the variance.

---

## 4. Tables & Matrices

In project controlling, tables represent a significant amount of the display area. Standard tables are often drawn like prisons (heavy grids).

| Standard Table (Low Ratio) | Tufte Table (High Ratio) |
| :--- | :--- |
| Boxed cells with vertical and horizontal borders. | **No Vertical Lines**: Remove all vertical lines. Clean spacing aligns the column naturally. |
| Zebra striping with dark alternating backgrounds. | **Whitespace as separator**: Use extra spacing or very light grey horizontal lines between rows. |
| Center-aligned text and numbers. | **Proper Alignment**: Always left-align text (makes reading easier) and right-align numbers (aligns decimal places). |
| Duplicate units (e.g. writing "NOK" in every row). | **Header Units**: Define units once in the column header (e.g. `AC (NOK)`). |

```
Standard (Prison Table):
┌──────────┬──────────┬──────────┐
│ WBS Code │ BAC (NOK)│ AC (NOK) │
├──────────┼──────────┼──────────┤
│ 1.0      │ 300 000  │ 419 230  │
└──────────┴──────────┴──────────┘

Tufte Style (Clean Table):
WBS Code      BAC (NOK)     AC (NOK)
────────────────────────────────────
1.0             300,000      419,230
2.0             600,000      620,450
────────────────────────────────────
Total         1,500,000    1,848,810
```

---

## 5. KPI Cards & Summaries

KPI Cards must convey raw metrics instantly.

* **Erase Fills & Shadows**: Remove cards' background drop-shadows, borders, and background fills. They do not represent data.
* **Typography Hierarchy**: Use a large, bold, clean sans-serif font for the number (e.g., `0.81` in 36pt font). Underneath, write a short, muted grey label in a smaller font (e.g., `Overall CPI` in 10pt font).
* **Avoid Decorative Icons**: Remove dollar signs, checkmarks, or target icons next to the numbers. The numbers and labels are self-explanatory.
