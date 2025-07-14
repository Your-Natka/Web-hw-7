/*3. Знайти середній бал у групах з певного предмета.*/
SELECT gr.name AS group_name, AVG(g.grade) AS avg_grade
FROM groups gr
JOIN students s ON s.group_id = gr.id
JOIN grades g ON g.student_id = s.id
WHERE g.subject_id = :subject_id
GROUP BY gr.name
ORDER BY avg_grade DESC;