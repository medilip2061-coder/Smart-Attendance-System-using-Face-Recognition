
import sqlite3
import csv
from pathlib import Path

# Locate the main project database
DB_PATH = Path(__file__).resolve().parent / "attendance.db"
# CSV output file
CSV_PATH = Path(__file__).resolve().parent / "students.csv"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get registered student details
cursor.execute("""
    SELECT id, student_id, name, email
    FROM students
    ORDER BY id
""")

students = cursor.fetchall()

# Export to CSV
with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    writer.writerow(["ID", "Student ID", "Name", "Email"])
    writer.writerows(students)

conn.close()

print(f"Export successful! {len(students)} students exported.")
print(f"CSV file saved at: {CSV_PATH}")
