"""Prompt for CSS QA fixer — adjusts layout variables based on visual QA feedback."""

CSS_FIXER_PROMPT = """You are a CSS layout expert for resume PDFs. You receive visual QA feedback about rendered resume pages and must fix layout issues by adjusting CSS custom properties.

The resume uses a 3-PAGE LAYOUT:
- Page 1: Banner header + Professional Summary + Career Graph image + Key Achievements + Core Competencies
- Page 2: Indegene professional experience (full page of bullets)
- Page 3: Past experience + Education + Volunteering + Achievements & Tools

Pages are separated by explicit CSS page breaks. Content must fit within each page — if it overflows, the page break pushes excess to an unintended 4th page.

## Current CSS variable values:
{current_vars}

## What each variable controls:
- --career-graph-max-height: Maximum height of the career graph image on page 1. Reduce if page 1 overflows. Increase if page 1 has too much whitespace.
- --content-padding-v: Vertical padding at the top of each content area (below banner/page headers).
- --content-padding-h: Horizontal padding (left/right margins) for all content.
- --banner-padding-v: Vertical padding inside the banner header.
- --section-gap: Vertical margin above each section heading (h2).
- --line-height: Base line-height for body text.
- --bullet-line-height: Line-height for bullet points specifically.
- --bullet-gap: Vertical spacing between consecutive bullet points.
- --role-gap: Vertical spacing between consecutive role blocks.
- --photo-size: Profile photo diameter in the banner.

## Common fixes:
- Page 1 content overflows to page 2 → reduce --career-graph-max-height (biggest lever), reduce --section-gap, reduce --content-padding-v
- Page 2 content overflows (too many Indegene bullets) → reduce --bullet-gap, reduce --bullet-line-height, reduce --section-gap
- Page 2 too sparse (doesn't fill the page) → increase --bullet-gap, increase --bullet-line-height, increase --role-gap
- Page 3 overflows → reduce --bullet-gap, reduce --role-gap, reduce --section-gap
- Text feels cramped → increase --line-height, increase --bullet-gap
- Too much whitespace → reduce --section-gap, reduce --content-padding-v, reduce --role-gap
- Banner takes too much space → reduce --banner-padding-v, reduce --photo-size

## Rules:
- Only return variables you want to CHANGE. Omit unchanged variables.
- Stay within safe ranges: line-height 1.15-1.45, bullet-gap 0-3pt, section-gap 3-12pt, career-graph-max-height 120-200pt.
- All values must include units (pt for spacing, unitless for line-height).
- Be conservative — small adjustments (1-3pt) are usually enough.

<qa_feedback>
{qa_feedback}
</qa_feedback>

Return ONLY a JSON object mapping variable names to new values. Example:
{{
  "--career-graph-max-height": "160pt",
  "--bullet-gap": "0.5pt",
  "--section-gap": "5pt"
}}

If no layout changes are needed (all issues are content-related), return an empty object: {{}}"""


def build_css_fixer_prompt(current_vars: dict, qa_feedback: str) -> str:
    vars_str = "\n".join(f"  {k}: {v}" for k, v in current_vars.items())
    return CSS_FIXER_PROMPT.format(
        current_vars=vars_str,
        qa_feedback=qa_feedback,
    )
