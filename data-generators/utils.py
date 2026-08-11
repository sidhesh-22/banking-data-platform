"""
utils.py

Contains reusable helper functions.
"""

import random

from config import fake

from constants import (
    CITY_STATE_MAP,
    CITY_MISSPELLINGS
)


# -------------------------------------------------------
# Probability Helper
# -------------------------------------------------------

def maybe(probability: float) -> bool:
    """
    Returns True with the specified probability.

    Example:
        maybe(0.05)
        -> Approximately 5% of the time
    """
    return random.random() < probability


# -------------------------------------------------------
# Geography Helpers
# -------------------------------------------------------

def get_city_state(misspell=False):
    """
    Returns a realistic Indian city-state pair.

    Example:
        ("Mumbai", "Maharashtra")
    """

    city = random.choice(list(CITY_STATE_MAP.keys()))
    state = CITY_STATE_MAP[city]

    if misspell and city in CITY_MISSPELLINGS:
        city = CITY_MISSPELLINGS[city]

    return city, state


# -------------------------------------------------------
# Date Helpers
# -------------------------------------------------------

def random_customer_since():
    """
    Random date in the past 15 years.
    """

    return fake.date_between(
        start_date="-15y",
        end_date="today"
    )


def future_customer_since():
    """
    Random future date (used intentionally for dirty data).
    """

    return fake.date_between(
        start_date="+1d",
        end_date="+365d"
    )


def random_account_open_date():
    """
    Random account opening date within the past 15 years.
    """

    return fake.date_between(
        start_date="-15y",
        end_date="today"
    )


def random_transaction_datetime():
    """
    Random transaction timestamp within the past 5 years.
    """

    return fake.date_time_between(
        start_date="-5y",
        end_date="now"
    )


# -------------------------------------------------------
# Number Generators
# -------------------------------------------------------

def generate_account_number():
    """
    Generates a realistic 12-digit account number.
    """

    return str(random.randint(10**11, (10**12) - 1))


def generate_card_number():
    """
    Generates a realistic 16-digit card number.
    """

    return str(random.randint(10**15, (10**16) - 1))


def generate_transaction_reference():
    """
    Example:
    TXN834729104823
    """

    return (
        "TXN"
        + str(random.randint(100000000000, 999999999999))
    )


# -------------------------------------------------------
# Financial Helpers
# -------------------------------------------------------

def random_balance():
    """
    Returns a realistic bank balance.
    """

    return round(random.uniform(0, 5_000_000), 2)


def random_transaction_amount():
    """
    Returns a transaction amount.
    """

    return round(random.uniform(10, 250_000), 2)


INCOME_RANGES = {

    "Student": (0, 300000),
    "Farmer": (200000, 800000),
    "Teacher": (400000, 1200000),
    "Professor": (800000, 2200000),
    "Software Engineer": (800000, 3500000),
    "Doctor": (1000000, 6000000),
    "Lawyer": (700000, 5000000),
    "Business Owner": (1000000, 20000000),
    "Bank Manager": (1200000, 3000000),
    "Government Employee": (500000, 1800000),
    "Nurse": (300000, 900000),
    "Sales Executive": (300000, 1500000),
    "Marketing Manager": (700000, 2500000),
    "Civil Engineer": (600000, 2200000),
    "Mechanical Engineer": (600000, 2200000),
    "Consultant": (1000000, 5000000),
    "Architect": (700000, 2500000),
    "Police Officer": (500000, 1500000),
    "Retired": (150000, 1000000),
    "Accountant": (500000, 1800000)
}


def random_income(occupation):

    low, high = INCOME_RANGES.get(
        occupation,
        (300000, 1000000)
    )

    return round(
        random.uniform(low, high),
        2
    )