# Лабораторная работа 2: Apache Airflow + Apache Spark

## Описание

Расширение проекта Airflow интеграцией с Apache Spark. Разработка DAG, выполняющего Spark-job через SparkSubmitOperator.

## Структура проекта

```
.
├── Dockerfile
├── docker-compose.yml
├── dags/
│   └── spark_dag.py
├── spark/
│   └── spark_job.py
├── logs/
├── plugins/
├── CHANGES.md
└── README.md
```

## Внесённые изменения (по сравнению с ЛР1)

1. **Dockerfile:**
   - Добавлена установка `procps` и `default-jre` через apt
   - Добавлена директива `USER root` и `USER airflow`
   - Добавлено копирование папки `spark/`
   - Добавлена установка `apache-airflow-providers-apache-spark`

2. **docker-compose.yml:**
   - Добавлены сервисы `spark-master` и `spark-worker`
   - Добавлен volume `./spark:/opt/airflow/spark`
   - Добавлена зависимость Airflow от `spark-master`

3. **Новые файлы:**
   - `spark/spark_job.py` - PySpark скрипт для вычислений
   - `dags/spark_dag.py` - DAG с SparkSubmitOperator

## Описание DAG

DAG `spark_math_calculations`:
- Запускает Spark-job через `SparkSubmitOperator`
- Spark-job выполняет расчёт чисел Фибоначчи и факториалов с использованием Spark DataFrame
- Вычисляет статистику (сумма, среднее, максимум) средствами Spark

## Развёртывание локально

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+
- Свободные порты: 8082, 4040, 7077

### Шаги для запуска

1. Клонировать репозиторий:
```bash
git clone https://github.com/katterns/DevOps.git
cd DevOps/airflow-lab2
```

2. Запустить сервисы:
```bash
docker compose up -d --build
```

3. Дождаться инициализации (1-2 минуты)

4. Создать Spark Connection в Airflow:
   - URL: http://localhost:8082
   - Логин/пароль: `airflow`/`airflow`
   - Admin → Connections → +
   - Connection Id: `spark_default`
   - Connection Type: `Spark`
   - Host: `spark://spark-master`
   - Port: `7077`

5. Активировать и запустить DAG `spark_math_calculations`

### Проверка работы

- **Airflow UI:** http://localhost:8082
- **Spark Master UI:** http://localhost:4040
- **Spark Worker UI:** http://localhost:8083 

### Остановка

```bash
docker compose down -v
```
