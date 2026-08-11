{{ config(materialized='table') }}

with card_versions as (

    select

        row_number() over (
            order by card_id, dbt_valid_from
        ) as card_key,

        card_id,

        account_id,

        card_number,

        card_type,

        network,

        issue_date,

        expiry_date,

        card_status,

        contactless_enabled,

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

    from {{ ref('cards_snapshot') }}

)

select *

from card_versions
