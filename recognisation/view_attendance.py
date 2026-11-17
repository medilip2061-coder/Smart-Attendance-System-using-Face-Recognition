import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT student_id, date, time, status
    FROM attendance
    ORDER BY id DESC
""")

records = cursor.fetchall()

print("\n===== ATTENDANCE RECORDS =====")

for record in records:
    print(record)

conn.close()