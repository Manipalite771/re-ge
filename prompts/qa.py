"""Prompt for visual QA of rendered resume PDFs."""

QA_PROMPT = """You are a meticulous resume QA reviewer. You have been given the rendered pages of a resume as images. Inspect every visual detail.

This is the **{variant_name}** variant of the resume, targeting the role of **{role}** at **{company}**.

The resume content was generated from structured JSON and rendered to PDF. Your job is to catch any visual or content issues that hurt professionalism, readability, or ATS compatibility.

Check for ALL of the following:

## Layout & Formatting
- Page count is handled by automatic font scaling, so 2 pages is expected. Only flag page count if text is unreadably small (below ~8pt equivalent).
- Is the page balance good? (Page 1 should be full and dense; page 2 should be at least 40% filled, not just 2 lines)
- Are there any text overflows, cut-off words, or clipped lines?
- Are margins consistent on all sides?
- Is the header properly centered and readable?
- Are section headings clearly distinguished from body text?
- Is there appropriate white space (not too cluttered, not too sparse)?

## Typography & Readability
- Is the font size readable (not too small, not too large)?
- Are bullet points properly aligned and indented?
- Is the line spacing consistent?
- Are bold/italic styles applied consistently?
- Are dates right-aligned or consistently positioned?

## Content Issues (Visible from Rendering)
- Are any bullet points awkwardly broken across pages?
- Is the professional summary visible in the top third of page 1?
- Are any sections missing or empty?
- Are there any encoding artifacts or garbled characters?
- Is the contact information complete and legible?

## ATS Concerns (Simple Variant Only)
- Is the layout truly single-column? (No side-by-side elements that could confuse ATS)
- Are section headings standard and clear?

Return a JSON object:

{{
  "passed": true or false,
  "page_count": number of pages,
  "critical_issues": [
    "Issues that MUST be fixed before sharing (overflow, 3+ pages, missing sections, garbled text)"
  ],
  "minor_issues": [
    "Nice-to-fix issues (spacing tweaks, minor alignment, page balance)"
  ],
  "content_adjustments_needed": [
    "Specific content changes to fix issues. Do NOT suggest trimming content to reduce page count — font scaling handles that automatically. Only suggest content changes for quality issues (garbled text, missing sections, awkward phrasing visible in the render)."
  ],
  "visual_quality_score": 0-100,
  "notes": "Any other observations about the visual quality"
}}

Be strict on critical issues (page count, readability, missing content) but pragmatic on minor cosmetic issues."""


def build_qa_prompt(variant_name: str, company: str, role: str) -> str:
    return QA_PROMPT.format(
        variant_name=variant_name,
        company=company,
        role=role,
    )
