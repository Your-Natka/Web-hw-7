import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

DB_PARAMS = {
    'dbname': 'students_db',
    'user': 'postgres',
    'password': 'your_password',  # заміни на свій пароль
    'host': 'localhost',
    'port': 5432,
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        sys.exit(1)

class DBManager:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def close(self):
        self.cur.close()
        self.conn.close()

    def create(self, model, **kwargs):
        if model == "Teacher":
            sql = "INSERT INTO teachers (fullname) VALUES (%s) RETURNING id"
            params = (kwargs['name'],)
        elif model == "Group":
            sql = "INSERT INTO groups (name) VALUES (%s) RETURNING id"
            params = (kwargs['name'],)
        elif model == "Student":
            sql = "INSERT INTO students (fullname, group_id) VALUES (%s, %s) RETURNING id"
            params = (kwargs['name'], kwargs['group_id'])
        elif model == "Subject":
            sql = "INSERT INTO subjects (name, teacher_id) VALUES (%s, %s) RETURNING id"
            params = (kwargs['name'], kwargs['teacher_id'])
        elif model == "Grade":
            sql = "INSERT INTO grades (student_id, subject_id, grade) VALUES (%s, %s, %s) RETURNING id"
            params = (kwargs['student_id'], kwargs['subject_id'], kwargs['grade'])
        else:
            print(f"Unknown model: {model}")
            return

        self.cur.execute(sql, params)
        new_id = self.cur.fetchone()['id']
        self.conn.commit()
        print(f"{model} created with id={new_id}")

    def list(self, model):
        queries = {
            "Teacher": "SELECT id, fullname FROM teachers ORDER BY id",
            "Group": "SELECT id, name FROM groups ORDER BY id",
            "Student": "SELECT id, fullname, group_id FROM students ORDER BY id",
            "Subject": "SELECT id, name, teacher_id FROM subjects ORDER BY id",
            "Grade": "SELECT id, student_id, subject_id, grade FROM grades ORDER BY id",
        }
        sql = queries.get(model)
        if not sql:
            print(f"Unknown model: {model}")
            return

        self.cur.execute(sql)
        rows = self.cur.fetchall()
        if not rows:
            print(f"No {model} records found.")
            return

        # Краще виведення
        for row in rows:
            print(", ".join(f"{key}={value}" for key, value in row.items()))

    def update(self, model, id, **kwargs):
        if not id:
            print("Missing id for update")
            return

        if model == "Teacher":
            if not kwargs.get('name'):
                print("Missing --name for Teacher update")
                return
            sql = "UPDATE teachers SET fullname=%s WHERE id=%s"
            params = (kwargs['name'], id)

        elif model == "Group":
            if not kwargs.get('name'):
                print("Missing --name for Group update")
                return
            sql = "UPDATE groups SET name=%s WHERE id=%s"
            params = (kwargs['name'], id)

        elif model == "Student":
            fields = []
            values = []
            if kwargs.get('name'):
                fields.append("fullname=%s")
                values.append(kwargs['name'])
            if kwargs.get('group_id'):
                fields.append("group_id=%s")
                values.append(kwargs['group_id'])
            if not fields:
                print("No fields to update for Student")
                return
            sql = f"UPDATE students SET {', '.join(fields)} WHERE id=%s"
            values.append(id)
            params = tuple(values)

        elif model == "Subject":
            fields = []
            values = []
            if kwargs.get('name'):
                fields.append("name=%s")
                values.append(kwargs['name'])
            if kwargs.get('teacher_id'):
                fields.append("teacher_id=%s")
                values.append(kwargs['teacher_id'])
            if not fields:
                print("No fields to update for Subject")
                return
            sql = f"UPDATE subjects SET {', '.join(fields)} WHERE id=%s"
            values.append(id)
            params = tuple(values)

        elif model == "Grade":
            fields = []
            values = []
            if kwargs.get('student_id'):
                fields.append("student_id=%s")
                values.append(kwargs['student_id'])
            if kwargs.get('subject_id'):
                fields.append("subject_id=%s")
                values.append(kwargs['subject_id'])
            if kwargs.get('grade') is not None:
                fields.append("grade=%s")
                values.append(kwargs['grade'])
            if not fields:
                print("No fields to update for Grade")
                return
            sql = f"UPDATE grades SET {', '.join(fields)} WHERE id=%s"
            values.append(id)
            params = tuple(values)

        else:
            print(f"Unknown model: {model}")
            return

        self.cur.execute(sql, params)
        self.conn.commit()
        print(f"{model} with id={id} updated")

    def remove(self, model, id):
        if model == "Teacher":
            # Спочатку видаляємо всі предмети, які пов'язані з цим вчителем
            self.cur.execute("DELETE FROM subjects WHERE teacher_id = %s", (id,))
            # Потім видаляємо самого вчителя
            sql = "DELETE FROM teachers WHERE id = %s"

        elif model == "Group":
            # Можна додати видалення студентів з цієї групи, якщо потрібно
            sql = "DELETE FROM groups WHERE id = %s"

        elif model == "Student":
            # Видаляємо всі оцінки цього студента, щоб уникнути порушення FK
            self.cur.execute("DELETE FROM grades WHERE student_id = %s", (id,))
            # Потім видаляємо самого студента
            sql = "DELETE FROM students WHERE id = %s"

        elif model == "Subject":
            # Можна додати видалення оцінок за цим предметом, якщо потрібно
            self.cur.execute("DELETE FROM grades WHERE subject_id = %s", (id,))
            sql = "DELETE FROM subjects WHERE id = %s"

        elif model == "Grade":
            sql = "DELETE FROM grades WHERE id = %s"

        else:
            print(f"Unknown model: {model}")
            return

        self.cur.execute(sql, (id,))
        self.conn.commit()
        print(f"{model} with id={id} removed")


def parse_args():
    parser = argparse.ArgumentParser(description="CLI CRUD for students_db")
    parser.add_argument('-a', '--action', required=True, choices=['create', 'list', 'update', 'remove'], help="Action to perform")
    parser.add_argument('-m', '--model', required=True, choices=['Teacher', 'Group', 'Student', 'Subject', 'Grade'], help="Model name")

    parser.add_argument('-n', '--name', help="Name or fullname")
    parser.add_argument('--id', type=int, help="ID of the record for update/remove")
    parser.add_argument('--group_id', type=int, help="Group ID (for Student)")
    parser.add_argument('--teacher_id', type=int, help="Teacher ID (for Subject)")
    parser.add_argument('--student_id', type=int, help="Student ID (for Grade)")
    parser.add_argument('--subject_id', type=int, help="Subject ID (for Grade)")
    parser.add_argument('--grade', type=int, help="Grade value (for Grade)")

    return parser.parse_args()

def main():
    args = parse_args()
    db = DBManager()

    try:
        if args.action == 'create':
            if args.model == 'Teacher':
                if not args.name:
                    print("Missing --name for Teacher creation")
                    return
                db.create('Teacher', name=args.name)

            elif args.model == 'Group':
                if not args.name:
                    print("Missing --name for Group creation")
                    return
                db.create('Group', name=args.name)

            elif args.model == 'Student':
                if not args.name or not args.group_id:
                    print("Missing --name or --group_id for Student creation")
                    return
                db.create('Student', name=args.name, group_id=args.group_id)

            elif args.model == 'Subject':
                if not args.name or not args.teacher_id:
                    print("Missing --name or --teacher_id for Subject creation")
                    return
                db.create('Subject', name=args.name, teacher_id=args.teacher_id)

            elif args.model == 'Grade':
                if not args.student_id or not args.subject_id or args.grade is None:
                    print("Missing --student_id or --subject_id or --grade for Grade creation")
                    return
                db.create('Grade', student_id=args.student_id, subject_id=args.subject_id, grade=args.grade)

        elif args.action == 'list':
            db.list(args.model)

        elif args.action == 'update':
            if not args.id:
                print("Missing --id for update")
                return
            db.update(args.model, args.id, 
                      name=args.name,
                      group_id=args.group_id,
                      teacher_id=args.teacher_id,
                      student_id=args.student_id,
                      subject_id=args.subject_id,
                      grade=args.grade)

        elif args.action == 'remove':
            if not args.id:
                print("Missing --id for remove")
                return
            db.remove(args.model, args.id)

    finally:
        db.close()

if __name__ == "__main__":
    main()

