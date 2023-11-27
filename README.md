# Sports-events

На этом сервисе пользователи могут найти интересующие их 
спортивные мероприятия, отсортировав их по виду спорта, месту проведения и дате,
добавлять новые мероприятия и подавать заявки на мероприятия 

## Технологии

[![Python](https://img.shields.io/badge/Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Postgres](https://img.shields.io/badge/Postgres-464646?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex Object Storage](https://img.shields.io/badge/Yandex_Object_Storage-464646?style=flat-square&logo=yandexcloud)](https://cloud.yandex.com/en-ru/services/storage)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://pytest-django.readthedocs.io/en/latest/)

## Запуск проекта локально

Клонировать репозиторий: 

```
git clone https://github.com/AlexandraPoturaeva/sports_events.git
```
Перейти в корень проекта:

```
cd .../sports_events
```

Создать файл .env в корне проекта. Пример заполнения: 

```
DEBUG=1
ALLOWED_HOSTS=*
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
CSRF_TRUSTED_ORIGINS=https://localhost
SECRET_KEY=django_secret_key
SOCIAL_AUTH_GITHUB_KEY=social_auth_github_key
SOCIAL_AUTH_GITHUB_SECRET=social_auth_github_secret
```
Создать и активировать виртуальное окружение

Windows:

```
python -m venv venv
venv\Scripts\activate
```
Linux:

```
python -m venv venv
source venv\Scripts\activate
```

Установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

При необходимости создать и применить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Запуск проекта в Docker

Клонировать репозиторий: 

```
git clone https://github.com/AlexandraPoturaeva/sports_events.git
```

Создать файл .env в корне проекта. Пример заполнения: 

```
DEBUG=0
ALLOWED_HOSTS=*
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
CSRF_TRUSTED_ORIGINS=https://*.example.com
SECRET_KEY=django-secret-key
SOCIAL_AUTH_GITHUB_KEY=social-auth_github-key
SOCIAL_AUTH_GITHUB_SECRET=social-auth_github-secret
YANDEX_BUCKET_NAME=yandex-bucket-name
AWS_ACCESS_KEY_ID=aws-access-key-id
AWS_SECRET_ACCESS_KEY=aws-secret-access-key
AWS_S3_ENDPOINT_URL=https://storage.yandexcloud.net
AWS_S3_REGION_NAME=aws-s3-region
```

Для сборки образа выполнить в корне проекта:

```
docker build --tag cheflist_web .
```

Запустить контейнер:

```
docker run --env-file=.env -p 8001:8000 sports_events
```

## Develop

Пример заполнения файла .env.prod:

```
DEBUG=0
ALLOWED_HOSTS=*
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
CSRF_TRUSTED_ORIGINS=https://*.example.com
SECRET_KEY=django-secret-key
SOCIAL_AUTH_GITHUB_KEY=social-auth_github-key
SOCIAL_AUTH_GITHUB_SECRET=social-auth_github-secret
YANDEX_BUCKET_NAME=yandex-bucket-name
AWS_ACCESS_KEY_ID=aws-access-key-id
AWS_SECRET_ACCESS_KEY=aws-secret-access-key
AWS_S3_ENDPOINT_URL=https://storage.yandexcloud.net
AWS_S3_REGION_NAME=aws-s3-region
```

Перед локальным запуском или применением миграций на удалённой базе данных для смены настроек с develop на production выполнить:


Windows
```
set ENV=prod 
```

Linux

```
export ENV=prod
```

При запуске докер-контейнера при необходимости использовать файл .env.prod:

```
docker run --env-file=.env.prod -p 8001:8000 sports_events
```