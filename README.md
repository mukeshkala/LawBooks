# LawBooks OCR

## Prerequisites

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure the `docker` CLI is available on your PATH.

## OCR a single PDF

```bash
python -m src.cli ocr-one --input "C:\Books\A.pdf" --output-folder "C:\Out" --chunk-size 25
```

Add `--dry-run` to print the Docker commands without running OCR.
