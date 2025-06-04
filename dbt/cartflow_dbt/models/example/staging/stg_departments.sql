with source as (
    select * from {{ source('public', 'departments') }}
),

renamed as (
    select
        department_id,
        department as department_name,
        lower(trim(department)) as department_name_clean
    from source
)

select * from renamed
