FROM python:3.8.5

RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code

RUN python3 manage.py collectstatic --noinput

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8020

FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic --noinput
