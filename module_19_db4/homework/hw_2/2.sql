SELECT
    s.full_name,
    AVG(ag.grade) AS avg_grade
FROM students s
JOIN assignments_grades ag
    ON s.student_id = ag.student_id
GROUP BY s.student_id, s.full_name
ORDER BY avg_grade DESC
LIMIT 10;