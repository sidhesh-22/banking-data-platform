{% snapshot cards_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='card_id',

        strategy='check',

        check_cols=[
            'card_status',
            'expiry_date',
            'contactless_enabled'
        ]
    )
}}

select *
from {{ ref('stg_cards') }}

{% endsnapshot %}