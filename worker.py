"""Background worker — polls for pending jobs and runs the pipeline."""

import sys
import json
import time
import traceback
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent))

from config import OUTPUT_DIR
from core.pipeline import run_pipeline
from knowledge.store import (
    init_db, get_pending_job, update_job_status, update_job_step, save_resume,
)

POLL_INTERVAL = 2  # seconds between polling for new jobs


def process_job(job: dict):
    """Run the full pipeline for a single job."""
    job_id = job["id"]
    print(f"[Worker] Starting job #{job_id}")

    update_job_status(job_id, "running")

    def on_step(name: str, step_num: int):
        update_job_step(job_id, name, step_num)
        print(f"  [Job #{job_id}] Step {step_num}: {name}")

    try:
        result = run_pipeline(
            jd_text=job["jd_text"],
            additional_details=job["additional_details"] or "",
            on_step=on_step,
            feedback=job["refinement_feedback"] or "",
        )

        # Save resume to history
        resume_id = save_resume(
            company=result["jd_analysis"].get("company", "Unknown"),
            role=result["jd_analysis"].get("role", "Unknown"),
            level=result["jd_analysis"].get("level", ""),
            jd_text=job["jd_text"],
            additional_details=job["additional_details"] or "",
            jd_analysis=result["jd_analysis"],
            strategy=result["strategy"],
            resume_content=result["resume_content"],
            evaluation=result["evaluation"],
            pdf_simple_path=str(result["pdf_simple_path"]),
            pdf_styled_path=str(result["pdf_styled_path"]),
            qa_results=result.get("qa_results"),
            job_id=job_id,
        )

        # Serialize result for storage (convert Path objects to strings)
        serializable_result = {
            "jd_analysis": result["jd_analysis"],
            "strategy": result["strategy"],
            "resume_content": result["resume_content"],
            "evaluation": result["evaluation"],
            "qa_results": result.get("qa_results", {}),
            "pdf_simple_path": str(result["pdf_simple_path"]),
            "pdf_styled_path": str(result["pdf_styled_path"]),
        }

        update_job_status(
            job_id, "completed",
            result_json=serializable_result,
            resume_id=resume_id,
            current_step="Done!",
        )
        print(f"[Worker] Job #{job_id} completed. Resume #{resume_id} saved.")

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        update_job_status(
            job_id, "failed",
            error_message=error_msg,
            current_step=f"Failed: {str(e)[:100]}",
        )
        print(f"[Worker] Job #{job_id} failed: {e}")


def main():
    """Main worker loop — polls for pending jobs."""
    init_db()
    print("[Worker] Background worker started. Polling for jobs...")

    while True:
        try:
            job = get_pending_job()
            if job:
                process_job(job)
            else:
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n[Worker] Shutting down.")
            break
        except Exception as e:
            print(f"[Worker] Unexpected error: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
