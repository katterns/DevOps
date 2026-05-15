FROM apache/airflow:2.7.0

WORKDIR /opt/airflow

USER root

RUN apt update && apt install -y procps default-jre && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

COPY ./dags/* ./dags/
COPY ./spark/* ./spark/

ARG AIRFLOW_CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-2.7.0/constraints-3.8.txt"
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark \
    --constraint "${AIRFLOW_CONSTRAINT_URL}"

RUN pip install --no-cache-dir pyspark==3.4.0
