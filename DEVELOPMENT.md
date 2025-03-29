# How to develop

## Requirement

- `python>=3.9`
- `java`

## Setup

Open [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) in the cloned project.

## Lint

```bash
task lint
```

## Fetch latest jar file

```bash
task download-latest-jar
```

## Run tests for all unpublished versions without publishing

```bash
task test-unpublished-versions
```

## Test

```bash
task test
```

## Publish all unpublished versions to PyPI (for CI)

```bash
task publish
```
