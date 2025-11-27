"""Test configuration for ensuring local imports work."""

import sys
from pathlib import Path


# Add repository root to sys.path so the "assistant" package can be imported
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

