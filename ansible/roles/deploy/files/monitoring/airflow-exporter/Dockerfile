FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#RUN apt-get update && \
 #   apt-get install -y git gcc python3-dev && \
  #  rm -rf /var/lib/apt/lists/*

COPY airflow_exporter.py .
#RUN git clone https://github.com/epoch8/airflow-exporter.git . && \
 #   pip install --no-cache-dir -e .

EXPOSE 9112
CMD ["python", "airflow_exporter.py"]
#CMD ["airflow-exporter", "--airflow-host=http://airflow-webserver:8080", "--airflow-username=admin", "--airflow-password=admin"]
