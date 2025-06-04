with source as (
    select * from {{ source('public', 'orders') }}
),

renamed as (
    select
        order_id,
        user_id,
        case
            when eval_set = 'prior' then 'Previous Order'
            when eval_set = 'train' then 'Training Order'
            when eval_set = 'test' then 'Test Order'
            else 'Unknown'
        end as order_type,
        order_number,
        order_dow,
        order_hour_of_day,
        order_dow || '-' || order_hour_of_day as order_time_slot,
        cast(order_number as integer) as order_sequence,
        days_since_prior_order::int as days_since_prior_order
    from source
)

select * from renamed
