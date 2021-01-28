FROM python:slim

ENV PIPENV_VENV_IN_PROJECT 1
ENV PATH "/app/.venv/bin:$PATH"

WORKDIR /app

RUN pip install pipenv \
    && apt-get update \
    && apt-get install -y gcc libpq-dev


COPY . .

RUN pipenv install
