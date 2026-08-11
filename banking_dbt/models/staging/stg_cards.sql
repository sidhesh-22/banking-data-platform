{{ config(materialized='view') }}

with cleaned as (

    select

        card_id,

        account_id,

        trim(card_number) as card_number,

        initcap(trim(card_type)) as card_type,

        upper(trim(network)) as network,

        dateadd(
            day,
            issue_date,
            date '1970-01-01'
        ) as issue_date,

        dateadd(
            day,
            expiry_date,
            date '1970-01-01'
        ) as expiry_date,

        upper(trim(card_status)) as card_status,

        contactless_enabled,

        dateadd(
            microsecond,
            created_at,
            '1970-01-01'::timestamp_ntz
        ) as created_at,

        load_timestamp

    from {{ source('raw', 'cards') }}

),

enriched as (

    select

        *,

        case
            when expiry_date < current_date()
            then true
            else false
        end as is_expired,

        datediff(
            year,
            issue_date,
            current_date()
        ) as card_age
    from cleaned

),

ranked as (

    select

        *,

        row_number() over (

            partition by card_id

            order by 
            load_timestamp desc

        ) as rn

    from enriched

)

select

    card_id,

    account_id,

    card_number,

    card_type,

    network,

    issue_date,

    expiry_date,

    card_status,

    contactless_enabled,

    is_expired,

    card_age,

    created_at,

    load_timestamp

from ranked

where rn = 1
