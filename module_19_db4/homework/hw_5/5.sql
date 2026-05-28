SELECT
    sg.group_id,
    COUNT(DISTINCT s.student_id) AS students_count,
    AVG(ag.grade) AS avg_grade,
    COUNT(DISTINCT CASE WHEN ag.grade_id IS NULL THEN s.student_id END) AS not_submitted_students,
    COUNT(DISTINCT CASE WHEN ag.date > a.due_date THEN s.student_id END) AS overdue_students,
    COUNT(CASE WHEN repeat_attempts.attempt_count > 1 THEN 1 END) AS repeated_attempts
FROM students_groups sg
LEFT JOIN students s
    ON sg.group_id = s.group_id
LEFT JOIN assignments a
    ON sg.group_id = a.group_id
LEFT JOIN assignments_grades ag
    ON a.assisgnment_id = ag.assisgnment_id
   AND s.student_id = ag.student_id
LEFT JOIN (
    SELECT
        student_id,
        assisgnment_id,
        COUNT(*) AS attempt_count
    FROM assignments_grades
    GROUP BY student_id, assisgnment_id
) AS repeat_attempts
    ON repeat_attempts.student_id = s.student_id
   AND repeat_attempts.assisgnment_id = a.assisgnment_id
GROUP BY sg.group_id
ORDER BY sg.group_id;