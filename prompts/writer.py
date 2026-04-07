"""Prompt for Step 4: Resume Writer — generates the full resume content."""

WRITER_PROMPT = """You are an expert resume writer. Using the strategy and knowledge base, write a complete, polished resume.

<strategy>
{strategy}
</strategy>

<knowledge_base>
{knowledge_base}
</knowledge_base>

<jd_analysis>
{jd_analysis}
</jd_analysis>

Write the full resume as a JSON object with this structure:

{{
  "header": {{
    "name": "TANMAY TIWARI",
    "target_title": "The headline from the strategy — this MUST reflect the candidate's actual current title (Senior Manager) and expertise, NOT the target job's title. Never use the JD's role title here.",
    "location": "Bangalore, India",
    "phone": "+91-9620506316",
    "email": "tanmay771@gmail.com",
    "linkedin": "linkedin.com/in/tanmay-tiwari-lifesciences"
  }},
  "summary": "A 3-5 line professional summary. Must sell the director hypothesis in seconds. Include scope, outcomes, and leadership themes. Mirror JD keywords naturally.",
  "signature_achievements": [
    "3-5 standalone achievement bullets with metrics. These appear before the experience section."
  ],
  "competencies": [
    "8-12 competency phrases in a single line, pipe-separated"
  ],
  "experience": [
    {{
      "company": "INDEGENE INC.",
      "title": "Senior Manager, GenAI Strategy",
      "location": "Bangalore, India",
      "dates": "May 2021 - Present",
      "progression": "Associate Manager (May 2021-Sep 2023) > Manager (Oct 2023-Dec 2025) > Senior Manager (Jan 2026-Present)",
      "scope_line": "One line establishing scope: team size, budget, portfolio, stakeholders",
      "bullets": [
        "10-15 impact bullets following the formula: Action (strategic decision) + scope + mechanism + outcome + stakeholder context. Each must be specific, quantified where possible, and framed at director level."
      ]
    }},
    {{
      "company": "NOVARTIS INDIA",
      "title": "Medical Representative (Institutional Sales / Key Accounts)",
      "location": "Hyderabad, India",
      "dates": "Apr 2017 - May 2019",
      "scope_line": null,
      "bullets": ["1-3 bullets based on strategy emphasis"]
    }},
    {{
      "company": "JOHNSON & JOHNSON LTD.",
      "title": "Medical Sales Representative (OTC / Territory Growth)",
      "location": "Bangalore, India",
      "dates": "Mar 2016 - Apr 2017",
      "scope_line": null,
      "bullets": ["1-2 bullets if included per strategy"]
    }},
    {{
      "company": "INTAS PHARMACEUTICALS",
      "title": "Field Sales Officer (Cardio-diabetic Portfolio)",
      "location": "Mangalore, India",
      "dates": "Jul 2014 - Jul 2015",
      "scope_line": null,
      "bullets": ["1 bullet if included per strategy"]
    }}
  ],
  "earlier_experience_summary": "A ONE-LINE bridge statement accounting for experience years not covered by the detailed roles above. REQUIRED when the summary says ~10 years but only ~6 years are detailed. Example: 'Earlier: Institutional sales and territory growth roles at Novartis India, Johnson & Johnson, and Intas Pharmaceuticals (2014-2019), building deep pharma commercial and field operations expertise.' This must cover the companies, years, and a brief theme. Set to null ONLY if all career years are already detailed above.",
  "early_career": [
    "Optional early career entries (Myntra, ManipalBlog) if strategy includes them"
  ],
  "volunteering": {{
    "org": "CWF CAMBODIA",
    "role": "Teacher",
    "location": "Phnom Penh, KH",
    "dates": "Dec 2015 - Feb 2016",
    "bullet": "One line if included per strategy"
  }},
  "education": [
    {{
      "institution": "NMIMS Mumbai",
      "degree": "MBA, Marketing",
      "dates": "Jun 2019 - Mar 2021",
      "gpa": "CGPA 3.59/4; Dean's Merit List (Top 5%)",
      "highlights": ["Selected highlights per strategy"]
    }},
    {{
      "institution": "Manipal University",
      "degree": "B.Pharm",
      "dates": "Jul 2009 - Jun 2014",
      "gpa": "CGPA 6.77/10",
      "highlights": ["Selected highlights per strategy"]
    }}
  ],
  "achievements_and_tools": {{
    "achievements": ["Selected achievements per strategy"],
    "tools": ["Selected tools per strategy"]
  }}
}}

CRITICAL RULES:
1. NEVER mention the target company name (from the JD) anywhere in the resume.
2. TITLE INTEGRITY: The "target_title" in the header MUST be based on the candidate's actual current title ("Senior Manager" at Indegene). You may angle the domain/specialization toward the JD (e.g., "Senior Manager, GenAI Strategy & Commercial Analytics"), but NEVER adopt the JD's job title or seniority level (e.g., do NOT use "Director", "VP", "Principal", "Head of", "Lead" unless that is the candidate's actual title). The headline sells positioning — it does not fabricate a title the candidate does not hold.
3. KB-GROUNDING (MANDATORY): Every single bullet point in the resume MUST be directly traceable to a specific experience, project, metric, or outcome documented in the knowledge base. You are REPOSITIONING and REFRAMING real experiences toward the JD — you are NOT inventing new experiences inspired by the JD. If a bullet cannot be traced to a specific KB entry, DELETE IT. The JD tells you what to emphasize; the KB tells you what actually happened. When in doubt, check: "Does the KB contain evidence for this claim?" If no, cut it.
4. Use strong action verbs that convey director-level agency: Led, Set, Established, Defined, Built, Drove, Owned, Transformed, Scaled, Aligned.
4. Quantify everything possible: percentages, dollar amounts, team sizes, timeframes.
5. Keep bullets concise (1-2 lines each). Do NOT trim content to fit pages — font scaling handles page fitting automatically.

3-PAGE LAYOUT RULES:
- Page 1 (The Snapshot): header + summary + career graph (embedded as image, not generated) + key achievements + core competencies. Keep the summary to 3-5 lines and achievements to 3-5 bullets so everything fits on page 1.
- Page 2 (The Deep Dive): ONLY the Indegene experience. This is a full dedicated page.
- Page 3 (Career & Credentials): All other roles (Novartis, J&J, Intas), education, volunteering, early career, achievements & tools. Keep these condensed.
- The Indegene role MUST be the FIRST entry in the "experience" array. Other roles follow after it.

CRITICAL — INDEGENE BULLETS (NON-NEGOTIABLE):
The experience[0] entry (Indegene) MUST contain a "bullets" array with EXACTLY 12-15 bullet points. This is the single most important section of the entire resume — it fills the entire Page 2. An empty or missing bullets array is a FATAL ERROR. Each bullet must be a complete, quantified impact statement drawn from the knowledge base. DO NOT leave the Indegene bullets array empty under any circumstances.
6. Mirror JD keywords in context — never stuff. IMPORTANT: Mirroring keywords means using JD language to DESCRIBE real KB experiences. It does NOT mean copying JD requirements and presenting them as accomplishments. Bad: "Developed enterprise data strategy aligned to business outcomes" (copied from JD). Good: "Defined GenAI content strategy for top-5 pharma account, reducing review cycles by 40%" (real KB experience, framed in JD language).
7. The Indegene experience should show clear progression and increasing scope.
8. Omit roles or sections that the strategy marks for exclusion.
9. EARLIER EXPERIENCE BRIDGE (MANDATORY): If the professional summary claims ~9-10 years of experience but only the recent ~5-6 years are detailed with bullets, you MUST include "earlier_experience_summary" — a single-line bridge that names the earlier companies, date range, and a thematic summary. This prevents a visible gap between claimed years and detailed roles. Example: "Earlier: Institutional sales and territory growth roles at Novartis India, Johnson & Johnson, and Intas Pharmaceuticals (2014–2019), building pharma commercial domain expertise across respiratory, OTC, and cardio-diabetic portfolios."
10. The professional summary can say "~10 years" if that is accurate based on total career span.

BOLD KEY PHRASES IN INDEGENE BULLETS (MANDATORY):
For INDEGENE ONLY, wrap the most JD-relevant phrases within each bullet in **double asterisks** for bold rendering.
- Bold specific phrases WITHIN sentences, NOT the entire bullet. Target 2-5 words per bold span.
- Pick the parts a hiring manager scanning for JD fit would want to see jump out: technology names, methodologies, quantified outcomes, domain terms, leadership scope.
- Aim for 1-3 bold spans per bullet. Not every bullet needs bold — only where it genuinely highlights JD alignment.
- Examples of good bolding:
  - "Led **end-to-end GenAI platform** development across 3 therapeutic areas, driving **40% reduction in content review cycles**"
  - "Built and scaled a **cross-functional team of 12** engineers and strategists to deliver **MLOps infrastructure** serving 5 enterprise clients"
  - "Defined **omnichannel content strategy** for top-5 pharma account, increasing **HCP engagement by 35%** across digital touchpoints"
- Do NOT bold generic verbs, prepositions, or filler. Bold the substance — the thing that proves JD fit.
- Do NOT apply bold to bullets in other roles (Novartis, J&J, Intas, etc.) — Indegene only."""


def build_writer_prompt(strategy: str, knowledge_base: str, jd_analysis: str) -> str:
    return WRITER_PROMPT.format(
        strategy=strategy,
        knowledge_base=knowledge_base,
        jd_analysis=jd_analysis,
    )
