#!/bin/sh

# Until server folder created
until cd /app/backend; do
  echo "Waiting for backend volume..."
done

echo "Start Elite-GO TaskIQ Worker"
# run a worker
taskiq worker src.worker.tkq:broker & taskiq scheduler src.worker.tkq:scheduler --skip-first-run