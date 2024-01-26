FROM python:3.11.4-slim-buster

COPY ./app /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]