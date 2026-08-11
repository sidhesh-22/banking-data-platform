{{ config(materialized='view') }}

with cleaned as (

    select

        merchant_id,

        initcap(trim(merchant_name)) as merchant_name,

        initcap(trim(merchant_category)) as merchant_category,

        initcap(trim(city)) as city,

        upper(trim(state)) as state,

        least(
            greatest(merchant_rating, 0),
            5
        ) as merchant_rating,

        is_online,

        established_year,

        timestampadd(
            microsecond,
            created_at,
            to_timestamp_ntz('1970-01-01')
        ) as created_at,

        load_timestamp

    from {{ source('raw', 'merchants') }}

),

enriched as (

    select

        *,

        case
            when merchant_rating >= 4.5 then 'Excellent'
            when merchant_rating >= 4.0 then 'Good'
            when merchant_rating >= 3.0 then 'Average'
            else 'Poor'
        end as merchant_rating_category,

        case
            when is_online then 'Online'
            else 'Offline'
        end as merchant_channel

    from cleaned

),

ranked as (

    select

        *,

        row_number() over (

            partition by merchant_id

            order by load_timestamp desc

        ) as rn

    from enriched

)

select

    merchant_id,

    merchant_name,

    merchant_category,

    city,

    state,

    merchant_rating,

    merchant_rating_category,

    merchant_channel,

    is_online,

    established_year,

    created_at,

    load_timestamp

from ranked

where rn = 1