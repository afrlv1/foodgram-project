FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN python3 manage.py collectstatic --noinput