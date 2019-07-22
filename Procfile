web: gunicorn recharge.wsgi --log-file -
worker: celery worker -A recharge --loglevel=info --beat