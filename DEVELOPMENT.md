# How to develop

## Requirement

- [mise](https://mise.jdx.dev/)

## Setup

```bash
mise install
mise generate git-pre-commit -w
uv sync
```

## Lint

```bash
mise run pre-commit
```

## Fetch latest jar file

```bash
mise run download-latest-jar
```

## Run tests for all unpublished versions without publishing

```bash
mise run test-unpublished-versions
```

## Test

```bash
mise run test
```

## Publish all unpublished versions to PyPI (for CI)

```bash
mise run publish
```
