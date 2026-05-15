from typing import List

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max as spark_max, sum as spark_sum


def fibonacci(count: int) -> List[int]:
    nums = [0, 1]
    for i in range(2, count):
        nums.append(nums[-1] + nums[-2])
    return nums


def factorial(n: int) -> int:
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def main() -> None:
    spark = (
        SparkSession.builder.appName("MathCalculationsSpark")
        .master("spark://spark-master:7077")
        .config("spark.executor.memory", "512m")
        .config("spark.driver.memory", "512m")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    fib_nums = fibonacci(15)
    facts = {i: factorial(i) for i in range(1, 11)}

    print(f"Фибоначчи (до {len(fib_nums)} чисел): {fib_nums}")
    print(f"Факториалы 1..10: {facts}")

    fib_df = spark.createDataFrame(
        [(i, v, "fibonacci") for i, v in enumerate(fib_nums)],
        ["idx", "value", "kind"],
    )
    fact_df = spark.createDataFrame(
        [(k, v, "factorial") for k, v in facts.items()],
        ["idx", "value", "kind"],
    )

    fib_df.union(fact_df).orderBy("kind", "idx").show(20, truncate=False)

    fib_row = fib_df.agg(
        spark_sum("value").alias("sum"),
        avg("value").alias("avg"),
        spark_max("value").alias("max"),
    ).first()
    fact_row = fact_df.agg(
        spark_sum("value").alias("sum"),
        avg("value").alias("avg"),
        spark_max("value").alias("max"),
    ).first()

    print(f"Фибоначчи: sum={fib_row['sum']} avg={fib_row['avg']:.2f} max={fib_row['max']}")
    print(f"Факториалы: sum={fact_row['sum']} avg={fact_row['avg']:.2f} max={fact_row['max']}")
    if fib_row["max"]:
        print(f"max factorial / max fibonacci = {fact_row['max'] / fib_row['max']:.2f}")

    spark.stop()


if __name__ == "__main__":
    main()
