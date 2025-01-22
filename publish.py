from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.request import urlopen

from natsort import natsorted

MVN_BASE_URL = "https://search.maven.org"
MVN_CENTRAL_BASE_URL = "https://central.sonatype.com"


def convert_pre_release_version(version: str) -> str:
    pattern = re.compile(r"(?P<ver>\d+\.\d+\.\d+)-(?P<stage>[ab])(?:lpha|eta)(?P<revision>\d*)$")
    if not (m := pattern.match(version)):
        return version

    if not (ver := m["ver"]):
        return version

    if not (stage := m["stage"]):
        return version

    revision = m["revision"] or 0
    return pattern.sub(f"{ver}{stage}{revision}", version, count=1)


def download_openapi_generator_jar(version: str) -> None:
    download_url = (
        MVN_BASE_URL
        + "/remotecontent?filepath=org/openapitools/openapi-generator-cli"
        + f"/{version}/openapi-generator-cli-{version}.jar"
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


def get_available_versions() -> set[str]:
    rows = 200
    versions: list[str] = []
    for page_index, _ in enumerate(iter(int, 1)):  # 0..Inf
        mvn_url = (
            MVN_CENTRAL_BASE_URL
            + "/solrsearch/select?q=g:org.openapitools+AND+a:openapi-generator-cli&core=gav&format=json"
            f"&start={page_index}&rows={rows}"
        )
        response = urlopen(mvn_url)  #  noqa: S310
        docs = json.loads(response.read())["response"]["docs"]
        if len(docs) == 0:
            break
        versions.extend(convert_pre_release_version(doc["v"]) for doc in docs)
    return set(versions)


def get_published_vesions() -> set[str]:
    pypi_url = "https://pypi.org/pypi/openapi-generator-cli/json"
    response = urlopen(pypi_url)  #  noqa: S310

    if response.status != 200:  # noqa: PLR2004
        msg = f"{response.status}: {pypi_url}"
        raise RuntimeError(msg)

    published_releases = json.loads(response.read()).get("releases")
    if not isinstance(published_releases, dict):
        msg = f"Expected dict, got {type(published_releases)}"
        raise TypeError(msg)

    return set(published_releases.keys())


def update_package_version(version: str) -> None:
    updated_toml = re.sub(
        r'(?<=name = "openapi-generator-cli"\nversion = ")[^"]+(?=")',
        version,
        Path("pyproject.toml").open("r").read(),  # noqa: SIM115
        count=1,
        flags=(re.MULTILINE),
    )
    with Path("pyproject.toml").open("w") as toml:
        toml.write(updated_toml)


def download_latest_jar_for_test() -> None:
    latest_version = natsorted(get_available_versions())[-1]
    print(f"[{latest_version}] Downloading...")
    download_openapi_generator_jar(latest_version)
    print(f"[{latest_version}] Downloaded!")


def publish(*, dryrun: bool = False) -> None:
    pytest_path = shutil.which("pytest")
    poetry_path = shutil.which("poetry")

    unpublished_versions = natsorted(get_available_versions() - get_published_vesions())

    if len(unpublished_versions) == 0:
        print("[!] Nothing to be released.")
        return

    for publishing_version in unpublished_versions:
        print(f"[{publishing_version}] Downloading...")
        download_openapi_generator_jar(publishing_version)

        print(f"[{publishing_version}] Updating package version...")
        update_package_version(publishing_version)

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
