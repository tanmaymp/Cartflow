with source as (
    select * from {{ source('public', 'aisles') }}
),

renamed as (
    select
        aisle_id,
        aisle as aisle_name,
        lower(trim(aisle)) as aisle_name_clean
    from source
)

select * from renamed
