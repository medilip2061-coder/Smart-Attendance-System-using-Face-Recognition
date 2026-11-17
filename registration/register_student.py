
import customtkinter as ctk
import sqlite3
from pathlib import Path
from tkinter import messagebox

# Database location
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "attendance.db"

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def register_student():
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    email = email_entry.get().strip()

    # Validate inputs
    if not student_id or not name:
        messagebox.showwarning(
            "Warning",
            "Please enter Student ID and Name!"
        )
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (student_id, name, email)
            VALUES (?, ?, ?)
        """, (student_id, name, email))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Student registered successfully!"
        )

        id_entry.delete(0, "end")
        name_entry.delete(0, "end")
        email_entry.delete(0, "end")

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "This Student ID already exists!"
        )

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error))


# Main application window
app = ctk.CTk()

app.title("Smart Attendance System")
app.geometry("600x550")

# Heading
title = ctk.CTkLabel(
    app,
    text="STUDENT REGISTRATION",
    font=("Arial", 26, "bold")
)
title.pack(pady=30)

# Student ID
id_entry = ctk.CTkEntry(
    app,
    placeholder_text="Enter Student ID",
    width=350,
    height=45
)
id_entry.pack(pady=12)

# Student Name
name_entry = ctk.CTkEntry(
    app,
    placeholder_text="Enter Student Name",
    width=350,
    height=45
)
name_entry.pack(pady=12)

# Email
email_entry = ctk.CTkEntry(
    app,
    placeholder_text="Enter Email Address",
    width=350,
    height=45
)
email_entry.pack(pady=12)

# Register button
register_button = ctk.CTkButton(
    app,
    text="REGISTER STUDENT",
    command=register_student,
    width=350,
    height=45,
    font=("Arial", 16, "bold")
)
register_button.pack(pady=30)

# Footer
footer = ctk.CTkLabel(
    app,
    text="Smart Attendance System | Face Recognition"
)
footer.pack(pady=15)

# Run application
app.mainloop()
