# syntax=docker/dockerfile:1

# LABEL maintainer="Wichai T."

FROM python:3.8-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc git gdal-bin

RUN pip install --upgrade pip
COPY . .

# install python dependencies
RUN pip install pipenv \
  && pipenv install $(test "$DJANGO_ENV" == production || echo "--dev") --deploy --system --ignore-pipfile

# change work directory
WORKDIR /app/django_api_example

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:8000 core.wsgi
