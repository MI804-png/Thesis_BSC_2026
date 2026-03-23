from __future__ import annotations

from io import BytesIO
from typing import Mapping

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_analysis_pdf(record: Mapping[str, object]) -> BytesIO:
    result = record["result"]
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("HR Insight Lab Analysis Report", styles["Title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Company: {result['company_name']}", styles["Heading2"]))
    story.append(Paragraph(f"Generated: {record['created_at']}", styles["BodyText"]))
    story.append(Paragraph(f"Source: {record['source']}", styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(result["prediction"]["verdict"], styles["Heading3"]))
    story.append(Paragraph(result["prediction"]["summary"], styles["BodyText"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("KPI Snapshot", styles["Heading2"]))
    kpi_table = Table(
        [["KPI", "Score", "Band"]] + [[kpi["name"], f"{kpi['score']}", kpi["band"]] for kpi in result["kpis"]],
        colWidths=[220, 80, 140],
    )
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8ccba")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fffdf8")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(kpi_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Inputs", styles["Heading2"]))
    input_rows = [["Input", "Value"]] + [[label, value] for label, value in result["display_inputs"]]
    input_table = Table(input_rows, colWidths=[220, 220])
    input_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f4f1")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8ccba")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(input_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Strategic Recommendations", styles["Heading2"]))
    bullet_style = ParagraphStyle("BulletBody", parent=styles["BodyText"], bulletIndent=12, leftIndent=24)
    for insight in result["insights"]:
        story.append(Paragraph(insight, bullet_style, bulletText="•"))
        story.append(Spacer(1, 4))

    ml_prediction = result.get("ml_prediction")
    if ml_prediction:
        story.append(Spacer(1, 8))
        story.append(Paragraph("Local ML Scoring", styles["Heading2"]))
        story.append(
            Paragraph(
                f"Probability: {ml_prediction['probability']}% | Model: {ml_prediction['model_name']} | "
                f"R²: {ml_prediction['r2']} | MAE: {ml_prediction['mae']}",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 8))
        contribution_rows = [["Driver", "Contribution"]] + [
            [item["label"], f"{item['contribution']:+.2f}"] for item in ml_prediction["top_contributors"]
        ]
        contribution_table = Table(contribution_rows, colWidths=[240, 120])
        contribution_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fff3df")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8ccba")),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(contribution_table)

    document.build(story)
    buffer.seek(0)
    return buffer
