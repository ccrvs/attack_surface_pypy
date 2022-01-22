FROM pypy:3.8-7.3.7-bullseye as python-base
#FROM python:3.8-bullseye as python-base

ENV PYTHONUNBUFFERED=1 \
    TZ=":/etc/localtime" \
    PROJECT_PATH="/opt/attack_surface" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_PATH="/opt/attack_surface/.venv" \
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_VERSION_CHECK=1

ENV PATH="${POETRY_HOME}/bin:${VENV_PATH}/bin:${PATH}"

FROM python-base as builder-base

RUN apt-get update && apt-get install --no-install-recommends -y curl

ENV POETRY_VERSION=1.1.12
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | pypy
#RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PROJECT_PATH

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

FROM builder-base as lint

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PROJECT_PATH $PROJECT_PATH

WORKDIR $PROJECT_PATH

COPY . .

RUN poetry install --no-dev

EXPOSE 8080
CMD ["poetry", "run", "pypy", "-m", "attack_surface_pypy"]
