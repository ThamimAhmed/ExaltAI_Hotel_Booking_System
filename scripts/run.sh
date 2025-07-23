#!/bin/bash

if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
fi

export PYTHONPATH=src

alembic upgrade head 2>/dev/null || true
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
