SELECT
    s.full_name
FROM students s
WHERE s.group_id IN (
    SELECT sg.group_id
    FROM students_groups sg
    WHERE sg.teacher_id = (
        SELECT t.teacher_id
        FROM teachers t
        JOIN assignments a
            ON t.teacher_id = a.teacher_id
        JOIN assignments_grades ag
            ON a.assisgnment_id = ag.assisgnment_id
        GROUP BY t.teacher_id
        ORDER BY AVG(ag.grade) DESC
        LIMIT 1
    )
);