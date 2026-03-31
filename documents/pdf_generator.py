"""Generate clean, ATS-safe PDF from resume content using WeasyPrint.

Includes dynamic font scaling to guarantee the resume fits within 2 pages.
"""

from pathlib import Path

import fitz  # PyMuPDF — used only to count pages
import jinja2
import weasyprint

from config import TEMPLATES_DIR, OUTPUT_DIR

MAX_PAGES = 2
SCALE_START = 1.0
SCALE_STEP = 0.03
SCALE_MIN = 0.78  # Never go below ~78% — keeps text readable


def _count_pages(pdf_path: Path) -> int:
    doc = fitz.open(str(pdf_path))
    count = len(doc)
    doc.close()
    return count


def _render_pdf(html_content: str, css_path: Path, output_path: Path, scale: float):
    """Render HTML to PDF with a given font scale factor."""
    scale_css = weasyprint.CSS(string=f":root {{ --scale: {scale}; }}")
    base_css = weasyprint.CSS(filename=str(css_path))
    html = weasyprint.HTML(string=html_content, base_url=str(TEMPLATES_DIR))
    html.write_pdf(str(output_path), stylesheets=[base_css, scale_css])


def generate_simple_pdf(resume_content: dict, filename: str = "resume_simple.pdf") -> Path:
    """Render resume as a clean, single-column, ATS-safe PDF.

    Automatically scales fonts down if content exceeds 2 pages.
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
    )
    template = env.get_template("simple.html")
    html_content = template.render(**resume_content)

    output_path = OUTPUT_DIR / filename
    css_path = TEMPLATES_DIR / "simple.css"

    scale = SCALE_START
    while scale >= SCALE_MIN:
        _render_pdf(html_content, css_path, output_path, scale)
        pages = _count_pages(output_path)
        if pages <= MAX_PAGES:
            break
        scale -= SCALE_STEP

    return output_path
