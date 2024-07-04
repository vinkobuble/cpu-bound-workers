FROM python:3.12.4

COPY ./src /app

WORKDIR /app

# Setup Poetry
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python - --version 1.8.3
ENV PATH="$POETRY_HOME/bin:$PATH"

# dependencies change more frequently then the previous steps.
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --only main

CMD ["python", "main.py"]
