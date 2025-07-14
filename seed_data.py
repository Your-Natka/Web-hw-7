import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    dbname="students_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Створення груп
groups = ["Group A", "Group B", "Group C"]
cur.executemany("INSERT INTO groups (name) VALUES (%s);", [(g,) for g in groups])

# Створення викладачів
teachers = [fake.name() for _ in range(4)]
cur.executemany("INSERT INTO teachers (full_name) VALUES (%s);", [(t,) for t in teachers])

# Отримання teacher_id
cur.execute("SELECT id FROM teachers;")
teacher_ids = [row[0] for row in cur.fetchall()]

# Створення предметів
subjects = ["Math", "Physics", "History", "Biology", "Literature", "Chemistry", "Art"]
subject_data = [(subj, random.choice(teacher_ids)) for subj in subjects]
cur.executemany("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s);", subject_data)

# Отримання subject_id
cur.execute("SELECT id FROM subjects;")
subject_ids = [row[0] for row in cur.fetchall()]

# Створення студентів
students = [(fake.name(), random.randint(1, len(groups))) for _ in range(50)]
cur.executemany("INSERT INTO students (full_name, group_id) VALUES (%s, %s);", students)

# Отримання student_id
cur.execute("SELECT id FROM students;")
student_ids = [row[0] for row in cur.fetchall()]

# Створення оцінок
grades = []
for student_id in student_ids:
    for _ in range(random.randint(10, 20)):
        subject_id = random.choice(subject_ids)
        grade = random.randint(60, 100)
        days_ago = random.randint(1, 120)
        grade_date = datetime.now() - timedelta(days=days_ago)
        grades.append((student_id, subject_id, grade, grade_date.date()))

cur.executemany(
    "INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s);",
    grades
)

conn.commit()
cur.close()
conn.close()
print("Database seeded successfully.")
