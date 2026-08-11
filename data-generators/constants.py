"""
constants.py

Contains all static values used throughout the project.
"""

# ----------------------------------------
# Indian Cities & States
# ----------------------------------------

CITY_STATE_MAP = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Nagpur": "Maharashtra",

    "Delhi": "Delhi",

    "Bengaluru": "Karnataka",
    "Mysuru": "Karnataka",
    "Mangalore": "Karnataka",

    "Chennai": "Tamil Nadu",
    "Coimbatore": "Tamil Nadu",
    "Madurai": "Tamil Nadu",

    "Hyderabad": "Telangana",
    "Warangal": "Telangana",

    "Ahmedabad": "Gujarat",
    "Surat": "Gujarat",
    "Vadodara": "Gujarat",

    "Jaipur": "Rajasthan",
    "Udaipur": "Rajasthan",

    "Lucknow": "Uttar Pradesh",
    "Kanpur": "Uttar Pradesh",
    "Noida": "Uttar Pradesh",

    "Kolkata": "West Bengal",
    "Howrah": "West Bengal",

    "Bhopal": "Madhya Pradesh",
    "Indore": "Madhya Pradesh",

    "Patna": "Bihar",

    "Bhubaneswar": "Odisha",

    "Kochi": "Kerala",
    "Thiruvananthapuram": "Kerala",

    "Chandigarh": "Chandigarh",

    "Guwahati": "Assam",

    "Ranchi": "Jharkhand"
}

# ----------------------------------------
# Intentional Misspellings
# ----------------------------------------

CITY_MISSPELLINGS = {
    "Mumbai": "Mumbi",
    "Pune": "Punne",
    "Delhi": "Delhii",
    "Bengaluru": "Bangalore",
    "Chennai": "Chenai",
    "Hyderabad": "Hydrabad",
    "Ahmedabad": "Ahemdabad",
    "Lucknow": "Lucknoww",
    "Kolkata": "Kolkatta",
    "Jaipur": "Jaypur"
}

# ----------------------------------------
# Customer Attributes
# ----------------------------------------

GENDERS = [
    "Male",
    "Female",
    "Other"
]

MARITAL_STATUS = [
    "Single",
    "Married",
    "Divorced",
    "Widowed"
]

OCCUPATIONS = [
    "Software Engineer",
    "Doctor",
    "Teacher",
    "Lawyer",
    "Accountant",
    "Business Owner",
    "Bank Manager",
    "Government Employee",
    "Nurse",
    "Sales Executive",
    "Marketing Manager",
    "Civil Engineer",
    "Mechanical Engineer",
    "Student",
    "Retired",
    "Farmer",
    "Consultant",
    "Architect",
    "Professor",
    "Police Officer"
]

EMPLOYMENT_TYPES = [
    "Full-Time",
    "Part-Time",
    "Self-Employed",
    "Business",
    "Retired",
    "Student",
    "Unemployed"
]

KYC_STATUS = [
    "Verified",
    "Pending",
    "Rejected"
]

# ----------------------------------------
# Accounts
# ----------------------------------------

ACCOUNT_TYPES = [
    "Savings",
    "Current",
    "Salary",
    "Fixed Deposit"
]

ACCOUNT_STATUS = [
    "Active",
    "Dormant",
    "Closed",
    "Frozen"
]

LOAN_TYPES = [
    None,
    "Home",
    "Car",
    "Education",
    "Personal",
    "Business"
]

# ----------------------------------------
# Cards
# ----------------------------------------

CARD_TYPES = [
    "Debit",
    "Credit"
]

CARD_NETWORKS = [
    "Visa",
    "Mastercard",
    "RuPay",
    "American Express"
]

CARD_STATUS = [
    "Active",
    "Blocked",
    "Expired"
]

# ----------------------------------------
# Merchants
# ----------------------------------------

MERCHANT_CATEGORIES = [
    "Restaurant",
    "Supermarket",
    "Fuel",
    "Hospital",
    "Pharmacy",
    "Electronics",
    "Fashion",
    "Travel",
    "Hotel",
    "Entertainment",
    "Education",
    "Healthcare",
    "Groceries",
    "Furniture",
    "Jewellery",
    "Insurance",
    "Telecom",
    "Utilities",
    "E-Commerce",
    "Food Delivery"
]

# ----------------------------------------
# Transactions
# ----------------------------------------

TRANSACTION_TYPES = [
    "Purchase",
    "Transfer",
    "Withdrawal",
    "Deposit",
    "Bill Payment",
    "Refund"
]

PAYMENT_CHANNELS = [
    "ATM",
    "POS",
    "Mobile Banking",
    "Internet Banking",
    "UPI",
    "Card"
]

TRANSACTION_STATUS = [
    "Success",
    "Failed",
    "Pending",
    "Reversed"
]

DEVICE_TYPES = [
    "Android",
    "iPhone",
    "Windows",
    "Mac",
    "ATM",
    "POS Terminal"
]