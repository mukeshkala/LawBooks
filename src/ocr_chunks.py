import json
import shutil
from pathlib import Path
from typing import List

from pypdf import PdfReader

from .runner import run_docker_ocrmypdf


def _load_status(status_path: Path) -> dict:
    if status_path.exists():
        return json.loads(status_path.read_text(encoding="utf-8"))
    return {"chunks": {}}


def _write_status(status_path: Path, status_data: dict) -> None:
    status_path.write_text(
        json.dumps(status_data, indent=2, sort_keys=True), encoding="utf-8"
    )


def ocr_pdf_in_chunks(
    input_pdf: str,
    workdir: str,
    chunk_size: int = 25,
    lang: str = "eng",
    dry_run: bool = False,
    force: bool = False,
) -> List[Path]:
    workdir_path = Path(workdir)
    workdir_path.mkdir(parents=True, exist_ok=True)
    chunks_dir = workdir_path / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    source_path = Path(input_pdf).resolve()
    local_input = workdir_path / "input.pdf"
    if source_path != local_input:
        shutil.copy2(source_path, local_input)

    reader = PdfReader(str(source_path))
    page_count = len(reader.pages)

    status_path = workdir_path / "status.json"
    status_data = _load_status(status_path)
    chunk_records = status_data.setdefault("chunks", {})

    chunk_paths: List[Path] = []

    for start_page in range(1, page_count + 1, chunk_size):
        end_page = min(start_page + chunk_size - 1, page_count)
        chunk_name = f"chunk_{start_page:04d}-{end_page:04d}.pdf"
        chunk_path = chunks_dir / chunk_name
        chunk_paths.append(chunk_path)

        record = chunk_records.get(
            chunk_name, {"attempts": 0, "last_error": None, "status": "pending"}
        )

        if chunk_path.exists() and not force:
            record["status"] = "skipped"
            chunk_records[chunk_name] = record
            _write_status(status_path, status_data)
            continue

        record["attempts"] = record.get("attempts", 0) + 1
        chunk_records[chunk_name] = record
        _write_status(status_path, status_data)

        try:
            run_docker_ocrmypdf(
                workdir=str(workdir_path),
                in_pdf=str(local_input),
                out_pdf=str(chunk_path),
                pages_range=(start_page, end_page),
                lang=lang,
                extra_args=None,
                timeout_sec=None,
                dry_run=dry_run,
            )
            record["status"] = "dry_run" if dry_run else "completed"
            record["last_error"] = None
        except Exception as exc:
            record["status"] = "failed"
            record["last_error"] = str(exc)
            chunk_records[chunk_name] = record
            _write_status(status_path, status_data)
            raise

        chunk_records[chunk_name] = record
        _write_status(status_path, status_data)

    return chunk_paths
"""OCR chunking placeholder."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def ocr_pdf(pdf_path: Path, output_folder: Path) -> None:
    """Placeholder OCR implementation."""
    logger.info("ocr_pdf placeholder: %s -> %s", pdf_path, output_folder)
