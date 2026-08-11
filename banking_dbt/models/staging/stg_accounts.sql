{{ config(materialized='view') }}

with cleaned as (

    select

        account_id,
        customer_id,

        trim(account_number) as account_number,

        initcap(trim(account_type)) as account_type,

        upper(trim(account_status)) as account_status,

        greatest(current_balance,0) as current_balance,

        greatest(available_balance,0) as available_balance,

        initcap(trim(branch_name)) as branch_name,

        initcap(trim(branch_city)) as branch_city,

        upper(trim(branch_state)) as branch_state,

        initcap(trim(loan_type)) as loan_type,

        case
            when loan_amount < 0 then 0
            else loan_amount
        end as loan_amount,

        case
            when outstanding_loan < 0 then 0
            else outstanding_loan
        end as outstanding_loan,

        least(greatest(interest_rate,0),50) as interest_rate,

        dateadd(
            day,
            account_open_date,
            date '1970-01-01'
        ) as account_open_date,

        dateadd(
            day,
            last_activity_date,
            date '1970-01-01'
        ) as last_activity_date,

        dateadd(
            microsecond,
            created_at,
            '1970-01-01'::timestamp_ntz
        ) as created_at,

        load_timestamp

    from {{ source('raw','accounts') }}

),

enriched as (

    select

        *,

        current_balance > 100000
            as high_balance_flag,

        loan_amount > 0
            as has_loan,

        datediff(
            day,
            last_activity_date,
            current_date()
        ) as days_since_last_activity

    from cleaned

),

ranked as (

    select

        *,

        row_number() over (

            partition by account_id

            order by load_timestamp desc

        ) as rn

    from enriched

)

select

    account_id,
    customer_id,
    account_number,
    account_type,
    account_status,
    current_balance,
    available_balance,
    branch_name,
    branch_city,
    branch_state,
    loan_type,
    loan_amount,
    outstanding_loan,
    interest_rate,
    account_open_date,
    last_activity_date,
    created_at,
    load_timestamp,

    high_balance_flag,
    has_loan,
    days_since_last_activity

from ranked

where rn = 1
