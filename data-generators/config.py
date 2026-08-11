from faker import Faker

# Indian locale
fake = Faker("en_IN")

# -----------------------------
# Record Counts
# -----------------------------

NUM_CUSTOMERS = 103_487
NUM_MERCHANTS = 8_731
NUM_ACCOUNTS = 214_263
NUM_CARDS = 147_892
NUM_TRANSACTIONS = 250_000

# -----------------------------
# Batch Size
# -----------------------------

BATCH_SIZE = 5000

# -----------------------------
# Data Quality Issues
# -----------------------------

INVALID_EMAIL_PERCENT = 3
MISSING_PHONE_PERCENT = 5
NULL_OCCUPATION_PERCENT = 2
FUTURE_DATE_PERCENT = 1
MISSPELT_CITY_PERCENT = 1
DUPLICATE_MERCHANT_PERCENT = 2

# -----------------------------
# Business Limits
# -----------------------------

MAX_BALANCE = 5_000_000
MAX_TRANSACTION_AMOUNT = 250_000
MAX_LOAN_AMOUNT = 2_500_000
