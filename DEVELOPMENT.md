# How to develop

## Requirement

- `python>=3.9`
- `java`

## Setup

```bash
pip install pipx
pipx install poetry

poetry install
poetry run pre-commit install
```

## Activate virtual environment (venv) for development

```bash
poetry shell
```

## Lint

```bash
# in venv:
task lint
```

## Fetch latest jar file

```bash
# in venv:
task download-latest-jar
```

## Run tests for all unpublished versions without publishing

```bash
# in venv:
task test-unpublished-versions
```

## Publish all unpublished versions to PyPI (for CI)

```bash
# in venv:
task publish
```
