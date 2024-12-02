from __future__ import annotations

import importlib.resources
import os
import subprocess
import sys


def run(args: list[str] | None = None) -> None:
    arguments = ["java"]

    java_opts = os.getenv("JAVA_OPTS")
    if java_opts:
        arguments.append(java_opts)

    arguments.append("-jar")

    jar_path = importlib.resources.files("openapi_generator_cli") / "openapi-generator.jar"
    arguments.append(str(jar_path))

    if args and type(args) == list:
        arguments.extend(args)

    subprocess.call(arguments)  # noqa: S603


def cli() -> None:
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    run(args)


if __name__ == "__main__":
    cli()
