"""SQLite storage for resume versions and background jobs."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import DB_PATH


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Allow concurrent reads during writes
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS resume_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            level TEXT,
            jd_text TEXT NOT NULL,
            additional_details TEXT,
            jd_analysis_json TEXT,
            strategy_json TEXT,
            resume_content_json TEXT,
            evaluation_json TEXT,
            qa_results_json TEXT,
            feedback TEXT,
            pdf_simple_path TEXT,
            pdf_styled_path TEXT,
            job_id INTEGER,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL DEFAULT 'pending',
            jd_text TEXT NOT NULL,
            additional_details TEXT DEFAULT '',
            refinement_feedback TEXT DEFAULT '',
            current_step TEXT DEFAULT '',
            step_number INTEGER DEFAULT 0,
            result_json TEXT,
            error_message TEXT,
            resume_id INTEGER,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            started_at TEXT,
            completed_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# ── Resume CRUD ──

def save_resume(
    company: str,
    role: str,
    level: str,
    jd_text: str,
    additional_details: str,
    jd_analysis: dict,
    strategy: dict,
    resume_content: dict,
    evaluation: dict,
    pdf_simple_path: str,
    pdf_styled_path: str,
    qa_results: dict = None,
    job_id: int = None,
) -> int:
    conn = _get_conn()
    cursor = conn.execute(
        """
        INSERT INTO resume_versions
            (company, role, level, jd_text, additional_details,
             jd_analysis_json, strategy_json, resume_content_json,
             evaluation_json, qa_results_json, pdf_simple_path, pdf_styled_path,
             job_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company, role, level, jd_text, additional_details,
            json.dumps(jd_analysis), json.dumps(strategy),
            json.dumps(resume_content), json.dumps(evaluation),
            json.dumps(qa_results) if qa_results else None,
            pdf_simple_path, pdf_styled_path, job_id,
        ),
    )
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id


def get_all_resumes() -> list[dict]:
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM resume_versions ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_resume_by_id(resume_id: int) -> Optional[dict]:
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM resume_versions WHERE id = ?", (resume_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_feedback(resume_id: int, feedback: str):
    conn = _get_conn()
    conn.execute(
        "UPDATE resume_versions SET feedback = ? WHERE id = ?",
        (feedback, resume_id),
    )
    conn.commit()
    conn.close()


# ── Job CRUD ──

def create_job(jd_text: str, additional_details: str = "", refinement_feedback: str = "") -> int:
    """Create a new pending job and return its ID."""
    conn = _get_conn()
    cursor = conn.execute(
        "INSERT INTO jobs (jd_text, additional_details, refinement_feedback) VALUES (?, ?, ?)",
        (jd_text, additional_details, refinement_feedback),
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id


def get_job(job_id: int) -> Optional[dict]:
    conn = _get_conn()
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_pending_job() -> Optional[dict]:
    """Get the oldest pending job (FIFO)."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT * FROM jobs WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_job_status(job_id: int, status: str, **kwargs):
    """Update a job's status and optional fields."""
    conn = _get_conn()
    sets = ["status = ?"]
    vals = [status]

    if status == "running" and "started_at" not in kwargs:
        kwargs["started_at"] = datetime.now().isoformat()
    if status in ("completed", "failed") and "completed_at" not in kwargs:
        kwargs["completed_at"] = datetime.now().isoformat()

    for key, val in kwargs.items():
        if key == "result_json" and isinstance(val, dict):
            val = json.dumps(val)
        sets.append(f"{key} = ?")
        vals.append(val)

    vals.append(job_id)
    conn.execute(f"UPDATE jobs SET {', '.join(sets)} WHERE id = ?", vals)
    conn.commit()
    conn.close()


def update_job_step(job_id: int, step_name: str, step_number: int):
    """Update the current step for progress tracking."""
    conn = _get_conn()
    conn.execute(
        "UPDATE jobs SET current_step = ?, step_number = ? WHERE id = ?",
        (step_name, step_number, job_id),
    )
    conn.commit()
    conn.close()


def get_active_jobs() -> list[dict]:
    """Get all non-completed jobs (pending + running), most recent first."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM jobs WHERE status IN ('pending', 'running') ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_jobs(limit: int = 20) -> list[dict]:
    """Get recent jobs across all statuses."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize on import
init_db()
