FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root