from prometheus_client import start_http_server, Gauge, Counter
import requests
import os
import time

AIRFLOW_HOST = os.getenv("AIRFLOW_HOST")
AIRFLOW_USER = os.getenv("AIRFLOW_USERNAME")
AIRFLOW_PASS = os.getenv("AIRFLOW_PASSWORD")

class AirflowExporter:
    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (AIRFLOW_USER, AIRFLOW_PASS)
        
        # Health metrics
        self.airflow_healthy = Gauge('airflow_healthy', 'Overall health status')
        
        # DAG metrics
        self.dag_status = Gauge('airflow_dag_status', 'DAG status', ['dag_id', 'status'])
        self.dag_run_count = Counter('airflow_dag_run_total', 'Total DAG runs', ['dag_id'])
        
        # Task metrics
        self.task_status = Counter('airflow_task_status', 'Task status count', ['dag_id', 'task_id', 'status'])
        
        # Scheduler metrics
        self.scheduler_heartbeat = Gauge('airflow_scheduler_heartbeat', 'Last scheduler heartbeat')

    def collect_metrics(self):
        try:
            # Health check
            health_resp = self.session.get(f"{AIRFLOW_HOST}/health")
            self.airflow_healthy.set(1 if health_resp.status_code == 200 else 0)
            
            # DAG metrics
            dags_resp = self.session.get(f"{AIRFLOW_HOST}/api/v1/dags")
            for dag in dags_resp.json()['dags']:
                dag_id = dag['dag_id']
                
                # DAG runs
                runs_resp = self.session.get(
                    f"{AIRFLOW_HOST}/api/v1/dags/{dag_id}/dagRuns"
                )
                runs = runs_resp.json()['dag_runs']
                self.dag_run_count.labels(dag_id=dag_id).inc(len(runs))
                
                # DAG status
                status_count = {}
                for run in runs:
                    status = run['state']
                    status_count[status] = status_count.get(status, 0) + 1
                
                for status, count in status_count.items():
                    self.dag_status.labels(
                        dag_id=dag_id, 
                        status=status
                    ).set(count)
            
            # Scheduler heartbeat
            scheduler_resp = self.session.get(f"{AIRFLOW_HOST}/api/v1/health")
            if scheduler_resp.status_code == 200:
                scheduler_data = scheduler_resp.json()
                if 'scheduler' in scheduler_data:
                    self.scheduler_heartbeat.set(
                        scheduler_data['scheduler']['latest_scheduler_heartbeat']
                    )

        except Exception as e:
            print(f"Error collecting metrics: {e}")

if __name__ == "__main__":
    exporter = AirflowExporter()
    start_http_server(9112)
    while True:
        exporter.collect_metrics()
        time.sleep(30)
