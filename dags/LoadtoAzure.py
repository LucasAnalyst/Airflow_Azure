from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Connection  
import pandas as pd
import os
import pyodbc
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
from airflow.utils.dates import days_ago

# get dag directory path
dag_path = os.getcwd()

# create function transform_data
def transform_data():
    products = pd.read_excel(os.path.join(dag_path, "Data/Retails/Products.xlsx"))
    transactions = pd.read_excel(os.path.join(dag_path, "Data/Retails/Transactions.xlsx"))
    customers = pd.read_excel(os.path.join(dag_path, "Data/Retails/Customers.xlsx"))
    stores = pd.read_excel(os.path.join(dag_path, "Data/Retails/Stores.xlsx"))

    # make date format consistent
    transactions.Date = pd.to_datetime(transactions.Date, infer_datetime_format=True)
  
    # load processed data
    products.to_csv(f"{dag_path}/processed_data/Products.csv", index=False)
    transactions.to_csv(f"{dag_path}/processed_data/Transactions.csv", index=False)   
    customers.to_csv(f"{dag_path}/processed_data/Customers.csv", index=False)
    stores.to_csv(f"{dag_path}/processed_data/Stores.csv", index=False)

# create function load_data
def load_data():
    connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:retails-data.database.windows.net,1433;Database=Retails_DW;Uid=Lucas;Pwd=1202Abc!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    csv_files = {
        'Customers': f"{dag_path}/processed_data/Customers.csv",
        'Products': f"{dag_path}/processed_data/Products.csv",
        'Stores': f"{dag_path}/processed_data/Stores.csv",
        'Transactions': f"{dag_path}/processed_data/Transactions.csv"
    }

    for table_name, csv_file_path in csv_files.items():

    # Read CSV
        records = pd.read_csv(csv_file_path)

    # Get parameterized column names 
        columns = ", ".join([f'[{col}]' for col in records.columns])

    # Construct insert query
        insert_query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({("?, " * len(records.columns))[:-2]})
            """
        
    # Retrieve existing records
        existing_ids = set()
        cursor.execute(f"SELECT {table_name[:-1]}ID FROM {table_name}")   #Example table name is Products and the ID column name is ProductID: {table_name[:-1]}
        existing_ids = {row[0] for row in cursor.fetchall()}
        
    # Check current data and insert new rows
        for _, row in records.iterrows():
            if row[f"{table_name[:-1]}ID"] not in existing_ids:
                values = tuple(row)
                cursor.execute(insert_query, values)

        conn.commit()

    conn.close()

# initializing the default arguments that we'll pass to our DAG
default_args = {
    'owner': 'Lucas',
    'start_date': days_ago(2)
}

ingestion_dag = DAG(
    'Airflow_excel',
    default_args=default_args,
    description='Pipelines that use to load data into dw',
    schedule_interval=timedelta(days=1),
    catchup=False
)

task_1 = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=ingestion_dag,
)

task_2 = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=ingestion_dag,
)

task_1 >> task_2 
