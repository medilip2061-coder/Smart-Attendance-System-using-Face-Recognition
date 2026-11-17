
import customtkinter as ctk
import sqlite3
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox

# Project settings
PROJECT_DIR = Path(__file__).resolve().parent
DB_PATH = PROJECT_DIR / "attendance.db"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AttendanceDashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Smart Attendance Management System")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.configure(fg_color="#F3F6FC")

        self.create_header()
        self.create_statistics()
        self.create_main_content()
        self.refresh_dashboard()

    def create_header(self):
        header = ctk.CTkFrame(
            self, fg_color="#163A70", corner_radius=0, height=90
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="SMART ATTENDANCE SYSTEM",
            font=("Arial", 25, "bold"),
            text_color="white"
        ).pack(side="left", padx=30, pady=25)

        ctk.CTkLabel(
            header,
            text="Face Recognition Dashboard",
            font=("Arial", 14),
            text_color="#DCE8FF"
        ).pack(side="right", padx=30)

    def create_statistics(self):
        stats_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        stats_frame.pack(fill="x", padx=25, pady=25)

        self.total_label = self.create_stat_card(
            stats_frame, "TOTAL STUDENTS", "0", 0
        )

        self.present_label = self.create_stat_card(
            stats_frame, "PRESENT TODAY", "0", 1
        )

        self.absent_label = self.create_stat_card(
            stats_frame, "ABSENT TODAY", "0", 2
        )

        self.percentage_label = self.create_stat_card(
            stats_frame, "ATTENDANCE RATE", "0%", 3
        )

    def create_stat_card(self, parent, title, value, column):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            height=125
        )
        card.grid(
            row=0, column=column,
            padx=8, sticky="nsew"
        )
        card.grid_propagate(False)

        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12, "bold"),
            text_color="#64748B"
        ).pack(pady=(22, 8))

        number = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold"),
            text_color="#163A70"
        )
        number.pack()

        return number

    def create_main_content(self):
        content = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        content.pack(
            fill="both", expand=True,
            padx=25, pady=(0, 20)
        )

        left = ctk.CTkFrame(
            content, fg_color="white",
            corner_radius=15, width=300
        )
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        ctk.CTkLabel(
            left,
            text="MAIN MENU",
            font=("Arial", 18, "bold"),
            text_color="#163A70"
        ).pack(pady=(25, 20))

        self.create_menu_button(
            left, "Register Student",
            self.open_registration
        )

        self.create_menu_button(
            left, "Start Face Recognition",
            self.start_recognition
        )

        self.create_menu_button(
            left, "View Attendance",
            self.show_attendance
        )

        self.create_menu_button(
            left, "Refresh Dashboard",
            self.refresh_dashboard
        )

        self.create_menu_button(
            left, "Exit Application",
            self.destroy
        )

        right = ctk.CTkFrame(
            content, fg_color="white",
            corner_radius=15
        )
        right.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            right,
            text="RECENT ATTENDANCE RECORDS",
            font=("Arial", 18, "bold"),
            text_color="#163A70"
        ).pack(anchor="w", padx=25, pady=25)

        self.records_box = ctk.CTkTextbox(
            right,
            font=("Consolas", 13),
            fg_color="#F7F9FD",
            text_color="#243247",
            corner_radius=10
        )
        self.records_box.pack(
            fill="both", expand=True,
            padx=20, pady=(0, 20)
        )

    def create_menu_button(self, parent, text, command):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=45,
            corner_radius=9,
            font=("Arial", 14, "bold"),
            fg_color="#2463A6",
            hover_color="#163A70"
        )
        button.pack(fill="x", padx=20, pady=9)

    def get_database_data(self):
        if not DB_PATH.exists():
            return 0, 0, []

        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()

            # Count registered students
            total = 0
            try:
                cursor.execute("SELECT COUNT(*) FROM students")
                total = cursor.fetchone()[0]
            except sqlite3.Error:
                pass

            # Get today's attendance
            cursor.execute("""
                SELECT DISTINCT student_id
                FROM attendance
                WHERE date = DATE('now', 'localtime')
                AND status = 'Present'
            """)
            present_ids = cursor.fetchall()
            present = len(present_ids)

            # Get recent attendance
            cursor.execute("""
                SELECT student_id, date, time, status
                FROM attendance
                ORDER BY id DESC
                LIMIT 10
            """)
            records = cursor.fetchall()

            conn.close()
            return total, present, records

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error", str(error)
            )
            return 0, 0, []

    def refresh_dashboard(self):
        total, present, records = self.get_database_data()

        absent = max(total - present, 0)
        percentage = (
            round((present / total) * 100)
            if total > 0 else 0
        )

        self.total_label.configure(text=str(total))
        self.present_label.configure(text=str(present))
        self.absent_label.configure(text=str(absent))
        self.percentage_label.configure(
            text=f"{percentage}%"
        )

        self.records_box.delete("1.0", "end")

        if records:
            for student_id, date, time, status in records:
                self.records_box.insert(
                    "end",
                    f"Student ID: {student_id}\n"
                    f"Date: {date}   Time: {time}\n"
                    f"Status: {status}\n"
                    "--------------------------------\n"
                )
        else:
            self.records_box.insert(
                "end", "No attendance records found yet."
            )

    def launch_script(self, relative_path):
        script = PROJECT_DIR / relative_path

        if not script.exists():
            messagebox.showerror(
                "File Not Found",
                f"Could not find:\n{script}"
            )
            return

        subprocess.Popen(
            [sys.executable, str(script)],
            cwd=str(PROJECT_DIR)
        )

    def open_registration(self):
        self.launch_script(
            Path("registration") / "register_student.py"
        )

    def start_recognition(self):
        self.launch_script(
            Path("recognisation") / "recognize_faces.py"
        )

    def show_attendance(self):
        self.refresh_dashboard()


if __name__ == "__main__":
    app = AttendanceDashboard()
    app.mainloop()
