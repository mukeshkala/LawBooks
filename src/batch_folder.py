"""Batch processing helpers for a folder of PDFs."""

from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


def iter_pdfs(input_folder: Path) -> Iterable[Path]:
    return sorted(path for path in input_folder.glob("*.pdf") if path.is_file())


def _book_id_for(pdf_path: Path) -> str:
    return pdf_path.stem


def _status_payload(pdf_path: Path) -> dict:
    return {
        "pdf_path": str(pdf_path),
        "steps": {
            "ocr": "pending",
            "extract_text": "pending",
        },
    }


def create_run_folders(runs_folder: Path, run_id: Optional[str] = None) -> Path:
    resolved_run_id = run_id or uuid.uuid4().hex
    run_path = runs_folder / resolved_run_id
    (run_path / "books").mkdir(parents=True, exist_ok=True)
    return run_path


def prepare_books(
    input_folder: Path,
    runs_folder: Path,
    run_id: Optional[str] = None,
) -> Path:
    """Enumerate PDFs and create per-book status files.

    This function is resumable: if a status.json already exists, it is preserved.
    """
    run_path = create_run_folders(runs_folder, run_id=run_id)
    books_root = run_path / "books"

    for pdf_path in iter_pdfs(input_folder):
        book_id = _book_id_for(pdf_path)
        book_path = books_root / book_id
        book_path.mkdir(parents=True, exist_ok=True)

        status_path = book_path / "status.json"
        if status_path.exists():
            logger.info("Skipping existing status for %s", pdf_path)
            continue

        payload = _status_payload(pdf_path)
        status_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info("Created status for %s", pdf_path)

    return run_path
