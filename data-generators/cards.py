import random
from datetime import date, timedelta

from tqdm import tqdm
from psycopg2.extras import execute_values

from config import (
    fake,
    NUM_CARDS,
    BATCH_SIZE
)

from database import conn, cursor

from constants import (
    CARD_TYPES,
    CARD_NETWORKS,
    CARD_STATUS
)

from utils import (
    maybe
)

INSERT_QUERY = """
INSERT INTO cards (
    account_id,
    card_number,
    card_type,
    network,
    issue_date,
    expiry_date,
    card_status,
    contactless_enabled
)
VALUES %s;
"""

cursor.execute("""
SELECT account_id, account_open_date
FROM accounts
ORDER BY account_id;
""")

accounts = cursor.fetchall()

generated_cards = set()

def generate_card(account_id, account_open_date):

    # ---------------------------------
    # Card Number
    # ---------------------------------

    while True:

        card_number = str(
            random.randint(10**15, (10**16) - 1)
        )

        if card_number not in generated_cards:
            generated_cards.add(card_number)
            break

    # ---------------------------------
    # Card Details
    # ---------------------------------

    card_type = random.choices(
        CARD_TYPES,
        weights=[75, 25],
        k=1
    )[0]

    network = random.choices(
        CARD_NETWORKS,
        weights=[45, 35, 15, 5],
        k=1
    )[0]

    issue_date = fake.date_between(
        start_date=account_open_date,
        end_date="today"
    )

    expiry_date = issue_date + timedelta(days=365 * 5)

    # ---------------------------------
    # Card Status
    # ---------------------------------

    if expiry_date < date.today():

        card_status = "Expired"

    else:

        card_status = random.choices(
            ["Active", "Blocked"],
            weights=[97, 3],
            k=1
        )[0]

        # 1% intentionally dirty data
        if maybe(0.01):
            card_status = "Active"

    contactless_enabled = random.choices(
        [True, False],
        weights=[85, 15],
        k=1
    )[0]

    return (
        account_id,
        card_number,
        card_type,
        network,
        issue_date,
        expiry_date,
        card_status,
        contactless_enabled
    )

def generate_cards():

    batch = []

    card_count = 0

    random.shuffle(accounts)

    account_index = 0

    while card_count < NUM_CARDS:

        account_id, account_open_date = accounts[account_index]

        # Each account gets 0–2 cards
        cards_per_account = random.choices(
            [0, 1, 2],
            weights=[20, 55, 25],
            k=1
        )[0]

        for _ in range(cards_per_account):

            if card_count >= NUM_CARDS:
                break

            batch.append(
                generate_card(
                    account_id,
                    account_open_date
                )
            )

            card_count += 1

            if len(batch) >= BATCH_SIZE:

                execute_values(
                    cursor,
                    INSERT_QUERY,
                    batch
                )

                conn.commit()

                batch.clear()

        account_index = (account_index + 1) % len(accounts)

    if batch:

        execute_values(
            cursor,
            INSERT_QUERY,
            batch
        )

        conn.commit()

    print(
        f"\n✅ Successfully inserted {card_count:,} cards."
    )


if __name__ == "__main__":

    try:

        generate_cards()

    except Exception as e:

        conn.rollback()

        print(f"\n❌ Error: {e}")

    finally:

        cursor.close()

        conn.close()

