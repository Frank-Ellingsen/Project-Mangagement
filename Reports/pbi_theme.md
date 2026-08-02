🏗️ Power BI Theme JSON (Construction Palette)
json
{
  "name": "Construction Engineering Theme",
  "dataColors": [
    "#3A5F7D", 
    "#D0D3D4",
    "#F57C00",
    "#C62828",
    "#2E7D32",
    "#455A64",
    "#1E88E5",
    "#8E24AA",
    "#43A047"
  ],
  "background": "#FFFFFF",
  "foreground": "#3A5F7D",
  "tableAccent": "#F57C00",

  "visualStyles": {
    "*": {
      "*": {
        "color": { "expression": { "Solid": { "color": "#3A5F7D" } } },
        "fontFamily": "Segoe UI",
        "fontSize": 12
      }
    },

    "card": {
      "*": {
        "background": { "expression": { "Solid": { "color": "#FFFFFF" } } },
        "border": { "color": "#D0D3D4", "radius": 6, "weight": 1 },
        "title": {
          "color": { "expression": { "Solid": { "color": "#455A64" } } },
          "fontSize": 12
        },
        "labels": {
          "color": { "expression": { "Solid": { "color": "#3A5F7D" } } },
          "fontSize": 18
        }
      }
    },

    "clusteredColumnChart": {
      "*": {
        "dataPoint": {
          "defaultColor": { "color": "#3A5F7D" },
          "fill": { "color": "#3A5F7D" }
        }
      }
    },

    "lineChart": {
      "*": {
        "dataPoint": {
          "defaultColor": { "color": "#1E88E5" }
        }
      }
    },

    "pieChart": {
      "*": {
        "dataPoint": {
          "defaultColor": { "color": "#F57C00" }
        }
      }
    }
  },

  "textClasses": {
    "title": {
      "fontFamily": "Segoe UI Semibold",
      "fontSize": 14,
      "color": "#3A5F7D"
    },
    "header": {
      "fontFamily": "Segoe UI",
      "fontSize": 12,
      "color": "#455A64"
    },
    "callout": {
      "fontFamily": "Segoe UI",
      "fontSize": 18,
      "color": "#3A5F7D"
    }
  },

  "colorPalette": {
    "primary": "#3A5F7D",
    "secondary": "#D0D3D4",
    "accent": "#F57C00",
    "critical": "#C62828",
    "success": "#2E7D32"
  },

  "statusColors": {
    "onTrack": "#2E7D32",
    "atRisk": "#F9A825",
    "delayed": "#C62828"
  }
}
🎨 What this theme gives you
Clean engineering aesthetic

Strong contrast for dashboards viewed on-site

Safety colors for risk and incident visuals

Discipline colors (Civil, Structural, MEP, Commissioning)

Professional KPI card styling

Consistent chart colors across all visuals

This theme is optimized for construction PMOs, EPC contractors, civil engineering firms, and industrial megaprojects.