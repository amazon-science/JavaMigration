"""I/O utility functions."""

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def load_json(filename: str, mode: str = "r", log: bool = True) -> Optional[Dict[Any, Any]]:
    """
    Load JSON file.

    Args:
        filename: Path to JSON file
        mode: File open mode
        log: Whether to log the operation

    Returns:
        Dictionary from JSON file, or None if file doesn't exist
    """
    if log:
        logger.info(f"Reading `{filename}`")

    import os
    if not os.path.exists(filename):
        return None

    with open(filename, mode) as ifile:
        return json.load(ifile)
