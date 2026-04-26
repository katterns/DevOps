## Описание

Развёртывание Apache Airflow с использованием Docker Compose и разработка кастомного DAG для математических вычислений.

## Структура проекта

.
├── Dockerfile              # Кастомный образ Airflow
├── docker-compose.yml      # Конфигурация сервисов
├── dags/                   # Директория с DAG-файлами
│   └── my_calculation_dag.py
├── logs/                   # Логи Airflow
├── plugins/                # Плагины
└── README.md              # Документация

## Внесённые изменения в docker-compose.yml

По сравнению с оригинальным файлом из документации Airflow:

1. Удалены сервисы: redis, airflow-worker, airflow-triggerer, airflow-cli, flower
2. Изменён Executor: CeleryExecutor -> LocalExecutor
3. Удалены зависимости от Redis: из блока depends_on убраны строки с redis
4. Используется кастомный образ: через директиву build вместо готового образа
5. Настроены учётные данные: логин/пароль через переменные _AIRFLOW_WWW_USER_*
6. Отключены примеры: AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

## Описание DAG

DAG math_calculations_dag выполняет следующие задачи:

1. calc_fibonacci — первые 15 чисел Фибоначчи, кладёт список в XCom
2. calc_factorials — факториалы 1..10, в XCom
   
3. calculate_statistics — тянет оба XCom, считает сумму/среднее/макс и печатает одну строку в лог

Граф: `[calc_fibonacci, calc_factorials] >> calculate_statistics`

## Развёртывание локально

### Предварительные требования

- Docker версии 20.10+
- Docker Compose версии 2.0+
- Свободный порт 8080 на localhost

### Шаги для запуска

1. Клонировать репозиторий

```bash
git clone https://github.com/katterns/DevOps.git
cd DevOps/airflow-lab1
```

2. Создать необходимые директории:
mkdir -p dags logs plugins

3. Запустить Airflow:
docker compose up -d

4. Дождаться инициализации (около 30-60 секунд):
docker ps
docker compose logs airflow-init

5. Открыть веб-интерфейс Airflow:
- URL: http://localhost:8080
- Логин: airflow
- Пароль: airflow

### Возможные проблемы и их решение

Проблема: Контейнеры в статусе unhealthy или starting
Решение: Проверить логи командой docker compose logs, возможно нужно больше времени на инициализацию

Проблема: Порт 8080 занят
Решение: Изменить порт в docker-compose.yml: "8081:8080"

Проблема: DAG не отображается в интерфейсе
Решение: Проверить права на файл DAG и перезапустить scheduler:
docker compose restart airflow-scheduler

### Остановка и очистка

Остановка контейнеров:
docker compose down

Остановка с удалением томов (полная очистка):
docker compose down -v

## Проверка работы DAG

1. В веб-интерфейсе найти DAG с именем math_calculations_dag
2. Активировать DAG (переключатель слева)
3. Нажать "Trigger DAG" (кнопка Play справа)
4. Выбрать "Trigger DAG" в появившемся окне
5. Отслеживать выполнение по цвету задач:
   - Зелёный - успешно
   - Красный - ошибка
   - Жёлтый - в процессе
6. Нажать на задачу -> "Log" для просмотра детальных логов

Ожидаемая строка в логе задачи `calculate_statistics`:

`fib: sum=986 avg=65.73 max=377 | fac: sum=4037913 avg=403791.30 max=3628800 | maxfac/maxfib=9625.46`

## Особенности конфигурации

- Executor: LocalExecutor (вместо CeleryExecutor) - упрощённая архитектура
- Примеры DAG-ов: отключены (AIRFLOW__CORE__LOAD_EXAMPLES: 'false')
- Архитектура: только webserver, scheduler, postgres и init
- Сборка образа: через локальный Dockerfile
- Синхронизация DAG-ов: через volume ./dags:/opt/airflow/dags

## Структура кастомного Dockerfile

```dockerfile
FROM apache/airflow:2.7.0
WORKDIR ${AIRFLOW_HOME}
COPY dags/ ${AIRFLOW_HOME}/dags/
```

Базовый образ расширяется только копированием DAG-файлов, дополнительные зависимости не требуются.
