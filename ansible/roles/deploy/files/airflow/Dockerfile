FROM apache/airflow:2.7.3-python3.11

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        postgresql-client-14 \
        openjdk-11-jdk \
	build-essential \
	python3-dev \
	libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
