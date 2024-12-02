from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.request import urlopen

from natsort import natsorted

if TYPE_CHECKING:
    from collections.abc import KeysView

MVN_BASE_URL = "https://search.maven.org"


def download_openapi_generator_jar(version: str) -> None:
    download_url = (
        MVN_BASE_URL
        + "/remotecontent?filepath=org/openapitools/openapi-generator-cli/"
        + version
        + f"/openapi-generator-cli-{version}.jar"
    )

    Path("openapi-generator.jar").unlink(missing_ok=True)

    print(f"[{version}] URL: {download_url!r}")
    response = urlopen(download_url)  #  noqa: S310

    if response.status != 200:  # noqa: PLR2004
        msg = f"{response.status}: {download_url}"
        raise RuntimeError(msg)

    with Path("openapi_generator_cli/openapi-generator.jar").open("wb") as openapi_generator_jar:
        openapi_generator_jar.write(response.read())
        openapi_generator_jar.close()

    updated_toml = (
        Path("pyproject.toml")  # noqa: SIM115
        .open("r")
        .read()
        .replace(
            '[tool.poetry]\nversion = "0"',
            f'[tool.poetry]\nversion = "{version}"',
            1,
        )
    )
    with Path("pyproject.toml").open("w") as toml:
        toml.write(updated_toml)


def get_available_versions() -> list[str]:
    mvn_url = (
        MVN_BASE_URL + "/solrsearch/select?q=g:org.openapitools+AND+a:openapi-generator-cli&core=gav"
        "&start=0&rows=200"
    )
    response = urlopen(mvn_url)  #  noqa: S310
    docs = json.loads(response.read())["response"]["docs"]
    return [doc["v"] for doc in docs]


def get_published_vesions() -> KeysView[str]:
    pypi_url = "https://pypi.org/pypi/openapi-generator-cli/json"
    response = urlopen(pypi_url)  #  noqa: S310

    if response.status != 200:  # noqa: PLR2004
        msg = f"{response.status}: {pypi_url}"
        raise RuntimeError(msg)

    published_releases = json.loads(response.read()).get("releases")
    if not isinstance(published_releases, dict):
        msg = f"Expected dict, got {type(published_releases)}"
        raise TypeError(msg)

    return published_releases.keys()


def download_latest_jar_for_test() -> None:
    latest_version = natsorted(get_available_versions())[-1]
    print(f"[{latest_version}] Downloading...")
    download_openapi_generator_jar(latest_version)
    print(f"[{latest_version}] Downloaded!")


def publish(*, dryrun: bool = False) -> None:
    pytest_path = shutil.which("pytest")
    poetry_path = shutil.which("poetry")

    unpublished_versions = natsorted(set(get_available_versions()) - set(get_published_vesions()))

    for publishing_version in unpublished_versions:
        print(f"[{publishing_version}] Downloading...")
        download_openapi_generator_jar(publishing_version)

        print(f"[{publishing_version}] Testing...")
        subprocess.check_call([pytest_path])

        if dryrun:
            continue

        print(f"[{publishing_version}] Building...")
        subprocess.check_call([poetry_path, "build", "-v"])

        print(f"[{publishing_version}] Publishing to TestPyPI...")
        subprocess.check_call([poetry_path, "publish", "-r", "testpypi", "-v"])

        print(f"[{publishing_version}] Publishing to PyPI...")
        subprocess.check_call([poetry_path, "publish", "-v"])

        print(f"[{publishing_version}] Published!")


if __name__ == "__main__":
    if os.getenv("DOWNLOAD_LATEST_ONLY") == "1":
        download_latest_jar_for_test()
    else:
        publish(dryrun=os.getenv("DRYRUN") == "1")
