FROM python:3.9.6-slim

ENV PORT=8000

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && apt-get clean

WORKDIR /app

RUN mkdir -p /app/vsf/spreadsheets/

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN python vsf/manage.py makemigrations
RUN python vsf/manage.py migrate

EXPOSE 8000

WORKDIR vsf

CMD gunicorn vsf.wsgi:application --bind 0.0.0.0:$PORT