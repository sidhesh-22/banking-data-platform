{% snapshot accounts_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='account_id',

        strategy='check',

        check_cols=[
            'account_status',
            'current_balance',
            'available_balance',
            'loan_amount',
            'outstanding_loan',
            'interest_rate',
            'last_activity_date'
        ]
    )
}}

select *
from {{ ref('stg_accounts') }}

{% endsnapshot %}