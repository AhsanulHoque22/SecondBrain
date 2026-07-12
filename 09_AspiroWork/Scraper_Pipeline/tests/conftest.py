"""Makes the pipeline's flat scripts (collector.py, extractor.py, ...)
importable from tests/ regardless of the working directory pytest is
invoked from — they're plain modules, not a package, matching the rest of
this pipeline's deliberately simple structure."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
