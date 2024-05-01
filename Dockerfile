FROM python:3.11.5-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

EXPOSE 5000

RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY todo_app ./todo_app
COPY .env poetry.lock *.toml ./

RUN /root/.local/bin/poetry install

ENTRYPOINT /root/.local/bin/poetry run flask run --host 0.0.0.0