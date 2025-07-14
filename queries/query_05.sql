/*5.Знайти які курси читає певний викладач.*/
SELECT t.full_name, s.name 
FROM teachers t 
JOIN subjects s ON s.teacher_id = t.id 
WHERE t.id = :teacher_id;