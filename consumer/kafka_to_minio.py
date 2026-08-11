import os
import json
from pathlib import Path
from datetime import datetime

import boto3
import pandas as pd
from kafka import KafkaConsumer
from dotenv import load_dotenv

# -----------------------------
# Load secrets from .env
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env.minio")

# Debugging
print("KAFKA_BOOTSTRAP =", os.getenv("KAFKA_BOOTSTRAP"))
print("KAFKA_GROUP =", os.getenv("KAFKA_GROUP"))

# Kafka consumer settings

consumer = KafkaConsumer(
    "banking_server.public.customers",
    "banking_server.public.accounts",
    "banking_server.public.cards",
    "banking_server.public.merchants",
    "banking_server.public.transactions",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP"),
    
    api_version=(3, 4, 0),

    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=os.getenv("KAFKA_GROUP"),
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),

    consumer_timeout_ms=30000
)

# MinIO client

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name="us-east-1"
)

bucket = os.getenv("MINIO_BUCKET")

try:
    s3.head_bucket(Bucket=bucket)
except Exception:
    s3.create_bucket(Bucket=bucket)

    s3.get_waiter("bucket_exists").wait(
        Bucket=bucket
    )

# Consume and write function

def write_to_minio(table_name, records):

    if not records:
        return

    df = pd.DataFrame(records)

    now = datetime.now()

    file_name = f"{table_name}_{now.strftime('%H%M%S%f')}.parquet"

    df.to_parquet(
        file_name,
        engine="pyarrow",
        index=False
    )

    s3_key = (
        f"{table_name}/"
        f"year={now.year}/"
        f"month={now.month:02}/"
        f"day={now.day:02}/"
        f"{file_name}"
    )

    s3.upload_file(
        file_name,
        bucket,
        s3_key
    )

    os.remove(file_name)

    print(f"Uploaded {len(records):,} rows -> {s3_key}")

# Batch consume
batch_size = 5000

buffer = {
    "banking_server.public.customers": [],
    "banking_server.public.accounts": [],
    "banking_server.public.cards": [],
    "banking_server.public.merchants": [],
    "banking_server.public.transactions": []
}

print("✅ Connected to Kafka. Listening for messages...")

try:

    for message in consumer:

        topic = message.topic
        event = message.value
        payload = event.get("payload", {})
        record = payload.get("after")

        if record:
            buffer[topic].append(record)

            if len(buffer[topic]) % 1000 == 0:
                print(
                    f"{topic}: {len(buffer[topic])} records buffered"
                )

        if len(buffer[topic]) >= batch_size:
            write_to_minio(
                topic.split(".")[-1],
                buffer[topic]
            )
            buffer[topic] = []

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:

    # Flush remaining records
    for topic, records in buffer.items():

        if records:

            write_to_minio(
                topic.split(".")[-1],
                records
            )

    consumer.close()

