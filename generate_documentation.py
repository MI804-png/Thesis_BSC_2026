"""
Thesis Doc Gen Script
I wrote this to handle the heavy lifting of turning my markdown notes and data into a 50+ page PDF. 
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, KeepTogether
)
from reportlab.lib import colors
import pathlib
import html
import re
from datetime import datetime

try:
    from pypdf import PdfReader, PdfWriter
except Exception:  # pragma: no cover
    PdfReader = None
    PdfWriter = None


def draw_page_number(canvas_obj, doc):
    """Draw a simple centered footer page number for thesis-style pages."""

    page_number = canvas_obj.getPageNumber()
    if page_number == 1:
        return

    canvas_obj.saveState()
    canvas_obj.setFont('Times-Roman', 10)
    canvas_obj.drawCentredString(A4[0] / 2.0, 1.25 * cm, str(page_number))
    canvas_obj.restoreState()


def enforce_pdf_page_limit(pdf_path: str, max_pages: int) -> None:
    """Trim the generated PDF to max_pages when a reader is available."""

    if max_pages <= 0:
        return
    if PdfReader is None or PdfWriter is None:
        return

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages[:max_pages]:
        writer.add_page(page)

    with open(pdf_path, "wb") as output_file:
        writer.write(output_file)


def create_thesis_documentation(
    filename: str | None = None,
    max_pages: int = 50,
    source_markdown: str = "THESIS_PROFESSIONAL.md",
):
    """Generate thesis PDF from markdown using a professional, thesis-style layout."""

    filename = filename or "Thesis_HR_Decision_Support_System.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=3.0 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )
    doc.title = "Design and Implementation of a Data-Driven HR and Management Decision Support System"
    doc.author = "Mikhael Nabil Salama Rezk"
    doc.subject = "Bachelor Thesis"
    doc.creator = "Mikhael Rezk"

    story = []
    styles = getSampleStyleSheet()
    logo_path = pathlib.Path("c:/Thesis_Hr_system/Picture1.png")
    thesis_path = pathlib.Path(f"c:/Thesis_Hr_system/{source_markdown}")

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.black,
        spaceAfter=18,
        alignment=TA_CENTER,
        leading=26,
        fontName="Times-Bold",
    )
    title_meta_style = ParagraphStyle(
        "TitleMeta",
        parent=styles["Normal"],
        fontSize=12,
        alignment=TA_CENTER,
        leading=18,
        spaceAfter=8,
        fontName="Times-Roman",
    )
    heading1_style = ParagraphStyle(
        "CustomHeading1",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=6,
        spaceBefore=18,
        leading=18,
        fontName="Times-Bold",
    )
    heading2_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.black,
        spaceAfter=6,
        spaceBefore=12,
        leading=17,
        fontName="Times-Bold",
    )
    heading3_style = ParagraphStyle(
        "CustomHeading3",
        parent=styles["Heading3"],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6,
        spaceBefore=10,
        leading=16,
        fontName="Times-Bold",
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=12,
        alignment=TA_JUSTIFY,
        firstLineIndent=0.7 * cm,
        spaceAfter=6,
        leading=18,
        fontName="Times-Roman",
    )
    bullet_style = ParagraphStyle(
        "BulletBody",
        parent=body_style,
        firstLineIndent=0,
        leftIndent=0.7 * cm,
        bulletIndent=0,
    )
    toc_style = ParagraphStyle(
        "CustomTOC",
        parent=body_style,
        fontSize=11,
        leading=15,
        firstLineIndent=0,
        leftIndent=0,
        spaceAfter=3,
    )

    def convert_inline_markup(text: str) -> str:
        escaped = html.escape(text, quote=False)
        return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)

    def append_paragraph(text: str, style) -> None:
        cleaned = text.strip()
        if cleaned:
            story.append(Paragraph(convert_inline_markup(cleaned), style))

    def format_toc_page_suffix(text: str) -> str:
        """Wrap trailing TOC page numbers in parentheses, e.g. 'Title 12' -> 'Title (12)'."""

        return re.sub(r"\s+(\d+)$", r" (\1)", text.strip())

    if logo_path.exists():
        logo = Image(str(logo_path), width=13.8 * cm, height=3.59 * cm)
        logo.hAlign = "CENTER"
        story.append(Spacer(1, 0.5 * cm))
        story.append(logo)
        story.append(Spacer(1, 1.0 * cm))
    else:
        story.append(Spacer(1, 2.2 * cm))

    story.append(Spacer(1, 0.7 * cm))
    story.append(
        Paragraph(
            "Design and Implementation of a Data-Driven HR and Management<br/>Decision Support System for Organizational Performance and Risk Analysis",
            title_style,
        )
    )
    story.append(Spacer(1, 3.8 * cm))
    story.append(Paragraph("Mikhael Nabil Salama Rezk<br/>IHUTSC", title_meta_style))
    story.append(Spacer(1, 1.4 * cm))
    story.append(
        Paragraph(
            "University Consultant: Mark Kovacs, position: Computer Engineering",
            title_meta_style,
        )
    )
    story.append(Spacer(1, 5.2 * cm))
    story.append(Paragraph("2026", title_meta_style))
    story.append(PageBreak())

    thesis_lines = thesis_path.read_text(encoding="utf-8").splitlines()
    try:
        start_index = thesis_lines.index("---") + 1
    except ValueError:
        start_index = 0

    current_section = None
    paragraph_buffer = []
    first_section = True

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            joined = " ".join(line.strip() for line in paragraph_buffer if line.strip())
            append_paragraph(joined, body_style)
            paragraph_buffer = []

    for raw_line in thesis_lines[start_index:]:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped == "---":
            flush_paragraph()
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            if not first_section:
                story.append(PageBreak())
            heading = stripped[2:].strip()

            story.append(Paragraph(convert_inline_markup(heading), heading1_style))
            current_section = heading
            first_section = False
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            heading = stripped[3:].strip()

            story.append(Paragraph(convert_inline_markup(heading), heading1_style))
            current_section = heading
            first_section = False
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(convert_inline_markup(stripped[4:].strip()), heading2_style))
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            story.append(Paragraph(convert_inline_markup(stripped[5:].strip()), heading3_style))
            continue

        if not stripped:
            flush_paragraph()
            story.append(Spacer(1, 0.15 * cm))
            continue

        if current_section and current_section.upper() == "TABLE OF CONTENTS" and re.match(r"^.+\s+\d+$", stripped):
            flush_paragraph()
            story.append(Paragraph(convert_inline_markup(format_toc_page_suffix(stripped)), toc_style))
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            story.append(Paragraph("&bull; " + convert_inline_markup(stripped[2:].strip()), bullet_style))
            continue

        if re.match(r"^\d+(?:\.\d+)*\.\s", stripped):
            flush_paragraph()
            style = toc_style if current_section and current_section.upper() == "TABLE OF CONTENTS" else body_style
            text_value = format_toc_page_suffix(stripped) if style == toc_style else stripped
            story.append(Paragraph(convert_inline_markup(text_value), style))
            continue

        paragraph_buffer.append(stripped)

    flush_paragraph()

    supporting_injected = True

    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)
    enforce_pdf_page_limit(filename, max_pages)
    return filename
