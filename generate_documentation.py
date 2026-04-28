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
from reportlab.lib.utils import ImageReader
import pathlib
import html
import re
import io
from datetime import datetime
from PIL import Image as PilImage

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
    source_markdown: str = "THESIS_PROFESSIONAL_original_before_humanized.md",
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
    figure_caption_style = ParagraphStyle(
        "FigureCaption",
        parent=styles["BodyText"],
        fontSize=10,
        alignment=TA_CENTER,
        leading=14,
        spaceAfter=8,
        fontName="Times-Italic",
    )
    code_block_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["BodyText"],
        fontName="Courier",
        fontSize=9,
        leading=12,
        leftIndent=0.6 * cm,
        rightIndent=0.4 * cm,
        firstLineIndent=0,
        spaceBefore=4,
        spaceAfter=6,
        backColor=colors.whitesmoke,
    )
    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["BodyText"],
        fontSize=10,
        leading=12,
        firstLineIndent=0,
        spaceAfter=0,
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

    def append_interface_screenshots_figures() -> None:
        screenshot_dir = pathlib.Path("c:/Thesis_Hr_system/video_assets/screenshots")
        screenshot_items = [
            ("01_home.png", "Figure 11. Home page interface."),
            ("02_login.png", "Figure 12. Authentication and login interface."),
            ("03_analysis.png", "Figure 13. Main analysis input workspace."),
            ("04_market_context.png", "Figure 14. Market context and external indicators view."),
            ("05_dashboard_ceo.png", "Figure 15. CEO dashboard with KPI summary cards."),
            ("06_history.png", "Figure 16. Historical analyses and trend tracking interface."),
        ]

        available_items = [
            (screenshot_dir / file_name, caption)
            for file_name, caption in screenshot_items
            if (screenshot_dir / file_name).exists()
        ]

        if not available_items:
            return

        story.append(Spacer(1, 0.25 * cm))

        max_width = doc.width
        max_height = 15.0 * cm
        # Tall-crop threshold: if aspect ratio (h/w) > 2.5, crop to top portion
        TALL_CROP_HEIGHT_PX = 1400

        for index, (image_path, caption) in enumerate(available_items):
            if index > 0:
                story.append(PageBreak())

            pil_img = PilImage.open(str(image_path))
            orig_w, orig_h = pil_img.size
            if orig_h / orig_w > 2.5:
                # Crop to top TALL_CROP_HEIGHT_PX pixels so image fills page width
                crop_h = min(TALL_CROP_HEIGHT_PX, orig_h)
                pil_img = pil_img.crop((0, 0, orig_w, crop_h))
            # Convert to bytes buffer so ReportLab can read it
            buf = io.BytesIO()
            pil_img.save(buf, format="PNG")
            buf.seek(0)
            img_width, img_height = pil_img.size

            width_scale = max_width / float(img_width)
            height_scale = max_height / float(img_height)
            scale = min(width_scale, height_scale)

            image = Image(
                buf,
                width=img_width * scale,
                height=img_height * scale,
            )
            image.hAlign = "CENTER"

            story.append(KeepTogether([image, Spacer(1, 0.12 * cm), Paragraph(caption, figure_caption_style)]))

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
    in_screenshot_section = False
    in_code_block = False
    code_block_lines = []
    pending_table_lines = []

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        if paragraph_buffer:
            joined = " ".join(line.strip() for line in paragraph_buffer if line.strip())
            append_paragraph(joined, body_style)
            paragraph_buffer = []

    def parse_table_row(row_text: str) -> list[str]:
        row = row_text.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [cell.strip() for cell in row.split("|")]

    def is_separator_row(cells: list[str]) -> bool:
        if not cells:
            return False
        return all(re.match(r"^:?-{3,}:?$", cell) for cell in cells)

    def flush_table() -> None:
        nonlocal pending_table_lines
        if not pending_table_lines:
            return

        parsed_rows = [parse_table_row(line) for line in pending_table_lines]
        data_rows = []
        for idx, cells in enumerate(parsed_rows):
            if idx == 1 and is_separator_row(cells):
                continue
            data_rows.append(cells)

        pending_table_lines = []
        if not data_rows:
            return

        max_cols = max(len(r) for r in data_rows)
        normalized_rows = [
            r + ([""] * (max_cols - len(r))) if len(r) < max_cols else r[:max_cols]
            for r in data_rows
        ]
        table_data = [
            [Paragraph(convert_inline_markup(cell), table_cell_style) for cell in row]
            for row in normalized_rows
        ]

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.15 * cm))

    def flush_code_block() -> None:
        nonlocal code_block_lines
        if not code_block_lines:
            return
        escaped_lines = [html.escape(line) for line in code_block_lines]
        story.append(Paragraph("<br/>".join(escaped_lines), code_block_style))
        code_block_lines = []

    for raw_line in thesis_lines[start_index:]:
        line = raw_line.rstrip()
        stripped = line.strip()

        if in_code_block:
            if stripped.startswith("```"):
                flush_code_block()
                in_code_block = False
            else:
                code_block_lines.append(line)
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            flush_table()
            in_code_block = True
            code_block_lines = []
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            pending_table_lines.append(stripped)
            continue

        if pending_table_lines:
            flush_table()

        if stripped == "---":
            flush_paragraph()
            flush_table()
            if in_screenshot_section:
                append_interface_screenshots_figures()
                in_screenshot_section = False
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            flush_table()
            if in_screenshot_section:
                append_interface_screenshots_figures()
                in_screenshot_section = False
            if not first_section:
                story.append(PageBreak())
            heading = stripped[2:].strip()

            story.append(Paragraph(convert_inline_markup(heading), heading1_style))
            current_section = heading
            first_section = False
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_table()
            if in_screenshot_section:
                append_interface_screenshots_figures()
                in_screenshot_section = False
            heading = stripped[3:].strip()

            story.append(Paragraph(convert_inline_markup(heading), heading1_style))
            current_section = heading
            first_section = False
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flush_table()
            if in_screenshot_section:
                append_interface_screenshots_figures()
                in_screenshot_section = False
            sub_heading = stripped[4:].strip()
            story.append(Paragraph(convert_inline_markup(sub_heading), heading2_style))
            if sub_heading.lower().startswith("4.6 system interface screenshots"):
                in_screenshot_section = True
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            flush_table()
            story.append(Paragraph(convert_inline_markup(stripped[5:].strip()), heading3_style))
            continue

        if not stripped:
            flush_paragraph()
            flush_table()
            story.append(Spacer(1, 0.15 * cm))
            continue

        if current_section and current_section.upper() == "TABLE OF CONTENTS" and re.match(r"^.+\s+\d+$", stripped):
            flush_paragraph()
            flush_table()
            story.append(Paragraph(convert_inline_markup(format_toc_page_suffix(stripped)), toc_style))
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            flush_table()
            story.append(Paragraph("&bull; " + convert_inline_markup(stripped[2:].strip()), bullet_style))
            continue

        if re.match(r"^\d+(?:\.\d+)*\.\s", stripped):
            flush_paragraph()
            flush_table()
            style = toc_style if current_section and current_section.upper() == "TABLE OF CONTENTS" else body_style
            text_value = format_toc_page_suffix(stripped) if style == toc_style else stripped
            story.append(Paragraph(convert_inline_markup(text_value), style))
            continue

        paragraph_buffer.append(stripped)

    flush_paragraph()
    flush_table()
    if in_code_block:
        flush_code_block()
    if in_screenshot_section:
        append_interface_screenshots_figures()

    supporting_injected = True

    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)
    enforce_pdf_page_limit(filename, max_pages)
    return filename
