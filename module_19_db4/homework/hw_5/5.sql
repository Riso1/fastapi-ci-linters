SELECT
    sg.group_id,
    COUNT(DISTINCT s.student_id) AS students_count,
    AVG(ag.grade) AS avg_grade,
    COUNT(
        DISTINCT CASE
            WHEN no_submissions.student_id IS NOT NULL THEN s.student_id
        END
    ) AS not_submitted_students,
    COUNT(
        DISTINCT CASE
            WHEN overdue_students.student_id IS NOT NULL THEN s.student_id
        END
    ) AS overdue_students,
    COALESCE(SUM(repeat_attempts.extra_attempts), 0) AS repeated_attempts
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
        s2.student_id
    FROM students s2
    LEFT JOIN assignments_grades ag2
        ON s2.student_id = ag2.student_id
    GROUP BY s2.student_id
    HAVING COUNT(ag2.grade_id) = 0
) AS no_submissions
    ON no_submissions.student_id = s.student_id
LEFT JOIN (
    SELECT DISTINCT
        ag3.student_id
    FROM assignments_grades ag3
    JOIN assignments a3
        ON ag3.assisgnment_id = a3.assisgnment_id
    WHERE ag3.date > a3.due_date
) AS overdue_students
    ON overdue_students.student_id = s.student_id
LEFT JOIN (
    SELECT
        student_id,
        assisgnment_id,
        COUNT(*) - 1 AS extra_attempts
    FROM assignments_grades
    GROUP BY student_id, assisgnment_id
    HAVING COUNT(*) > 1
) AS repeat_attempts
    ON repeat_attempts.student_id = s.student_id
   AND repeat_attempts.assisgnment_id = a.assisgnment_id
GROUP BY sg.group_id
ORDER BY sg.group_id;