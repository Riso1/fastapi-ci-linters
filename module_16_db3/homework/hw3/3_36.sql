SELECT s.name
FROM Ships s
JOIN Classes c ON s.name = c.class

UNION

SELECT o.ship
FROM Outcomes o
JOIN Classes c ON o.ship = c.class;