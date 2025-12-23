"""Subprocess helpers (placeholder)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Sequence

logger = logging.getLogger(__name__)


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
