import os
from datetime import datetime, timedelta
from pathlib import Path
import boto3
import snowflake.connector
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR /".env.minio_snowflake")

# -------------------------------------------------
# MinIO Configuration
# -------------------------------------------------

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

LOCAL_DIR = os.getenv(
    "MINIO_LOCAL_DIR",
    "/tmp/minio_downloads"
)

# -------------------------------------------------
# Snowflake Configuration
# -------------------------------------------------

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# -------------------------------------------------
# Tables
# -------------------------------------------------

TABLES = [
    "customers",
    "accounts",
    "cards",
    "merchants",
    "transactions",
]

# -------------------------------------------------
# Download from MinIO
# -------------------------------------------------

def download_from_minio():

    os.makedirs(
        LOCAL_DIR,
        exist_ok=True
    )

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    downloaded_files = {}

    paginator = s3.get_paginator("list_objects_v2")

    for table in TABLES:

        downloaded_files[table] = []

        for page in paginator.paginate(
            Bucket=MINIO_BUCKET,
            Prefix=f"{table}/"
        ):

            for obj in page.get("Contents", []):

                key = obj["Key"]

                if not key.endswith(".parquet"):
                    continue

                local_path = os.path.join(
                    LOCAL_DIR,
                    key
                )

                os.makedirs(
                    os.path.dirname(local_path),
                    exist_ok=True
                )

                s3.download_file(
                    MINIO_BUCKET,
                    key,
                    local_path
                )

                print(
                    f"Downloaded: {key}"
                )

                downloaded_files[table].append(
                    local_path
                )

    return downloaded_files


# -------------------------------------------------
# Load into Snowflake
# -------------------------------------------------

def load_to_snowflake(ti=None):

    files = ti.xcom_pull(
        task_ids="download_minio"
    )

    if not files:
        print("No files found.")
        return

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

    cur = conn.cursor()

    cur.execute(f"USE WAREHOUSE {SNOWFLAKE_WAREHOUSE}")
    cur.execute(f"USE DATABASE {SNOWFLAKE_DATABASE}")
    cur.execute(f"USE SCHEMA {SNOWFLAKE_SCHEMA}")

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    try:

        for table, parquet_files in files.items():

            if not parquet_files:
                continue

            print(
                f"\nProcessing {len(parquet_files)} files for {table}"
            )

            for file in parquet_files:

                try:

                    print(
                        f"\nLoading {os.path.basename(file)}"
                    )

                    # Upload ONE file

                    cur.execute(
                        f"PUT file://{file} @%{table} "
                        f"OVERWRITE=TRUE AUTO_COMPRESS=FALSE"
                    )

                    # Copy ONLY that file

                    filename = os.path.basename(file)

                    cur.execute(

                        f"""
                        COPY INTO {table}
                        FROM @%{table}
                        FILES = ('{filename}')
                        FILE_FORMAT=(TYPE=PARQUET)
                        MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
                        FORCE=FALSE
                        ON_ERROR='CONTINUE';
                        """
                    )

                    # Print Snowflake COPY results
                    copy_results = cur.fetchall()

                    print(f"\nCOPY INTO results for {filename}")

                    for row in copy_results:
                        print(row)

                    print(
                        f"Loaded {filename}"
                    )

                    # Remove file from Snowflake stage
                    cur.execute(
                        f"""
                        REMOVE @%{table}
                        PATTERN='.*{filename}';
                        """
                    )

                    print(f"Removed {filename} from Snowflake stage")

                    # Archive in MinIO

                    minio_key = os.path.relpath(
                        file,
                        LOCAL_DIR
                    ).replace("\\", "/")

                    archive_key = (
                        f"archive/{minio_key}"
                    )

                    s3.copy_object(
                        Bucket=MINIO_BUCKET,
                        CopySource={
                            "Bucket": MINIO_BUCKET,
                            "Key": minio_key,
                        },
                        Key=archive_key,
                    )

                    s3.delete_object(
                        Bucket=MINIO_BUCKET,
                        Key=minio_key,
                    )

                    print(
                        f"Archived {minio_key}"
                    )

                    # Delete local copy

                    if os.path.exists(file):
                        os.remove(file)

                except Exception as e:

                    print(
                        f"Failed processing "
                        f"{os.path.basename(file)}"
                    )

                    print(e)

                    # Continue with remaining files

                    continue

    finally:

        cur.close()

        conn.close()


# -------------------------------------------------
# DAG
# -------------------------------------------------

default_args = {

    "owner": "airflow",

    "depends_on_past": False,

    "retries": 1,

    "retry_delay": timedelta(
        minutes=2
    ),
}

with DAG(

    dag_id="minio_to_snowflake_banking",

    description="Load Banking Parquet files from MinIO into Snowflake",

    default_args=default_args,

    start_date=datetime(
        2026,
        8,
        2
    ),

    schedule="*/5 * * * *",

    catchup=False,

    tags=[
        "banking",
        "snowflake",
        "minio",
    ],

) as dag:

    download_task = PythonOperator(

        task_id="download_minio",

        python_callable=download_from_minio,

    )

    load_task = PythonOperator(

        task_id="load_to_snowflake",

        python_callable=load_to_snowflake,

    )

    download_task >> load_task
