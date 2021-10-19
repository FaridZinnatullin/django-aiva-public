#!/usr/bin/env sh

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

gunicorn django_shop_my_version.wsgi:application --bind 0.0.0.0:8000 --reload -w 4
