FROM python:3.12

ENV VIRTUAL_ENV=/usr/local

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME /opt/dagster/app
COPY dagster.yaml $DAGSTER_HOME

WORKDIR /opt/dagster/app

COPY requirements.lock pyproject.toml .env README.md ./
RUN pip install --no-cache-dir -r requirements.lock
