from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
import pandas as pd
import requests
from clickhouse_driver import Client

default_args = {
    'owner': 'bionicpro',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_user_reports',
    default_args=default_args,
    description='ETL для подготовки отчетов пользователей BionicPRO',
    schedule_interval='@hourly',  # запуск каждый час
)

def extract_crm():
    # пример запроса к CRM API
    response = requests.get('http://crm-api/users')
    users = response.json()
    df = pd.DataFrame(users)
    df.to_csv('/tmp/users.csv', index=False)

extract_crm_task = PythonOperator(
    task_id='extract_crm',
    python_callable=extract_crm,
    dag=dag,
)

def extract_telemetry():
    # пример запроса к BFF или MongoDB
    response = requests.get('http://telemetry-api/data')
    telemetry = response.json()
    df = pd.DataFrame(telemetry)
    df.to_csv('/tmp/telemetry.csv', index=False)

extract_telemetry_task = PythonOperator(
    task_id='extract_telemetry',
    python_callable=extract_telemetry,
    dag=dag,
)

def transform():
    users = pd.read_csv('/tmp/users.csv')
    telemetry = pd.read_csv('/tmp/telemetry.csv')
    # пример объединения данных
    report = telemetry.groupby('user_id').agg({
        'steps': 'sum',
        'battery': 'mean'
    }).reset_index()
    report = report.merge(users, left_on='user_id', right_on='id', how='left')
    report.to_csv('/tmp/user_report.csv', index=False)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

def load():
    client = Client('clickhouse-server')  # имя сервиса в docker-compose
    df = pd.read_csv('/tmp/user_report.csv')
    # создаём таблицу, если не существует
    client.execute('''
        CREATE TABLE IF NOT EXISTS user_reports (
            user_id UInt64,
            steps UInt64,
            battery Float32,
            name String
        ) ENGINE = MergeTree()
        ORDER BY user_id
    ''')
    data = [tuple(x) for x in df[['user_id', 'steps', 'battery', 'name']].to_numpy()]
    client.execute('INSERT INTO user_reports (user_id, steps, battery, name) VALUES', data)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag,
)

