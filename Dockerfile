FROM python:3.9.6-slim

ENV PORT=8000

RUN apt-get update \
    && apt-get -y install libpq-dev gcc curl gnupg -yq \
    && pip install psycopg2 \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash \
    && apt-get install nodejs -yq \
    && apt-get clean

WORKDIR /app

RUN mkdir -p /app/vsf/spreadsheets/

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY package*.json .
RUN npm install

COPY . .

RUN python vsf/manage.py makemigrations
RUN python vsf/manage.py migrate
RUN npm run build

EXPOSE 8000 2999

WORKDIR vsf

CMD gunicorn vsf.wsgi:application --bind 0.0.0.0:$PORT --error-logfile ./gunicorn-error-log.log --log-level debug