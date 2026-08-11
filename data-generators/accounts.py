import random

from datetime import timedelta
from tqdm import tqdm
from psycopg2.extras import execute_values

from config import (
    fake,
    NUM_ACCOUNTS,
    BATCH_SIZE
)

from database import conn, cursor

from constants import (
    ACCOUNT_TYPES,
    ACCOUNT_STATUS,
    LOAN_TYPES
)

from utils import (
    random_account_open_date,
    random_balance,
    maybe
)

INSERT_QUERY = """
INSERT INTO accounts (
    customer_id,
    account_number,
    account_type,
    account_status,
    current_balance,
    available_balance,
    branch_name,
    branch_city,
    branch_state,
    loan_type,
    loan_amount,
    outstanding_loan,
    interest_rate,
    account_open_date,
    last_activity_date
)
VALUES %s;
"""

cursor.execute("""
SELECT customer_id
FROM customers
ORDER BY customer_id;
""")

customer_ids = [row[0] for row in cursor.fetchall()]

BRANCHES = [
    ("Mumbai Main", "Mumbai", "Maharashtra"),
    ("Pune Central", "Pune", "Maharashtra"),
    ("Delhi CP", "Delhi", "Delhi"),
    ("Bengaluru MG Road", "Bengaluru", "Karnataka"),
    ("Hyderabad Banjara Hills", "Hyderabad", "Telangana"),
    ("Chennai T Nagar", "Chennai", "Tamil Nadu"),
    ("Ahmedabad CG Road", "Ahmedabad", "Gujarat"),
    ("Kolkata Park Street", "Kolkata", "West Bengal"),
    ("Jaipur MI Road", "Jaipur", "Rajasthan"),
    ("Lucknow Hazratganj", "Lucknow", "Uttar Pradesh")
]

generated_accounts = set()


def generate_account(customer_id):

    # ---------------------------------
    # Account Number
    # ---------------------------------

    while True:

        account_number = str(
            random.randint(10**11, (10**12) - 1)
        )

        if account_number not in generated_accounts:
            generated_accounts.add(account_number)
            break

    # ---------------------------------
    # Account Details
    # ---------------------------------

    account_type = random.choices(
        ACCOUNT_TYPES,
        weights=[45, 25, 20, 10],
        k=1
    )[0]

    account_status = random.choices(
        ACCOUNT_STATUS,
        weights=[88, 6, 4, 2],
        k=1
    )[0]

    current_balance = random_balance()

    available_balance = round(
        max(0, current_balance - random.uniform(0, 50000)),
        2
    )

    branch_name, branch_city, branch_state = random.choice(
        BRANCHES
    )

    # ---------------------------------
    # Loan Details
    # ---------------------------------

    if maybe(0.25):

        loan_type = random.choice(
            LOAN_TYPES[1:]
        )

        loan_amount = round(
            random.uniform(100000, 5000000),
            2
        )

        outstanding_loan = round(
            loan_amount * random.uniform(0.1, 1.0),
            2
        )

        interest_rate = round(
            random.uniform(7.0, 15.0),
            2
        )

    else:

        loan_type = None
        loan_amount = None
        outstanding_loan = None
        interest_rate = None

    # ---------------------------------
    # Dates
    # ---------------------------------

    account_open_date = random_account_open_date()

    if maybe(0.01):
        # 1% intentionally bad data
        last_activity_date = account_open_date - timedelta(days=365)

    else:
        last_activity_date = fake.date_between(
            start_date=account_open_date,
            end_date="today"
    )

    return (
        customer_id,
        account_number,
        account_type,
        account_status,
        current_balance,
        available_balance,
        branch_name,
        branch_city,
        branch_state,
        loan_type,
        loan_amount,
        outstanding_loan,
        interest_rate,
        account_open_date,
        last_activity_date
    )


def generate_accounts():

    batch = []

    account_count = 0

    random.shuffle(customer_ids)

    customer_index = 0

    while account_count < NUM_ACCOUNTS:

        customer_id = customer_ids[customer_index]

        accounts_for_customer = random.choices(
            [1, 2, 3],
            weights=[35, 45, 20],
            k=1
        )[0]

        for _ in range(accounts_for_customer):

            if account_count >= NUM_ACCOUNTS:
                break

            batch.append(
                generate_account(customer_id)
            )

            account_count += 1

            if len(batch) >= BATCH_SIZE:

                execute_values(
                    cursor,
                    INSERT_QUERY,
                    batch
                )

                conn.commit()

                batch.clear()

        customer_index = (customer_index + 1) % len(customer_ids)

    if batch:

        execute_values(
            cursor,
            INSERT_QUERY,
            batch
        )

        conn.commit()

    print(
        f"\n✅ Successfully inserted {account_count:,} accounts."
    )


if __name__ == "__main__":

    try:

        generate_accounts()

    except Exception as e:

        conn.rollback()

        print(f"\n❌ Error: {e}")

    finally:

        cursor.close()

        conn.close()

