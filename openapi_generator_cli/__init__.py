"""A Python wrapper for the OpenAPI Generator CLI."""

from __future__ import annotations

import importlib.resources
import os
import shutil
import subprocess
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def run(args: list[str] | None = None) -> subprocess.CompletedProcess[bytes]:
    """Run the OpenAPI Generator CLI with the given arguments.

    Args:
        args (list[str], optional):
            The list of arguments to pass to the Open
            API Generator CLI. If not provided, the CLI will
            be run without any arguments.

    Returns:
        subprocess.CompletedProcess[bytes]: The result of running the OpenAPI Generator CLI.

    """
    java_path: Path | str | None
    try:
        from jdk4py import JAVA

        java_path = JAVA
    except ImportError:
        java_path = shutil.which("java")
    if not java_path:
        msg = "java runtime is not found in PATH"
        raise RuntimeError(msg)

    arguments = [java_path]

    java_opts = os.getenv("JAVA_OPTS")
    if java_opts:
        arguments.append(java_opts)

    arguments.append("-jar")

    jar_path = importlib.resources.files("openapi_generator_cli") / "openapi-generator.jar"
    arguments.append(str(jar_path))

    if args and isinstance(args, list):
        arguments.extend(args)

    return subprocess.run(arguments, check=False)  # noqa: S603


def cli() -> None:
    """Run the OpenAPI Generator CLI with the arguments provided on the command line."""
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    run(args)


if __name__ == "__main__":
    cli()
