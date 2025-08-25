FROM tiangolo/uwsgi-nginx-flask:python3.12 as builder
COPY ./pyproject.toml /app/pyproject.toml
RUN uv sync

COPY . /app

RUN /bin/bash -c "cd /autismdrive/backend/"
ENV FLASK_DEBUG=0
ENV FLASK_APP=/autismdrive/backend/main.py
ENV PYTHONPATH=/autismdrive/backend
ENV ENV_NAME=docker


FROM builder
