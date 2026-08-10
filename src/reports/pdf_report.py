import os
import pandas as pd
import plotly.express as px

# from datetime import datetime
from datetime import datetime
from pathlib import Path
BASE_DIR = Path("/tmp/ciphervista")
BASE_DIR.mkdir(parents=True, exist_ok=True)

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER
title_style.fontName = "Helvetica-Bold"
title_style.fontSize = 28
title_style.leading = 34
title_style.textColor = colors.HexColor("#1E40AF")

heading_style = styles["Heading2"]
heading_style.fontName = "Helvetica-Bold"
heading_style.fontSize = 18
heading_style.leading = 24
heading_style.textColor = colors.HexColor("#2563EB")

body_style = styles["BodyText"]
body_style.fontName = "Helvetica"
body_style.fontSize = 11
body_style.leading = 18

small_style = styles["BodyText"]
small_style.fontName = "Helvetica"
small_style.fontSize = 9
small_style.leading = 13


def generate_pdf_report(
    filename,
    total,
    benign,
    attacks,
    anomalies,
    confidence,
    risk_level,
    attack_breakdown,
    ai_report
):

    

    output_path = str(BASE_DIR / "CipherVista_Report.pdf")

    doc = SimpleDocTemplate(
        output_path,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    logo = os.path.join(
        os.path.dirname(__file__),
        "assets",
        "logo.png"
    )

    if os.path.exists(logo):

        img = Image(
            logo,
            width=2.3 * inch,
            height=2.3 * inch
        )

        img.hAlign = "CENTER"

        story.append(img)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<font size=30><b>CipherVista</b></font>",
            title_style
        )
    )

    story.append(Spacer(1,10))

    story.append(
        Paragraph(
            "<font size=17>AI Threat Intelligence Report</font>",
            heading_style
        )
    )

    info = [

        ["Prepared For", "Enterprise Security Team"],

        ["Prepared By", "CipherVista AI"],

        ["Dataset", filename],

        ["Generated On", datetime.now().strftime("%d %B %Y")],

        ["Version", "3.0"]

    ]

    info_table = Table(
        info,
        colWidths=[150,270]
    )

    info_table.setStyle(

        TableStyle([

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

            ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#1E40AF")),

            ("BOTTOMPADDING",(0,0),(-1,-1),10),

            ("TOPPADDING",(0,0),(-1,-1),10),

            ("GRID",(0,0),(-1,-1),0.25,colors.lightgrey)

        ])

    )

    story.append(info_table)

    story.append(Spacer(1,25))

    risk_color = {

        "LOW": colors.HexColor("#16A34A"),

        "MEDIUM": colors.HexColor("#EA580C"),

        "HIGH": colors.HexColor("#DC2626"),

        "CRITICAL": colors.HexColor("#7F1D1D")

    }.get(
        risk_level.upper(),
        colors.HexColor("#2563EB")
    )

    risk_table = Table(
        [
            ["OVERALL RISK"],
            [risk_level.upper()]
        ],
        colWidths=[420]
    )

    risk_table.setStyle(
        TableStyle(
            [

                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1E40AF")),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                (("BACKGROUND",(0,1),(-1,1),risk_color)),
                ("TEXTCOLOR",(0,1),(-1,1),colors.white),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

                ("FONTSIZE",(0,1),(-1,1),22),

                ("TOPPADDING",(0,1),(-1,1),15),

                ("BOTTOMPADDING",(0,1),(-1,1),15),

                ("GRID",(0,0),(-1,-1),1,colors.white)

            ]
        )
    )

    story.append(risk_table)

    story.append(Spacer(1,30))
    story.append(PageBreak())

    story.append(
    Paragraph(
        "Executive Dashboard",
        title_style
    )
)

    story.append(Spacer(1,20))

    # story.append(
    #     Paragraph(
    #         "Executive Threat Intelligence Report",
    #         title_style
    #     )
    # )

    story.append(Spacer(1, 12))

    stats = [

    ["Metric","Value"],

    ["Total Flows", f"{total:,}"],

    ["Benign Traffic", f"{benign:,}"],

    ["Malicious Traffic", f"{attacks:,}"],

    ["Anomalies", f"{anomalies:,}"],

    ["Average Confidence", f"{confidence}%"],

    ["Overall Risk", risk_level]

]

    table = Table(
        stats,
        colWidths=[220,180]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1E40AF")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

            ("TOPPADDING",(0,0),(-1,0),10),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

        ])

    )

    story.append(table)

    # story.append(PageBreak())

    chart_df = pd.DataFrame(
    attack_breakdown.items(),
    columns=["Attack Type", "Count"]
)

    pie = px.pie(
        chart_df,
        names="Attack Type",
        values="Count",
        hole=0.45,
        title="Attack Distribution"
    )

    

    pie_path = BASE_DIR / "attack_pie.png"
    bar_path = BASE_DIR / "attack_bar.png"

    pie.write_image(str(pie_path))

    bar = px.bar(
        chart_df,
        x="Attack Type",
        y="Count",
        color="Attack Type",
        title="Attack Breakdown"
    )

    bar.write_image(str(bar_path))

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Attack Analytics",
            title_style
        )
    )

    story.append(Spacer(1,20))

    story.append(
    Image(
    str(pie_path),
    width=5.8*inch,
    height=4.2*inch
)
)

    story.append(Spacer(1,20))

    story.append(
    Image(
    str(bar_path),
    width=6.2*inch,
    height=4.0*inch
)
)

    story.append(
        Paragraph(
            """
            This report was automatically generated by
            <b>CipherVista AI</b> using Machine Learning,
            Isolation Forest anomaly detection, Random Forest classification,
            and Google Gemini AI.
            """,
            body_style
        )
    )

    story.append(Spacer(1, 20))

    import re

    for line in ai_report.split("\n"):

        line = line.strip()

        # blank line
        if line == "":
            story.append(Spacer(1,8))
            continue

        # horizontal rule
        if line == "---":
            story.append(Spacer(1,15))
            continue

        # ignore markdown code fences
        if line.startswith("```"):
            continue

        # Heading 1
        if line.startswith("# "):
            story.append(
                Paragraph(
                    line[2:],
                    title_style
                )
            )
            story.append(Spacer(1,12))
            continue

        # Heading 2
        if line.startswith("## "):
            story.append(
                Paragraph(
                    line[3:],
                    heading_style
                )
            )
            story.append(Spacer(1,10))
            continue

        # Heading 3
        if line.startswith("### "):
            story.append(
                Paragraph(
                    "<b>"+line[4:]+"</b>",
                    heading_style
                )
            )
            story.append(Spacer(1,8))
            continue

        # Bullet list
        if line.startswith("* "):
            bullet = line[2:]
            bullet = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", bullet)

            story.append(
                Paragraph(
                    "• " + bullet,
                    body_style
                )
            )
            continue

        # Numbered list
        if re.match(r"^\d+\.", line):
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )
            continue

        # Markdown bold
        line = re.sub(
            r"\*\*(.*?)\*\*",
            r"<b>\1</b>",
            line
        )

        story.append(
        Paragraph(
            line,
            body_style
        )
    )

    

    story.append(PageBreak())

    story.append(
            Paragraph(
                "MITRE ATT&CK Mapping",
                title_style
            )
        )

    story.append(Spacer(1,20))

    mitre_data = [

    ["Threat",
     "Technique",
     "ID"],

    ["DDoS",
     "Network Denial of Service",
     "T1498"],

    ["DoS Hulk",
     "Endpoint Denial of Service",
     "T1499"],

    ["Bot",
     "Application Layer Protocol",
     "T1071"],

    ["Web Brute Force",
     "Brute Force",
     "T1110"],

    ["SSH-Patator",
     "Brute Force",
     "T1110"],

    ["XSS",
     "Exploit Public Facing Application",
     "T1190"]

]

    mitre_table = Table(
    mitre_data,
    colWidths=[140,230,80]
)

    mitre_table.setStyle(

    TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1E40AF")),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

        ("TOPPADDING",(0,0),(-1,0),10),

    ])

)
    story.append(mitre_table)

    doc.build(story)

    return output_path