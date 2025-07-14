/* 7. Знайти оцінки студентів у окремій групі з певного предмета */
SELECT st.full_name, g.name AS group_name, sub.name AS subject_name, gr.grade
FROM grades gr
JOIN students st ON gr.student_id = st.id
JOIN groups g ON st.group_id = g.id
JOIN subjects sub ON gr.subject_id = sub.id
WHERE g.id = :group_id AND sub.id = :subject_id;