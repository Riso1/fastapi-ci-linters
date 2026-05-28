SELECT
    overdue_stats.group_id,
    AVG(overdue_stats.overdue_count) AS avg_overdue,
    MAX(overdue_stats.overdue_count) AS max_overdue,
    MIN(overdue_stats.overdue_count) AS min_overdue
FROM (
    SELECT
        s.group_id,
        s.student_id,
        COUNT(*) AS overdue_count
    FROM students s
    JOIN assignments_grades ag
        ON s.student_id = ag.student_id
    JOIN assignments a
        ON ag.assisgnment_id = a.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY s.group_id, s.student_id
) AS overdue_stats
GROUP BY overdue_stats.group_id;