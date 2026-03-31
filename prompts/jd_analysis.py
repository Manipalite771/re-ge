"""Prompt for Step 1: JD Analysis."""

JD_ANALYSIS_PROMPT = """Analyze the following job description and extract structured information.

<job_description>
{jd_text}
</job_description>

{additional_details_section}

Extract and return a JSON object with these fields:

{{
  "company": "Company name (detected from JD)",
  "role": "Exact role title from the JD",
  "level": "Detected seniority level (e.g., Director, Senior Manager, VP)",
  "department": "Functional area (e.g., Product, Engineering, Operations, Marketing)",
  "role_type": "One of: strategy, product, delivery, operations, consulting, hybrid",
  "location": "Location if mentioned",
  "key_requirements": [
    "Top 10 most important requirements/qualifications from the JD, ordered by importance"
  ],
  "must_have_skills": [
    "Hard skills and technical competencies explicitly required"
  ],
  "leadership_competencies": [
    "Leadership capabilities mentioned or implied (e.g., strategy setting, change management, talent development)"
  ],
  "keywords_to_mirror": [
    "Top 15 keywords/phrases from the JD that should appear in the resume"
  ],
  "industry_context": "Industry or domain context (pharma, tech, consulting, etc.)",
  "outcome_metrics_valued": [
    "Types of metrics/outcomes this role cares about (revenue, efficiency, quality, adoption, etc.)"
  ],
  "experience_years": "Years of experience required if stated",
  "culture_signals": [
    "Any cultural or soft skill signals (collaborative, entrepreneurial, data-driven, etc.)"
  ]
}}

Be precise. Only include what's actually in the JD or strongly implied. Do not invent requirements."""


def build_jd_analysis_prompt(jd_text: str, additional_details: str = "") -> str:
    additional_section = ""
    if additional_details.strip():
        additional_section = f"""<additional_context>
The candidate has provided these additional details to consider:
{additional_details}
</additional_context>"""

    return JD_ANALYSIS_PROMPT.format(
        jd_text=jd_text,
        additional_details_section=additional_section,
    )
