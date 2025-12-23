"""PDF helper operations."""

from __future__ import annotations

import logging
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def count_pages(pdf_path: Path) -> int:
    reader = PdfReader(str(pdf_path))
    return len(reader.pages)


def merge_pdfs(inputs: list[Path], output_path: Path) -> None:
    """Placeholder for merging PDFs.

    This is a stub to be implemented later.
    """
    logger.info("merge_pdfs placeholder: %s -> %s", inputs, output_path)
