import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, "/opt/airflow")

from src.utils.file_validation import validate_file
from src.etl.read_csv import read_hospital_records
from src.etl.data_quality import check_data_quality
from src.etl.clean import clean_hospital_records
from src.etl.transform import transform_hospital_records
from src.etl.load import load_to_postgres

FILE_PATH = "/opt/airflow/data/hospital_records.csv"


def task_validate_file():
    validate_file(FILE_PATH)


def task_read_csv(**context):
    df = read_hospital_records(FILE_PATH, nrows=10000)
    context["ti"].xcom_push(key="hospital_df", value=df.to_json())


def task_data_quality(**context):
    import pandas as pd
    from io import StringIO

    df_json = context["ti"].xcom_pull(task_ids="read_csv", key="hospital_df")
    df = pd.read_json(StringIO(df_json))

    report = check_data_quality(df)
    context["ti"].xcom_push(key="quality_report", value=report)


def task_clean(**context):
    import pandas as pd
    from io import StringIO

    df_json = context["ti"].xcom_pull(task_ids="read_csv", key="hospital_df")
    df = pd.read_json(StringIO(df_json))

    df_clean = clean_hospital_records(df)
    context["ti"].xcom_push(key="hospital_df_clean", value=df_clean.to_json())


def task_transform(**context):
    import pandas as pd
    from io import StringIO

    df_json = context["ti"].xcom_pull(task_ids="clean", key="hospital_df_clean")
    df = pd.read_json(StringIO(df_json))

    df_transformed = transform_hospital_records(df)
    context["ti"].xcom_push(key="hospital_df_transformed", value=df_transformed.to_json())


def task_load(**context):
    import pandas as pd
    from io import StringIO

    df_json = context["ti"].xcom_pull(task_ids="transform", key="hospital_df_transformed")
    df = pd.read_json(StringIO(df_json))

    load_to_postgres(df)


with DAG(
    dag_id="hospital_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["hospital", "etl"],
) as dag:

    validate = PythonOperator(
        task_id="validate_file",
        python_callable=task_validate_file,
    )

    read = PythonOperator(
        task_id="read_csv",
        python_callable=task_read_csv,
    )

    quality = PythonOperator(
        task_id="data_quality",
        python_callable=task_data_quality,
    )

    clean = PythonOperator(
        task_id="clean",
        python_callable=task_clean,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=task_transform,
    )

    load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=task_load,
    )

    validate >> read >> quality >> clean >> transform >> load