FROM python:3.12.0-alpine


RUN apk add --update bash
# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Переменные Django (можно оставить пустыми или задать дефолты)
ENV DEBUG=False
ENV ALLOWED_HOSTS=localhost

# Переменные БД (лучше передавать через `docker-compose.yml` или секреты)
ENV DB_NAME=postgres
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=db
ENV DB_PORT=5432

# CSRF-настройки (укажите свои домены)
ENV CSRF_COOKIE_DOMAIN=.localhost
ENV CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# copy project
COPY . /app

EXPOSE 8000
