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
  "target_title_headline": "A professional headline that reflects the candidate's ACTUAL current role and expertise, angled toward the target domain. MUST be grounded in the candidate's real title and experience — do NOT copy or mirror the target job title from the JD. Good: 'Senior Manager, GenAI Strategy & Life Sciences Commercialization' (based on real role). Bad: 'Director of Digital Transformation' (copied from JD). The candidate's current title is Senior Manager — the headline must reflect that seniority level, not the level of the role being applied to.",
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
    "indegene_bullets": "12-15 (Page 2 is entirely dedicated to Indegene — use the full page)",
    "other_roles_bullets": "4-6 (Page 3 — condensed past experience)",
    "total_target_pages": 3,
    "page_1": "Snapshot: summary + career graph (fixed image) + key achievements + competencies",
    "page_2": "Deep Dive: Indegene experience ONLY — full page of properly sequenced, JD-relevant bullets",
    "page_3": "Full Picture: past experience (Novartis, J&J, Intas) + education + volunteering + achievements & tools"
  }}
}}

Key principles:
- For a product/strategy role: prioritize GenAI platform work, product development, and strategic planning
- For a delivery/ops role: prioritize commercial operations, automation, process optimization
- For a consulting role: prioritize solutioning, client engagement, pre-sales, and cross-functional leadership
- Always lead with the most recent and most relevant experience
- The candidate's name is Tanmay Tiwari. Never mention the target company name in the resume content.
- TITLE RULE: The candidate's current title is "Senior Manager" at Indegene. The headline must be built from this real title — never use the target JD's job title (e.g., Director, VP, Principal, etc.) as the candidate's headline. You may angle the domain/specialization toward the JD, but the seniority level must match reality.
- IMPORTANT: The candidate has ~10 years of total experience. If only the recent ~5-6 years are detailed, you MUST include an earlier_experience_bridge to account for the remaining years. The professional summary should reflect total experience (~10 years), not just the detailed portion.
- KB-GROUNDING RULE: Every bullet you select in "indegene_bullets_to_include" MUST trace back to a specific experience, project, or outcome documented in the knowledge base. You are selecting and repositioning real experiences — not inventing new ones from the JD. For each bullet, cite the specific KB source (project name, initiative, metric) so the writer can verify traceability.
- The resume uses a 3-PAGE LAYOUT: Page 1 = snapshot (summary, career graph image, achievements, competencies). Page 2 = Indegene deep-dive (full page of bullets). Page 3 = past experience + education + credentials. Plan content depth accordingly — Indegene gets a full dedicated page, so include 12-15 rich bullets.
- Do NOT worry about font scaling — it handles page fitting automatically. Focus on including the right content at the right depth."""


def build_strategy_prompt(jd_analysis: str, knowledge_base: str) -> str:
    return STRATEGY_PROMPT.format(
        jd_analysis=jd_analysis,
        knowledge_base=knowledge_base,
    )
