"""Evaluation panel — ATS score dashboard and improvement suggestions."""

import streamlit as st


def render_evaluation_panel(evaluation: dict):
    """Display the resume evaluation results."""

    st.markdown("### Resume Evaluation")

    # Overall score
    overall = evaluation.get("overall_score", 0)
    color = "green" if overall >= 80 else "orange" if overall >= 60 else "red"
    st.markdown(f"**Overall Score: :{color}[{overall}/100]**")

    # Score breakdown
    scores = evaluation.get("scores", {})

    cols = st.columns(3)
    score_items = [
        ("ATS Safety", "ats_parsing_safety"),
        ("Keyword Coverage", "keyword_coverage"),
        ("Director Signals", "director_signal_density"),
        ("Quantification", "quantification_density"),
        ("Relevance", "relevance_alignment"),
        ("Summary Impact", "summary_effectiveness"),
    ]

    for i, (label, key) in enumerate(score_items):
        score_data = scores.get(key, {})
        score_val = score_data.get("score", 0)
        with cols[i % 3]:
            st.metric(label, f"{score_val}/100")

    # Company name check
    name_check = evaluation.get("company_name_check", {})
    if name_check.get("passed"):
        st.success("Company name check: PASSED (target company not mentioned)")
    else:
        st.error(f"Company name check: FAILED - {name_check.get('details', '')}")

    # Keyword details
    kw = scores.get("keyword_coverage", {})
    if kw.get("keywords_found"):
        with st.expander("Keywords Found in Resume"):
            st.markdown(", ".join(f"`{k}`" for k in kw["keywords_found"]))
    if kw.get("keywords_missing"):
        with st.expander("Keywords Missing from Resume", expanded=True):
            st.markdown(", ".join(f"`{k}`" for k in kw["keywords_missing"]))

    # Strengths
    strengths = evaluation.get("strengths", [])
    if strengths:
        st.markdown("**Strengths:**")
        for s in strengths:
            st.markdown(f"- {s}")

    # Improvement suggestions
    suggestions = evaluation.get("improvement_suggestions", [])
    if suggestions:
        st.markdown("**Improvement Suggestions:**")
        for s in suggestions:
            st.warning(s)
