# ЛР 4: Loki, Prometheus, Grafana

Airflow + Spark в compose, сверху Loki/Alloy для логов и Prometheus для метрик, Grafana с дашбордом.

Что где: логи тасков лежат в `./logs` (маска как в методичке), логи Spark — в `./spark-logs` (`*.out` уходят в Loki как `job=spark_logs`). Prometheus снимает `/admin/metrics/` с webserver и два endpoint’а Spark Master из `spark/metrics.properties`. Grafana с provisioning’ом датасорсов и дашбордом в папке **lab4** (две панели: Loki и Prometheus).

## Структура

```
.
├── Dockerfile
├── docker-compose.yml
├── alloy.conf
├── prometheus.yml
├── dags/spark_dag.py
├── spark/
│   ├── spark_job.py
│   └── metrics.properties
├── grafana/
├── spark-logs/
├── logs/
└── plugins/
```

## Порты (на хосте)

Порты сдвинуты от дефолтных, чтобы не конфликтовать с lab2/lab3, если они ещё запущены.

| Куда | Адрес |
|------|--------|
| Airflow | http://localhost:18082 |
| Spark Master UI | http://localhost:14040 |
| Spark UI воркера | http://localhost:18083 |
| Spark RPC с хоста | `localhost:17077` |
| Loki | :3100 |
| Alloy | :12345 |
| Prometheus | :9090 |
| Grafana | :3000 |

## Запуск

```bash
git clone https://github.com/katterns/DevOps.git  
cd airflow-lab4
mkdir -p logs plugins spark-logs
docker compose up -d --build
```

Подожать минуту-две. Связка `spark_default` и `deploy_mode=cluster` задана переменной `AIRFLOW_CONN_SPARK_DEFAULT` в compose.

Войти в Airflow (`airflow` / `airflow`), включить DAG `spark_math_calculations`.

Проверка: Prometheus - Targets все три job’а зелёные; Grafana - папка `lab4` и дашборд; Loki Explore — `{job="airflow_logs"}` или `{job="spark_logs"}`.

Остановка: `docker compose down -v`
