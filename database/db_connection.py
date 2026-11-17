
import sqlite3
from pathlib import Path
from datetime import datetime

# Always use the database in the main project folder
DB_PATH = Path(__file__).resolve().parents[1] / "attendance.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            name TEXT NOT NULL,
            email TEXT,
            face_encoding TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            date TEXT,
            time TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


def mark_attendance(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    # Prevent duplicate attendance on the same day
    cursor.execute("""
        SELECT id FROM attendance
        WHERE student_id = ? AND date = ?
    """, (student_id, today))

    existing = cursor.fetchone()

    if existing:
        print(f"Attendance already marked for {student_id} today.")
    else:
        cursor.execute("""
            INSERT INTO attendance
            (student_id, date, time, status)
            VALUES (?, ?, ?, ?)
        """, (student_id, today, current_time, "Present"))

        conn.commit()
        print(f"Attendance marked for {student_id}!")

    conn.close()


if __name__ == "__main__":
    create_database()
