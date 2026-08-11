{{ config(materialized='view') }}

with cleaned as (

    select

        transaction_id,

        account_id,

        merchant_id,

        trim(transaction_reference) as transaction_reference,

        timestampadd(
            microsecond,
            transaction_timestamp,
            to_timestamp_ntz('1970-01-01')
        ) as transaction_timestamp,

        case
            when amount <= 0 then null
            else amount
        end as amount,

        upper(trim(transaction_type)) as transaction_type,

        upper(trim(payment_channel)) as payment_channel,

        upper(trim(transaction_status)) as transaction_status,

        upper(trim(device_type)) as device_type,

        initcap(trim(city)) as city,

        timestampadd(
            microsecond,
            created_at,
            to_timestamp_ntz('1970-01-01')
        ) as created_at,

        load_timestamp

    from {{ source('raw', 'transactions') }}

),

enriched as (

    select

        *,

        case
            when amount >= 10000 then true
            else false
        end as high_value_transaction,

        case
            when dayofweek(transaction_timestamp) in (1,7)
            then true
            else false
        end as is_weekend_transaction,

        hour(transaction_timestamp) as transaction_hour,

        case
            when hour(transaction_timestamp) between 6 and 11
                then 'Morning'

            when hour(transaction_timestamp) between 12 and 16
                then 'Afternoon'

            when hour(transaction_timestamp) between 17 and 21
                then 'Evening'

            else 'Night'

        end as transaction_time_of_day,

        date(transaction_timestamp) as transaction_date,

        month(transaction_timestamp) as transaction_month,

        quarter(transaction_timestamp) as transaction_quarter,

        year(transaction_timestamp) as transaction_year

    from cleaned

),

ranked as (

    select

        *,

        row_number() over (

            partition by transaction_id

            order by load_timestamp desc

        ) as rn

    from enriched

)

select

    transaction_id,

    account_id,

    merchant_id,

    transaction_reference,

    transaction_timestamp,

    transaction_date,

    transaction_year,

    transaction_quarter,

    transaction_month,

    transaction_hour,

    transaction_time_of_day,

    amount,

    high_value_transaction,

    transaction_type,

    payment_channel,

    transaction_status,

    device_type,

    city,

    is_weekend_transaction,

    created_at,

    load_timestamp

from ranked

where rn = 1