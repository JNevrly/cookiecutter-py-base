# cookiecutter-py-base

A small Cookiecutter template for Poetry-managed Python packages. 

A fork of https://github.com/audreyfeldroy/cookiecutter-pypackage 

## Features

- Poetry 2 project metadata and dependency management
- Python 3.13 by default, with support for Python 3.11 and newer
- GitHub Actions or GitLab CI configuration
- Optional devcontainer with Python, Ruff, and OpenCode extensions
- Optional pytest and Click setup
- Command line interface using Click (optional)

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (requires Cookiecutter 1.4.0 or higher):

```bash
pip install -U cookiecutter
```

Generate a project from this template:

```bash
cookiecutter https://github.com/JNevrly/cookiecutter-py-base.git
```

Then install dependencies in the generated project:

```bash
poetry install
```
