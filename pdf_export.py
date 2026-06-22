from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm


def format_duration(hours, hours_per_week):
    """Format hours into a human-readable duration with months, weeks, and days"""
    weeks = hours / hours_per_week
    
    months = int(weeks // 4.33)
    remaining_weeks = weeks - (months * 4.33)
    weeks_part = int(remaining_weeks)
    days_part = int((remaining_weeks - weeks_part) * 5)  # 5 working days per week
    
    parts = []
    
    if months > 0:
        parts.append(f"{months} month{'s' if months > 1 else ''}")
    
    if weeks_part > 0:
        parts.append(f"{weeks_part} week{'s' if weeks_part > 1 else ''}")
    
    if days_part > 0 or (months == 0 and weeks_part == 0):
        parts.append(f"{days_part} day{'s' if days_part != 1 else ''}")
    
    if not parts:
        return "0 days"
    
    return " ".join(parts)


def export_pdf(
    data,
    months_single,
    months_team,
    hours_per_week
):    
    
    # Softer color palette
    primary = colors.HexColor("#8E7CC3")   # soft lilac

    styles = getSampleStyleSheet()

    # Cover page title style
    styles["Title"].alignment = TA_CENTER
    styles["Title"].fontSize = 22
    styles["Title"].leading = 26
    styles["Title"].textColor = primary

    # Smaller heading styles for content pages
    heading2_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        textColor=primary,
        fontSize=13,
        leading=16,
        spaceBefore=10,
        spaceAfter=4
    )
    
    heading3_style = ParagraphStyle(
        "CustomHeading3",
        parent=styles["Heading3"],
        textColor=primary,
        fontSize=11,
        leading=14,
        alignment=TA_CENTER
    )

    summary_style = ParagraphStyle(
        "SummaryTitle",
        parent=styles["Heading3"],
        alignment=TA_LEFT,
        textColor=primary,
        fontSize=11,
        leading=14
    )

    # Style for roadmap descriptions with better wrapping
    roadmap_style = ParagraphStyle(
        "RoadmapText",
        parent=styles["BodyText"],
        leading=12,
        fontSize=8,
        alignment=TA_LEFT
    )
    
    # Style for phase table content
    phase_style = ParagraphStyle(
        "PhaseText",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        alignment=TA_LEFT
    )
    
    # Style for stack table content
    stack_style = ParagraphStyle(
        "StackText",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
        alignment=TA_LEFT
    )

    # Improved table style with better padding
    COMMON_TABLE_STYLE = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), primary),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("ROWBACKGROUNDS",
            (0,1),
            (-1,-1),
            [
                colors.whitesmoke,
                colors.HexColor("#F3F0FA")
            ]
        ),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ])
    
    # Special style for tables with wrapped content
    WRAPPED_TABLE_STYLE = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), primary),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("ROWBACKGROUNDS",
            (0,1),
            (-1,-1),
            [
                colors.whitesmoke,
                colors.HexColor("#F3F0FA")
            ]
        ),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ])


    doc = SimpleDocTemplate(
        "project_analysis.pdf",
        topMargin=40,
        bottomMargin=40,
        leftMargin=50,
        rightMargin=50
    )

    content = []

    # =========================
    # COVER PAGE (Page 1)
    # =========================

    content.append(Spacer(1, 80))

    logo = Image(
        "static/PlanForge.png",
        width=220,
        height=220
    )

    logo.hAlign = "CENTER"

    content.append(logo)

    content.append(Spacer(1, 40))

    content.append(
        Paragraph(
            "PROJECT ANALYSIS REPORT",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 50)
    )

    content.append(
        Paragraph(
            f"{data.get('project_type', 'Unknown').upper()} PROJECT",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 50)
    )

    content.append(
        Paragraph(
            "Generated by Gemini Project Analyzer",
            heading3_style
        )
    )

    content.append(
        Spacer(1, 200)
    )
    
    content.append(PageBreak())

    # =========================
    # PROJECT DETAILS (Page 2+)
    # =========================

    content.append(
        Paragraph(
            "PROJECT DETAILS",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary
        )
    )

    content.append(Spacer(1, 8))


    # =========================
    # General Information
    # =========================

    project_details_table = Table(
        [
            ["Field", "Value"],
            ["Project Type",
            data.get("project_type", "Unknown")],

            ["Complexity",
            data.get("complexity", "Unknown")],

            ["Estimation Certainty",
            data.get("Confidence Level", "Unknown")]
        ],
        colWidths=[180, 250],
        repeatRows=1
    )

    project_details_table.setStyle(COMMON_TABLE_STYLE)

    content.append(project_details_table)
    content.append(Spacer(1, 12))

    summary_table = Table(
        [
            [
                Paragraph(
                    "<b>EXECUTIVE SUMMARY</b>",
                    styles["Heading3"]
                )
            ],
            [
                Paragraph(
                    data.get(
                        "project_summary",
                        "Not provided"
                    ),
                    styles["BodyText"]
                )
            ]
        ],
        colWidths=[480]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FAF9FD")),
        ("BOX", (0,0), (-1,-1), 1, primary),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))


    content.append(summary_table)

    content.append(
        Spacer(1, 12)
    )

    # =========================
    # Confidence Range
    # =========================

    effort = data.get("estimated_effort_hours", 0)
    complexity = data.get("complexity", "Medium")

    if complexity == "Low":
        best_case = int(effort * 0.9)
        worst_case = int(effort * 1.2)

    elif complexity == "Medium":
        best_case = int(effort * 0.8)
        worst_case = int(effort * 1.5)

    else:  # High
        best_case = int(effort * 0.7)
        worst_case = int(effort * 2.0)

    # =========================
    # Time Estimates
    # =========================

    content.append(
        Paragraph(
            "TIME ESTIMATES",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    time_table = Table(
        [
            ["Metric", "Value"],
            ["Best Case",
            f"{best_case:,} hours"],

            ["Expected",
            f"{effort:,} hours"],

            ["Worst Case",
            f"{worst_case:,} hours"],

            ["Single Engineer Duration",
            format_duration(
                data.get("estimated_effort_hours", 0),
                hours_per_week
            )],

            ["Estimated Team Duration",
            format_duration(
                data.get("estimated_effort_hours", 0) / max(1, data.get("recommended_team_size", 1)),
                hours_per_week
            )],

            ["Team Size",
            str(data.get('recommended_team_size', 1))]
        ],
        colWidths=[200, 180],
        repeatRows=1
    )
    time_table.setStyle(COMMON_TABLE_STYLE)

    content.append(time_table)
    content.append(Spacer(1, 12))

    # =========================
    # Recommended Team
    # =========================

    content.append(
        Paragraph(
            "RECOMMENDED TEAM",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    table_data = [
        ["Role", "Count"]
    ]

    for member in data.get("recommended_team", []):
        table_data.append([
            member.get("role", "Unknown"),
            str(member.get("count", 0))
        ])

    table_data.append([
        Paragraph(
            "<b>TOTAL TEAM SIZE</b>",
            styles["Normal"]
        ),
        Paragraph(
            f"<b>{data.get('recommended_team_size', 1)}</b>",
            styles["Normal"]
        )
    ])


    team_table = Table(
        table_data,
        colWidths=[350, 80],
        repeatRows=1
    )

    team_table.setStyle(COMMON_TABLE_STYLE)
    
    # Highlight the TOTAL TEAM SIZE row
    team_table.setStyle(TableStyle([
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E8E0F5")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))

    content.append(team_table)

    content.append(Spacer(1, 12))

    # =========================
    # Complexity Reasons
    # =========================

    content.append(
        Paragraph(
            "COMPLEXITY REASONS",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    for reason in data.get("complexity_reasons", []):
        content.append(
            Paragraph(
                f"• {reason}",
                styles["BodyText"]
            )
        )
    
    content.append(Spacer(1, 6))

    content.append(
        Paragraph(
            "ASSUMPTIONS",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    for assumption in data.get(
        "assumptions",
        []
    ):
        content.append(
            Paragraph(
                f"• {assumption}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 6)
    )


    # =========================
    # Core Deliverables
    # =========================

    content.append(
        Paragraph(
            "CORE DELIVERABLES",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    for item in data.get(
        "core_deliverables",
        []
    ):
        content.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 6)
    )

    
    # =========================
    # Risks
    # =========================

    content.append(
        Paragraph(
            "RISKS",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    for risk in data.get("risks", []):
        content.append(
            Paragraph(
                f"• {risk}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 6))


    # =========================
    # Project Phases
    # =========================

    content.append(
        Paragraph(
            "PROJECT PHASES",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    team_size = max(
        1,
        int(
            data.get(
                "recommended_team_size",
                1
            )
        )
    )

    phase_table_data = [
        [
            Paragraph("<b>Phase</b>", phase_style),
            Paragraph("<b>Effort</b>", phase_style),
            Paragraph("<b>Solo</b>", phase_style),
            Paragraph("<b>Team</b>", phase_style)
        ]
    ]

    for phase in data.get(
        "project_phases",
        []
    ):

        phase_hours = phase.get(
            "estimated_hours",
            0
        )

        phase_table_data.append(
            [
                Paragraph(phase.get("phase", "Unknown"), phase_style),
                Paragraph(f"{phase_hours} hrs", phase_style),
                Paragraph(
                    format_duration(phase_hours, hours_per_week),
                    phase_style
                ),
                Paragraph(
                    format_duration(phase_hours / team_size, hours_per_week),
                    phase_style
                )
            ]
        )

    phase_table = Table(
        phase_table_data,
        colWidths=[
            180,
            80,
            120,
            120
        ],
        repeatRows=1
    )

    phase_table.setStyle(WRAPPED_TABLE_STYLE)

    content.append(phase_table)

    content.append(
        Spacer(1, 12)
    )

    # =========================
    # Implementation Roadmap
    # =========================

    content.append(
        Paragraph(
            "IMPLEMENTATION ROADMAP",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    roadmap_table_data = [
        [
            Paragraph("<b>Step</b>", roadmap_style),
            Paragraph("<b>Title</b>", roadmap_style),
            Paragraph("<b>Description</b>", roadmap_style)
        ]
    ]

    for step in data.get(
        "implementation_roadmap",
        []
    ):
        roadmap_table_data.append(
            [
                Paragraph(str(step.get("step", "")), roadmap_style),
                Paragraph(step.get("title", ""), roadmap_style),
                Paragraph(step.get("description", ""), roadmap_style)
            ]
        )

    roadmap_table = Table(
        roadmap_table_data,
        colWidths=[
            35,
            120,
            275
        ],
        repeatRows=1
    )

    roadmap_table.setStyle(WRAPPED_TABLE_STYLE)

    content.append(roadmap_table)

    content.append(
        Spacer(1, 12)
    )

   
    # =========================
    # Technology Stack
    # =========================

    if data.get("recommended_stack"):

        stack = data["recommended_stack"]

        content.append(
            Paragraph(
                "MVP STACK",
                heading2_style
            )
        )

        content.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=primary,
                spaceBefore=2,
                spaceAfter=8
            )
        )

        mvp_table_data = [
            [
                Paragraph("<b>Component</b>", stack_style),
                Paragraph("<b>Technology</b>", stack_style)
            ],
            [
                Paragraph("Frontend", stack_style),
                Paragraph(stack.get("mvp_stack", {}).get("frontend", "N/A"), stack_style)
            ],
            [
                Paragraph("Backend", stack_style),
                Paragraph(stack.get("mvp_stack", {}).get("backend", "N/A"), stack_style)
            ],
            [
                Paragraph("Database", stack_style),
                Paragraph(stack.get("mvp_stack", {}).get("database", "N/A"), stack_style)
            ]
        ]

        mvp_table = Table(
            mvp_table_data,
            colWidths=[120, 310],
            repeatRows=1
        )

        mvp_table.setStyle(COMMON_TABLE_STYLE)

        content.append(mvp_table)

        content.append(Spacer(1, 12))



        content.append(
            Paragraph(
                "PRODUCTION STACK",
                heading2_style
            )
        )

        content.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=primary,
                spaceBefore=2,
                spaceAfter=8
            )
        )   

        production_table_data = [
            [
                Paragraph("<b>Component</b>", stack_style),
                Paragraph("<b>Technology</b>", stack_style)
            ],
            [
                Paragraph("Frontend", stack_style),
                Paragraph(stack.get("production_stack", {}).get("frontend", "N/A"), stack_style)
            ],
            [
                Paragraph("Backend", stack_style),
                Paragraph(stack.get("production_stack", {}).get("backend", "N/A"), stack_style)
            ],
            [
                Paragraph("Database", stack_style),
                Paragraph(stack.get("production_stack", {}).get("database", "N/A"), stack_style)
            ]
        ]

        production_table = Table(
            production_table_data,
            colWidths=[120, 310],
            repeatRows=1
        )

        production_table.setStyle(COMMON_TABLE_STYLE)

        content.append(production_table)


        content.append(Spacer(1, 12))

    # =========================
    # Future Enhancements
    # =========================

    content.append(
        Paragraph(
            "FUTURE ENHANCEMENTS",
            heading2_style
        )
    )

    content.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=primary,
            spaceBefore=2,
            spaceAfter=8
        )
    )

    for item in data.get(
        "future_enhancements",
        []
    ):
        content.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )

    content.append(
        Spacer(1, 6)
    )

    # Page numbering function
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        # Don't show page number on cover page (page 1)
        if doc.page > 1:
            canvas.drawRightString(
                200 * mm,
                10 * mm,
                f"Page {doc.page - 1}"
            )
        canvas.restoreState()

    # Build the document with page numbers
    doc.build(
        content,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )