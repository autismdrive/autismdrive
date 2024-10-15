FROM tiangolo/uwsgi-nginx-flask:python3.9 as builder
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

RUN /bin/bash -c "cd /autismdrive/backend/ && echo $PWD && mkdir instance && cp -r config instance/config && cp instance/config/docker.py instance/config.py"
ENV FLASK_DEBUG=1
ENV FLASK_APP=/app/__init__.py

FROM builder
