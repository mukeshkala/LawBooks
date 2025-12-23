import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def merge_pdfs(chunk_paths, merged_path):
    if not chunk_paths:
        raise ValueError("No chunk PDFs supplied for merging.")

    merged_path = Path(merged_path)
    merged_path.parent.mkdir(parents=True, exist_ok=True)

    chunks_dir = Path(chunk_paths[0]).resolve().parent
    workdir = chunks_dir.parent
    status_path = workdir / "status.json"
    if not status_path.exists():
        raise FileNotFoundError(f"Missing status file: {status_path}")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    expected_pages = status.get("page_count")

    writer = PdfWriter()
    for chunk_path in chunk_paths:
        reader = PdfReader(str(chunk_path))
        for page in reader.pages:
            writer.add_page(page)

    actual_pages = len(writer.pages)
    if expected_pages is not None and actual_pages != expected_pages:
        raise ValueError(
            f"Merged PDF has {actual_pages} pages; expected {expected_pages}."
        )

    with merged_path.open("wb") as output_file:
        writer.write(output_file)
