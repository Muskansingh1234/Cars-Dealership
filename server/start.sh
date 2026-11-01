#!/bin/sh
# Production/Docker entrypoint: prepare the database, then run gunicorn.
set -e
python manage.py makemigrations djangoapp --noinput
python manage.py migrate --noinput
python manage.py seed
python manage.py collectstatic --noinput
exec gunicorn djangoproj.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --access-logfile -
