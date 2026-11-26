"""A tkinter app for viewing and managing student marks."""

import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk


# This is the text file for the studentmarks
FILE_NAME = "studentMarks.txt" 
MAXIMUM_MARK = 160


class StudentManager:
    """Display and manage student records."""

    def __init__(self, window):
        self.window = window
        self.window.title("Student Manager")
        self.window.geometry("920x610")
        self.window.minsize(760, 520)
        self.window.configure(bg="#EDF7FA")
        self.students = self.load_students()
        self.create_widgets()
        self.view_all_students()

    def load_students(self):
        """Read the student file and store its records in a list."""
        student = []

        try:
            with open(FILE_NAME, "r", encoding="utf-8") as student_file:
                lines = student_file.readlines()

            # the first line is the record count, so student data starts on the second line.
            for line in lines[1:]:
                line = line.strip()
                if line:
                    student.append(line)

        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {FILE_NAME}")
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror("Error", f"Could not read {FILE_NAME}: {error}")

        return student

    def save_students(self):
        """Write all student lines back to the file with an updated record count."""
        try:
            with open(FILE_NAME, "w", encoding="utf-8") as student_file:
                student_file.write(f"{len(self.students)}\n")
                for student_line in self.students:
                    student_file.write(student_line + "\n")

        except OSError as error:
            messagebox.showerror(
                "Save error",
                f"Could not save {FILE_NAME}:\n{error}",
            )

    def parse_student(self, student_line):
        """Split a saved student line into its separate field."""
        parts = student_line.split(",")

        if len(parts) != 6:
            return None

        try:
            return {
                "code": parts[0].strip(),
                "name": parts[1].strip(),
                "coursework": [
                    int(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                ],
                "exam": int(parts[5]),
            }
        except ValueError:
            return None

    def create_widgets(self):
        """Create the menu buttons and the area used to display results."""
        title = tk.Label(
            self.window,
            text="STUDENT  /  RECORDS",
            font=("Consolas", 20, "bold"),
            fg="#EAFBFF",
            bg="#123A55",
            anchor="w",
            padx=18,
        )
        title.pack(fill="x", ipady=12)

        main_frame = tk.Frame(self.window, bg="#EDF7FA")
        main_frame.pack(fill="both", expand=True, padx=14, pady=14)

        menu_frame = tk.Frame(main_frame, bg="#123A55", padx=12, pady=12)
        menu_frame.pack(side="left", fill="y", padx=(0, 14))

        output_frame = tk.Frame(main_frame, bg="#FFFFFF", highlightthickness=1, highlightbackground="#D7E1E8")
        output_frame.pack(side="right", fill="both", expand=True)

        # Each button runs the method for one student management option.
        menu_options = [
            ("1. View all records", self.view_all_students),
            ("2. Find a student", self.find_student),
            ("3. Highest total", self.show_highest),
            ("4. Lowest total", self.show_lowest),
            ("5. Sort ascending", self.sort_ascending),
            ("6. Sort descending", self.sort_descending),
            ("7. Add a student", self.add_student),
            ("8. Delete a student", self.delete_student),
            ("9. Update a student", self.update_student),
        ]

        for label, action in menu_options:
            tk.Button(
                menu_frame,
                text=label,
                width=21,
                command=action,
                font=("Segoe UI", 9, "bold"),
                fg="#123A55",
                bg="#D6EEF5",
                activebackground="#A9DCE8",
                activeforeground="#123A55",
                relief="flat",
                anchor="w",
                padx=10,
                cursor="hand2",
            ).pack(fill="x", pady=3, ipady=5)

        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure(
            "Student.Treeview",
            background="#FFFFFF",
            foreground="#123A55",
            fieldbackground="#FFFFFF",
            borderwidth=0,
            rowheight=38,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Student.Treeview.Heading",
            background="#D6EEF5",
            foreground="#123A55",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Student.Treeview",
            background=[("selected", "#A9DCE8")],
            foreground=[("selected", "#123A55")],
        )

        header_frame = tk.Frame(output_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=16, pady=(14, 8))

        self.output_heading = tk.Label(
            header_frame,
            text="All Student Records",
            font=("Segoe UI", 15, "bold"),
            fg="#123A55",
            bg="#FFFFFF",
            anchor="w",
        )
        self.output_heading.pack(side="left", fill="x", expand=True)

        self.output_summary = tk.Label(
            header_frame,
            text="",
            font=("Segoe UI", 9),
            fg="#5C7F91",
            bg="#FFFFFF",
            anchor="e",
        )
        self.output_summary.pack(side="right")

        table_frame = tk.Frame(output_frame, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columns = (
            "name",
            "code",
            "coursework",
            "exam",
            "total",
            "percentage",
            "grade",
        )
        self.output = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Student.Treeview",
        )

        headings = {
            "name": ("STUDENT NAME", 180),
            "code": ("NUMBER", 90),
            "coursework": ("COURSEWORK", 105),
            "exam": ("EXAM", 75),
            "total": ("TOTAL", 75),
            "percentage": ("PERCENTAGE", 105),
            "grade": ("GRADE", 65),
        }
        for column, (heading, width) in headings.items():
            self.output.heading(column, text=heading)
            self.output.column(
                column,
                width=width,
                minwidth=65,
                anchor="center",
            )
        self.output.column("name", anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.output.yview,
        )
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def coursework_total(self, student):
        """Add together a student's three coursework marks."""
        return sum(student["coursework"])

    def total_mark(self, student):
        """Add the coursework total and exam mark."""
        return self.coursework_total(student) + student["exam"]

    def percentage(self, student):
        """Calculate the percentage from the overall mark out of 160."""
        return self.total_mark(student) / MAXIMUM_MARK * 100

    def grade(self, student):
        """Return the letter grade that matches the student's percentage."""
        mark_percentage = self.percentage(student)

        if mark_percentage >= 70:
            return "A"
        elif mark_percentage >= 60:
            return "B"
        elif mark_percentage >= 50:
            return "C"
        elif mark_percentage >= 40:
            return "D"
        else:
            return "F"

    def format_student(self, student):
        """Create a readable summary of one student's results."""
        coursework = self.coursework_total(student)

        return (
            f"Name: {student['name']}\n"
            f"Student number: {student['code']}\n"
            f"Coursework total: {coursework} / 60\n"
            f"Exam mark: {student['exam']} / 100\n"
            f"Overall mark: {self.total_mark(student)} / 160\n"
            f"Percentage: {self.percentage(student):.1f}%\n"
            f"Grade: {self.grade(student)}\n"
            f"{'-' * 42}\n"
        )

    def show_records(self, student_lines, heading):
        """Display selected records in a table and calculate the average percentage."""
        self.output_heading.config(text=heading)

        for item in self.output.get_children():
            self.output.delete(item)

        records = []

        for student_line in student_lines:
            student = self.parse_student(student_line)

            if student is not None:
                records.append(student)

        if not records:
            self.output_summary.config(text="0 records")
            return

        for student in records:
            coursework = self.coursework_total(student)
            self.output.insert(
                "",
                tk.END,
                values=(
                    student["name"],
                    student["code"],
                    f"{coursework} / 60",
                    f"{student['exam']} / 100",
                    f"{self.total_mark(student)} / 160",
                    f"{self.percentage(student):.1f}%",
                    self.grade(student),
                ),
            )

        average = sum(self.percentage(student) for student in records) / len(records)
        self.output_summary.config(
            text=f"{len(records)} record{'s' if len(records) != 1 else ''}  |  Average {average:.1f}%"
        )

    def view_all_students(self):
        """Show every student's results and the class average."""
        self.show_records(self.students, "All Student Records")

    def find_student_by_code(self, window_title):
        """Ask for a student number and return the matching line of data."""
        code = simpledialog.askstring(
            window_title,
            "Enter the student's number:",
            parent=self.window,
        )

        if code is None:
            return None

        code = code.strip()

        for student_line in self.students:
            student = self.parse_student(student_line)

            if student is not None and student["code"] == code:
                return student_line

        messagebox.showinfo(
            "Student not found",
            f"No student has the number {code}.",
        )
        return None

    def find_student(self):
        """Find a student by number and display their results."""
        student_line = self.find_student_by_code("Find a student")

        if student_line is not None:
            self.show_records([student_line], "Student Record")

    def show_highest(self):
        """Display the student with the highest combined mark."""
        valid_lines = [
            line for line in self.students if self.parse_student(line) is not None
        ]

        if not valid_lines:
            messagebox.showinfo("No records", "There are no valid student records.")
            return

        highest = max(
            valid_lines,
            key=lambda line: self.total_mark(self.parse_student(line)),
        )
        self.show_records([highest], "Student with the Highest Total")

    def show_lowest(self):
        """Display the student with the lowest combined mark."""
        valid_lines = [
            line for line in self.students if self.parse_student(line) is not None
        ]

        if not valid_lines:
            messagebox.showinfo("No records", "There are no valid student records.")
            return

        lowest = min(
            valid_lines,
            key=lambda line: self.total_mark(self.parse_student(line)),
        )
        self.show_records([lowest], "Student with the Lowest Total")

    def sort_ascending(self):
        """Show records ordered from the lowest total mark to the highest."""
        sorted_students = sorted(
            self.students,
            key=lambda line: self.total_mark(self.parse_student(line))
            if self.parse_student(line) is not None
            else -1,
        )
        self.show_records(sorted_students, "Records Sorted: Ascending")

    def sort_descending(self):
        """Show records ordered from the highest total mark to the lowest."""
        sorted_students = sorted(
            self.students,
            key=lambda line: self.total_mark(self.parse_student(line))
            if self.parse_student(line) is not None
            else -1,
            reverse=True,
        )
        self.show_records(sorted_students, "Records Sorted: Descending")

    def ask_for_details(self, old_student=None):
        """Collect and check a student's number, name, and marks."""
        if old_student:
            old_code = old_student["code"]
            old_name = old_student["name"]
        else:
            old_code = ""
            old_name = ""

        code = simpledialog.askinteger(
            "Student details",
            "Enter a student number from 1000 to 9999:",
            initialvalue=int(old_code) if old_code else None,
            minvalue=1000,
            maxvalue=9999,
            parent=self.window,
        )

        if code is None:
            return None

        for student_line in self.students:
            student = self.parse_student(student_line)

            if student is not None and student["code"] == str(code):
                is_current_student = old_student and student["code"] == old_code

                if not is_current_student:
                    messagebox.showerror(
                        "Number already used",
                        "Each student must have a unique student number.",
                    )
                    return None

        name = simpledialog.askstring(
            "Student details",
            "Enter the student's name:",
            initialvalue=old_name,
            parent=self.window,
        )

        if name is None:
            return None

        name = name.strip()

        if not name or "," in name:
            messagebox.showerror(
                "Invalid name",
                "Enter a name without commas.",
            )
            return None

        coursework = []

        for mark_number in range(1, 4):
            if old_student:
                initial_mark = old_student["coursework"][mark_number - 1]
            else:
                initial_mark = 0

            mark = simpledialog.askinteger(
                "Student details",
                f"Enter coursework mark {mark_number} (0 to 20):",
                initialvalue=initial_mark,
                minvalue=0,
                maxvalue=20,
                parent=self.window,
            )

            if mark is None:
                return None

            coursework.append(mark)

        if old_student:
            initial_exam = old_student["exam"]
        else:
            initial_exam = 0

        exam = simpledialog.askinteger(
            "Student details",
            "Enter the exam mark (0 to 100):",
            initialvalue=initial_exam,
            minvalue=0,
            maxvalue=100,
            parent=self.window,
        )

        if exam is None:
            return None

        # Builds the comma-separated line in the same format used by the text file.
        return f"{code},{name},{coursework[0]},{coursework[1]},{coursework[2]},{exam}"

    def add_student(self):
        """Add a new student line and save the updated records."""
        student_line = self.ask_for_details()

        if student_line is None:
            return

        self.students.append(student_line)
        self.save_students()
        self.view_all_students()
        messagebox.showinfo("Student added", "The student record was added.")

    def delete_student(self):
        """Delete the selected student after asking the user to confirm."""
        student_line = self.find_student_by_code("Delete a student")

        if student_line is None:
            return

        student = self.parse_student(student_line)
        confirm = messagebox.askyesno(
            "Confirm deletion",
            f"Delete the record for {student['name']}?",
        )

        if confirm:
            self.students.remove(student_line)
            self.save_students()
            self.view_all_students()

    def update_student(self):
        """Replace a student's line with updated details and save the file."""
        student_line = self.find_student_by_code("Update a student")

        if student_line is None:
            return

        old_student = self.parse_student(student_line)
        updated_line = self.ask_for_details(old_student)

        if updated_line is None:
            return

        index = self.students.index(student_line)
        self.students[index] = updated_line
        self.save_students()
        self.view_all_students()
        messagebox.showinfo("Student updated", "The student record was updated.")


def main():
    """Create the window and start Tkinter's event loop."""
    window = tk.Tk()
    StudentManager(window)
    window.mainloop()


if __name__ == "__main__":
    main()
                
