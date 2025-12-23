"""Configuration handling for the LawBooks tools."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class AppConfig:
    input_folder: Path
    output_folder: Path
    runs_folder: Path


DEFAULT_RUNS_FOLDER = Path("runs")


def load_config(
    input_folder: Optional[str] = None,
    output_folder: Optional[str] = None,
    runs_folder: Optional[str] = None,
) -> AppConfig:
    """Load configuration from environment variables and defaults."""
    load_dotenv()

    env_input = os.getenv("INPUT_FOLDER")
    env_output = os.getenv("OUTPUT_FOLDER")
    env_runs = os.getenv("RUNS_FOLDER")

    input_value = input_folder or env_input or "input"
    output_value = output_folder or env_output or "output"
    runs_value = runs_folder or env_runs or str(DEFAULT_RUNS_FOLDER)

    return AppConfig(
        input_folder=Path(input_value),
        output_folder=Path(output_value),
        runs_folder=Path(runs_value),
    )
