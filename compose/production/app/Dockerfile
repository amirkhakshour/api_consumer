FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN addgroup --system appuser \
    && adduser --system --ingroup appuser appuser

# Install & Config Poetry as package manager
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

# Requirements are installed here to ensure they will be cached.
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-interaction  --no-dev


COPY ./compose/production/app/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown appuser /entrypoint

COPY ./compose/production/app/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown appuser /start
COPY --chown=appuser:appuser . /app

USER appuser


ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
