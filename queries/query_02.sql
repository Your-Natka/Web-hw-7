/*2. Знайти студента із найвищим середнім балом з певного предмета.*/
SELECT s.id, s.full_name, AVG(g.grade) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.subject_id = :subject_id
GROUP BY s.id, s.full_name
ORDER BY avg_grade DESC
LIMIT 1;