"""This module defines constants that are global across the app."""
import os

from typing import Any, Dict, Optional  # noqa

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

JAVASCRIPT_DIR = os.path.join(PROJECT_ROOT, 'javascript')

structure = None  # type: Optional[Dict[str, Dict[str, Any]]]
