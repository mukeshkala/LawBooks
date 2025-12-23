"""Subprocess helpers."""

from __future__ import annotations

import logging
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

logger = logging.getLogger(__name__)

__all__ = [
    "DockerNotFoundError",
    "GhostscriptNotFoundError",
    "OcrmypdfNotFoundError",
    "TesseractNotFoundError",
    "docker_available",
    "ghostscript_available",
    "local_ocrmypdf_ready",
    "ocrmypdf_available",
    "run_docker_ocrmypdf",
    "run_local_ocrmypdf",
    "tesseract_available",
]


class DockerNotFoundError(RuntimeError):
    pass


class OcrmypdfNotFoundError(RuntimeError):
    pass


class TesseractNotFoundError(RuntimeError):
    pass


class GhostscriptNotFoundError(RuntimeError):
    pass


def _format_command_for_display(command: Iterable[str]) -> str:
    if os.name == "nt":
        return subprocess.list2cmdline(list(command))
    return " ".join(shlex.quote(part) for part in command)


def docker_available() -> bool:
    return shutil.which("docker") is not None


def ocrmypdf_available() -> bool:
    return shutil.which("ocrmypdf") is not None


def tesseract_available() -> bool:
    return shutil.which("tesseract") is not None


def ghostscript_available() -> bool:
    return any(
        shutil.which(candidate) is not None
        for candidate in ("gs", "gswin64c", "gswin32c")
    )


def local_ocrmypdf_ready() -> bool:
    return (
        ocrmypdf_available()
        and tesseract_available()
        and ghostscript_available()
    )


def _resolve_optimize_level(requested_level: int) -> int:
    if requested_level in {2, 3} and shutil.which("pngquant") is None:
        logger.warning(
            "pngquant not found; falling back to optimize=1. "
            "Install pngquant to enable optimize=%s.",
            requested_level,
        )
        return 1
    return requested_level


def run_docker_ocrmypdf(
    workdir: str,
    in_pdf: str,
    out_pdf: str,
    pages_range: Tuple[int, int],
    lang: str,
    clean: bool = False,
    extra_args: Optional[Iterable[str]] = None,
    timeout_sec: Optional[int] = None,
    dry_run: bool = False,
) -> str:
    workdir_path = Path(workdir).resolve()
    in_path = Path(in_pdf).resolve()
    out_path = Path(out_pdf).resolve()

    try:
        rel_in = in_path.relative_to(workdir_path)
        rel_out = out_path.relative_to(workdir_path)
    except ValueError as exc:
        raise ValueError("Input and output PDFs must be within the workdir.") from exc

    if shutil.which("docker") is None:
        raise DockerNotFoundError(
            "Docker not found. Install Docker Desktop and ensure 'docker' is on PATH."
        )

    start_page, end_page = pages_range
    pages_spec = f"{start_page}-{end_page}"

    optimize_level = _resolve_optimize_level(3)
    args = [
        "--skip-text",
        "--deskew",
        "--optimize",
        str(optimize_level),
        "--language",
        lang,
        "--pages",
        pages_spec,
    ]
    if clean:
        args.append("--clean")
    if extra_args:
        args.extend(extra_args)

    volume_arg = f"{workdir_path}:/data"

    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        volume_arg,
        "jbarlow83/ocrmypdf-alpine",
        *args,
        f"/data/{rel_in.as_posix()}",
        f"/data/{rel_out.as_posix()}",
    ]

    display_command = _format_command_for_display(command)
    if dry_run:
        print(f"DRY RUN: {display_command}")
        return display_command

    try:
        subprocess.run(command, check=True, timeout=timeout_sec)
    except FileNotFoundError as exc:
        raise DockerNotFoundError(
            "Docker not found. Install Docker Desktop and ensure 'docker' is on PATH."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError("OCRmyPDF timed out.") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("OCRmyPDF failed. See docker output for details.") from exc

    return display_command


def run_local_ocrmypdf(
    in_pdf: str,
    out_pdf: str,
    pages_range: Tuple[int, int],
    lang: str,
    clean: bool = False,
    extra_args: Optional[Iterable[str]] = None,
    timeout_sec: Optional[int] = None,
    dry_run: bool = False,
) -> str:
    if not ocrmypdf_available():
        raise OcrmypdfNotFoundError(
            "ocrmypdf not found. Install it locally or use the docker backend."
        )
    if not tesseract_available():
        raise TesseractNotFoundError(
            "tesseract not found. Install it locally or use the docker backend."
        )
    if not ghostscript_available():
        raise GhostscriptNotFoundError(
            "ghostscript not found. Install it locally or use the docker backend."
        )

    start_page, end_page = pages_range
    pages_spec = f"{start_page}-{end_page}"

    optimize_level = _resolve_optimize_level(3)
    args = [
        "--skip-text",
        "--deskew",
        "--optimize",
        str(optimize_level),
        "--language",
        lang,
        "--pages",
        pages_spec,
    ]
    if clean:
        args.append("--clean")
    if extra_args:
        args.extend(extra_args)

    command = [
        "ocrmypdf",
        *args,
        str(in_pdf),
        str(out_pdf),
    ]

    display_command = _format_command_for_display(command)
    if dry_run:
        print(f"DRY RUN: {display_command}")
        return display_command

    try:
        subprocess.run(command, check=True, timeout=timeout_sec)
    except FileNotFoundError as exc:
        raise OcrmypdfNotFoundError(
            "ocrmypdf not found. Install it locally or use the docker backend."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError("ocrmypdf timed out.") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("ocrmypdf failed. See output for details.") from exc

    return display_command


@dataclass
class CommandResult:
    args: Sequence[str]
    returncode: int
    stdout: str = ""
    stderr: str = ""


def run_command(args: Sequence[str]) -> CommandResult:
    """Placeholder subprocess helper.

    This function does not execute anything yet; it returns a dummy result.
    """
    logger.info("run_command placeholder: %s", args)
    return CommandResult(args=args, returncode=0)
