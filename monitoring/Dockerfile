FROM python:3.12.4

WORKDIR /app

# Setup Poetry
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python - --version 1.8.3
ENV PATH="$POETRY_HOME/bin:$PATH"

# dependencies change more frequently then the previous steps.
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY ./src /app

CMD ["fastapi", "run", "app.py", "--port", "80"]