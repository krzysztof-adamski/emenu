FROM python:3.8.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/opt/service

WORKDIR /opt/service

RUN apt update && apt install -y python3-dev vim

RUN pip install -U pip

RUN pip install pipenv gunicorn psycopg2-binary ipdb jedi==0.17.2

COPY Pipfile .

COPY Pipfile.lock .

RUN pipenv lock -r > requirements.txt

RUN pip install -r requirements.txt

COPY . /opt/service

RUN rm -f /opt/service/local_settings.py
