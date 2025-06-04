-- models/marts/dim_products.sql

with products as (
    select * from {{ ref('stg_products') }}
),

aisles as (
    select * from {{ ref('stg_aisles') }}
),

departments as (
    select * from {{ ref('stg_departments') }}
)

select
    p.product_id,
    p.product_name,
    a.aisle_name,
    d.department_name
from products p
left join aisles a on p.aisle_id = a.aisle_id
left join departments d on p.department_id = d.department_id
