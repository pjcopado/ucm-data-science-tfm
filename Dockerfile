# Pull official Python Docker image
# FROM --platform=linux/amd64 python:3.11.7-slim
# FROM ghcr.io/astral-sh/uv:latest

FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /code

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    g++ \
    git-lfs \
    && apt-get update \
    && rm -rf /var/lib/apt/lists/*

# Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Python dependencies
COPY ./pyproject.toml ./
RUN uv sync

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Copy all files
COPY ./src ./src

# Run start script
CMD ["/start.sh"]
