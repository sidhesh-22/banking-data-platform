{{ config(materialized='table') }}

with customer_versions as (

    select

        row_number() over (
            order by customer_id, dbt_valid_from
        ) as customer_key,

        customer_id,

        first_name,

        last_name,

        concat(
            first_name,
            ' ',
            last_name
        ) as customer_name,

        date_of_birth,

        gender,

        email,

        phone_number,

        marital_status,

        occupation,

        annual_income,

        employment_type,

        city,

        state,

        customer_since,

        kyc_status,

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

    from {{ ref('customers_snapshot') }}

)

select *

from customer_versions