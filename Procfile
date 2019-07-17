web: gunicorn recharge.wsgi --log-file -
worker: celery beat -A recharge --loglevel=info