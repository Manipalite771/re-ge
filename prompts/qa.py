"""Prompt for visual QA of rendered resume PDFs."""

QA_PROMPT = """You are a meticulous resume QA reviewer. You have been given the rendered pages of a resume as images. Inspect every visual detail.

This is the **{variant_name}** variant of the resume, targeting the role of **{role}** at **{company}**.

The resume content was generated from structured JSON and rendered to PDF. Your job is to catch any visual or content issues that hurt professionalism, readability, or ATS compatibility.

Check for ALL of the following:

## Layout & Formatting
- The resume uses a 3-PAGE LAYOUT with explicit page breaks: Page 1 = Snapshot (banner, summary, career graph image, achievements, competencies), Page 2 = Deep Dive (Indegene experience only), Page 3 = Full Picture (past experience, education, etc.). Exactly 3 pages is expected.
- Is page 1 complete? (banner + summary + career graph + achievements + competencies — all fitting on one page)
- Is page 2 properly filled? (Indegene bullets should use most of the page — not sparse, not overflowing). If page 2 has more than ~10% blank space at the bottom, you MUST add this EXACT text to content_adjustments_needed: "Page 2 has blank space — add 1-2 more Indegene bullet points." This is critical — the system uses this flag to pull additional experiences from the knowledge base.
- Is page 3 balanced? (past roles + education + remaining sections)
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
- Are any bullet points awkwardly broken across pages? (page breaks are explicit — content should not overflow between the 3 sections)
- Is the professional summary visible in the top third of page 1?
- Is the career graph image visible and properly sized on page 1?
- There is a narrow right-side navigation panel on every page — this is INTENTIONAL and should NOT be flagged as a layout issue. It shows three vertical labels ("Profile Snapshot", "The Deep Dive", "Career & Credentials") with the current page highlighted. Do NOT penalize this.
- The career graph image on page 1 is a FIXED ASSET (a skill architecture visualization). It is intentionally included and should NOT be flagged as unusual or problematic. Only flag it if it's missing, broken, or severely misaligned.
- Are any sections missing or empty? CRITICAL: Page 2 MUST have Indegene bullet points. If page 2 shows only a header/scope but no bullets, that is a critical content failure.
- Are there any encoding artifacts or garbled characters?
- Is the contact information complete and legible?

## ATS Concerns (Simple Variant Only)
- The main content area is single-column. The narrow right nav panel is a decorative sidebar and does NOT affect ATS parsing of the main content.
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
