"""Makes the pipeline's flat scripts (collector.py, extractor.py, ...)
importable from tests/ regardless of the working directory pytest is
invoked from — they're plain modules, not a package, matching the rest of
this pipeline's deliberately simple structure."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# canary.py, pipeline.py, and discover.py all call load_dotenv() at import
# time, which reads a real local .env if one exists in this directory (it
# does, for real development use) straight into the process environment —
# outside any single test's control. Without this fixture, a developer's
# own credentials/backend-chain config would silently change which code
# path individual tests exercise (e.g. LLM_BACKEND_CHAIN overriding
# LLM_PROVIDER), breaking tests that never touched those variables
# themselves. Every test gets a blank slate for these; a test that wants a
# credential present sets it itself via monkeypatch, same as before.
_LLM_ENV_VARS = [
    "LLM_PROVIDER",
    "LLM_BACKEND_CHAIN",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_MODEL_CASCADE",
    "OPENAI_API_KEY",
    "OPENAI_BASE_URL",
    "OPENAI_MODEL_CASCADE",
    "GOOGLE_API_KEY",
    "GOOGLE_MODEL_CASCADE",
    "GROQ_API_KEY",
    "GROQ_MODEL_CASCADE",
    "DEEPSEEK_API_KEY",
    "DEEPSEEK_MODEL_CASCADE",
    "EXTRACTION_MODEL_CASCADE",
    "DISCOVERY_MODEL",
]


@pytest.fixture(autouse=True)
def _clean_llm_env(monkeypatch):
    for var in _LLM_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
