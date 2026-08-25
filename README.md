# cookiecutter-py-base

A small Cookiecutter template for uv-managed Python packages.

A fork of https://github.com/audreyfeldroy/cookiecutter-pypackage

## Features

- uv dependency management with Hatchling build backend
- Python 3.13 by default, with support for Python 3.11 and newer
- GitHub Actions or GitLab CI configuration
- Optional devcontainer with Python, uv, Ruff, and OpenCode extensions
- Optional pytest and Click setup
- Command line interface using Click (optional)

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (requires Cookiecutter 1.4.0 or higher):

```bash
pip install -U cookiecutter
```

Install uv if you don't already have it: https://docs.astral.sh/uv/

Generate a project from this template:

```bash
cookiecutter https://github.com/JNevrly/cookiecutter-py-base.git
```

Then install dependencies in the generated project:

```bash
uv sync --group dev
```
