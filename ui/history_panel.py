"""History panel — browse previously generated resumes."""

import json
from pathlib import Path

import streamlit as st

from knowledge.store import get_all_resumes, get_resume_by_id, update_feedback


def render_history_panel():
    """Show all previously generated resumes grouped by company/role."""

    st.markdown("### Resume History")

    resumes = get_all_resumes()

    if not resumes:
        st.info("No resumes generated yet. Use the Generator tab to create your first resume.")
        return

    for r in resumes:
        resume_id = r["id"]
        company = r["company"]
        role = r["role"]
        created = r["created_at"]
        feedback = r.get("feedback", "")

        with st.expander(f"{company} — {role} ({created})", expanded=False):
            # Resume content preview
            try:
                content = json.loads(r["resume_content_json"]) if r["resume_content_json"] else {}
                summary = content.get("summary", "No summary available")
                st.markdown(f"**Summary:** {summary[:200]}...")
            except (json.JSONDecodeError, TypeError):
                st.markdown("*Resume content unavailable*")

            # Evaluation score
            try:
                evaluation = json.loads(r["evaluation_json"]) if r["evaluation_json"] else {}
                score = evaluation.get("overall_score", "N/A")
                st.metric("ATS Score", f"{score}/100")
            except (json.JSONDecodeError, TypeError):
                pass

            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                if r.get("pdf_simple_path") and Path(r["pdf_simple_path"]).exists():
                    with open(r["pdf_simple_path"], "rb") as f:
                        st.download_button(
                            "Simple PDF",
                            data=f.read(),
                            file_name=Path(r["pdf_simple_path"]).name,
                            mime="application/pdf",
                            key=f"simple_{resume_id}",
                        )

            with col2:
                if r.get("pdf_styled_path") and Path(r["pdf_styled_path"]).exists():
                    p = Path(r["pdf_styled_path"])
                    mime = "application/pdf" if p.suffix == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    with open(p, "rb") as f:
                        st.download_button(
                            f"Styled {'PDF' if p.suffix == '.pdf' else 'DOCX'}",
                            data=f.read(),
                            file_name=p.name,
                            mime=mime,
                            key=f"styled_{resume_id}",
                        )

            # Feedback / outcome tracking
            outcome_options = ["", "Got Interview", "Rejected", "No Response", "Offer", "Did not apply"]
            feedback_val = st.selectbox(
                "Outcome",
                outcome_options,
                index=outcome_options.index(feedback) if feedback in outcome_options else 0,
                key=f"feedback_{resume_id}",
            )
            if feedback_val and feedback_val != feedback:
                update_feedback(resume_id, feedback_val)
                st.success(f"Feedback updated to: {feedback_val}")
