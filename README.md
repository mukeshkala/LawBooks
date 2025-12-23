# LawBooks OCR

## Setup

1. Install Docker Desktop and ensure `docker` is available on your PATH.
2. Install Python dependencies (not included here) such as `pypdf`.

## OCR one PDF with chunking

```bash
python -m src.cli ocr-one --input "C:\Books\A.pdf" --output-folder "C:\Out" --chunk-size 25
```

Add `--dry-run` to print the Docker commands without running them.
