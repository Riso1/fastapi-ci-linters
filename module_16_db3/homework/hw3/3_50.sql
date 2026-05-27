SELECT DISTINCT o.battle
FROM Outcomes o
JOIN Ships s ON o.ship = s.name
WHERE s.class = 'Kongo'

UNION

SELECT DISTINCT o.battle
FROM Outcomes o
WHERE o.ship = 'Kongo';