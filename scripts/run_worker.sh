#!/bin/sh

python3.6 manage.py migrate
celery -A pycon.celery worker -Q default -l info
