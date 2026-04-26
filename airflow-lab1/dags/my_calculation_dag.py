import math
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def fib_15(**context):
    a, b = 0, 1
    fib = [a, b]
    for _ in range(13):
        a, b = b, a + b
        fib.append(b)
    context["ti"].xcom_push(key="fibonacci", value=fib)
    print(fib)
    return fib


def facts_1_10(**context):
    out = {i: math.factorial(i) for i in range(1, 11)}
    context["ti"].xcom_push(key="factorials", value=out)
    print(out)
    return out


def stats(**context):
    ti = context["ti"]
    fib = ti.xcom_pull(task_ids="calc_fibonacci", key="fibonacci")
    fac = ti.xcom_pull(task_ids="calc_factorials", key="factorials")
    fvals = list(fac.values())
    fsum, fmax = sum(fib), max(fib)
    dsum, dmax = sum(fvals), max(fvals)
    print(
        f"fib: sum={fsum} avg={fsum/len(fib):.2f} max={fmax} | "
        f"fac: sum={dsum} avg={dsum/len(fvals):.2f} max={dmax} | "
        f"maxfac/maxfib={dmax/fmax:.2f}"
    )


with DAG(
    dag_id="math_calculations_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["lab1"],
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
) as dag:
    t_fib = PythonOperator(
        task_id="calc_fibonacci",
        python_callable=fib_15,
    )
    t_fac = PythonOperator(
        task_id="calc_factorials",
        python_callable=facts_1_10,
    )
    t_stats = PythonOperator(
        task_id="calculate_statistics",
        python_callable=stats,
    )
    [t_fib, t_fac] >> t_stats
