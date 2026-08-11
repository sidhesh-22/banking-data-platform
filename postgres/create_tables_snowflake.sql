-- Creating the required tables in Snowflake without constraints:

-- 1) customers --

CREATE TABLE customers (

    customer_id NUMBER,
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    date_of_birth DATE,
    gender VARCHAR(20),
    email VARCHAR(120),
    phone_number VARCHAR(20),
    marital_status VARCHAR(20),
    occupation VARCHAR(80),
    annual_income NUMERIC(12,2),
    employment_type VARCHAR(30),
    city VARCHAR(80),
    state VARCHAR(80),
    customer_since DATE,
    kyc_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2) accounts ---

CREATE TABLE accounts (

    account_id NUMBER,
    customer_id NUMBER,
    account_number VARCHAR(20),
    account_type VARCHAR(30),
    account_status VARCHAR(20),
    current_balance NUMERIC(15,2),
    available_balance NUMERIC(15,2),
    branch_name VARCHAR(120),
    branch_city VARCHAR(80),
    branch_state VARCHAR(80),
    loan_type VARCHAR(40),
    loan_amount NUMERIC(15,2),
    outstanding_loan NUMERIC(15,2),
    interest_rate NUMERIC(5,2),
    account_open_date DATE,
    last_activity_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3) merchants --

CREATE TABLE merchants (

    merchant_id NUMBER,
    merchant_name VARCHAR(120),
    merchant_category VARCHAR(60),
    city VARCHAR(80),
    state VARCHAR(80),
    merchant_rating NUMERIC(2,1),
    is_online BOOLEAN DEFAULT FALSE,
    established_year SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4) transactions --

CREATE TABLE transactions (

    transaction_id NUMBER,
    account_id NUMBER,
    merchant_id NUMBER,
    transaction_reference VARCHAR(50),
    transaction_timestamp TIMESTAMP,
    amount NUMERIC(15,2),
    transaction_type VARCHAR(30),
    payment_channel VARCHAR(30),
    transaction_status VARCHAR(20),
    device_type VARCHAR(30),
    city VARCHAR(80),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP


);

-- 5) cards --

CREATE TABLE cards (

    card_id NUMBER,
    account_id NUMBER,
    card_number VARCHAR(19),
    card_type VARCHAR(20),
    network VARCHAR(20),
    issue_date DATE,
    expiry_date DATE,
    card_status VARCHAR(20),
    contactless_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);