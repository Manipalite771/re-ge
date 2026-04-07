"""Prompt for Step 5: Resume Evaluator — ATS scoring and quality checks."""

EVALUATOR_PROMPT = """You are an ATS and resume quality evaluator. Score this resume against the job description.

<resume_content>
{resume_content}
</resume_content>

<jd_analysis>
{jd_analysis}
</jd_analysis>

<jd_keywords>
{jd_keywords}
</jd_keywords>

Evaluate the resume and return a JSON object:

{{
  "overall_score": 85,
  "scores": {{
    "ats_parsing_safety": {{
      "score": 95,
      "max": 100,
      "details": "Assessment of formatting safety for ATS parsing"
    }},
    "keyword_coverage": {{
      "score": 80,
      "max": 100,
      "keywords_found": ["list of JD keywords found in resume"],
      "keywords_missing": ["list of JD keywords NOT found in resume"],
      "coverage_pct": 80
    }},
    "director_signal_density": {{
      "score": 85,
      "max": 100,
      "signals_found": ["scope lines", "cross-functional governance", "outcome ownership", "talent development"],
      "signals_missing": ["any director signals that should be added"],
      "details": "Assessment of director-level positioning"
    }},
    "quantification_density": {{
      "score": 75,
      "max": 100,
      "quantified_bullets": 12,
      "total_bullets": 15,
      "details": "Percentage of bullets with concrete metrics"
    }},
    "relevance_alignment": {{
      "score": 85,
      "max": 100,
      "details": "How well the resume content aligns with the specific JD requirements"
    }},
    "summary_effectiveness": {{
      "score": 90,
      "max": 100,
      "details": "Does the top-third sell the director hypothesis?"
    }}
  }},
  "improvement_suggestions": [
    "Specific, actionable suggestions to improve the resume for this role (max 5)"
  ],
  "company_name_check": {{
    "passed": true,
    "details": "Whether the target company name appears in the resume (it should NOT)"
  }},
  "title_authenticity_check": {{
    "passed": true,
    "details": "Whether the header headline reflects the candidate's actual current title (Senior Manager) rather than copying the JD's target title. The domain/specialization can be angled toward the JD, but the seniority level must match reality."
  }},
  "kb_grounding_check": {{
    "score": 90,
    "max": 100,
    "fabricated_bullets": ["List any bullets that appear to be paraphrased from the JD rather than sourced from the candidate's actual experience in the knowledge base. A bullet fails this check if it reads like a JD requirement restated as an accomplishment without specific projects, metrics, or context from the KB."],
    "details": "Assessment of whether resume content is genuinely drawn from the knowledge base vs. regurgitated from the JD"
  }},
  "estimated_page_count": 3,
  "strengths": [
    "Top 3 strengths of this resume for this role"
  ]
}}

IMPORTANT: The resume uses a 3-PAGE LAYOUT:
- Page 1: Snapshot (summary, career graph, key achievements, competencies)
- Page 2: Deep Dive (Indegene experience only — full page)
- Page 3: Full Picture (past experience, education, volunteering, tools)
Evaluate whether the content is properly distributed across this structure. The Indegene section should have 12-15 rich bullets filling page 2.

Be rigorous but fair. Score against real-world hiring standards for this level and function."""


def build_evaluator_prompt(resume_content: str, jd_analysis: str, jd_keywords: list) -> str:
    return EVALUATOR_PROMPT.format(
        resume_content=resume_content,
        jd_analysis=jd_analysis,
        jd_keywords=", ".join(jd_keywords),
    )
