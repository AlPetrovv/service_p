FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/home/app/src

ENV POETRY_VIRTUALENVS_CREATE=false


RUN useradd -m app

WORKDIR /home/app

RUN mkdir -p /home/app/data/ \
    /home/app/data/logs/app

ADD ./pyproject.toml ./poetry.lock ./

RUN pip install --upgrade pip
RUN pip install "poetry==2.2.1"

# Install pinned dependencies from the committed lock (runtime only).
RUN poetry install --no-interaction --no-ansi --no-root --without dev

COPY . .

RUN chown -R app:app /home/app/

USER app
