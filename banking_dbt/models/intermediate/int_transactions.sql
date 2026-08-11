{{ config(materialized='view') }}

select

    t.transaction_id,

    t.transaction_timestamp,

    t.transaction_date,

    t.transaction_year,

    t.transaction_quarter,

    t.transaction_month,

    t.transaction_hour,

    t.transaction_time_of_day,

    t.amount,

    t.high_value_transaction,

    t.transaction_type,

    t.payment_channel,

    t.transaction_status,

    t.device_type,

    t.city as transaction_city,

    -------------------------------------------------
    -- Account
    -------------------------------------------------

    a.account_id,

    a.account_number,

    a.account_type,

    a.account_status,

    a.current_balance,

    a.available_balance,

    a.has_loan,

    a.loan_type,

    a.loan_amount,

    a.branch_name,

    a.branch_city,

    a.branch_state,

    -------------------------------------------------
    -- Customer
    -------------------------------------------------

    c.customer_id,

    concat(
        c.first_name,
        ' ',
        c.last_name
    ) as customer_name,

    c.gender,

    c.age,

    c.age_group,

    c.annual_income,

    c.occupation,

    c.city as customer_city,

    c.state,

    c.kyc_status,

    -------------------------------------------------
    -- Merchant
    -------------------------------------------------

    m.merchant_id,

    m.merchant_name,

    m.merchant_category,

    m.merchant_rating,

    m.merchant_rating_category,

    m.merchant_channel

from {{ ref('stg_transactions') }} t

left join {{ ref('stg_accounts') }} a

on t.account_id = a.account_id

left join {{ ref('stg_customers') }} c

on a.customer_id = c.customer_id

left join {{ ref('stg_merchants') }} m

on t.merchant_id = m.merchant_id
