/*9.Знайти список курсів, які відвідує студент.*/
SELECT DISTINCT s.name AS course_name, t.full_name AS teacher_name
FROM subjects s
JOIN grades g ON g.subject_id = s.id
JOIN teachers t ON s.teacher_id = t.id
WHERE g.student_id = :student_id;