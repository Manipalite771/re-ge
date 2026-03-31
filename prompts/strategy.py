"""Prompt for Step 3: Resume Strategy — content selection and sequencing."""

STRATEGY_PROMPT = """You are a resume strategist. Given the JD analysis and the candidate's full knowledge base, create a content strategy for a tailored resume.

<jd_analysis>
{jd_analysis}
</jd_analysis>

<knowledge_base>
{knowledge_base}
</knowledge_base>

Your task: Decide WHAT content to include, HOW to sequence it, and WHAT to emphasize to maximize interview conversion for this specific role.

Return a JSON object:

{{
  "target_title_headline": "The headline to use under the candidate's name (e.g., 'Senior Director, GenAI Strategy & Life Sciences Transformation')",
  "summary_themes": [
    "3-5 themes the professional summary should weave together (e.g., 'GenAI platform leadership', 'cross-functional program delivery', 'pharma domain depth')"
  ],
  "signature_achievements": [
    "3-5 specific achievements from the KB that best prove director-level capability for THIS role. Each should reference a specific metric or outcome."
  ],
  "competencies_to_list": [
    "8-12 competency phrases to include in the Core Competencies section, mirroring JD keywords"
  ],
  "indegene_bullets_to_include": [
    "10-15 specific bullet points or experiences from the KB to include for the Indegene role, ordered by relevance to this JD. Each entry should note: the source experience, why it's relevant, and how to frame it."
  ],
  "indegene_bullets_to_exclude": [
    "Experiences from the KB that should be downplayed or excluded because they're not relevant to this role"
  ],
  "workstream_grouping": "How to group the Indegene experience — by workstream (recommended for breadth roles) or chronological (recommended for deep specialization roles). One of: 'workstream' or 'chronological'",
  "workstream_sequence": [
    "If workstream grouping: ordered list of workstream labels to use and what each covers"
  ],
  "novartis_emphasis": "How much to emphasize Novartis — 'full' (2-3 bullets), 'brief' (1 bullet), or 'minimal' (one-liner)",
  "jnj_intas_emphasis": "How much to emphasize J&J and Intas — 'include' or 'exclude'",
  "earlier_experience_bridge": "REQUIRED if some roles are condensed or excluded. A one-line statement bridging the experience gap, e.g.: 'Earlier: Institutional sales roles at Novartis, J&J, and Intas (2014-2019) — pharma field sales, key accounts, and territory growth across respiratory, OTC, and cardio-diabetic portfolios.' Set to null only if ALL roles are detailed with bullets.",
  "early_career_include": true,
  "volunteering_include": true,
  "education_highlights": [
    "Which education achievements to emphasize for this role"
  ],
  "achievements_tools_include": [
    "Which achievements and tools to highlight"
  ],
  "tone": "Recommended tone: 'strategic-executive', 'technical-leader', 'hybrid-operator', or 'consultative'",
  "page_budget": {{
    "summary_lines": 4,
    "signature_achievements_count": 4,
    "indegene_bullets": 12,
    "other_roles_bullets": 4,
    "total_target_pages": 2
  }}
}}

Key principles:
- For a product/strategy role: prioritize GenAI platform work, product development, and strategic planning
- For a delivery/ops role: prioritize commercial operations, automation, process optimization
- For a consulting role: prioritize solutioning, client engagement, pre-sales, and cross-functional leadership
- Always lead with the most recent and most relevant experience
- The candidate's name is Tanmay Tiwari. Never mention the target company name in the resume content.
- IMPORTANT: The candidate has ~10 years of total experience. If only the recent ~5-6 years are detailed, you MUST include an earlier_experience_bridge to account for the remaining years. The professional summary should reflect total experience (~10 years), not just the detailed portion.
- Do NOT worry about page count — font scaling handles page fitting automatically. Focus on including the right content at the right depth."""


def build_strategy_prompt(jd_analysis: str, knowledge_base: str) -> str:
    return STRATEGY_PROMPT.format(
        jd_analysis=jd_analysis,
        knowledge_base=knowledge_base,
    )
