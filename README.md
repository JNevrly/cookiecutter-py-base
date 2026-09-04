# cookiecutter-py-base

A small Cookiecutter template for uv-managed Python packages.

A fork of https://github.com/audreyfeldroy/cookiecutter-pypackage

## Features

- uv dependency management with Hatchling build backend
- Python 3.13 by default, with support for Python 3.11 and newer
- GitHub Actions or GitLab CI configuration
- Optional devcontainer with Python, uv, Ruff, OpenCode, and Claude Code extensions
- Optional pytest and Click setup
- Command line interface using Click (optional)
- Optional Backlog.md task management, initialized with Git and a standard project configuration

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

## Backlog.md

Selecting Backlog.md without a devcontainer requires Git and the `backlog`
command on the machine running Cookiecutter. Install it with:

```bash
npm install -g backlog.md
```

After initialization, the project is a Git repository. Backlog.md stores its
configuration in `backlog/config.yml` and tasks in `backlog/tasks/`. Task IDs
use the `TASK-001` format and task filenames use `task-001 - Title.md`.
Generated devcontainers install and initialize Backlog.md when the container is
first created, so the host does not need Git or Backlog.md. Every generated
project has an `AGENTS.md`; it contains the Backlog.md workflow when Backlog.md
is selected.
