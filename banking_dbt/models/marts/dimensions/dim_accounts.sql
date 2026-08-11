{{ config(materialized='table') }}

with account_versions as (

    select

        row_number() over (
            order by account_id, dbt_valid_from
        ) as account_key,

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

        dbt_scd_id,

        dbt_updated_at,

        dbt_valid_from,

        dbt_valid_to,

        case
            when dbt_valid_to is null
            then true
            else false
        end as is_current,

        cast(dbt_valid_from as date) as effective_date,

        cast(dbt_valid_to as date) as expiration_date

    from {{ ref('accounts_snapshot') }}

)

select *

from account_versions
