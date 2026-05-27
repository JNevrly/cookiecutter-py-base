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

[JNevrly/cookiecutter-pypackage-poetry](https://github.com/JNevrly/cookiecutter-pypackage-poetry)
