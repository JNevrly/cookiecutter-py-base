#!/usr/bin/env python
import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
BACKLOG_CONFIG_TEMPLATE = ".backlog-config.yml"


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


def require_command(command, installation_instructions):
    executable = shutil.which(command)
    if executable is None:
        raise RuntimeError(
            "Backlog.md integration requires '{}'. {}".format(
                command, installation_instructions
            )
        )
    return executable


def run_command(command):
    try:
        subprocess.run(command, cwd=PROJECT_DIRECTORY, check=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            "Backlog.md initialization failed while running: {}".format(
                " ".join(command)
            )
        ) from error


def initialize_backlog():
    git = require_command("git", "Install Git and run Cookiecutter again.")
    backlog = require_command(
        "backlog", "Install it with 'npm install -g backlog.md' and run Cookiecutter again."
    )

    run_command([git, "init"])
    run_command(
        [
            backlog,
            "init",
            "{{ cookiecutter.project_name }}",
            "--defaults",
            "--backlog-dir",
            "backlog",
            "--config-location",
            "folder",
            "--task-prefix",
            "task",
            "--zero-padded-ids",
            "3",
            "--check-branches",
            "false",
            "--include-remote",
            "false",
            "--branch-days",
            "30",
            "--bypass-git-hooks",
            "true",
            "--web-port",
            "6420",
            "--auto-open-browser",
            "false",
            "--integration-mode",
            "cli",
            "--agent-instructions",
            "agents",
        ]
    )
    os.replace(
        os.path.join(PROJECT_DIRECTORY, BACKLOG_CONFIG_TEMPLATE),
        os.path.join(PROJECT_DIRECTORY, "backlog", "config.yml"),
    )


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

    if "{{ cookiecutter.use_backlog }}" == "y":
        if "{{ cookiecutter.use_devcontainer }}" == "n":
            initialize_backlog()
    else:
        remove_file(BACKLOG_CONFIG_TEMPLATE)

    if "{{ cookiecutter.use_devcontainer }}" == "n":
        remove_dir(".devcontainer")
