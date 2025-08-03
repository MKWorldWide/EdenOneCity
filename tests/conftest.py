"""Test configuration for path adjustments."""
import sys
from pathlib import Path

# Ensure repository root is on path for "src" package imports
sys.path.append(str(Path(__file__).resolve().parents[1]))
