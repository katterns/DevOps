# Лабораторная работа 3: GitLab CI/CD + Airflow + Spark

## Описание

Стек Airflow и Spark в Docker Compose: DAG запускает PySpark-скрипт через `SparkSubmitOperator`. В корне — `.gitlab-ci.yml` с проверкой структуры репозитория, сборкой образа и деплоем через compose.

## Структура проекта

```
.
├── .gitlab-ci.yml
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

## CI/CD (GitLab)

- **test** — есть каталоги `dags/`, `spark/` и файл `Dockerfile`;
- **build** — `docker build` (для веток `feature/*` не запускается);
- **deploy** — `docker-compose up` (авто для `main`, `master`, `develop`; в остальных ветках — вручную);
- **clear-job** — `docker-compose down -v`, только manual;
- все джобы с тегом раннера `airflow-spark`.

## Описание DAG

DAG `spark_math_calculations`: один таск `SparkSubmitOperator` на скрипт `/opt/airflow/spark/spark_job.py`, подключение `spark_default`, в `conf` заданы память и число cores для драйвера/executor.

## Развёртывание локально

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+
- свободные порты: 8082, 4040, 7078, 8083

### Запуск

1. Клонировать репозиторий и перейти в каталог проекта:

```bash
git clone https://github.com/katterns/DevOps.git
cd DevOps/airflow-lab3
```

2. Поднять сервисы:

```bash
docker compose up -d --build
```

3. Подождать инициализацию (1–2 минуты).

4. В Airflow (http://localhost:8082, `airflow` / `airflow`) создать подключение Spark:

   - Connection Id: `spark_default`
   - Connection Type: `Spark`
   - Host: `spark://spark-master`
   - Port: `7077`

5. Включить DAG `spark_math_calculations` и при необходимости запустить вручную.

### Проверка

- **Airflow UI:** http://localhost:8082
- **Spark Master UI:** http://localhost:4040
- **Spark Worker UI:** http://localhost:8083

### Остановка

```bash
docker compose down -v
```

## Раннер для CI

Нужен GitLab Runner с тегом `airflow-spark` и примонтированным Docker socket, чтобы джобы могли вызывать `docker`/`docker-compose`. Статус пайплайнов — в GitLab: **CI/CD → Pipelines**.
