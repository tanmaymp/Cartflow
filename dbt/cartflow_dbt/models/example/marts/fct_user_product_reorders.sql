with order_products_prior as (
    select * from {{ ref('stg_order_products_prior') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

joined as (
    select
        o.user_id,
        opp.product_id,
        count(*) as total_orders,
        sum(case when opp.reordered = true then 1 else 0 end) as times_reordered
    from order_products_prior opp
    join orders o on opp.order_id = o.order_id
    group by o.user_id, opp.product_id
)

select * from joined
