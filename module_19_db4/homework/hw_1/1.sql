SELECT
    t.full_name,
    AVG(ag.grade) AS avg_grade
FROM teachers t
JOIN assignments a
    ON t.teacher_id = a.teacher_id
JOIN assignments_grades ag
    ON a.assisgnment_id = ag.assisgnment_id
GROUP BY t.teacher_id, t.full_name
ORDER BY avg_grade ASC
LIMIT 1;