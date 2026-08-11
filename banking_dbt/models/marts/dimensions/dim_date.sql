{{ config(materialized='table') }}

with date_range as (

    select

        min(transaction_date) as start_date,

        max(transaction_date) as end_date

    from {{ ref('stg_transactions') }}

),

calendar as (

    select

        dateadd(
            day,
            seq4(),
            start_date
        ) as full_date,

        end_date

    from date_range,
         table(generator(rowcount => 10000))

),

dates as (

    select *

    from calendar

    where full_date <= end_date

)

select

    -------------------------------------------------
    -- Surrogate Key
    -------------------------------------------------

    to_number(
        to_char(full_date, 'YYYYMMDD')
    ) as date_key,

    -------------------------------------------------
    -- Date
    -------------------------------------------------

    full_date,

    -------------------------------------------------
    -- Day
    -------------------------------------------------

    day(full_date) as day_of_month,

    dayofweek(full_date) as day_of_week,

    dayname(full_date) as day_name,

    dayofyear(full_date) as day_of_year,

    -------------------------------------------------
    -- Week
    -------------------------------------------------

    week(full_date) as week_of_year,

    -------------------------------------------------
    -- Month
    -------------------------------------------------

    month(full_date) as month_number,

    monthname(full_date) as month_name,

    to_char(full_date, 'Mon YYYY') as month_year,

    (year(full_date) * 100 + month(full_date)) as month_year_sort,

    -------------------------------------------------
    -- Quarter
    -------------------------------------------------

    quarter(full_date) as quarter,

    -------------------------------------------------
    -- Year
    -------------------------------------------------

    year(full_date) as year,

    -------------------------------------------------
    -- Flags
    -------------------------------------------------

    case

        when dayofweek(full_date) in (1,7)

        then true

        else false

    end as is_weekend,

    case

        when month(full_date) in (4,5,6)

        then 'Q1'

        when month(full_date) in (7,8,9)

        then 'Q2'

        when month(full_date) in (10,11,12)

        then 'Q3'

        else 'Q4'

    end as financial_quarter,

    case

        when month(full_date) between 4 and 6 then 'Spring'

        when month(full_date) between 7 and 9 then 'Monsoon'

        when month(full_date) between 10 and 11 then 'Autumn'

        else 'Winter'

    end as season

from calendar

order by full_date
