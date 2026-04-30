from __future__ import annotations

import os
import re

import pytest

from openapi_generator_cli import cli, run


def test_cli_version(capfd: pytest.CaptureFixture[str]) -> None:
    result = run(args=["version"])
    assert result.returncode == 0

    captured = capfd.readouterr()
    assert re.match(r"^\d+\.\d+\.\d+(?:-beta\d*)?$", captured.out.split(os.linesep)[0])
    assert not captured.err


def test_no_args(capfd: pytest.CaptureFixture[str]) -> None:
    result = run(args=[])
    assert result.returncode == 1

    captured = capfd.readouterr()
    assert captured.out.split("\n")[0] in (
        # >=5.0.0
        "usage: openapi-generator-cli <command> [<args>]",
        # >=3.0.1,<5.0.0
        "The following generators are available:",
        # ==3.0.0
        "",
    )
    assert not captured.err


def test_invalid_arg(capfd: pytest.CaptureFixture[str]) -> None:
    result = run(args=["--invalid-arg-404"])
    assert result.returncode == 1

    captured = capfd.readouterr()
    assert not captured.out
    assert (
        "Found unexpected parameters: [--invalid-arg-404]"
        in captured.err.split(os.linesep)[0]
    )


def test_cli_invalid_arg(capfd: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli(["openapi-generator-cli", "--invalid-arg-404"])
    assert exc_info.value.code == 1

    captured = capfd.readouterr()
    assert not captured.out
    assert (
        "Found unexpected parameters: [--invalid-arg-404]"
        in captured.err.split(os.linesep)[0]
    )
