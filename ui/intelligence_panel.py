"""Intelligence panel — displays JD analysis results."""

import streamlit as st


def render_intelligence_panel(jd_analysis: dict):
    """Show the extracted JD analysis for user confirmation."""

    st.markdown("### JD Intelligence")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Company", jd_analysis.get("company", "Unknown"))
    with col2:
        st.metric("Role", jd_analysis.get("role", "Unknown"))
    with col3:
        st.metric("Level", jd_analysis.get("level", "Unknown"))

    col4, col5 = st.columns(2)
    with col4:
        st.metric("Department", jd_analysis.get("department", "Unknown"))
    with col5:
        st.metric("Role Type", jd_analysis.get("role_type", "Unknown"))

    # Key requirements
    st.markdown("**Top Requirements:**")
    for i, req in enumerate(jd_analysis.get("key_requirements", [])[:7], 1):
        st.markdown(f"{i}. {req}")

    # Keywords to mirror
    keywords = jd_analysis.get("keywords_to_mirror", [])
    if keywords:
        st.markdown("**Keywords to Mirror:**")
        st.markdown(" | ".join(f"`{k}`" for k in keywords))

    # Leadership competencies
    lc = jd_analysis.get("leadership_competencies", [])
    if lc:
        st.markdown("**Leadership Competencies:**")
        st.markdown(", ".join(lc))

    # Outcome metrics
    om = jd_analysis.get("outcome_metrics_valued", [])
    if om:
        st.markdown("**Metrics This Role Values:**")
        st.markdown(", ".join(om))
