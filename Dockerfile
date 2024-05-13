FROM python:3.11.5-alpine as base

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

EXPOSE 5000

RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH $PATH:/root/.local/bin

COPY poetry.lock pyproject.toml ./
RUN mkdir todo_app; mkdir todo_app/test; touch todo_app/test/__init__.py
RUN poetry install


FROM base as production
COPY todo_app ./todo_app
ENTRYPOINT poetry run flask run --host 0.0.0.0

FROM base as development
ENTRYPOINT poetry run flask run --host 0.0.0.0

FROM base as debug
ENTRYPOINT tail -f /dev/null

FROM base as test
ENTRYPOINT poetry run pytest-watch --poll