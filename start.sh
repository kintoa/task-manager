#!/bin/sh
set -e

# Запускаем приложение
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
