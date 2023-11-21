FROM python:3.11-alpine

EXPOSE 8000

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app

RUN python -m pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]