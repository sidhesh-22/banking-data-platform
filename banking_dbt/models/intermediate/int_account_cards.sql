{{ config(materialized='view') }}

select

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

    c.employment_type,

    c.city as customer_city,

    c.state as customer_state,

    c.customer_since,

    c.customer_tenure,

    c.kyc_status,

    -------------------------------------------------
    -- Account
    -------------------------------------------------

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

    -------------------------------------------------
    -- Card
    -------------------------------------------------

    cd.card_id,

    cd.card_number,

    cd.card_type,

    cd.network,

    cd.issue_date,

    cd.expiry_date,

    cd.card_status,

    cd.contactless_enabled,

    cd.is_expired,

    cd.card_age,

    -------------------------------------------------
    -- Audit
    -------------------------------------------------

    greatest(
        c.created_at,
        a.created_at,
        cd.created_at
    ) as created_at,

    current_timestamp() as load_timestamp

from {{ ref('stg_cards') }} cd

left join {{ ref('stg_accounts') }} a

    on cd.account_id = a.account_id

left join {{ ref('stg_customers') }} c

    on a.customer_id = c.customer_id