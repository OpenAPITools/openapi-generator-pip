import os
import subprocess

import requests

MVN_BASE_URL = "https://search.maven.org"


def download_openapi_generator_jar(version):
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

    if os.path.exists("version"):
        os.remove("version")

    print(download_url)
    response = requests.get(download_url)
    print("Downloading complete")

    with open(
        "openapi_generator_cli/openapi-generator.jar", "wb"
    ) as openapi_generator_jar:
        openapi_generator_jar.write(response.content)
        openapi_generator_jar.close()

    with open("version", "w") as version_file:
        version_file.write(version)
    version_file.close()


def get_available_versions():
    mvn_url = (
        MVN_BASE_URL
        + "/solrsearch/select?q=g:org.openapitools+AND+a:openapi-generator-cli&core=gav"
        "&start=0&rows=200"
    )
    response = requests.get(mvn_url)
    docs = response.json()["response"]["docs"]
    return [doc["v"] for doc in docs]


def get_published_vesions():
    pypi_url = "https://pypi.org/pypi/openapigenerator/json"
    response = requests.get(pypi_url)

    if response.status_code == 404:
        return []

    published_versions = response.json().get("releases").keys()
    return published_versions


def publish():
    available_versions = get_available_versions()
    published_versions = get_published_vesions()

    print("Available versions: " + str(available_versions))
    print("Published versions: " + str(published_versions))

    versions_to_publish = set(available_versions) - set(published_versions)
    print(versions_to_publish)

    for version in versions_to_publish:
        print("Publishing version " + version)
        download_openapi_generator_jar(version)
        subprocess.check_call("python setup.py upload", shell=True)


if __name__ == "__main__":
    publish()
