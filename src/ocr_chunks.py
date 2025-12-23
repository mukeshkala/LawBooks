import json
import shutil
from pathlib import Path

from pypdf import PdfReader

from src.runner import run_docker_ocrmypdf


def _load_status(status_path: Path):
    if not status_path.exists():
        return {"page_count": None, "chunks": {}}
    return json.loads(status_path.read_text(encoding="utf-8"))


def _write_status(status_path: Path, data):
    status_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def ocr_pdf_in_chunks(input_pdf, workdir, chunk_size=25, lang="eng", dry_run=False, force=False):
    workdir_path = Path(workdir).resolve()
    workdir_path.mkdir(parents=True, exist_ok=True)
    chunks_dir = workdir_path / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(input_pdf).resolve()
    staged_input = workdir_path / "input.pdf"
    if staged_input.exists():
        staged_input.unlink()
    shutil.copy2(input_path, staged_input)

    reader = PdfReader(str(input_path))
    page_count = len(reader.pages)

    status_path = workdir_path / "status.json"
    status = _load_status(status_path)
    status["page_count"] = page_count

    chunk_paths = []
    for start_page in range(1, page_count + 1, chunk_size):
        end_page = min(start_page + chunk_size - 1, page_count)
        chunk_name = f"chunk_{start_page:04d}-{end_page:04d}.pdf"
        chunk_path = chunks_dir / chunk_name
        chunk_paths.append(chunk_path)

        key = f"{start_page:04d}-{end_page:04d}"
        chunk_record = status["chunks"].get(
            key, {"status": "pending", "attempts": 0, "last_error": None}
        )
        chunk_record["path"] = str(chunk_path.relative_to(workdir_path))

        if chunk_path.exists() and not force:
            chunk_record["status"] = "skipped"
            status["chunks"][key] = chunk_record
            _write_status(status_path, status)
            continue

        chunk_record["attempts"] += 1
        try:
            chunk_record["status"] = "running"
            chunk_record["last_error"] = None
            status["chunks"][key] = chunk_record
            _write_status(status_path, status)

            if dry_run:
                run_docker_ocrmypdf(
                    workdir_path,
                    staged_input,
                    chunk_path,
                    (start_page, end_page),
                    lang,
                    extra_args=None,
                    dry_run=True,
                )
                chunk_record["status"] = "dry_run"
            else:
                run_docker_ocrmypdf(
                    workdir_path,
                    staged_input,
                    chunk_path,
                    (start_page, end_page),
                    lang,
                    extra_args=None,
                )
                chunk_record["status"] = "success"
            status["chunks"][key] = chunk_record
        except Exception as exc:
            chunk_record["status"] = "failed"
            chunk_record["last_error"] = str(exc)
            status["chunks"][key] = chunk_record
            _write_status(status_path, status)
            raise
        else:
            _write_status(status_path, status)

    return chunk_paths
