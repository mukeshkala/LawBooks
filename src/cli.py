import argparse

from .batch_folder import ocr_one


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OCR PDFs with OCRmyPDF chunks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ocr_one_parser = subparsers.add_parser("ocr-one", help="OCR a single PDF")
    ocr_one_parser.add_argument("--input", required=True, help="Input PDF path")
    ocr_one_parser.add_argument(
        "--output-folder", required=True, help="Output folder for OCR runs"
    )
    ocr_one_parser.add_argument(
        "--chunk-size", type=int, default=25, help="Pages per OCR chunk"
    )
    ocr_one_parser.add_argument("--lang", default="eng", help="OCR language")
    ocr_one_parser.add_argument(
        "--dry-run", action="store_true", help="Print docker commands without running"
    )
    ocr_one_parser.add_argument(
        "--force", action="store_true", help="Re-run OCR even if chunk exists"
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "ocr-one":
        output_path = ocr_one(
            input_pdf=args.input,
            output_folder=args.output_folder,
            chunk_size=args.chunk_size,
            lang=args.lang,
            dry_run=args.dry_run,
            force=args.force,
        )
        print(str(output_path))


if __name__ == "__main__":
    main()
