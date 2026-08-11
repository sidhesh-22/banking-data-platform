{{ config(materialized='view') }}

with cleaned as (

    select

        customer_id,

        initcap(trim(first_name)) as first_name,

        initcap(trim(last_name)) as last_name,

        dateadd(
            day,
            date_of_birth,
            date '1970-01-01'
        ) as date_of_birth,

        upper(trim(gender)) as gender,

        lower(trim(email)) as email,

        regexp_replace(
            phone_number,
            '[^0-9]',
            ''
        ) as phone_number,

        initcap(trim(marital_status)) as marital_status,

        coalesce(
            trim(occupation),
            'Unknown'
        ) as occupation,

        case
            when annual_income < 0 then null
            else annual_income
        end as annual_income,

        initcap(trim(employment_type)) as employment_type,

        initcap(trim(city)) as city,

        upper(trim(state)) as state,

        dateadd(
            day,
            customer_since,
            date '1970-01-01'
        ) as customer_since,

        upper(trim(kyc_status)) as kyc_status,

        dateadd(
            microsecond,
            created_at,
            '1970-01-01'::timestamp_ntz
        ) as created_at,

        load_timestamp

    from {{ source('raw','customers') }}

),

enriched as (

    select

        *,

        datediff(
            year,
            date_of_birth,
            current_date()
        ) as age,

        case
            when datediff(year,date_of_birth,current_date()) < 25
                then '18-24'

            when datediff(year,date_of_birth,current_date()) < 40
                then '25-39'

            when datediff(year,date_of_birth,current_date()) < 60
                then '40-59'

            else '60+'

        end as age_group,

        datediff(
            year,
            customer_since,
            current_date()
        ) as customer_tenure

    from cleaned

),

ranked as (

    select

        *,

        row_number() over (

            partition by customer_id

            order by 
            load_timestamp desc

        ) as rn

    from enriched

)

select

    customer_id,
    first_name,
    last_name,
    date_of_birth,
    age,
    age_group,
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
    customer_tenure,
    kyc_status,
    created_at,
    load_timestamp

from ranked

where rn = 1