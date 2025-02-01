# Pull official Python Docker image
FROM --platform=linux/amd64 python:3.12.8-slim-bookworm

# Set the working directory
WORKDIR /code/backend

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    g++ \
    git-lfs \
    && apt-get update \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy all files
COPY ./src ./src

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run start script
CMD ["/start.sh"]
