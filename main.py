import psycopg2
import os

def run_query(query_path):
    with open(query_path, 'r') as file:
        query = file.read()

    conn = psycopg2.connect(
        dbname="students_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(query)
    try:
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception:
        print("Query executed (no output to fetch).")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    for i in range(1, 11):
        path = f"queries/query_{i:02}.sql"
        if os.path.exists(path):
            print(f"\n--- Running {path} ---")
            run_query(path)
