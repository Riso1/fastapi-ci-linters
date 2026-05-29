SELECT
    AVG(ag.grade) AS avg_grade
FROM assignments a
JOIN assignments_grades ag
    ON a.assisgnment_id = ag.assisgnment_id
WHERE a.assignment_text LIKE '%прочитать%'
   OR a.assignment_text LIKE '%выучить%';