#!/bin/sh

alembic upgrade head

gunicorn fast_api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
