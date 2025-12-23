import datetime
from pathlib import Path

from src.ocr_chunks import ocr_pdf_in_chunks
from src.pdf_ops import merge_pdfs


def ocr_one(input_pdf, output_folder, chunk_size=25, lang="eng", dry_run=False, force=False):
    input_path = Path(input_pdf).resolve()
    output_folder_path = Path(output_folder).resolve()
    run_id = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    book_id = input_path.stem

    run_root = output_folder_path / "runs" / run_id / "books" / book_id
    workdir = run_root / "work"
    output_dir = run_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    chunk_paths = ocr_pdf_in_chunks(
        input_path,
        workdir,
        chunk_size=chunk_size,
        lang=lang,
        dry_run=dry_run,
        force=force,
    )

    merged_path = output_dir / "searchable.pdf"
    if dry_run:
        return merged_path

    merge_pdfs(chunk_paths, merged_path)
    return merged_path
