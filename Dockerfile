FROM python:3.9

ARG SQLALCHEMY_DEPENDENCIES=""

COPY requirements.txt requirements.txt /tmp/
COPY requirements-dev.txt requirements-dev.txt /tmp/
RUN python3.9 -m pip install ${SQLALCHEMY_DEPENDENCIES} -r /tmp/requirements-dev.txt && rm /tmp/requirements-dev.txt && rm /tmp/requirements.txt

WORKDIR /datalake_metrics_db
