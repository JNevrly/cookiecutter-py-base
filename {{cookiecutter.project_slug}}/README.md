{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
# {{ cookiecutter.project_name }}

{% if is_open_source %}
[![PyPI](https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg)](https://pypi.python.org/pypi/{{ cookiecutter.project_slug }})

{% if cookiecutter.ci_tool == 'GitHub' -%}
[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/ci.yml)
{%- endif %}

{% if cookiecutter.ci_tool == 'GitLab' -%}
[![CI](https://gitlab.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/badges/master/pipeline.svg)](https://gitlab.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/-/commits/master)
{%- endif %}

{%- endif %}

{% if cookiecutter.add_pyup_badge == 'y' %}
[![Updates](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg)](https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/)
{% endif %}


{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
{% endif %}

## Installation

```console
$ pip install {{ cookiecutter.project_slug }}
```

## Features

* TODO

{% if cookiecutter.use_devcontainer == "y" and cookiecutter.use_adoc_builder == "y" %}
## Local AsciiDoc builder

The devcontainer connects to the existing local ALAP AsciiDoc builder. Before
opening it in VS Code, start the builder on the Docker host from your local
`adoc_alap_template` checkout:

```bash
docker compose up -d asciibuilder
```

This creates the required `alap-asciibuilder` network. If the builder uses
authentication, export the matching `ADOC_BUILDER_TOKEN` in the host environment
before launching VS Code; the devcontainer forwards it by environment reference.

Inside the devcontainer, `ADOC_BUILDER_URL` is set to
`http://asciibuilder:18743`. Check connectivity with:

```bash
curl --fail "$ADOC_BUILDER_URL/health"
```

Use the `adoc-build` client/agent skill to render PDFs with this endpoint and the
optional token. The container-network port stays `18743` even if the builder's
host-published port is customized. Rebuild the devcontainer after changing its
configuration.
{% endif %}

{% if cookiecutter.use_backlog == "y" %}
## Task Management

This project uses [Backlog.md](https://github.com/MrLesk/Backlog.md). Its
configuration is in `backlog/config.yml`, and task files are stored in
`backlog/tasks/` with zero-padded IDs such as `TASK-001` and filenames such as
`task-001 - Describe-the-work.md`. The agent workflow is documented in
`AGENTS.md`.

```console
$ backlog task create "Describe the work"
$ backlog board
```
{% endif %}
