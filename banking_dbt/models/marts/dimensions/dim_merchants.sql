{{ config(materialized='table') }}

with merchants as (

    select

        row_number() over (
            order by merchant_id
        ) as merchant_key,

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

    from {{ ref('stg_merchants') }}

)

select *

from merchants