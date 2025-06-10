with source as (
    select * from {{ source('public', 'products') }}
),

renamed as (
    select
        product_id,
        product_name,
        aisle_id,
        department_id,
        lower(trim(product_name)) as product_name_clean
    from source
)

select * from renamed
