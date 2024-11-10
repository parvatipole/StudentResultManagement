from tkinter import *
from PIL import Image, ImageTk  # Make sure Pillow is installed: pip install pillow
from tkinter import ttk, messagebox
import sqlite3

class courseclass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # Load and initialize the logo image
        logo_image = Image.open("project.jpg")
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)
        self.logo_dash = ImageTk.PhotoImage(logo_image)

        # Title label with the image
        title = Label(self.root, text="Manage Course Details", padx=10, compound=LEFT, image=self.logo_dash,
                      font=("goudy old style", 20, "bold"), bg="#022C43", fg="white")
        title.place(x=10, y=15, width=1180, height=35)

        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # Labels and Entry Fields
        lb1_coursename = Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg='white')
        lb1_coursename.place(x=10, y=60)

        lb1_duration = Label(self.root, text="Duration", font=("goudy old style", 15, "bold"), bg='white')
        lb1_duration.place(x=10, y=100)

        lb1_charges = Label(self.root, text="Charges", font=("goudy old style", 15, "bold"), bg='white')
        lb1_charges.place(x=10, y=140)

        lb1_description = Label(self.root, text="Description", font=("goudy old style", 15, "bold"), bg='white')
        lb1_description.place(x=10, y=180)

        # Entry Widgets
        self.txt_coursename = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg='lightyellow')
        self.txt_coursename.place(x=150, y=60, width=200)

        txt_duration = Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15, "bold"), bg='lightyellow')
        txt_duration.place(x=150, y=100, width=200)

        txt_charges = Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15, "bold"), bg='lightyellow')
        txt_charges.place(x=150, y=140, width=200)

        self.txt_description = Text(self.root, font=("goudy old style", 15, "bold"), bg='lightyellow')
        self.txt_description.place(x=150, y=180, width=500, height=100)

        # Buttons
        self.btn_add = Button(self.root, text='Save', font=("goudy old style", 15, "bold"), bg="#0288D1", fg="white", cursor="hand2", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)

        self.btn_update = Button(self.root, text='Update', font=("goudy old style", 15, "bold"), bg="#388E3C", fg="white", cursor="hand2", command=self.update)
        self.btn_update.place(x=270, y=400, width=110, height=40)

        self.btn_delete = Button(self.root, text='Delete', font=("goudy old style", 15, "bold"), bg="#D32F2F", fg="white", cursor="hand2", command=self.delete)
        self.btn_delete.place(x=390, y=400, width=110, height=40)

        self.btn_clear = Button(self.root, text='Clear', font=("goudy old style", 15, "bold"), bg="#455A64", fg="white", cursor="hand2", command=self.clear)
        self.btn_clear.place(x=510, y=400, width=110, height=40)

        # Search Panel
        lb1_search_coursename = Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg='white')
        lb1_search_coursename.place(x=720, y=60)
        txt_search_coursename = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg='lightyellow')
        txt_search_coursename.place(x=870, y=60, width=180)
        btn_search = Button(self.root, text='Search', font=("goudy old style", 15, "bold"), bg="#03A9F4", fg="white", cursor="hand2", command=self.search)
        btn_search.place(x=1070, y=60, width=120, height=28)

        # Course Details Table
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        # Define the Treeview to display course data
        self.coursetable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.coursetable.xview)
        scrolly.config(command=self.coursetable.yview)
        self.coursetable.pack(fill=BOTH, expand=1)

        # Configure columns
        self.coursetable.heading("cid", text="Course_ID")
        self.coursetable.heading("name", text="Name")
        self.coursetable.heading("duration", text="Duration")
        self.coursetable.heading("charges", text="Charges")
        self.coursetable.heading("description", text="Description")
        self.coursetable["show"] = "headings"

        # Set column widths and display the columns
        self.coursetable.column("cid", width=50, anchor=CENTER)
        self.coursetable.column("name", width=100)
        self.coursetable.column("duration", width=80)
        self.coursetable.column("charges", width=80)
        self.coursetable.column("description", width=150)
        
        self.coursetable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name is required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course name already exists", parent=self.root)
                else:
                    cur.execute("insert into course (name, duration, charges, description) values(?, ?, ?, ?)", (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name is required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Select a course from the list", parent=self.root)
                else:
                    cur.execute("update course set duration=?, charges=?, description=? where name=?", (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0", END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name is required", parent=self.root)
            else:
                cur.execute("select * from course where name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid course name", parent=self.root)
                else:
                    cur.execute("delete from course where name=?", (self.var_course.get(),))
                    con.commit()
                    messagebox.showinfo("Delete", "Course deleted successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.txt_description.delete("1.0", END)
        self.var_search.set("")
        self.show()

    def get_data(self, ev):
        f = self.coursetable.focus()
        content = self.coursetable.item(f)
        row = content['values']
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete("1.0", END)
        self.txt_description.insert(END, row[4])

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            rows = cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", (self.var_search.get() + '%',))
            rows = cur.fetchall()
            self.coursetable.delete(*self.coursetable.get_children())
            for row in rows:
                self.coursetable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


# Create and run the GUI
if __name__ == "__main__":
    root = Tk()
    obj = courseclass(root)
    root.mainloop()
