#!/bin/sh
set -e

# Wait for PostgreSQL to be ready
circuit_breaker=0
max_attempts=20

while ! PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USERNAME -d $POSTGRES_DB -t 1; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
  circuit_breaker=$((circuit_breaker+1))
  if [ $circuit_breaker -ge $max_attempts ]; then
    echo "Max number of attempts reached. PostgreSQL is not ready."
    exit 1
  fi
done
echo "PostgreSQL is ready."

# Run Alembic migrations
echo "Run Alembic Migrations..."
alembic -c ./src/alembic.ini upgrade head

# Start the application
echo "Starting the application..."
uvicorn src.app.main:app --host 0.0.0.0 --port $PORT
