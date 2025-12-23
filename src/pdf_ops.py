from pathlib import Path
from typing import Iterable

from pypdf import PdfReader, PdfWriter


def merge_pdfs(chunk_paths: Iterable[Path], merged_path: Path) -> Path:
    writer = PdfWriter()
    expected_pages = 0

    for chunk_path in chunk_paths:
        reader = PdfReader(str(chunk_path))
        expected_pages += len(reader.pages)
        for page in reader.pages:
            writer.add_page(page)

    merged_path.parent.mkdir(parents=True, exist_ok=True)
    with merged_path.open("wb") as output_file:
        writer.write(output_file)

    merged_reader = PdfReader(str(merged_path))
    merged_count = len(merged_reader.pages)

    if merged_count != expected_pages:
        raise ValueError(
            f"Merged PDF page count mismatch: expected {expected_pages}, got {merged_count}."
        )

    return merged_path
