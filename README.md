# LawBooks OCR

## Setup

1. Install Docker Desktop and ensure `docker` is available on your PATH.
2. Install Python dependencies (not included here) such as `pypdf`.

## OCR one PDF with chunking

```bash
python -m src.cli ocr-one --input "C:\Books\A.pdf" --output-folder "C:\Out" --chunk-size 25
```

Add `--dry-run` to print the Docker commands without running them.
# LawBooks PDF Processing (Beginner-Friendly)

This repo provides a small, beginner-friendly CLI for preparing PDF processing runs and extracting text from individual PDFs.

## Quick Start (Windows)

### 1) Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) (Optional) Configure environment variables

Copy `.env.example` to `.env` and edit values if you want defaults for input/output folders.

### 4) Run the CLI

Example: prepare a run folder with status files for each PDF in `C:\Books`:

```powershell
python -m src.cli process-folder --input-folder "C:\Books" --output-folder "C:\Out"
```

## Commands

### `process-folder`

Enumerates PDFs in the input folder and creates a run folder:

```
runs/<run_id>/books/<book_id>/status.json
```

The `status.json` is resumable: existing files are preserved.

### `extract-text-one`

Extracts text per page from a single PDF and writes a single text file with page separators:

```
<output-folder>\output_text\<pdfname>.txt
```

Example:

```powershell
python -m src.cli extract-text-one --pdf-path "C:\Books\MyBook.pdf" --output-folder "C:\Out"
```

### `ocr-one`

Placeholder command for future OCR integration.
