"""Input panel — JD textarea + guided additional details."""

import streamlit as st


def render_input_panel() -> tuple[str, str]:
    """Render the input panel and return (jd_text, additional_details)."""

    st.markdown("### Job Description")
    jd_text = st.text_area(
        "Paste the full job description here",
        height=250,
        key="jd_input",
        placeholder="Paste the complete job description...",
    )

    st.markdown("### Additional Details")

    col1, col2 = st.columns(2)
    with col1:
        target_title = st.text_input(
            "Target title (optional override)",
            key="target_title",
            placeholder="e.g., Director, GenAI Strategy",
        )
        highlights = st.text_area(
            "Must-highlight experiences",
            key="highlights",
            placeholder="e.g., Emphasize AstraZeneca work, GenAI platforms...",
            height=80,
        )
    with col2:
        exclusions = st.text_input(
            "Things to exclude or downplay",
            key="exclusions",
            placeholder="e.g., Exclude early career, minimize Novartis...",
        )
        tone = st.selectbox(
            "Resume tone",
            ["Auto-detect from JD", "Strategic Executive", "Technical Leader", "Hybrid Operator", "Consultative"],
            key="tone",
        )

    extra_notes = st.text_area(
        "Any other notes for the generator",
        key="extra_notes",
        placeholder="e.g., This is for a referral, they want someone strong in pharma AI...",
        height=60,
    )

    # Assemble additional details
    parts = []
    if target_title:
        parts.append(f"Preferred target title: {target_title}")
    if highlights:
        parts.append(f"Must highlight: {highlights}")
    if exclusions:
        parts.append(f"Exclude/downplay: {exclusions}")
    if tone != "Auto-detect from JD":
        parts.append(f"Preferred tone: {tone}")
    if extra_notes:
        parts.append(f"Additional notes: {extra_notes}")

    additional_details = "\n".join(parts)

    return jd_text, additional_details
