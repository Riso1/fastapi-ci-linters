select
    c1.full_name as customer_1,
    c2.full_name as customer_2
from customer as c1
join customer as c2
    on c1.city = c2.city
    and c1.manager_id = c2.manager_id
    and c1.customer_id < c2.customer_id;
