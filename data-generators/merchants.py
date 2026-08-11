import random

from tqdm import tqdm
from psycopg2.extras import execute_values

from config import (
    fake,
    NUM_MERCHANTS,
    BATCH_SIZE,
    DUPLICATE_MERCHANT_PERCENT,
    MISSPELT_CITY_PERCENT
)

from database import conn, cursor

from constants import (
    MERCHANT_CATEGORIES
)

from utils import (
    maybe,
    get_city_state
)

INSERT_QUERY = """
INSERT INTO merchants (
    merchant_name,
    merchant_category,
    city,
    state,
    merchant_rating,
    is_online,
    established_year
)
VALUES %s;
"""

generated_names = []

PREFIXES = [
    "Shree",
    "Sri",
    "Royal",
    "National",
    "Modern",
    "New",
    "Prime",
    "Star",
    "City",
    "Metro",
    "Elite"
]

SUFFIXES = [
    "Stores",
    "Mart",
    "Traders",
    "Enterprises",
    "Cafe",
    "Restaurant",
    "Electronics",
    "Pharmacy",
    "Supermarket",
    "Fashion",
    "Jewellers"
]

def generate_merchant():

    # ---------------------------------
    # Merchant Name
    # ---------------------------------

    if generated_names and maybe(DUPLICATE_MERCHANT_PERCENT / 100):

        merchant_name = random.choice(generated_names)

    else:

        merchant_name = (
            f"{random.choice(PREFIXES)} "
            f"{fake.last_name()} "
            f"{random.choice(SUFFIXES)}"
        )

        generated_names.append(merchant_name)

    # ---------------------------------
    # Merchant Category
    # ---------------------------------

    merchant_category = random.choice(MERCHANT_CATEGORIES)

    # ---------------------------------
    # City & State
    # ---------------------------------

    city, state = get_city_state(
        misspell=maybe(MISSPELT_CITY_PERCENT / 100)
    )

    # ---------------------------------
    # Rating
    # ---------------------------------

    merchant_rating = round(
        random.uniform(2.5, 5.0),
        1
    )

    # ---------------------------------
    # Online Merchant
    # ---------------------------------

    is_online = random.choices(
        [True, False],
        weights=[30, 70],
        k=1
    )[0]

    # ---------------------------------
    # Established Year
    # ---------------------------------

    established_year = random.randint(
        1980,
        2024
    )

    return (
        merchant_name,
        merchant_category,
        city,
        state,
        merchant_rating,
        is_online,
        established_year
    )

def generate_merchants():

    batch = []

    for _ in tqdm(
        range(NUM_MERCHANTS),
        desc="Generating Merchants"
    ):

        batch.append(
            generate_merchant()
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
        f"\n✅ Successfully inserted {NUM_MERCHANTS:,} merchants."
    )


if __name__ == "__main__":

    try:

        generate_merchants()

    except Exception as e:

        conn.rollback()

        print(f"\n❌ Error: {e}")

    finally:

        cursor.close()

        conn.close()

