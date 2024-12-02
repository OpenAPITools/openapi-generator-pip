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

## Fetch latest jar file and run tests

```bash
# in venv:
DOWNLOAD_LATEST_ONLY=1 python publish.py
task test
```

## Run tests for all unpublished versions without publishing

```bash
# in venv:
DRYRUN=1 python publish.py
```

## Publish all unpublished versuibs to PyPI (for CI)

```bash
# in venv:
python publish.py
```
