# История изменений

## [3.0.0] - 2026-05-02

### Добавлено

- `.gitlab-ci.yml`: стадии test / build / deploy, ручная `clear-job`, тег раннера `airflow-spark`
- правила: test всегда; build не для `feature/*`; deploy авто для `main`, `master`, `develop`

## [2.0.0] - 2026-04-15

### Добавлено

- Интеграция с Apache Spark
- Сервисы `spark-master` и `spark-worker` в docker-compose.yml
- Spark-job `spark_job.py` для вычислений с использованием PySpark
- DAG `spark_dag.py` с `SparkSubmitOperator`
- Установка Java и procps в Dockerfile
- Провайдер `apache-airflow-providers-apache-spark`

### Изменено

- Dockerfile: переключения пользователя (USER root/airflow)
- docker-compose.yml: volume для spark, зависимость от spark-master
- Обновлена документация в README.md

## [1.0.0] - 2026-04-02

### Добавлено

- Начальная версия проекта с Airflow
- Базовый DAG для математических вычислений
