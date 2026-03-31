"""Step 1: JD Analyzer — extracts structured requirements from a job description."""

from core.llm import call_llm_json
from prompts.jd_analysis import build_jd_analysis_prompt


def analyze_jd(jd_text: str, additional_details: str = "") -> dict:
    """Parse a job description into structured fields.

    Returns a dict with: company, role, level, department, role_type,
    key_requirements, must_have_skills, leadership_competencies,
    keywords_to_mirror, etc.
    """
    prompt = build_jd_analysis_prompt(jd_text, additional_details)
    return call_llm_json(
        user_prompt=prompt,
        system_prompt="You are a precise JD analysis engine. Return valid JSON only.",
        temperature=0.0,
    )
