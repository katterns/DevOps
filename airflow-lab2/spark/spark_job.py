"""
Spark job для расчёта статистики
"""
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import sum as spark_sum, avg, max as spark_max


def calculate_fibonacci(n=15):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def calculate_factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def main():
    print("=" * 60)
    print("ЗАПУСК SPARK JOB: РАСЧЁТ СТАТИСТИКИ")
    print("=" * 60)
    
    # Создаём SparkSession
    spark = SparkSession.builder \
        .appName("MathCalculationsSpark") \
        .master("spark://spark-master:7077") \
        .config("spark.executor.memory", "512m") \
        .config("spark.driver.memory", "512m") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    
    print(f"Spark версия: {spark.version}")
    print(f"Master: {spark.sparkContext.master}")
    print(f"App Name: {spark.sparkContext.appName}")
    
    # Вычисляем числа Фибоначчи
    fib_numbers = calculate_fibonacci(15)
    print(f"\nЧисла Фибоначчи (первые 15): {fib_numbers}")
    
    # Вычисляем факториалы
    factorials = {i: calculate_factorial(i) for i in range(1, 11)}
    print(f"Факториалы (1-10): {factorials}")
    
    # Создаём DataFrame с числами Фибоначчи
    fib_data = [(i, val, "fibonacci") for i, val in enumerate(fib_numbers)]
    fib_df = spark.createDataFrame(fib_data, ["index", "value", "type"])
    
    # Создаём DataFrame с факториалами
    fact_data = [(k, v, "factorial") for k, v in factorials.items()]
    fact_df = spark.createDataFrame(fact_data, ["index", "value", "type"])
    
    # Объединяем данные
    all_data_df = fib_df.union(fact_df)
    
    print("\n" + "=" * 60)
    print("ДАННЫЕ В SPARK DATAFRAME:")
    print("=" * 60)
    all_data_df.orderBy("type", "index").show(10, truncate=False)
    
    # Вычисляем статистику
    print("\n" + "=" * 60)
    print("СТАТИСТИКА (ВЫЧИСЛЕНА С ПОМОЩЬЮ SPARK):")
    print("=" * 60)
    
    fib_stats = fib_df.agg(
        spark_sum("value").alias("sum"),
        avg("value").alias("avg"),
        spark_max("value").alias("max")
    ).collect()[0]
    
    print(f"Фибоначчи:")
    print(f"  - Сумма: {fib_stats['sum']}")
    print(f"  - Среднее: {fib_stats['avg']:.2f}")
    print(f"  - Максимум: {fib_stats['max']}")
    
    fact_stats = fact_df.agg(
        spark_sum("value").alias("sum"),
        avg("value").alias("avg"),
        spark_max("value").alias("max")
    ).collect()[0]
    
    print(f"\nФакториалы:")
    print(f"  - Сумма: {fact_stats['sum']}")
    print(f"  - Среднее: {fact_stats['avg']:.2f}")
    print(f"  - Максимум: {fact_stats['max']}")
    
    ratio = fact_stats['max'] / fib_stats['max']
    print(f"\nСравнительный анализ:")
    print(f"  - Отношение макс. факториала к макс. Фибоначчи: {ratio:.2f}")
    
    spark.stop()
    
    print("\n" + "=" * 60)
    print("SPARK JOB УСПЕШНО ЗАВЕРШЁН!")
    print("=" * 60)


if __name__ == "__main__":
    main()
