from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

import pandas as pd
import pyodbc

azure_server = 'retail-sales-dw.database.windows.net' 
azure_database = 'retail-sales-dw'
azure_username = 'Lucas'
azure_password = '1202Abc!' 

dag = DAG('excel_to_azure', start_date=datetime(2023, 3, 10))

def extract():
    df = pd.read_excel('C:/Users/lucas/OneDrive/Desktop/VSproject/Retails_DW/Retails_DW/sample_data.xlsx')
    return df

def transform(df):
    # Transform df here 
    return df

def load_to_azure(df):
    conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={azure_server};DATABASE={azure_database};UID={azure_username};PWD={azure_password}' 
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO mytable VALUES(?, ?)", row['col1'], row['col2'])

    conn.commit()

extract_task = PythonOperator(
    task_id='extract_from_excel',
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    op_kwargs={'df': '{{ ti.xcom_pull(task_ids="extract_from_excel") }}'}, 
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_azure',
    python_callable=load_to_azure,
    op_kwargs={'df': '{{ ti.xcom_pull(task_ids="transform") }}'},
    dag=dag,
)

extract_task >> transform_task >> load_task