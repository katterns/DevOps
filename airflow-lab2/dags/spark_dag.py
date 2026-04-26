from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

SPARK_SUBMIT_CONF = {
    "spark.executor.memory": "1g",
    "spark.driver.memory": "1g",
    "spark.executor.cores": "1",
    "spark.sql.shuffle.partitions": "2",
    "spark.driver.maxResultSize": "512m",
}

with DAG(
    dag_id="spark_math_calculations",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["lab2"],
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
) as dag:
    SparkSubmitOperator(
        task_id="spark_math_job",
        application="/opt/airflow/spark/spark_job.py",
        name="spark_math_calculations",
        conn_id="spark_default",
        conf=SPARK_SUBMIT_CONF,
        verbose=True,
    )
