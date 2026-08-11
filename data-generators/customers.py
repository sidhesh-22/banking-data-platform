import random
from datetime import date

from tqdm import tqdm
from psycopg2.extras import execute_values

from config import (
    fake,
    NUM_CUSTOMERS,
    BATCH_SIZE,
    INVALID_EMAIL_PERCENT,
    MISSING_PHONE_PERCENT,
    NULL_OCCUPATION_PERCENT,
    FUTURE_DATE_PERCENT,
    MISSPELT_CITY_PERCENT
)

from database import conn, cursor

from constants import (
    GENDERS,
    MARITAL_STATUS,
    OCCUPATIONS,
    KYC_STATUS
)

from utils import (
    maybe,
    get_city_state,
    random_customer_since,
    future_customer_since,
    random_income
)

INSERT_QUERY = """
INSERT INTO customers (
    first_name,
    last_name,
    date_of_birth,
    gender,
    email,
    phone_number,
    marital_status,
    occupation,
    annual_income,
    employment_type,
    city,
    state,
    customer_since,
    kyc_status
)
VALUES %s;
"""

EMPLOYMENT_MAP = {
    "Software Engineer": "Full-Time",
    "Doctor": "Full-Time",
    "Teacher": "Full-Time",
    "Lawyer": "Full-Time",
    "Accountant": "Full-Time",
    "Business Owner": "Business",
    "Bank Manager": "Full-Time",
    "Government Employee": "Full-Time",
    "Nurse": "Full-Time",
    "Sales Executive": "Full-Time",
    "Marketing Manager": "Full-Time",
    "Civil Engineer": "Full-Time",
    "Mechanical Engineer": "Full-Time",
    "Student": "Student",
    "Retired": "Retired",
    "Farmer": "Self-Employed",
    "Consultant": "Self-Employed",
    "Architect": "Self-Employed",
    "Professor": "Full-Time",
    "Police Officer": "Full-Time"
}

generated_emails = set()
generated_phone_numbers = set()

def generate_customer():

    gender = random.choice(GENDERS)

    if gender == "Male":
        first_name = fake.first_name_male()
    elif gender == "Female":
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name()

    last_name = fake.last_name()

    dob = fake.date_of_birth(
        minimum_age=18,
        maximum_age=85
    )

    # -----------------------------
    # Email
    # -----------------------------

    while True:

        if maybe(INVALID_EMAIL_PERCENT / 100):

            email = (
                f"{first_name.lower()}"
                f"{last_name.lower()}"
                f"{random.randint(100000,999999)}"
            )

        else:

            email = (
                f"{first_name.lower()}."
                f"{last_name.lower()}."
                f"{random.randint(100000,999999)}@gmail.com"
            )

        if email not in generated_emails:
            generated_emails.add(email)
            break

    # -----------------------------
    # Phone Number
    # -----------------------------

    phone = None

    if not maybe(MISSING_PHONE_PERCENT / 100):

        while True:

            phone = (
                random.choice(["6", "7", "8", "9"])
                + "".join(random.choices("0123456789", k=9))
            )

            if phone not in generated_phone_numbers:

                generated_phone_numbers.add(phone)
                break

    # -----------------------------
    # Occupation, Employment & Income
    # -----------------------------

    if maybe(NULL_OCCUPATION_PERCENT / 100):

        occupation = None
        employment_type = None
        annual_income = None

    else:

        occupation = random.choice(OCCUPATIONS)
        employment_type = EMPLOYMENT_MAP[occupation]
        annual_income = random_income(occupation)

    # -----------------------------
    # City & State
    # -----------------------------

    city, state = get_city_state(
        misspell=maybe(MISSPELT_CITY_PERCENT / 100)
    )

    # -----------------------------
    # Customer Since
    # -----------------------------

    adult_date = date(
        dob.year + 18,
        dob.month,
        min(dob.day, 28)
    )

    if maybe(FUTURE_DATE_PERCENT / 100):

        customer_since = future_customer_since()

    else:

        customer_since = random_customer_since()

        if customer_since < adult_date:
            customer_since = adult_date

    # -----------------------------
    # KYC Status
    # -----------------------------

    kyc_status = random.choices(
        KYC_STATUS,
        weights=[90, 8, 2],
        k=1
    )[0]

    return (
        first_name,
        last_name,
        dob,
        gender,
        email,
        phone,
        random.choice(MARITAL_STATUS),
        occupation,
        annual_income,
        employment_type,
        city,
        state,
        customer_since,
        kyc_status
    )

def generate_customers():

    batch = []

    for _ in tqdm(
        range(NUM_CUSTOMERS),
        desc="Generating Customers"
    ):

        batch.append(
            generate_customer()
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
        f"\n✅ Successfully inserted {NUM_CUSTOMERS:,} customers."
    )


if __name__ == "__main__":

    try:

        generate_customers()

    except Exception as e:

        conn.rollback()

        print(f"\n❌ Error: {e}")

    finally:

        cursor.close()

        conn.close()

