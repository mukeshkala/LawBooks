"""Command-line interface for LawBooks."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from pypdf import PdfReader

from src import batch_folder
from src.config import load_config
from src.log import configure_logging
from src.ocr_chunks import ocr_pdf


def _extract_text_one(pdf_path: Path, output_folder: Path) -> Path:
    output_text_dir = output_folder / "output_text"
    output_text_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_text_dir / f"{pdf_path.stem}.txt"

    reader = PdfReader(str(pdf_path))
    lines: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        lines.append(f"===== PAGE {index:04d} =====")
        text = page.extract_text() or ""
        lines.append(text)

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process PDFs for LawBooks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    process_parser = subparsers.add_parser(
        "process-folder",
        help="Prepare a run folder with status files for each PDF.",
    )
    process_parser.add_argument("--input-folder", required=False)
    process_parser.add_argument("--output-folder", required=False)
    process_parser.add_argument("--run-id", required=False)

    ocr_parser = subparsers.add_parser(
        "ocr-one",
        help="Placeholder OCR command.",
    )
    ocr_parser.add_argument("--pdf-path", required=True)
    ocr_parser.add_argument("--output-folder", required=True)

    extract_parser = subparsers.add_parser(
        "extract-text-one",
        help="Extract text from a single PDF.",
    )
    extract_parser.add_argument("--pdf-path", required=True)
    extract_parser.add_argument("--output-folder", required=True)

    return parser


def main() -> int:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "process-folder":
        config = load_config(args.input_folder, args.output_folder)
        run_path = batch_folder.prepare_books(
            input_folder=config.input_folder,
            runs_folder=config.runs_folder,
            run_id=args.run_id,
        )
        logging.getLogger(__name__).info("Prepared run at %s", run_path)
        return 0

    if args.command == "ocr-one":
        ocr_pdf(Path(args.pdf_path), Path(args.output_folder))
        return 0

    if args.command == "extract-text-one":
        output_path = _extract_text_one(Path(args.pdf_path), Path(args.output_folder))
        logging.getLogger(__name__).info("Wrote text to %s", output_path)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
