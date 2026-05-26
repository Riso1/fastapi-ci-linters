SELECT DISTINCT o.battle
FROM Outcomes o
JOIN Ships s ON o.ship = s.name
WHERE s.class = 'Kongo'
