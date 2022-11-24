FROM python:3.10-slim

WORKDIR /app

COPY . /app

EXPOSE 8080

RUN pip install -r requirements.txt

RUN python manage.py collectstatic

CMD  python manage.py migrate && gunicorn -w 2 --bind 0.0.0.0:8080 measure_it.wsgi
