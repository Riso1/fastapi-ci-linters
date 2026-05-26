select
    customer.full_name
from customer
left join "order"
    on customer.customer_id = "order".customer_id
where "order".order_no is null;
