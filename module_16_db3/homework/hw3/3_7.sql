SELECT PC.model, PC.price
FROM Product
JOIN PC ON Product.model = PC.model
WHERE Product.maker = 'B'

UNION

SELECT Laptop.model, Laptop.price
FROM Product
JOIN Laptop ON Product.model = Laptop.model
WHERE Product.maker = 'B'

UNION

SELECT Printer.model, Printer.price
FROM Product
JOIN Printer ON Product.model = Printer.model
WHERE Product.maker = 'B';