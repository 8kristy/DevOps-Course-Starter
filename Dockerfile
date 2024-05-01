FROM python:3.11.5-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

EXPOSE 5000

RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH $PATH:/root/.local/bin

COPY todo_app ./todo_app
COPY poetry.lock pyproject.toml ./

RUN poetry install

ENTRYPOINT poetry run flask run --host 0.0.0.0