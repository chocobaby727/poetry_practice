# syntax=docker/dockerfile:1

ARG POETRY_HOME=/opt/poetry
ARG PYTHON_VERSION=3.9
ARG ENVIRONMENT


FROM python:${PYTHON_VERSION}-buster as builder
ARG POETRY_HOME
ARG POETRY_VERSION=1.1.15
ENV PATH="$POETRY_HOME/bin:$PATH"

# poetryの導入
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version $POETRY_VERSION \
    && poetry config virtualenvs.create false

WORKDIR /poetry_practice
COPY pyproject.toml poetry.lock* ./

RUN --mount=type=cache,target=~/.cache/pypoetry poetry install --no-root
RUN if [ "${ENVIRONMENT}" = "PROD" ]; then poetry export -f requirements.txt -o requirements.txt --without-hashes; fi


# https://github.com/microsoft/vscode-dev-containers/tree/main/containers/python-3
FROM mcr.microsoft.com/vscode/devcontainers/python:${PYTHON_VERSION}-buster as dev
ARG POETRY_HOME
ARG USER="vscode"
ARG GROUP="ccds"
ENV PATH="$POETRY_HOME/bin:$PATH"
ARG ENVIRONMENT
ENV ENVIRONMENT=$ENVIRONMENT

COPY --from=builder --chown=$USER:$GROUP /root/.cache/pypoetry /home/$USER/.cache/pypoetry
COPY --from=builder --chown=$USER:$GROUP $POETRY_HOME $POETRY_HOME
# COPY --from=builder --chown=$USER:$GROUP /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/site-packages/

RUN if ! cat /etc/group | grep -e $GROUP: > /dev/null 2>&1; then groupadd -r $GROUP; fi \
    && usermod -a -G $GROUP $USER \
    && umask 0002 && mkdir poetry_practice \
    && chown -R $USER:$GROUP /poetry_practice

WORKDIR /poetry_practice
COPY pyproject.toml poetry.lock* ./

# RUN apt-get update && apt-get -y install --no-install-recommends \
#     git \
#     vim \
#     curl \
#     && \
#     apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

USER $USER

RUN poetry config virtualenvs.create false \
    && poetry completions bash | sudo tee -a /etc/bash_completion.d/poetry.bash-completion \
    && poetry install --no-root && rm -rf ~/.cache/pypoetry

# CMD [ "pre-commit", "init-templatedir", "~/.git-template" ]


# # 本番用
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# FROM tiangolo/uvicorn-gunicorn:python:${PYTHON_VERSION}-slim as prod
# COPY --from=requirements-stage ./requirements.txt ./requirements.txt
# WORKDIR /poetry_practice
# RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
# RUN poetry install --no-root --no-dev && rm -rf ~/.cache/pypoetry
