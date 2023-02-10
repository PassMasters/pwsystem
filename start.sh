python manage.py collectstatic
gunicorn munchypw.wsgi --bind 0.0.0.0:$PORT
