FROM python:3.11-alpine

EXPOSE 8000

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"
RUN apk add --no-cache --update musl-locales

COPY . /app

CMD ["python", "manage.py", "collectstatic", "--noinput"]

CMD ["gunicorn", "sports_events.wsgi:application", "--bind", "0.0.0.0:8000"]