"""QA panel — displays visual QA results from the PDF review loop."""

import streamlit as st


def render_qa_panel(qa_results: dict):
    """Show visual QA results across iterations."""

    st.markdown("### Visual QA Results")

    if not qa_results or not qa_results.get("iterations"):
        st.info("No QA results available yet.")
        return

    # Overall status
    if qa_results.get("final_passed"):
        st.success("Visual QA: PASSED")
    else:
        st.warning("Visual QA: Issues remain (see details below)")

    # Summary scores
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Simple PDF Score", f"{qa_results.get('simple_score', 'N/A')}/100")
    with col2:
        st.metric("Styled PDF Score", f"{qa_results.get('styled_score', 'N/A')}/100")

    # Per-iteration details
    for iteration in qa_results.get("iterations", []):
        pass_num = iteration["pass"]
        st.divider()
        st.markdown(f"#### QA Pass {pass_num}")

        for variant_key, variant_label in [("simple", "Simple (ATS-Safe)"), ("styled", "Styled (Formatted)")]:
            qa = iteration.get(variant_key, {})
            if not qa:
                continue

            with st.expander(f"{variant_label} — Score: {qa.get('visual_quality_score', 'N/A')}/100", expanded=(pass_num == len(qa_results["iterations"]))):
                # Page count
                page_count = qa.get("page_count", "?")
                if isinstance(page_count, int) and page_count > 2:
                    st.error(f"Page count: {page_count} (should be 2 or less)")
                else:
                    st.markdown(f"**Pages:** {page_count}")

                # Critical issues
                critical = qa.get("critical_issues", [])
                if critical:
                    st.markdown("**Critical Issues:**")
                    for issue in critical:
                        st.error(issue)
                else:
                    st.success("No critical issues")

                # Minor issues
                minor = qa.get("minor_issues", [])
                if minor:
                    st.markdown("**Minor Issues:**")
                    for issue in minor:
                        st.warning(issue)

                # Content adjustments
                adjustments = qa.get("content_adjustments_needed", [])
                if adjustments:
                    st.markdown("**Content Adjustments Applied:**")
                    for adj in adjustments:
                        st.info(adj)

                # Notes
                notes = qa.get("notes", "")
                if notes:
                    st.caption(notes)
