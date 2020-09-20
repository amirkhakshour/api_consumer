FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install & Config Poetry as package manager
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Requirements are installed here to ensure they will be cached.
WORKDIR /app
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-interaction

COPY ./compose/production/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]
