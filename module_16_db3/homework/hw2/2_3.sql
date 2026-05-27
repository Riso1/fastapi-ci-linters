select
    "order".order_no,
    manager.full_name as manager_name,
    customer.full_name as customer_name
from "order"
join customer
    on "order".customer_id = customer.customer_id
join manager
    on "order".manager_id = manager.manager_id
where customer.city <> manager.city;
