import datetime
from pathlib import Path

from .ocr_chunks import ocr_pdf_in_chunks
from .pdf_ops import merge_pdfs


def ocr_one(
    input_pdf: str,
    output_folder: str,
    chunk_size: int = 25,
    lang: str = "eng",
    dry_run: bool = False,
    force: bool = False,
) -> Path:
    run_id = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    book_id = Path(input_pdf).stem

    base_dir = Path(output_folder) / "runs" / run_id / "books" / book_id
    output_dir = base_dir / "output"
    output_pdf = output_dir / "searchable.pdf"

    chunk_paths = ocr_pdf_in_chunks(
        input_pdf=input_pdf,
        workdir=str(base_dir),
        chunk_size=chunk_size,
        lang=lang,
        dry_run=dry_run,
        force=force,
    )

    if not dry_run:
        merge_pdfs(chunk_paths, output_pdf)

    return output_pdf
