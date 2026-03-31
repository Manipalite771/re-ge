"""Preview panel — resume preview and PDF download."""

import json
from pathlib import Path

import streamlit as st


def render_preview_panel(resume_content: dict, pdf_simple_path, pdf_styled_path):
    """Show resume preview and download buttons."""

    st.markdown("### Resume Preview")

    header = resume_content.get("header", {})
    st.markdown(f"## {header.get('name', '')}")
    st.markdown(f"*{header.get('target_title', '')}*")
    st.markdown(f"{header.get('location', '')} | {header.get('email', '')} | {header.get('phone', '')}")
    st.divider()

    # Summary
    st.markdown("**Professional Summary**")
    st.markdown(resume_content.get("summary", ""))

    # Signature achievements
    achievements = resume_content.get("signature_achievements", [])
    if achievements:
        st.markdown("**Key Achievements**")
        for a in achievements:
            st.markdown(f"- {a}")

    # Competencies
    comps = resume_content.get("competencies", [])
    if comps:
        st.markdown("**Core Competencies**")
        st.markdown(" | ".join(comps))

    # Experience
    for role in resume_content.get("experience", []):
        st.markdown(f"**{role.get('company', '')}** — *{role.get('title', '')}* | {role.get('dates', '')}")
        if role.get("progression"):
            st.caption(role["progression"])
        if role.get("scope_line"):
            st.markdown(f"**{role['scope_line']}**")
        for b in role.get("bullets", []):
            st.markdown(f"- {b}")

    # Education
    for edu in resume_content.get("education", []):
        st.markdown(f"**{edu['institution']}** — {edu['degree']} | {edu.get('dates', '')}")
        if edu.get("gpa"):
            st.caption(edu["gpa"])

    st.divider()

    # Download buttons
    st.markdown("### Download")
    col1, col2 = st.columns(2)

    with col1:
        pdf_simple_path = Path(pdf_simple_path) if pdf_simple_path else None
        if pdf_simple_path and pdf_simple_path.exists():
            with open(pdf_simple_path, "rb") as f:
                st.download_button(
                    "Download Simple PDF",
                    data=f.read(),
                    file_name=pdf_simple_path.name,
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.info("Simple PDF not yet generated")

    with col2:
        pdf_styled_path = Path(pdf_styled_path) if pdf_styled_path else None
        if pdf_styled_path and pdf_styled_path.exists():
            suffix = pdf_styled_path.suffix
            mime = "application/pdf" if suffix == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            with open(pdf_styled_path, "rb") as f:
                st.download_button(
                    f"Download Styled {'PDF' if suffix == '.pdf' else 'DOCX'}",
                    data=f.read(),
                    file_name=pdf_styled_path.name,
                    mime=mime,
                    use_container_width=True,
                )
        else:
            st.info("Styled document not yet generated")
