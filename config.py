"""Application configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
KB_PATH = BASE_DIR / "knowledge" / "kb_content.md"
DB_PATH = BASE_DIR / "knowledge" / "resumes.db"
TEMPLATES_DIR = BASE_DIR / "documents" / "templates"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# AWS / Bedrock
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "us.anthropic.claude-opus-4-6-v1")

# LLM settings
MAX_TOKENS = 16384
TEMPERATURE = 0.3  # Slight creativity for resume writing
TEMPERATURE_ANALYSIS = 0.0  # Deterministic for JD analysis / evaluation
