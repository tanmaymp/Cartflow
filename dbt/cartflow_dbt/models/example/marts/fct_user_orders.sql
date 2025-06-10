-- models/marts/fct_user_orders.sql

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_products_prior as (
    select * from {{ ref('stg_order_products_prior') }}
),

user_order_summary as (
    select
        o.user_id,
        o.order_id,
        o.order_number,
        o.order_dow,
        o.order_hour_of_day,
        o.days_since_prior_order,
        count(op.product_id) as num_products,
        sum(case when op.reordered = true then 1 else 0 end) as num_reordered
    from orders o
    left join order_products_prior op on o.order_id = op.order_id
    group by o.user_id, o.order_id, o.order_number, o.order_dow, o.order_hour_of_day, o.days_since_prior_order
)

select * from user_order_summary
