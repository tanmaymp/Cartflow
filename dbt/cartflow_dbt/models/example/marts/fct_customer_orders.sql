with orders as (
    select * from {{ ref('stg_orders') }}
),

agg as (
    select
        user_id,
        count(order_id) as total_orders,
        avg(days_since_prior_order) as avg_days_between_orders,
        max(order_number) as max_order_number
    from orders
    where order_type = 'Previous Order'
    group by user_id
)

select * from agg
