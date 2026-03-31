"""Step 5: Resume Evaluator — ATS scoring and quality checks."""

import json

from core.llm import call_llm_json
from prompts.evaluator import build_evaluator_prompt


def evaluate_resume(resume_content: dict, jd_analysis: dict) -> dict:
    """Score a generated resume against ATS and quality criteria.

    Returns a dict with: overall_score, scores (ats_parsing_safety,
    keyword_coverage, director_signal_density, quantification_density,
    relevance_alignment, summary_effectiveness), improvement_suggestions,
    company_name_check, strengths.
    """
    keywords = jd_analysis.get("keywords_to_mirror", [])

    prompt = build_evaluator_prompt(
        resume_content=json.dumps(resume_content, indent=2),
        jd_analysis=json.dumps(jd_analysis, indent=2),
        jd_keywords=keywords,
    )
    return call_llm_json(
        user_prompt=prompt,
        system_prompt="You are a rigorous resume quality evaluator. Return valid JSON only.",
        temperature=0.0,
    )
