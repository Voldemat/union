FROM python:3.9

RUN pip install pipenv --upgrade --no-cache-dir

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

ADD Pipfile* /app

RUN pipenv install --system --dev --deploy

ADD . /app
