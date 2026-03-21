#!/bin/bash
cd /app
uv run python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 2>&1 | tee /app/startup.log
