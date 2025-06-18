#!/bin/sh

# Until server folder created
until cd /app/backend; do
  echo "Waiting for backend volume..."
done

echo "Make Migrations"
alembic upgrade head
echo "Start Elite-GO FastAPI server"
python main.py
exec "$@"