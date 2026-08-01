import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 10 slides data conforming to the 10-20-30 rule (10 slides, min 30pt font size)
    slides_data = [
        {
            "title": "Project Portfolio Executive Review",
            "subtitle": "Q2 2026 Status Report | Frank Ellingsen",
            "bullets": [
                "Comprehensive status of 6 active & completed projects",
                "EVM metrics overview & financial audits",
                "Strategic recommendations & corrective actions"
            ]
        },
        {
            "title": "1. Portfolio Overview & Health",
            "bullets": [
                "Total Baseline (BAC): 7,100,000 USD",
                "Total Spent (AC): 5,220,810 USD",
                "Earned Value (EV): 4,752,500 USD",
                "Portfolio CPI: 0.91 (Muted cost overrun)"
            ]
        },
        {
            "title": "2. PRJ-001 Vessel Construction",
            "bullets": [
                "Status: Completed (99.5% progress)",
                "Baseline: 1.5M USD | Actual Cost: 1.85M USD",
                "CPI: 0.81 | Total Overrun: -356K USD",
                "Action: Renegotiate contractor rates & freeze VOs"
            ]
        },
        {
            "title": "3. PRJ-002 Patrol Vessel Design",
            "bullets": [
                "Status: Planned (0% progress)",
                "Baseline Budget: 800,000 USD",
                "Planned Start: Aug 2026 | Finish: Dec 2026",
                "Focus: Carbon mold design and CFD analysis"
            ]
        },
        {
            "title": "4. PRJ-003 Subsea Cable Frame",
            "bullets": [
                "Status: Active (30% progress)",
                "Baseline: 1.2M USD | Spent: 382.5K USD",
                "CPI: 0.94 (Tracking close to budget)",
                "Focus: Engineering complete, steel fabrication starting"
            ]
        },
        {
            "title": "5. PRJ-004 Workboat Hull",
            "bullets": [
                "Status: Active (70% progress)",
                "Baseline: 2.0M USD | Spent: 1.48M USD",
                "CPI: 0.95 (Slight budget pressure)",
                "Focus: Drawings approved, welding & assembly ongoing"
            ]
        },
        {
            "title": "6. PRJ-005 Logistics Pontoon",
            "bullets": [
                "Status: Active (90% progress)",
                "Baseline: 1.0M USD | Spent: 927K USD",
                "CPI: 0.97 (In good financial standing)",
                "Project Manager: Frank Ellingsen"
            ]
        },
        {
            "title": "7. PRJ-006 Composite Cargo Hatch",
            "bullets": [
                "Status: Completed (100% progress)",
                "Baseline: 600,000 USD | Spent: 586,500 USD",
                "CPI: 1.02 (Under budget success)",
                "Deliverables: Molding & testing fully verified"
            ]
        },
        {
            "title": "8. Key Portfolio Risks & RAID Log",
            "bullets": [
                "Risk: Carbon sheet delivery delay from supplier",
                "Issue: Welder overtime limits exceeded in fabrication",
                "Dependency: Sea trials depend on DNV class approval",
                "Mitigation: Allocate junior welders to assist"
            ]
        },
        {
            "title": "9. Recommendations & Next Steps",
            "bullets": [
                "Renegotiate outfitting contractor rates (WBS 1 & 3)",
                "Shift composite fabricators to outfitting to optimize",
                "Enforce double-shift schedules to recover sea trials",
                "Integrate DuckDB tracking into future estimations"
            ]
        }
    ]
    
    # Muted clean Tufte colors
    navy = RGBColor(26, 37, 47)
    slate = RGBColor(44, 62, 80)
    dark_gray = RGBColor(85, 85, 85)
    
    for i, slide_info in enumerate(slides_data):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
        
        # Title Box
        title_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(11.83), Inches(1.5))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = slide_info["title"]
        p_title.font.name = 'Outfit'
        p_title.font.size = Pt(44)
        p_title.font.bold = True
        p_title.font.color.rgb = navy
        
        # Content Box
        content_box = slide.shapes.add_textbox(Inches(0.75), Inches(2.0), Inches(11.83), Inches(4.5))
        tf_content = content_box.text_frame
        tf_content.word_wrap = True
        
        if "subtitle" in slide_info:
            p_sub = tf_content.paragraphs[0]
            p_sub.text = slide_info["subtitle"]
            p_sub.font.name = 'Inter'
            p_sub.font.size = Pt(30)
            p_sub.font.bold = True
            p_sub.font.color.rgb = slate
            p_sub.space_after = Pt(20)
            
            for b in slide_info["bullets"]:
                p = tf_content.add_paragraph()
                p.text = "• " + b
                p.font.name = 'Inter'
                p.font.size = Pt(30)
                p.font.color.rgb = dark_gray
                p.space_after = Pt(14)
        else:
            first = True
            for b in slide_info["bullets"]:
                if first:
                    p = tf_content.paragraphs[0]
                    first = False
                else:
                    p = tf_content.add_paragraph()
                p.text = "• " + b
                p.font.name = 'Inter'
                p.font.size = Pt(30)
                p.font.color.rgb = dark_gray
                p.space_after = Pt(20)
                
    # Save presentation
    os.makedirs("Data", exist_ok=True)
    prs.save("Data/Project_Portfolio_Review.pptx")
    print("PowerPoint presentation generated successfully!")

if __name__ == "__main__":
    create_presentation()
