/*1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.*/
SELECT s.id, s.full_name, AVG(g.grade) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY avg_grade DESC
LIMIT 5;