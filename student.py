import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("800x500")

        # Connect to SQLite database (create if not exists)
        self.conn = sqlite3.connect("student_management.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Title Label
        title = tk.Label(self.root, text="Manage Student Details", font=("Arial", 15), bg="navy", fg="white", padx=10, pady=5)
        title.pack(side=tk.TOP, fill=tk.X)

        # Frame for form inputs
        form_frame = tk.Frame(self.root, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        # Student Detail Fields
        labels = ["Roll No.", "Name", "Email", "Gender", "State", "D.O.B", "Contact", "Admission", "Course", "City", "Pin", "Address"]
        self.entries = {}

        for i, label in enumerate(labels):
            row, col = divmod(i, 4)  # 4 columns layout
            lbl = tk.Label(form_frame, text=label)
            lbl.grid(row=row, column=col * 2, padx=5, pady=5, sticky=tk.W)

            if label == "Gender":  # Combo box for Gender with default "Select"
                entry = ttk.Combobox(form_frame, values=["Select", "Male", "Female", "Other"], width=17, state="readonly")
                entry.set("Select")
            elif label == "Address":  # Text box for Address
                entry = tk.Text(form_frame, height=3, width=17)
            else:
                entry = tk.Entry(form_frame, width=20)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            self.entries[label] = entry

        # Button Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        # Buttons
        save_btn = tk.Button(btn_frame, text="Save", bg="blue", fg="white", command=self.save)
        update_btn = tk.Button(btn_frame, text="Update", bg="green", fg="white", command=self.update)
        delete_btn = tk.Button(btn_frame, text="Delete", bg="red", fg="white", command=self.delete)
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear)

        save_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        update_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        delete_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        clear_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Search Frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="Roll No.").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)

        # Frame for Treeview and Scrollbars
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Scrollbars for Treeview
        y_scroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        x_scroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        # Treeview for displaying records
        columns = ("roll_no", "name", "email", "gender", "dob", "contact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Configure scrollbars
        y_scroll.config(command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        x_scroll.config(command=self.tree.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Define column headings
        self.tree.heading("roll_no", text="Roll No.")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("dob", text="D.O.B")
        self.tree.heading("contact", text="Contact")

        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.update_treeview()  # Load existing records

    def create_table(self):
        # Create students table if it does not exist
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS students (
                roll_no TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                state TEXT,
                dob TEXT,
                contact TEXT,
                admission TEXT,
                course TEXT,
                city TEXT,
                pin TEXT,
                address TEXT
            ) 
        """)
        self.conn.commit()

    def save(self):
        # Collect all field values
        missing_fields = []
        student_data = {}

        for field, entry in self.entries.items():
            if isinstance(entry, tk.Text):  # For the Address field
                value = entry.get("1.0", tk.END).strip()
            else:
                value = entry.get().strip()

            if not value or (field == "Gender" and value == "Select"):
                missing_fields.append(field)
            else:
                student_data[field] = value

        if missing_fields:
            messagebox.showerror("Error", f"Please fill in the following fields: {', '.join(missing_fields)}")
            return

        try:
            self.cursor.execute(""" 
                INSERT INTO students (roll_no, name, email, gender, state, dob, contact, admission, course, city, pin, address) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """, (student_data["Roll No."], student_data["Name"], student_data["Email"], student_data["Gender"],
                  student_data["State"], student_data["D.O.B"], student_data["Contact"], student_data["Admission"],
                  student_data["Course"], student_data["City"], student_data["Pin"], student_data["Address"]))
            self.conn.commit()
            self.update_treeview()
            messagebox.showinfo("Success", "Student record saved successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll No. already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update(self):
        roll_no = self.entries["Roll No."].get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter Roll No. to update!")
            return

        student_data = {k: (v.get("1.0", tk.END).strip() if isinstance(v, tk.Text) else v.get().strip()) for k, v in self.entries.items()}

        try:
            self.cursor.execute(""" 
                UPDATE students SET name = ?, email = ?, gender = ?, state = ?, dob = ?, contact = ?, 
                admission = ?, course = ?, city = ?, pin = ?, address = ? WHERE roll_no = ? 
            """, (student_data["Name"], student_data["Email"], student_data["Gender"], student_data["State"],
                  student_data["D.O.B"], student_data["Contact"], student_data["Admission"], student_data["Course"],
                  student_data["City"], student_data["Pin"], student_data["Address"], roll_no))
            self.conn.commit()
            self.update_treeview()
            messagebox.showinfo("Success", "Student record updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete(self):
        roll_no = self.entries["Roll No."].get()
        if not roll_no:
            messagebox.showerror("Error", "Please enter Roll No. to delete!")
            return

        self.cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
        self.conn.commit()
        self.update_treeview()
        messagebox.showinfo("Success", "Student record deleted successfully!")

    def clear(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set("Select")
            else:
                entry.delete(0, tk.END)

    def search(self):
        roll_no = self.search_var.get()
        self.cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        student = self.cursor.fetchone()

        if student:
            for idx, field in enumerate(["Roll No.", "Name", "Email", "Gender", "State", "D.O.B", "Contact", "Admission", "Course", "City", "Pin", "Address"]):
                entry = self.entries[field]
                value = student[idx]
                if isinstance(entry, tk.Text):
                    entry.delete("1.0", tk.END)
                    entry.insert(tk.END, value)
                elif isinstance(entry, ttk.Combobox):
                    entry.set(value)
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
            messagebox.showinfo("Success", "Record found and loaded.")
        else:
            messagebox.showerror("Error", "Record not found!")

    def update_treeview(self):
        # Clear the current treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch all records
        self.cursor.execute("SELECT roll_no, name, email, gender, dob, contact FROM students")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
