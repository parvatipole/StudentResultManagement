import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk  # Make sure Pillow is installed: pip install pillow
from course import courseclass
from student import StudentManagementSystem
from result import StudentResultSystem  # Import the StudentResultSystem class
from report import StudentResultDashboard  # Import the StudentResultDashboard class

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # Load, resize, and convert the image for Tkinter
        logo_image = Image.open("project.jpg")
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)  # Resize to 50x50 pixels
        self.logo_dash = ImageTk.PhotoImage(logo_image)

        # Create the title label with the smaller image beside the text
        title = Label(self.root, text="Student Result Management System", padx=10, image=self.logo_dash,
                      font=("goudy oldstyle", 20, "bold"), bg="#033054", fg="white", compound=LEFT)
        title.place(x=0, y=0, relwidth=1, height=50)

        # Menu Frame with extra height to allow vertical centering
        M_Frame = LabelFrame(self.root, text="Menus", font=("times new roman", 15), bg="white")
        M_Frame.place(x=10, y=70, width=1340, height=80)  # Increased height for better alignment

        # Center the button vertically in the frame
        btn_course = Button(M_Frame, text="Course", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                            cursor="hand2", command=self.add_course)
        btn_course.place(x=20, y=5, width=200, height=40)
        
        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                             cursor="hand2", command=self.add_student)
        btn_student.place(x=240, y=5, width=200, height=40)
        
        btn_result = Button(M_Frame, text="Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                            cursor="hand2", command=self.add_result)  # Connect to add_result
        btn_result.place(x=460, y=5, width=200, height=40)

        btn_view = Button(M_Frame, text="View", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white",
                          cursor="hand2", command=self.view_results)  # Connect to view_results
        btn_view.place(x=680, y=5, width=200, height=40)
        
        btn_logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white")
        btn_logout.place(x=900, y=5, width=200, height=40)
        
        btn_exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white")
        btn_exit.place(x=1120, y=5, width=200, height=40)

        # Footer Label
        footer = Label(self.root, text="SRMS-Student Result Management System\nContact us for any technical issue: 987xxxx01",
                       font=("goudy oldstyle", 15, "bold"), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        # Background Image
        self.lb1_img = Image.open("study2.jpg")
        self.lb1_img = self.lb1_img.resize((920, 350), Image.LANCZOS)  # Corrected resizing method
        self.lb1_img = ImageTk.PhotoImage(self.lb1_img)

        # Display Background Image
        self.lb1_bg = Label(self.root, image=self.lb1_img)
        self.lb1_bg.place(x=400, y=180, width=920, height=350)

        # Summary Labels
        self.lb1_course = Label(self.root, text="Total Courses\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE,
                                bg="#e43b06", fg="white").place(x=400, y=530, width=300, height=100)
        self.lb1_student = Label(self.root, text="Total Students\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE,
                                 bg="#0676ad", fg="white").place(x=710, y=530, width=300, height=100)
        self.lb1_result = Label(self.root, text="Total Results\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE,
                                bg="#038074", fg="white").place(x=1020, y=530, width=300, height=100)

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = courseclass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentManagementSystem(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = StudentResultSystem(self.new_win)  # Instantiate StudentResultSystem

    def view_results(self):
        self.new_win = Toplevel(self.root)  # Create a new top-level window
        self.new_obj = StudentResultDashboard(self.new_win)  # Instantiate StudentResultDashboard

if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
