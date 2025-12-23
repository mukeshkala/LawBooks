"""Text extraction placeholder."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_text(pdf_path: Path, output_path: Path) -> None:
    """Placeholder text extraction."""
    logger.info("extract_text placeholder: %s -> %s", pdf_path, output_path)
