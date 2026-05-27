FROM python:{{ cookiecutter.python_version }}-slim

# Install git and other dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates curl git \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Install OpenCode CLI
RUN curl -fsSL https://opencode.ai/install | bash
