import datetime
import os
from contextlib import contextmanager

from cookiecutter.utils import rmtree


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def top_level_files(result):
    return {item.basename for item in result.project.listdir()}


def project_files(result):
    project_slug = os.path.basename(str(result.project))
    project_dir = result.project.join(project_slug)
    return {item.basename for item in project_dir.listdir()}


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        files = top_level_files(result)
        assert "pyproject.toml" in files
        assert "README.md" in files
        assert "tox.ini" in files
        assert "tests" in files

        assert "docs" not in files
        assert "Makefile" not in files
        assert "make.ps1" not in files
        assert "AUTHORS.md" not in files
        assert "CONTRIBUTING.md" not in files


def test_default_python_version(cookies):
    with bake_in_temp_dir(cookies) as result:
        pyproject = result.project.join("pyproject.toml").read()
        tox = result.project.join("tox.ini").read()

        assert 'requires-python = ">=3.13"' in pyproject
        assert 'target-version = "py313"' in pyproject
        assert "Programming Language :: Python :: 3.13" in pyproject
        assert "Programming Language :: Python :: 3.12" not in pyproject
        assert "Programming Language :: Python :: 3.10" not in pyproject
        assert "py313" in tox
        assert "uv sync --group dev" in tox
        assert "uv run pytest" in tox


def test_pyproject_uses_uv_and_hatchling(cookies):
    with bake_in_temp_dir(cookies) as result:
        pyproject = result.project.join("pyproject.toml").read()

        assert "[tool.poetry]" not in pyproject
        assert "poetry.core.masonry.api" not in pyproject
        assert "dynamic = [\"dependencies\", \"classifiers\"]" not in pyproject
        assert "[dependency-groups]" in pyproject
        assert 'requires = ["hatchling>=1.27.0"]' in pyproject
        assert 'build-backend = "hatchling.build"' in pyproject
        assert "[tool.hatch.build.targets.wheel]" in pyproject
        assert 'click>=8.1.7,<9.0.0' in pyproject
        assert 'onacol>=0.3.5,<0.4.0' in pyproject
        assert 'tox>=4.34.0,<5.0.0' in pyproject
        assert 'coverage[toml]>=7.4,<8.0.0' in pyproject
        assert 'ruff>=0.14.0,<0.15.0' in pyproject
        assert 'pytest>=9.0,<10.0.0' in pyproject
        assert 'pytest-cov>=4.1,<5.0.0' in pyproject
        assert 'mypy>=1.19,<2.0.0' in pyproject


def test_no_classic_aiohttp_setup(cookies):
    with bake_in_temp_dir(cookies) as result:
        files = project_files(result)
        pyproject = result.project.join("pyproject.toml").read()

        assert "http_handler.py" not in files
        assert "aiohttp" not in pyproject
        assert "sockjs" not in pyproject


def test_no_bumpversion_config(cookies):
    with bake_in_temp_dir(cookies) as result:
        pyproject = result.project.join("pyproject.toml").read()

        assert "bumpversion" not in pyproject.lower()
        assert "bump-my-version" not in pyproject


def test_devcontainer_opencode(cookies):
    with bake_in_temp_dir(cookies, extra_context={"use_devcontainer": "y"}) as result:
        devcontainer = result.project.join(".devcontainer/devcontainer.json").read()
        dockerfile = result.project.join(".devcontainer/Dockerfile").read()

        assert "sst-dev.opencode" in devcontainer
        assert ".config/opencode" in devcontainer
        assert ".local/share/opencode" in devcontainer
        assert "uv sync --group dev" in devcontainer
        assert "poetry" not in devcontainer.lower()
        assert "pip install uv" in dockerfile
        assert "poetry" not in dockerfile.lower()


def test_no_devcontainer_by_default(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert ".devcontainer" not in top_level_files(result)


def test_bake_selecting_license(cookies):
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the above copyright notice, this",
        "ISC license": "ISC License",
        "Apache Software License 2.0": "Licensed under the Apache License, Version 2.0",
        "GNU General Public License v3": "GNU GENERAL PUBLIC LICENSE",
    }
    for license_name, target_string in license_strings.items():
        with bake_in_temp_dir(
            cookies,
            extra_context={"open_source_license": license_name},
        ) as result:
            assert target_string in result.project.join("LICENSE").read()
            assert license_name in result.project.join("pyproject.toml").read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"open_source_license": "Not open source"},
    ) as result:
        assert "LICENSE" not in top_level_files(result)
        assert "License" not in result.project.join("README.md").read()


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        assert str(datetime.datetime.now().year) in license_file_path.read()


def test_bake_with_no_console_script(cookies):
    context = {"command_line_interface": "No command-line interface"}
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert "cli.py" not in project_files(result)


def test_bake_with_console_script_files(cookies):
    context = {"command_line_interface": "Click"}
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert "cli.py" in project_files(result)
        assert "[project.scripts]" in result.project.join("pyproject.toml").read()
