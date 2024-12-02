# OpenAPI Generator in Package Installer for Python (PIP)

[![Join the Slack chat room](
  <https://img.shields.io/badge/Slack-Join%20the%20chat%20room-orange>
)](
  <https://join.slack.com/t/openapi-generator/shared_invite/zt-12jxxd7p2-XUeQM~4pzsU9x~eGLQqX2g>
) [![PyPI version](
  <https://badge.fury.io/py/openapi-generator-cli.svg>
)](
  <https://badge.fury.io/py/openapi-generator-cli>
) [![Code style: black](
  <https://img.shields.io/badge/code%20style-black-000000.svg>
)](
  <https://github.com/psf/black>
) [![Ruff](
  <https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json>
)](
  <https://github.com/astral-sh/ruff>
)

OpenAPI Generator allows generation of API client libraries (SDK generation), server stubs, documentation and configuration automatically given an OpenAPI Spec (both 2.0 and 3.0 are supported). Please see [OpenAPITools/openapi-generator]

---

This project checks the [maven repository] once a day for a new version and will publish this new version automatically as a python package.

## Installation

You must have the `java` binary executable available on your PATH for this to work. (JDK 11 is the minimal version supported. To install OpenJDK, please visit <https://adoptium.net/>)

You can install the package either in a virtual environment or globally.

```sh
# install the latest version of "openapi-generator-cli"
pip install openapi-generator-cli

# install a specific version of "openapi-generator-cli"
pip install openapi-generator-cli==4.3.1
```

You can also install with [`jdk4py`] instead of `java` binary. (`python>=3.10` is required)

```sh
pip install openapi-generator-cli[jdk4py]
```

After installation `openapi-generator-cli` command will be available in your virtual environment or globally depending on your installation.

To check the version, for example. Type the following command

```sh
# this will print the correct version number
openapi-generator-cli version
```

## Further Documentation

Please refer to the [official openapi-generator docs] for more information about the possible arguments and a detailed usage manual of the command line interface.

## Like the package?

Please leave a star.

## Have suggestions or feedback?

Please raise an issue, happy to hear from you :)

[OpenAPITools/openapi-generator]: <https://github.com/OpenAPITools/openapi-generator>
[maven repository]: <https://mvnrepository.com/artifact/org.openapitools/openapi-generator-cli>
[`jdk4py`]: <https://github.com/activeviam/jdk4py>
[official openapi-generator docs]: <https://github.com/OpenAPITools/openapi-generator#3---usage>
