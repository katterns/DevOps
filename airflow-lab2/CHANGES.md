# История изменений

## [2.0.0] - 2026-04-19

### Добавлено
- Интеграция с Apache Spark
- Сервисы `spark-master` и `spark-worker` в docker-compose.yml
- Spark-job `spark_job.py` для вычислений с использованием PySpark
- DAG `spark_dag.py` с `SparkSubmitOperator`
- Установка Java и procps в Dockerfile
- Провайдер `apache-airflow-providers-apache-spark`

### Изменено
- Dockerfile: добавлены переключения пользователя (USER root/airflow)
- docker-compose.yml: добавлены volume для spark, зависимости от spark-master
- Обновлена документация в README.md

## [1.0.0] - 2026-04-18

### Добавлено
- Начальная версия проекта с Airflow
- Базовый DAG для математических вычислений
