from airflow import DAG
from datetime import timedelta
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from extract import extract_data
from load import load_data

## VARIABLES
schedule_interval = '0 9 * * *' # Runs daily at 9 a.m.
start_date = days_ago(1)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='reddit_pipeline',
    default_args=default_args,
    description='DAG',
    start_date=start_date,
    schedule_interval=schedule_interval,
    max_active_runs=1,
    catchup=False,
    is_paused_upon_creation=False  # Automatically unpauses DAG upon creation
) as dag:
    
    reddit_task1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    reddit_task2 = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

reddit_task1 >> reddit_task2