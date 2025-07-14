/* 8. Знайти середній бал, який ставить певний викладач зі своїх предметів */
SELECT t.full_name AS teacher,
       AVG(gr.grade) AS average_grade
FROM teachers t
JOIN subjects s ON s.teacher_id = t.id
JOIN grades gr ON gr.subject_id = s.id
WHERE t.id = :teacher_id
GROUP BY t.full_name;