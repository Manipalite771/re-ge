"""Visual QA layer — renders PDF pages as images and sends to Claude for review."""

import base64
import json
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF

from core.llm import get_client
from config import ANTHROPIC_MODEL, MAX_TOKENS
from prompts.qa import build_qa_prompt


def pdf_to_images(pdf_path: Path, dpi: int = 200) -> list[bytes]:
    """Convert each page of a PDF to a PNG image bytes.

    Args:
        pdf_path: Path to the PDF file.
        dpi: Resolution for rendering (200 is good for QA without huge payloads).

    Returns:
        List of PNG image bytes, one per page.
    """
    doc = fitz.open(str(pdf_path))
    images = []
    zoom = dpi / 72  # fitz default is 72 DPI
    matrix = fitz.Matrix(zoom, zoom)

    for page in doc:
        pix = page.get_pixmap(matrix=matrix)
        images.append(pix.tobytes("png"))

    doc.close()
    return images


def run_visual_qa(
    pdf_path: Path,
    variant_name: str,
    company: str,
    role: str,
) -> dict:
    """Run visual QA on a rendered PDF.

    Converts PDF pages to images, sends them to Claude Opus 4.6
    with a QA prompt, and returns structured feedback.

    Args:
        pdf_path: Path to the rendered PDF.
        variant_name: "Simple (ATS-Safe)" or "Styled (Formatted)".
        company: Target company name.
        role: Target role name.

    Returns:
        QA result dict with: passed, page_count, critical_issues,
        minor_issues, content_adjustments_needed, visual_quality_score.
    """
    # Convert PDF to images
    page_images = pdf_to_images(pdf_path)

    # Build multimodal message content
    content = []
    for i, img_bytes in enumerate(page_images):
        b64 = base64.b64encode(img_bytes).decode("utf-8")
        content.append({
            "type": "text",
            "text": f"--- Page {i + 1} of {len(page_images)} ---",
        })
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": b64,
            },
        })

    content.append({
        "type": "text",
        "text": "Now review all pages above and provide your QA assessment as JSON.",
    })

    # Build prompt
    qa_prompt = build_qa_prompt(variant_name, company, role)

    # Call Claude with images
    client = get_client()
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=0.0,
        system=qa_prompt,
        messages=[{"role": "user", "content": content}],
    )

    text = response.content[0].text.strip()

    # Parse JSON response
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    text = text.strip()

    return json.loads(text)


def build_qa_fix_instructions(qa_simple: dict, qa_styled: dict) -> str:
    """Combine QA feedback from both variants into fix instructions for the writer.

    Returns a string of specific instructions for the writer to adjust content.
    """
    instructions = []

    for variant, qa in [("Simple PDF", qa_simple), ("Styled DOCX", qa_styled)]:
        critical = qa.get("critical_issues", [])
        adjustments = qa.get("content_adjustments_needed", [])

        if critical:
            instructions.append(f"\n[{variant} - CRITICAL ISSUES]")
            for issue in critical:
                instructions.append(f"- {issue}")

        if adjustments:
            instructions.append(f"\n[{variant} - Content Adjustments]")
            for adj in adjustments:
                instructions.append(f"- {adj}")

    if not instructions:
        return ""

    return "VISUAL QA FEEDBACK — You MUST address these issues:\n" + "\n".join(instructions)
