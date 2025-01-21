FROM python:3.12.0-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry and add to PATH
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only poetry files first
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies only (without installing the project itself)
RUN poetry install --no-root --no-interaction --no-ansi

# Now copy the rest of the project files
COPY . .

# Install the project itself
RUN poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["poetry", "run", "uvicorn", "workshop_genai_student.main:app", "--host", "0.0.0.0", "--port", "8001"] 