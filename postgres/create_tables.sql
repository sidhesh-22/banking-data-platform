-- Creating the required tables:

-- 1) customers --

CREATE TABLE customers (

    customer_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),
    email VARCHAR(120) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    marital_status VARCHAR(20),
    occupation VARCHAR(80),
    annual_income NUMERIC(12,2) CHECK (annual_income >= 0),
    employment_type VARCHAR(30),
    city VARCHAR(80) NOT NULL,
    state VARCHAR(80) NOT NULL,
    customer_since DATE NOT NULL,
    kyc_status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2) accounts ---

CREATE TABLE accounts (

    account_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_type VARCHAR(30),
    account_status VARCHAR(20),
    current_balance NUMERIC(15,2) NOT NULL CHECK (current_balance >= 0),
    available_balance NUMERIC(15,2) NOT NULL CHECK (available_balance >= 0),
    branch_name VARCHAR(120),
    branch_city VARCHAR(80),
    branch_state VARCHAR(80),
    loan_type VARCHAR(40),
    loan_amount NUMERIC(15,2) CHECK (loan_amount >= 0),
    outstanding_loan NUMERIC(15,2) CHECK (outstanding_loan >= 0),
    interest_rate NUMERIC(5,2) CHECK (interest_rate BETWEEN 0 AND 30),
    account_open_date DATE NOT NULL,
    last_activity_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_accounts_customer
    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)
);

-- 3) transactions --

CREATE TABLE transactions (

    transaction_id BIGSERIAL PRIMARY KEY,
    account_id BIGINT NOT NULL,
    merchant_id BIGINT NOT NULL,
    transaction_reference VARCHAR(50) UNIQUE NOT NULL,
    transaction_timestamp TIMESTAMP NOT NULL,
    amount NUMERIC(15,2) NOT NULL CHECK (amount > 0),
    transaction_type VARCHAR(30),
    payment_channel VARCHAR(30),
    transaction_status VARCHAR(20),
    device_type VARCHAR(30),
    city VARCHAR(80),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transactions_account
    FOREIGN KEY(account_id)
    REFERENCES accounts(account_id),

    CONSTRAINT fk_transactions_merchant
    FOREIGN KEY(merchant_id)
    REFERENCES merchants(merchant_id)
);

-- 4) merchants --

CREATE TABLE merchants (

    merchant_id BIGSERIAL PRIMARY KEY,
    merchant_name VARCHAR(120) NOT NULL,
    merchant_category VARCHAR(60) NOT NULL,
    city VARCHAR(80),
    state VARCHAR(80),
    merchant_rating NUMERIC(2,1),
    is_online BOOLEAN DEFAULT FALSE,
    established_year SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5) cards --

CREATE TABLE cards (

    card_id BIGSERIAL PRIMARY KEY,
    account_id BIGINT NOT NULL,
    card_number VARCHAR(19) UNIQUE NOT NULL,
    card_type VARCHAR(20),
    network VARCHAR(20),
	issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    card_status VARCHAR(20),
    contactless_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cards_account
    FOREIGN KEY(account_id)
    REFERENCES accounts(account_id)
);