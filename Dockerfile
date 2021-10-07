###
FROM python:3.9.6
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn task_list.wsgi:application --bind 0.0.0.0:8000
