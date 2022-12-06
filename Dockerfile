FROM python:3.10

ENV DASH_DEBUG_MODE False
COPY ./app /app
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

CMD exec gunicorn --bind 0.0.0.0:8050 app:server --timeout 600