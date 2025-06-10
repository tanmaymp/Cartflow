with source as (
    select * from {{ source('public', 'order_products_train') }}
),

renamed as (
    select
        order_id,
        product_id,
        add_to_cart_order,
        case when reordered = 1 then true else false end as reordered
    from source
)

select * from renamed
