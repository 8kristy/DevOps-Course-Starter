FROM python:3.11.5-alpine as base

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

EXPOSE 5000

RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH $PATH:/root/.local/bin

FROM base as production

COPY todo_app ./todo_app
COPY poetry.lock pyproject.toml ./

RUN poetry install

ENTRYPOINT poetry run flask run --host 0.0.0.0

FROM base as development

ENTRYPOINT poetry install; poetry run flask run --host 0.0.0.0

FROM base as debug

ENTRYPOINT poetry install; tail -f /dev/null

FROM base as test

ENTRYPOINT poetry install; poetry run pytest