FROM apache/airflow:2.7.0

WORKDIR /opt/airflow

USER root

RUN apt update && apt install -y procps default-jre && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

COPY ./dags/* ./dags/
COPY ./spark/* ./spark/

RUN pip install apache-airflow-providers-apache-spark && \
    pip install 'apache-airflow-providers-openlineage>=1.8.0' --upgrade && \
    pip install pyspark==3.4.0
