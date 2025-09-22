#!/bin/bash

# 等待資料庫
until pg_isready -h db -p 5432 -U postgres
do
  echo "Waiting for database..."
  sleep 2
done

echo "Database is ready, running migrations..."
alembic upgrade head

# 啟動 FastAPI
python -m app
