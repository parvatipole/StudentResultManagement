import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class StudentResultSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Student Result")
        self.root.geometry("800x400")

        # Database Connection
        self.conn = sqlite3.connect('student_management.db')
        self.cursor = self.conn.cursor()

        # Creating Table if not exists
        self.create_table()

        # Select Student Section
        tk.Label(self.root, text="Select Student").grid(row=0, column=0, padx=10, pady=5)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(self.root, textvariable=self.student_var, state="readonly")
        self.student_dropdown.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Search", command=self.search_student).grid(row=0, column=2, padx=5, pady=5)

        # Add form fields
        tk.Label(self.root, text="Name").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Course").grid(row=2, column=0, padx=10, pady=5)
        self.course_entry = tk.Entry(self.root)
        self.course_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Marks Obtained").grid(row=3, column=0, padx=10, pady=5)
        self.marks_obtained_entry = tk.Entry(self.root)
        self.marks_obtained_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Full Marks").grid(row=4, column=0, padx=10, pady=5)
        self.full_marks_entry = tk.Entry(self.root)
        self.full_marks_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self.root, text="Submit", command=self.submit_result).grid(row=5, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self.root, text="Clear", command=self.clear_fields).grid(row=5, column=1, padx=5, pady=10, sticky="e")

        # Load and display the image
        self.load_image("result1.jpg")  # Specify the image path here

        # Populate the dropdown with roll numbers from the students table
        self.populate_dropdown()

    def create_table(self):
        # Create results table if it does not exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                               roll_no TEXT PRIMARY KEY,
                               name TEXT,
                               course TEXT,
                               marks_obtained INTEGER,
                               full_marks INTEGER,
                               FOREIGN KEY(roll_no) REFERENCES students(roll_no))''')
        self.conn.commit()

    def load_image(self, path):
        img = Image.open(path)
        img = img.resize((200, 150), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(self.root, image=self.photo)
        img_label.grid(row=1, column=3, rowspan=4, padx=10, pady=10)  # Adjust row, column, and rowspan for positioning

    def populate_dropdown(self):
        # Fetching the roll numbers of all students from the students table
        self.cursor.execute("SELECT roll_no FROM students")
        roll_numbers = [row[0] for row in self.cursor.fetchall()]
        self.student_dropdown['values'] = roll_numbers

    def search_student(self):
        roll_no = self.student_var.get()
        if roll_no:
            # Fetch the student details based on the selected roll number
            self.cursor.execute("SELECT name, course FROM students WHERE roll_no=?", (roll_no,))
            result = self.cursor.fetchone()
            if result:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, result[0])  # Display student name
                self.course_entry.delete(0, tk.END)
                self.course_entry.insert(0, result[1])  # Display student course
            else:
                messagebox.showerror("Error", "Student not found")

    def submit_result(self):
        roll_no = self.student_var.get()
        marks_obtained = self.marks_obtained_entry.get()
        full_marks = self.full_marks_entry.get()

        if roll_no and marks_obtained and full_marks:
            # Insert or update the result for the student
            self.cursor.execute("""INSERT OR REPLACE INTO results (roll_no, name, course, marks_obtained, full_marks) 
                                   VALUES (?, ?, ?, ?, ?)""",
                                (roll_no, self.name_entry.get(), self.course_entry.get(), marks_obtained, full_marks))
            self.conn.commit()
            messagebox.showinfo("Success", "Result added successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.marks_obtained_entry.delete(0, tk.END)
        self.full_marks_entry.delete(0, tk.END)
        self.student_var.set("")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultSystem(root)
    root.mainloop()
