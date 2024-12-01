from __future__ import annotations

import json
import os
import subprocess
from typing import TYPE_CHECKING
from urllib.request import urlopen

if TYPE_CHECKING:
    from collections.abc import KeysView

MVN_BASE_URL = "https://search.maven.org"


def download_openapi_generator_jar(version: str) -> None:
    download_url = (
        MVN_BASE_URL
        + "/remotecontent?filepath=org/openapitools/openapi-generator-cli/"
        + version
        + "/openapi-generator-cli-"
        + version
        + ".jar"
    )

    if os.path.exists("openapi-generator.jar"):
        os.remove("openapi-generator.jar")

    print(download_url)
    response = urlopen(download_url)

    if response.status != 200:
        raise RuntimeError(f"{response.status}: {download_url}")

    print("Downloading complete")

    with open("openapi_generator_cli/openapi-generator.jar", "wb") as openapi_generator_jar:
        openapi_generator_jar.write(response.read())
        openapi_generator_jar.close()

    updated_toml = (
        open("pyproject.toml")
        .read()
        .replace(
            '[tool.poetry]\nversion = "0"',
            f'[tool.poetry]\nversion = "{version}"',
            1,
        )
    )
    with open("pyproject.toml", "w") as toml:
        toml.write(updated_toml)


def get_available_versions() -> list[str]:
    mvn_url = (
        MVN_BASE_URL + "/solrsearch/select?q=g:org.openapitools+AND+a:openapi-generator-cli&core=gav"
        "&start=0&rows=200"
    )
    response = urlopen(mvn_url)
    docs = json.loads(response.read())["response"]["docs"]
    return [doc["v"] for doc in docs]


def get_published_vesions() -> KeysView[str]:
    pypi_url = "https://pypi.org/pypi/openapi-generator-cli/json"
    response = urlopen(pypi_url)

    if response.status != 200:
        raise RuntimeError(f"{response.status}: {pypi_url}")

    published_releases = json.loads(response.read()).get("releases")
    if not isinstance(published_releases, dict):
        raise TypeError(f"Expected dict, got {type(published_releases)}")

    return published_releases.keys()


def publish() -> None:
    latest_version = get_available_versions()[0]
    published_versions = get_published_vesions()

    if latest_version not in published_versions:
        print("Publishing version " + latest_version)
        download_openapi_generator_jar(latest_version)
        subprocess.check_call("poetry build", shell=True)
        subprocess.check_call("poetry publish -r testpypi", shell=True)
        subprocess.check_call("poetry publish", shell=True)


if __name__ == "__main__":
    publish()
