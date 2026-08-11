{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',

        strategy='check',

        check_cols=[
            'email',
            'phone_number',
            'marital_status',
            'occupation',
            'annual_income',
            'employment_type',
            'city',
            'state',
            'kyc_status'
        ]
    )
}}

select *
from {{ ref('stg_customers') }}

{% endsnapshot %}