{{ config(materialized='table') }}

with transaction_base as (

    select

        transaction_id,

        transaction_reference,

        account_id,

        merchant_id,

        transaction_timestamp,

        transaction_date,

        amount,

        transaction_type,

        payment_channel,

        transaction_status,

        device_type,

        high_value_transaction

    from {{ ref('stg_transactions') }}

),

account_lookup as (

    select

        t.*,

        a.account_key,

        a.customer_id

    from transaction_base t

    left join {{ ref('dim_accounts') }} a
        on t.account_id = a.account_id
        and a.is_current = true

),

customer_lookup as (

    select

        a.*,

        c.customer_key

    from account_lookup a

    left join {{ ref('dim_customers') }} c
         on a.customer_id = c.customer_id
         and c.is_current = true

),

merchant_lookup as (

    select

        c.*,

        m.merchant_key

    from customer_lookup c

    left join {{ ref('dim_merchants') }} m

        on c.merchant_id = m.merchant_id

),

date_lookup as (

    select

        m.*,

        d.date_key

    from merchant_lookup m

    left join {{ ref('dim_date') }} d

        on cast(m.transaction_date as date)=d.full_date

)

select

    -------------------------------------------------
    -- Degenerate Dimension
    -------------------------------------------------

    transaction_id,

    transaction_reference,

    -------------------------------------------------
    -- Foreign Keys
    -------------------------------------------------

    date_key,

    customer_key,

    account_key,

    merchant_key,

    -------------------------------------------------
    -- Measures
    -------------------------------------------------

    amount,

    -------------------------------------------------
    -- Transaction Attributes
    -------------------------------------------------

    transaction_timestamp,

    transaction_type,

    payment_channel,

    transaction_status,

    device_type,

    high_value_transaction

from date_lookup
