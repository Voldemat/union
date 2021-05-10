FROM python:3.9

RUN pip install pipenv --upgrade --no-cache-dir

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

ADD Pipfile* /app

RUN pipenv install --system --dev --deploy

ADD . /app


#See more details in wheels/README.txt
RUN cp wheels/django-rest-swagger/index.html /usr/local/lib/python3.9/site-packages/rest_framework_swagger/templates/rest_framework_swagger