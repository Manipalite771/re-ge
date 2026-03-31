"""Orchestration pipeline — ties all steps together, including visual QA loop."""

import json
from pathlib import Path
from typing import Callable, Optional

from core.jd_analyzer import analyze_jd
from core.knowledge import load_knowledge_base
from core.strategist import create_strategy
from core.writer import write_resume
from core.evaluator import evaluate_resume
from core.qa import run_visual_qa, build_qa_fix_instructions
from documents.pdf_generator import generate_simple_pdf
from documents.docx_generator import generate_styled_pdf


MAX_QA_ITERATIONS = 5
QA_SCORE_THRESHOLD = 80


def _generate_documents(resume_content: dict, base_name: str) -> tuple[Path, Path]:
    """Generate both PDF variants and return their paths."""
    pdf_simple = generate_simple_pdf(resume_content, f"{base_name}_simple.pdf")
    styled_path = generate_styled_pdf(resume_content, f"{base_name}_styled.pdf")
    return pdf_simple, styled_path


def run_pipeline(
    jd_text: str,
    additional_details: str = "",
    on_step: Optional[Callable[[str, int], None]] = None,
    feedback: str = "",
) -> dict:
    """Run the full resume generation pipeline with visual QA loop.

    Steps 1-5: JD Analysis -> KB Load -> Strategy -> Write -> Evaluate
    Step 6: Render PDFs
    Steps 7+: Visual QA loop — keeps iterating until both variants
              score >= 80 or max 5 iterations reached.

    Args:
        jd_text: The raw job description text.
        additional_details: Extra context from the user.
        on_step: Callback(step_name, step_number) for progress updates.
        feedback: Optional refinement feedback for regeneration.

    Returns:
        dict with keys: jd_analysis, strategy, resume_content, evaluation,
                        qa_results, pdf_simple_path, pdf_styled_path
    """

    def _step(name: str, num: int):
        if on_step:
            on_step(name, num)

    # Step 1: Analyze JD
    _step("Analyzing job description...", 1)
    if feedback:
        additional_details += f"\n\nREGENERATION FEEDBACK: {feedback}"
    jd_analysis = analyze_jd(jd_text, additional_details)

    # Step 2: Load knowledge base
    _step("Loading knowledge base...", 2)
    kb = load_knowledge_base()

    # Step 3: Create strategy
    _step("Creating content strategy...", 3)
    strategy = create_strategy(jd_analysis, kb)

    # Step 4: Write resume
    _step("Writing resume...", 4)
    resume_content = write_resume(strategy, kb, jd_analysis)

    # Step 5: Evaluate
    _step("Evaluating resume quality...", 5)
    evaluation = evaluate_resume(resume_content, jd_analysis)

    # Prepare file names
    company = jd_analysis.get("company", "Unknown").replace(" ", "_").replace("/", "_")
    role = jd_analysis.get("role", "Unknown").replace(" ", "_").replace("/", "_")
    timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{company}_{role}_{timestamp}"

    # Step 6: Initial render
    _step("Generating PDF documents...", 6)
    pdf_simple, pdf_styled = _generate_documents(resume_content, base_name)

    # Steps 7+: Visual QA loop — score-based with threshold
    qa_results = {"iterations": [], "final_passed": False}
    # Accumulate fix instructions across iterations so the writer sees full history
    cumulative_fixes = []

    for qa_pass in range(MAX_QA_ITERATIONS):
        step_label = f"Visual QA pass {qa_pass + 1}/{MAX_QA_ITERATIONS}"
        _step(f"{step_label} — reviewing simple PDF...", 7 + qa_pass)

        # QA the simple PDF
        qa_simple = run_visual_qa(
            pdf_path=pdf_simple,
            variant_name="Simple (ATS-Safe)",
            company=jd_analysis.get("company", "Unknown"),
            role=jd_analysis.get("role", "Unknown"),
        )

        _step(f"{step_label} — reviewing styled PDF...", 7 + qa_pass)

        # QA the styled PDF
        qa_styled = run_visual_qa(
            pdf_path=pdf_styled,
            variant_name="Styled (Formatted)",
            company=jd_analysis.get("company", "Unknown"),
            role=jd_analysis.get("role", "Unknown"),
        )

        iteration_result = {
            "pass": qa_pass + 1,
            "simple": qa_simple,
            "styled": qa_styled,
        }
        qa_results["iterations"].append(iteration_result)

        # Check scores
        simple_score = qa_simple.get("visual_quality_score", 0)
        styled_score = qa_styled.get("visual_quality_score", 0)

        if simple_score >= QA_SCORE_THRESHOLD and styled_score >= QA_SCORE_THRESHOLD:
            qa_results["final_passed"] = True
            break

        # Last iteration — accept whatever we have
        if qa_pass >= MAX_QA_ITERATIONS - 1:
            qa_results["final_passed"] = False
            break

        # Build fix instructions and re-run writer
        _step(f"Fixing issues from QA pass {qa_pass + 1} (simple: {simple_score}, styled: {styled_score})...", 7 + qa_pass)

        fix_instructions = build_qa_fix_instructions(qa_simple, qa_styled)
        if fix_instructions:
            cumulative_fixes.append(f"--- QA Pass {qa_pass + 1} Feedback ---\n{fix_instructions}")

        combined_fixes = "\n\n".join(cumulative_fixes)

        # Re-run writer with cumulative QA fix instructions
        resume_content = write_resume(
            strategy=strategy,
            knowledge_base=kb,
            jd_analysis=jd_analysis,
            qa_fix_instructions=combined_fixes,
        )

        # Re-render documents
        base_name_fixed = f"{base_name}_v{qa_pass + 2}"
        pdf_simple, pdf_styled = _generate_documents(resume_content, base_name_fixed)

    # Final QA scores
    last_iter = qa_results["iterations"][-1]
    qa_results["simple_score"] = last_iter["simple"].get("visual_quality_score", 0)
    qa_results["styled_score"] = last_iter["styled"].get("visual_quality_score", 0)
    qa_results["total_iterations"] = len(qa_results["iterations"])

    return {
        "jd_analysis": jd_analysis,
        "strategy": strategy,
        "resume_content": resume_content,
        "evaluation": evaluation,
        "qa_results": qa_results,
        "pdf_simple_path": pdf_simple,
        "pdf_styled_path": pdf_styled,
    }
