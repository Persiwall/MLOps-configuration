# Базовый образ Spark 3.4.1
FROM bitnami/spark:3.4.1

# Создание папки для DAG-файлов Airflow
USER root
RUN mkdir -p /opt/airflow/dags

# Устанавка Python-библиотек
RUN pip install pyspark==3.4.1 psycopg2-binary

# Копирование конфига Spark
COPY spark-defaults.conf /opt/bitnami/spark/conf/spark-defaults.conf
