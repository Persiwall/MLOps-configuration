from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "test_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once",
    catchup=False,
) as dag:
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )
