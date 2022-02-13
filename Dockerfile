FROM python:3.10

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY poetry.lock ./
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN apt update && apt install -y librdkafka-dev
RUN $HOME/.local/bin/poetry install

COPY . .