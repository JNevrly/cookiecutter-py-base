import datetime
import json
import os
import stat
import sys
from contextlib import contextmanager
from pathlib import Path

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


def write_fake_command(command_dir, name, source):
    command_dir = Path(command_dir)
    if os.name == "nt":
        script = command_dir / "{}.py".format(name)
        script.write_text(source)
        command = command_dir / "{}.bat".format(name)
        command.write_text('@"{}" "%~dp0{}.py" %*\n'.format(sys.executable, name))
    else:
        command = command_dir / name
        command.write_text("#!{}\n{}".format(sys.executable, source))
        command.chmod(command.stat().st_mode | stat.S_IXUSR)


def fake_backlog_commands(tmp_path, monkeypatch):
    command_dir = tmp_path / "commands"
    command_dir.mkdir()
    command_log = tmp_path / "commands.jsonl"
    monkeypatch.setenv("BACKLOG_COMMAND_LOG", str(command_log))
    monkeypatch.setenv("PATH", "{}{}{}".format(command_dir, os.pathsep, os.environ.get("PATH", "")))

    write_fake_command(
        command_dir,
        "git",
        """import json
import os
import sys
from pathlib import Path

with Path(os.environ["BACKLOG_COMMAND_LOG"]).open("a") as log:
    log.write(json.dumps(["git", *sys.argv[1:]]) + "\\n")
Path(".git").mkdir(exist_ok=True)
""",
    )
    write_fake_command(
        command_dir,
        "backlog",
        """import json
import os
import sys
from pathlib import Path

with Path(os.environ["BACKLOG_COMMAND_LOG"]).open("a") as log:
    log.write(json.dumps(["backlog", *sys.argv[1:]]) + "\\n")
Path("backlog").mkdir(exist_ok=True)
Path("backlog/config.yml").write_text("generated config\\n")
with Path("AGENTS.md").open("a") as agents:
    agents.write("\\nBacklog.md instructions\\n")
""",
    )
    return command_log


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
        assert "AGENTS.md" in files
        assert result.project.join("AGENTS.md").read() == ""

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
        assert "nodejs npm" not in dockerfile
        assert "npm install -g backlog.md" not in dockerfile


def test_no_devcontainer_by_default(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert ".devcontainer" not in top_level_files(result)


def test_bake_without_backlog_by_default(cookies):
    with bake_in_temp_dir(cookies) as result:
        files = top_level_files(result)

        assert "backlog" not in files
        assert ".backlog-config.yml" not in files


def test_bake_with_backlog(cookies, tmp_path, monkeypatch):
    command_log = fake_backlog_commands(tmp_path, monkeypatch)

    with bake_in_temp_dir(cookies, extra_context={"use_backlog": "y"}) as result:
        expected_config = """project_name: "Python Boilerplate"
default_status: "To Do"
statuses: ["To Do", "In Progress", "Done"]
labels: []
definition_of_done: []
date_format: yyyy-mm-dd
max_column_width: 20
auto_open_browser: false
default_port: 6420
remote_operations: false
auto_commit: false
filesystem_only: false
zero_padded_ids: 3
bypass_git_hooks: true
check_active_branches: false
active_branch_days: 30
task_prefix: "task"
"""
        commands = [json.loads(line) for line in command_log.read_text().splitlines()]

        assert result.project.join(".git").isdir()
        assert result.project.join("backlog/config.yml").read() == expected_config
        agents = result.project.join("AGENTS.md").read()
        assert "## Backlog.md workflow" in agents
        assert "Only the human may accept a task as complete." in agents
        assert "Do not create or use Backlog.md decision records." in agents
        assert "Backlog.md instructions" in agents
        assert ".backlog-config.yml" not in top_level_files(result)
        assert ["git", "init"] in commands
        assert [
            "backlog",
            "init",
            "Python Boilerplate",
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
        ] in commands
        assert "TASK-001" in result.project.join("README.md").read()


def test_bake_with_backlog_requires_backlog_command(cookies, tmp_path, monkeypatch):
    command_dir = tmp_path / "commands"
    command_dir.mkdir()
    command_log = tmp_path / "commands.jsonl"
    monkeypatch.setenv("BACKLOG_COMMAND_LOG", str(command_log))
    monkeypatch.setenv("PATH", str(command_dir))
    write_fake_command(
        command_dir,
        "git",
        """from pathlib import Path
Path(".git").mkdir(exist_ok=True)
""",
    )

    with bake_in_temp_dir(cookies, extra_context={"use_backlog": "y"}) as result:
        assert result.exit_code == 1
        assert "requires 'backlog'" in str(result.exception)
        assert not result.project.join(".git").exists()


def test_backlog_devcontainer_defers_initialization(cookies, tmp_path, monkeypatch):
    command_dir = tmp_path / "commands"
    command_dir.mkdir()
    monkeypatch.setenv("PATH", str(command_dir))

    with bake_in_temp_dir(
        cookies,
        extra_context={"use_backlog": "y", "use_devcontainer": "y"},
    ) as result:
        dockerfile = result.project.join(".devcontainer/Dockerfile").read()
        devcontainer = result.project.join(".devcontainer/devcontainer.json").read()

        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.join(".backlog-config.yml").isfile()
        assert not result.project.join(".git").exists()
        assert not result.project.join("backlog").exists()
        assert "nodejs npm" in dockerfile
        assert "npm install -g backlog.md" in dockerfile
        assert "if [ -f .backlog-config.yml ]; then" in devcontainer
        assert "git init" in devcontainer
        assert "backlog init --defaults" in devcontainer
        assert "mv .backlog-config.yml backlog/config.yml" in devcontainer
        assert "uv sync --group dev" in devcontainer


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
