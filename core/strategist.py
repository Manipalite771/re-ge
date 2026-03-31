"""Step 3: Resume Strategist — decides content selection and sequencing."""

import json

from core.llm import call_llm_json
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.strategy import build_strategy_prompt


def create_strategy(jd_analysis: dict, knowledge_base: str) -> dict:
    """Given JD analysis and full KB, create a content strategy.

    Returns a dict with: target_title_headline, summary_themes,
    signature_achievements, competencies_to_list, bullets to include/exclude,
    grouping approach, emphasis levels, tone, page_budget.
    """
    prompt = build_strategy_prompt(
        jd_analysis=json.dumps(jd_analysis, indent=2),
        knowledge_base=knowledge_base,
    )
    return call_llm_json(
        user_prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.2,
    )
