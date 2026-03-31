"""Resume Generator App — Streamlit entry point.

Submits jobs to a background worker via SQLite. The browser can be closed
and reopened — completed resumes appear in History.
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from knowledge.store import (
    init_db, create_job, get_job, get_active_jobs, get_recent_jobs,
    get_all_resumes, get_resume_by_id, update_feedback,
)
from ui.input_panel import render_input_panel
from ui.intelligence_panel import render_intelligence_panel
from ui.evaluation_panel import render_evaluation_panel
from ui.preview_panel import render_preview_panel
from ui.history_panel import render_history_panel
from ui.qa_panel import render_qa_panel

# --- Page Config ---
st.set_page_config(
    page_title="Resume Generator | Tanmay Tiwari",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# --- Sidebar ---
with st.sidebar:
    st.title("Resume Generator")
    st.caption("Custom resume tailored to every JD")
    st.divider()

    # Show active jobs count
    active_jobs = get_active_jobs()
    if active_jobs:
        st.info(f"{'🔄' * len(active_jobs)} {len(active_jobs)} job{'s' if len(active_jobs) > 1 else ''} in progress")

    tab_choice = st.radio(
        "Navigate",
        ["Generate", "Jobs", "History"],
        key="nav",
    )

# ══════════════════════════════════════════════════════════
# TAB: Generate
# ══════════════════════════════════════════════════════════
if tab_choice == "Generate":
    st.title("Generate Resume")

    jd_text, additional_details = render_input_panel()

    feedback = st.text_area(
        "Refinement feedback (optional)",
        key="feedback",
        placeholder="e.g., More emphasis on GenAI, remove volunteering section...",
        height=60,
    )

    if st.button(
        "Submit Job",
        type="primary",
        use_container_width=True,
        disabled=not jd_text.strip(),
    ):
        job_id = create_job(
            jd_text=jd_text.strip(),
            additional_details=additional_details,
            refinement_feedback=feedback,
        )
        st.success(f"Job #{job_id} submitted! The pipeline is running in the background. You can close this tab and check back later.")
        st.info("Go to the **Jobs** tab to track progress, or **History** to see completed resumes.")

# ══════════════════════════════════════════════════════════
# TAB: Jobs
# ══════════════════════════════════════════════════════════
elif tab_choice == "Jobs":
    st.title("Jobs")

    recent_jobs = get_recent_jobs(limit=30)

    if not recent_jobs:
        st.info("No jobs yet. Submit one from the Generate tab.")
    else:
        for job in recent_jobs:
            job_id = job["id"]
            status = job["status"]
            created = job["created_at"]
            step = job["current_step"] or ""
            step_num = job["step_number"] or 0

            # Status badge
            if status == "pending":
                badge = "🕐 Pending"
            elif status == "running":
                badge = "🔄 Running"
            elif status == "completed":
                badge = "✅ Completed"
            else:
                badge = "❌ Failed"

            # Header
            jd_preview = (job["jd_text"] or "")[:80].replace("\n", " ")
            with st.expander(f"**Job #{job_id}** — {badge} — {created}", expanded=(status == "running")):

                st.caption(f"JD: {jd_preview}...")

                if status == "running":
                    # Show live progress
                    progress_pct = min(step_num / 13, 0.99) if step_num else 0
                    st.progress(progress_pct, text=step)
                    st.caption("This page auto-refreshes every 5 seconds while a job is running.")

                elif status == "completed":
                    # Show results
                    result_raw = job.get("result_json")
                    if result_raw:
                        result = json.loads(result_raw) if isinstance(result_raw, str) else result_raw

                        # Download buttons
                        st.markdown("#### Download")
                        dl1, dl2 = st.columns(2)

                        pdf_simple = Path(result.get("pdf_simple_path", ""))
                        pdf_styled = Path(result.get("pdf_styled_path", ""))

                        with dl1:
                            if pdf_simple.exists():
                                with open(pdf_simple, "rb") as f:
                                    st.download_button(
                                        "Download Simple PDF",
                                        data=f.read(),
                                        file_name=pdf_simple.name,
                                        mime="application/pdf",
                                        use_container_width=True,
                                        type="primary",
                                        key=f"dl_simple_{job_id}",
                                    )
                        with dl2:
                            if pdf_styled.exists():
                                with open(pdf_styled, "rb") as f:
                                    st.download_button(
                                        "Download Styled PDF",
                                        data=f.read(),
                                        file_name=pdf_styled.name,
                                        mime="application/pdf",
                                        use_container_width=True,
                                        type="primary",
                                        key=f"dl_styled_{job_id}",
                                    )

                        # Detail tabs
                        t_intel, t_preview, t_eval, t_qa = st.tabs(
                            ["JD Intelligence", "Preview", "Evaluation", "Visual QA"]
                        )
                        with t_intel:
                            render_intelligence_panel(result.get("jd_analysis", {}))
                        with t_preview:
                            render_preview_panel(
                                result.get("resume_content", {}),
                                result.get("pdf_simple_path"),
                                result.get("pdf_styled_path"),
                            )
                        with t_eval:
                            render_evaluation_panel(result.get("evaluation", {}))
                        with t_qa:
                            render_qa_panel(result.get("qa_results", {}))

                elif status == "failed":
                    st.error(job.get("error_message", "Unknown error"))

    # Auto-refresh if any jobs are running
    if any(j["status"] in ("pending", "running") for j in recent_jobs):
        time.sleep(5)
        st.rerun()

# ══════════════════════════════════════════════════════════
# TAB: History
# ══════════════════════════════════════════════════════════
elif tab_choice == "History":
    render_history_panel()
