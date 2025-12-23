import os
import shlex
import shutil
import subprocess
from pathlib import Path


def _quote_windows_path(path_str: str) -> str:
    if os.name != "nt":
        return shlex.quote(path_str)
    if path_str.startswith('"') and path_str.endswith('"'):
        return path_str
    return f'"{path_str}"'


def _build_docker_command(workdir: Path, in_pdf: Path, out_pdf: Path, pages_range, lang, extra_args):
    start_page, end_page = pages_range
    args = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{workdir}:/data",
        "jbarlow83/ocrmypdf-alpine",
        "--skip-text",
        "--deskew",
        "--clean",
        "--optimize",
        "3",
        "--language",
        lang,
        "--pages",
        f"{start_page}-{end_page}",
    ]
    if extra_args:
        args.extend(extra_args)
    args.extend([f"/data/{in_pdf.as_posix()}", f"/data/{out_pdf.as_posix()}"])
    return args


def _command_for_display(args):
    display = []
    for arg in args:
        if os.name == "nt" and (":" in arg or "\\" in arg or " " in arg):
            display.append(_quote_windows_path(arg))
        else:
            display.append(shlex.quote(arg))
    return " ".join(display)


def run_docker_ocrmypdf(
    workdir,
    in_pdf,
    out_pdf,
    pages_range,
    lang,
    extra_args=None,
    timeout_sec=1800,
    dry_run=False,
):
    if shutil.which("docker") is None:
        raise RuntimeError(
            "Docker executable not found. Install Docker Desktop and ensure `docker` "
            "is on your PATH."
        )

    workdir_path = Path(workdir).resolve()
    rel_in = Path(in_pdf).resolve().relative_to(workdir_path)
    rel_out = Path(out_pdf).resolve().relative_to(workdir_path)

    args = _build_docker_command(workdir_path, rel_in, rel_out, pages_range, lang, extra_args)
    display_command = _command_for_display(args)
    if dry_run:
        print(display_command)
        return display_command

    result = subprocess.run(
        args,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    return result.stdout
