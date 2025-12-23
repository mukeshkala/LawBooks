import argparse

from src.batch_folder import ocr_one


def build_parser():
    parser = argparse.ArgumentParser(description="OCR processing utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ocr_one_parser = subparsers.add_parser("ocr-one", help="OCR a single PDF in chunks.")
    ocr_one_parser.add_argument("--input", required=True, help="Path to the input PDF.")
    ocr_one_parser.add_argument(
        "--output-folder", required=True, help="Folder where output runs are created."
    )
    ocr_one_parser.add_argument("--chunk-size", type=int, default=25)
    ocr_one_parser.add_argument("--lang", default="eng")
    ocr_one_parser.add_argument("--dry-run", action="store_true", help="Print docker commands only.")
    ocr_one_parser.add_argument("--force", action="store_true", help="Rebuild existing chunks.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "ocr-one":
        output_path = ocr_one(
            args.input,
            args.output_folder,
            chunk_size=args.chunk_size,
            lang=args.lang,
            dry_run=args.dry_run,
            force=args.force,
        )
        if not args.dry_run:
            print(f"Searchable PDF written to {output_path}")


if __name__ == "__main__":
    main()
