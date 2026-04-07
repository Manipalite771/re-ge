"""Step 4: Resume Writer — generates the full resume content as structured JSON."""

import json

from core.llm import call_llm_json
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.writer import build_writer_prompt


def write_resume(
    strategy: dict,
    knowledge_base: str,
    jd_analysis: dict,
    qa_fix_instructions: str = "",
) -> dict:
    """Generate a complete resume as structured JSON.

    Args:
        strategy: Content strategy from the strategist.
        knowledge_base: Full KB text.
        jd_analysis: Parsed JD analysis.
        qa_fix_instructions: Optional fix instructions from visual QA.

    Returns a dict with: header, summary, signature_achievements,
    competencies, experience (list of roles with bullets),
    education, achievements_and_tools, etc.
    """
    prompt = build_writer_prompt(
        strategy=json.dumps(strategy, indent=2),
        knowledge_base=knowledge_base,
        jd_analysis=json.dumps(jd_analysis, indent=2),
    )

    if qa_fix_instructions:
        prompt += f"\n\n{qa_fix_instructions}"

    result = call_llm_json(
        user_prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.3,
    )

    # Safeguard: if Indegene bullets are empty, retry once with explicit instruction
    experience = result.get("experience", [])
    if experience and len(experience[0].get("bullets", [])) < 3:
        retry_prompt = prompt + (
            "\n\nCRITICAL RETRY: Your previous output had ZERO or very few bullets "
            "in the Indegene experience entry. This is a fatal error — Page 2 of the "
            "resume is completely blank. You MUST generate 12-15 detailed impact bullets "
            "for the Indegene role. This is the most important section of the resume."
        )
        result = call_llm_json(
            user_prompt=retry_prompt,
            system_prompt=SYSTEM_PROMPT,
            temperature=0.3,
        )

    return result
