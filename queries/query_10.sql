/*10.Список курсів, які певному студенту читає певний викладач.*/

SELECT DISTINCT s.name AS course_name
FROM subjects s
JOIN grades g ON g.subject_id = s.id
JOIN students st ON st.id = g.student_id
WHERE st.id = :student_id
  AND s.teacher_id = :teacher_id;
  