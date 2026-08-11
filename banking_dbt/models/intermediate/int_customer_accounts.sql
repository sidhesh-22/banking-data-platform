{{ config(materialized='view') }}

select

    a.account_id,

    a.account_number,

    a.account_type,

    a.account_status,

    a.current_balance,

    a.available_balance,

    a.high_balance_flag,

    a.has_loan,

    a.loan_type,

    a.loan_amount,

    a.outstanding_loan,

    a.interest_rate,

    a.account_open_date,

    a.last_activity_date,

    a.days_since_last_activity,

    a.branch_name,

    a.branch_city,

    a.branch_state,

    c.customer_id,

    c.first_name,

    c.last_name,

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

    c.employment_type,

    c.city,

    c.state,

    c.customer_since,

    c.customer_tenure,

    c.kyc_status

from {{ ref('stg_accounts') }} a

left join {{ ref('stg_customers') }} c

on a.customer_id = c.customer_id