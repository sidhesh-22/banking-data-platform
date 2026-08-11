import random

from tqdm import tqdm
from psycopg2.extras import execute_values

from config import (
    fake,
    NUM_TRANSACTIONS,
    BATCH_SIZE,
    MISSPELT_CITY_PERCENT
)

from database import conn, cursor

from constants import (
    TRANSACTION_TYPES,
    PAYMENT_CHANNELS,
    TRANSACTION_STATUS,
    DEVICE_TYPES
)

from utils import (
    maybe,
    get_city_state,
    random_transaction_datetime
)

INSERT_QUERY = """
INSERT INTO transactions (
    account_id,
    merchant_id,
    transaction_reference,
    transaction_timestamp,
    amount,
    transaction_type,
    payment_channel,
    transaction_status,
    device_type,
    city
)
VALUES %s;
"""

# -----------------------------
# Fetch Parent Keys
# -----------------------------

cursor.execute("""
SELECT account_id
FROM accounts;
""")

account_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("""
SELECT merchant_id
FROM merchants;
""")

merchant_ids = [row[0] for row in cursor.fetchall()]

generated_refs = set()

def generate_transaction():

    account_id = random.choice(account_ids)

    merchant_id = random.choice(merchant_ids)

    # ---------------------------------
    # Transaction Reference
    # ---------------------------------

    while True:

        transaction_reference = (
            "TXN"
            + str(random.randint(100000000000, 999999999999))
        )

        if transaction_reference not in generated_refs:
            generated_refs.add(transaction_reference)
            break

    # ---------------------------------
    # Transaction Timestamp
    # ---------------------------------

    transaction_timestamp = random_transaction_datetime()

    # ---------------------------------
    # Amount
    # ---------------------------------

    amount = round(
        random.uniform(10, 250000),
        2
    )

    # ---------------------------------
    # Transaction Type
    # ---------------------------------

    transaction_type = random.choices(
        TRANSACTION_TYPES,
        weights=[50, 20, 10, 8, 10, 2],
        k=1
    )[0]

    # ---------------------------------
    # Payment Channel
    # ---------------------------------

    payment_channel = random.choices(
        PAYMENT_CHANNELS,
        weights=[10, 20, 30, 15, 20, 5],
        k=1
    )[0]

    # ---------------------------------
    # Transaction Status
    # ---------------------------------

    transaction_status = random.choices(
        TRANSACTION_STATUS,
        weights=[92, 3, 4, 1],
        k=1
    )[0]

    # Introduce dirty data (3%)
    if maybe(0.03):
        transaction_status = transaction_status.lower()

    # ---------------------------------
    # Device Type
    # ---------------------------------

    device_type = random.choice(
        DEVICE_TYPES
    )

    # ---------------------------------
    # City
    # ---------------------------------

    city, _ = get_city_state(
        misspell=maybe(
            MISSPELT_CITY_PERCENT / 100
        )
    )

    return (
        account_id,
        merchant_id,
        transaction_reference,
        transaction_timestamp,
        amount,
        transaction_type,
        payment_channel,
        transaction_status,
        device_type,
        city
    )


def generate_transactions():

    batch = []

    for _ in tqdm(
        range(NUM_TRANSACTIONS),
        desc="Generating Transactions"
    ):

        batch.append(
            generate_transaction()
        )

        if len(batch) >= BATCH_SIZE:

            execute_values(
                cursor,
                INSERT_QUERY,
                batch
            )

            conn.commit()

            batch.clear()

    if batch:

        execute_values(
            cursor,
            INSERT_QUERY,
            batch
        )

        conn.commit()

    print(
        f"\n✅ Successfully inserted {NUM_TRANSACTIONS:,} transactions."
    )


if __name__ == "__main__":

    try:

        generate_transactions()

    except Exception as e:

        conn.rollback()

        print(f"\n❌ Error: {e}")

    finally:

        cursor.close()

        conn.close()

