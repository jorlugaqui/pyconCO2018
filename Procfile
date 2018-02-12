web: gunicorn pycon.wsgi --log-file -
worker: celery -A pycon.celery worker -Q default -l info
