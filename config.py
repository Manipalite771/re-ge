"""Application configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent

# Persistent data dir — use RAILWAY_VOLUME_MOUNT_PATH if on Railway, else local
DATA_DIR = Path(os.getenv("RAILWAY_VOLUME_MOUNT_PATH", str(BASE_DIR)))
DB_PATH = DATA_DIR / "resumes.db"
OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# These stay with the app code (not persistent volume)
KB_PATH = BASE_DIR / "knowledge" / "kb_content.md"
TEMPLATES_DIR = BASE_DIR / "documents" / "templates"

# AWS / Bedrock
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "us.anthropic.claude-opus-4-6-v1")

# LLM settings
MAX_TOKENS = 16384
TEMPERATURE = 0.3
TEMPERATURE_ANALYSIS = 0.0
