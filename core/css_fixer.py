"""CSS QA fixer — adjusts layout CSS variables based on visual QA feedback."""

import json

from core.llm import call_llm_json
from prompts.css_fixer import build_css_fixer_prompt

# Default CSS variable values (must match what's in simple.css / styled.css)
DEFAULT_CSS_VARS = {
    "--career-graph-max-height": "210pt",
    "--content-padding-v": "10pt",
    "--content-padding-h": "28pt",
    "--banner-padding-v": "16pt",
    "--section-gap": "7pt",
    "--line-height": "1.32",
    "--bullet-line-height": "1.3",
    "--bullet-gap": "1pt",
    "--role-gap": "5pt",
    "--photo-size": "82pt",
    "--nav-width": "26pt",
}


def generate_css_fixes(qa_simple: dict, qa_styled: dict, current_vars: dict | None = None) -> str:
    """Generate CSS variable overrides based on QA feedback.

    Args:
        qa_simple: QA result dict for the simple PDF variant.
        qa_styled: QA result dict for the styled PDF variant.
        current_vars: Current CSS variable values. Defaults to DEFAULT_CSS_VARS.

    Returns:
        A CSS string with :root overrides, or empty string if no changes needed.
        Example: ":root { --career-graph-max-height: 160pt; --bullet-gap: 0.5pt; }"
    """
    if current_vars is None:
        current_vars = DEFAULT_CSS_VARS.copy()

    # Build QA feedback summary for the CSS fixer
    feedback_parts = []
    for variant, qa in [("Simple PDF", qa_simple), ("Styled PDF", qa_styled)]:
        parts = [f"[{variant}]"]
        parts.append(f"  Pages: {qa.get('page_count', '?')}")
        parts.append(f"  Score: {qa.get('visual_quality_score', '?')}/100")

        critical = qa.get("critical_issues", [])
        if critical:
            parts.append("  Critical issues:")
            for issue in critical:
                parts.append(f"    - {issue}")

        minor = qa.get("minor_issues", [])
        if minor:
            parts.append("  Minor issues:")
            for issue in minor:
                parts.append(f"    - {issue}")

        adjustments = qa.get("content_adjustments_needed", [])
        if adjustments:
            parts.append("  Content adjustments:")
            for adj in adjustments:
                parts.append(f"    - {adj}")

        notes = qa.get("notes", "")
        if notes:
            parts.append(f"  Notes: {notes}")

        feedback_parts.append("\n".join(parts))

    qa_feedback = "\n\n".join(feedback_parts)

    # Call LLM to generate CSS fixes
    prompt = build_css_fixer_prompt(current_vars, qa_feedback)
    try:
        overrides = call_llm_json(prompt, temperature=0.0)
    except Exception:
        # If LLM returns empty/unparseable response, skip CSS fixes gracefully
        return ""

    if not overrides:
        return ""

    # Build CSS override string
    declarations = []
    for var_name, value in overrides.items():
        # Validate it's a known variable
        if var_name in DEFAULT_CSS_VARS:
            declarations.append(f"  {var_name}: {value};")
            # Update current_vars for next iteration
            current_vars[var_name] = value

    if not declarations:
        return ""

    return ":root {\n" + "\n".join(declarations) + "\n}"
