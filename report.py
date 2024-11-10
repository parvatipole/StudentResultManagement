import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentResultDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("800x500")

        # Database Connection
        self.conn = sqlite3.connect('student_management.db')
        self.cursor = self.conn.cursor()

        # Title
        title = tk.Label(self.root, text="View Student Results", font=("Arial", 20), bg="orange", fg="white")
        title.pack(side=tk.TOP, fill=tk.X)

        # Search by Roll No.
        tk.Label(self.root, text="Search By | Roll No.", font=("Arial", 12)).place(x=50, y=70)
        self.roll_no_var = tk.StringVar()
        self.roll_entry = tk.Entry(self.root, textvariable=self.roll_no_var, font=("Arial", 12), width=15)
        self.roll_entry.place(x=200, y=70)
        
        search_btn = tk.Button(self.root, text="Search", command=self.search_student, font=("Arial", 10), bg="blue", fg="white")
        search_btn.place(x=380, y=68)
        
        clear_btn = tk.Button(self.root, text="Clear", command=self.clear_fields, font=("Arial", 10), bg="gray", fg="white")
        clear_btn.place(x=440, y=68)

        # Result Table
        self.result_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        self.result_frame.place(x=50, y=120, width=700, height=200)

        # Table columns
        columns = ("roll_no", "name", "course", "marks_obtained", "full_marks", "percentage")
        self.result_table = ttk.Treeview(self.result_frame, columns=columns, show="headings")
        self.result_table.pack(fill=tk.BOTH, expand=True)

        # Column headings
        for col in columns:
            self.result_table.heading(col, text=col.replace("_", " ").title())
            self.result_table.column(col, width=100)

        # Delete button
        delete_btn = tk.Button(self.root, text="Delete", command=self.delete_record, font=("Arial", 12), bg="red", fg="white")
        delete_btn.place(x=350, y=350)

    def search_student(self):
        roll_no = self.roll_no_var.get()
        
        if not roll_no:
            messagebox.showerror("Error", "Please enter a Roll No.")
            return
        
        # Clear any existing data in the table
        for row in self.result_table.get_children():
            self.result_table.delete(row)
        
        # Fetch data from the database
        self.cursor.execute("SELECT roll_no, name, course, marks_obtained, full_marks, ROUND((marks_obtained * 100.0 / full_marks), 2) as percentage FROM results WHERE roll_no = ?", (roll_no,))
        row = self.cursor.fetchone()
        
        if row:
            self.result_table.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("No Record", "No record found for this Roll No.")

    def clear_fields(self):
        # Clear the search field and result table
        self.roll_no_var.set("")
        for row in self.result_table.get_children():
            self.result_table.delete(row)

    def delete_record(self):
        selected_item = self.result_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.")
            return
        
        # Get the roll_no of the selected item
        roll_no = self.result_table.item(selected_item)["values"][0]
        
        # Delete from database
        self.cursor.execute("DELETE FROM results WHERE roll_no = ?", (roll_no,))
        self.conn.commit()
        
        # Remove from the treeview
        self.result_table.delete(selected_item)
        messagebox.showinfo("Success", f"Record with Roll No {roll_no} has been deleted.")

    def __del__(self):
        # Close the database connection when the program exits
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultDashboard(root)
    root.mainloop()
