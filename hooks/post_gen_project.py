#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    try:
        os.remove(os.path.join(PROJECT_DIRECTORY, filepath))
    except FileNotFoundError:
        pass


def remove_dir(dirpath):
    try:
        shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))
    except FileNotFoundError:
        pass


if __name__ == "__main__":

    if "{{ cookiecutter.use_pytest }}" == "y":
        remove_file("tests/__init__.py")

    if "no" in "{{ cookiecutter.command_line_interface|lower }}":
        cli_file = os.path.join("{{ cookiecutter.project_slug }}", "cli.py")
        remove_file(cli_file)

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    # CI/CD selection
    ci_tool = "{{ cookiecutter.ci_tool }}"

    if ci_tool != "GitHub":
        remove_dir(".github")

    if ci_tool != "GitLab":
        remove_file(".gitlab-ci.yml")

    if "{{ cookiecutter.use_onacol }}" == "n":
        config_file = os.path.join("{{ cookiecutter.project_slug }}",
                                   "default_config.yaml")
        remove_file(config_file)

    if "{{ cookiecutter.use_devcontainer }}" == "n":
        remove_dir(".devcontainer")
