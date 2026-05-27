SELECT DISTINCT Product.maker, Laptop.speed
FROM Product
JOIN Laptop ON Product.model = Laptop.model
WHERE Laptop.hd >= 10
