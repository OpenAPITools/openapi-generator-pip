from __future__ import annotations

import os
import re
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from openapi_generator_cli import cli, run

RETURN_CODE = 23


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


@patch("openapi_generator_cli.run", autospec=True)
@patch("sys.argv", ["openapi-generator-cli", "version"])
def test_cli_exits_with_returncode(run_mock: MagicMock) -> None:
    run_mock.return_value = subprocess.CompletedProcess(args=[], returncode=RETURN_CODE)

    with pytest.raises(SystemExit) as exc_info:
        cli()

    assert exc_info.value.code == RETURN_CODE

    run_mock.assert_called_once_with(["version"])
