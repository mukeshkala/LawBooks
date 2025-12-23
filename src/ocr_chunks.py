"""OCR chunking placeholder."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def ocr_pdf(pdf_path: Path, output_folder: Path) -> None:
    """Placeholder OCR implementation."""
    logger.info("ocr_pdf placeholder: %s -> %s", pdf_path, output_folder)
