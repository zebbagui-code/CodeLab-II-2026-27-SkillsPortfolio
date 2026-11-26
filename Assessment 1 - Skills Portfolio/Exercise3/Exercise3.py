"""Tkinter student record manager for the Student Manager exercise."""

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk


STUDENT_DATA_FILE = Path(__file__).resolve().parent / "studentMarks.txt"
MAXIMUM_COURSEWORK_MARK = 60
MAXIMUM_EXAM_MARK = 100
MAXIMUM_OVERALL_MARK = MAXIMUM_COURSEWORK_MARK + MAXIMUM_EXAM_MARK
BACKGROUND_COLOR = "#F3ECE7"
SIDEBAR_COLOR = "#2A1A35"
PRIMARY_RED = "#681F32"
PRIMARY_RED_DARK = "#4E1727"
SECONDARY_COLOR = "#C59A82"
TEXT_COLOR = "#2A1A35"
MUTED_TEXT_COLOR = "#806559"
TABLE_BORDER_COLOR = "#CDBBB1"


@dataclass
class StudentRecord:
    """Store one student's validated details and calculated results."""

    student_number: int
    student_name: str
    coursework_marks: list[int]
    exam_mark: int

    @property
    def coursework_total(self) -> int:
        return sum(self.coursework_marks)

    @property
    def overall_mark(self) -> int:
        return self.coursework_total + self.exam_mark

    @property
    def percentage(self) -> float:
        return self.overall_mark / MAXIMUM_OVERALL_MARK * 100

    @property
    def grade(self) -> str:
        if self.percentage >= 70:
            return "A"
        if self.percentage >= 60:
            return "B"
        if self.percentage >= 50:
            return "C"
        if self.percentage >= 40:
            return "D"
        return "F"

    def to_file_line(self) -> str:
        coursework = ",".join(str(mark) for mark in self.coursework_marks)
        return (
            f"{self.student_number},{self.student_name},"
            f"{coursework},{self.exam_mark}"
        )


class StudentManager:
    """Provide the GUI and operations for managing student records."""

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.window.title("Student Record Manager")
        self.window.geometry("980x650")
        self.window.minsize(820, 560)
        self.window.configure(bg=BACKGROUND_COLOR)

        self.students: list[StudentRecord] = []
        self.load_students()
        self.create_widgets()
        self.view_all_students()

    def load_students(self) -> None:
        """Load and validate records while reporting bad source-file data."""
        try:
            with STUDENT_DATA_FILE.open("r", encoding="utf-8") as student_file:
                lines = [line.strip() for line in student_file if line.strip()]

            if not lines:
                messagebox.showerror("File error", "The student data file is empty.")
                return

            try:
                declared_count = int(lines[0])
            except ValueError:
                messagebox.showerror(
                    "File error",
                    "The first line must contain the number of students.",
                )
                return

            invalid_lines: list[str] = []
            for line_number, line in enumerate(lines[1:], start=2):
                student = self.parse_student(line)
                if student is None:
                    invalid_lines.append(str(line_number))
                else:
                    self.students.append(student)

            if len(self.students) != declared_count:
                messagebox.showwarning(
                    "Student count warning",
                    f"The file declares {declared_count} students, "
                    f"but {len(self.students)} valid records were loaded.",
                )

            if invalid_lines:
                messagebox.showwarning(
                    "Invalid records",
                    "Skipped invalid data on lines: " + ", ".join(invalid_lines),
                )

        except FileNotFoundError:
            messagebox.showerror(
                "File error",
                f"Could not find {STUDENT_DATA_FILE}",
            )
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror(
                "File error",
                f"Could not read {STUDENT_DATA_FILE}: {error}",
            )

    def parse_student(self, student_line: str) -> StudentRecord | None:
        """Convert a correctly formatted CSV line into a StudentRecord."""
        fields = [field.strip() for field in student_line.split(",")]
        if len(fields) != 6:
            return None

        try:
            student_number = int(fields[0])
            coursework_marks = [int(fields[index]) for index in range(2, 5)]
            exam_mark = int(fields[5])
        except ValueError:
            return None

        student_name = fields[1]
        if not student_name:
            return None
        if not 1000 <= student_number <= 9999:
            return None
        if any(mark < 0 or mark > 20 for mark in coursework_marks):
            return None
        if not 0 <= exam_mark <= 100:
            return None

        return StudentRecord(
            student_number,
            student_name,
            coursework_marks,
            exam_mark,
        )

    def save_students(self) -> bool:
        """Save all in-memory records and return whether the save succeeded."""
        temporary_file = STUDENT_DATA_FILE.with_suffix(".txt.tmp")

        try:
            with temporary_file.open("w", encoding="utf-8") as student_file:
                student_file.write(f"{len(self.students)}\n")
                for student in self.students:
                    student_file.write(student.to_file_line() + "\n")

            temporary_file.replace(STUDENT_DATA_FILE)
            return True
        except OSError as error:
            messagebox.showerror(
                "Save error",
                f"Could not save {STUDENT_DATA_FILE}: {error}",
            )
            return False

    def create_widgets(self) -> None:
        """Create the application menu, search tools, table, and summary area."""
        title = tk.Label(
            self.window,
            text="STUDENT RECORD MANAGEMENT",
            font=("Consolas", 20, "bold"),
            fg="#FFFFFF",
            bg=SIDEBAR_COLOR,
            anchor="w",
            padx=18,
        )
        title.pack(fill="x", ipady=13)

        main_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        main_frame.pack(fill="both", expand=True, padx=14, pady=14)

        menu_frame = tk.Frame(main_frame, bg=SIDEBAR_COLOR, padx=12, pady=12)
        menu_frame.pack(side="left", fill="y", padx=(0, 14))

        menu_options = [
            ("1. View all records", self.view_all_students),
            ("2. Find a student", self.find_student),
            ("3. Highest overall mark", self.show_highest),
            ("4. Lowest overall mark", self.show_lowest),
            ("5. Sort ascending", self.sort_ascending),
            ("6. Sort descending", self.sort_descending),
            ("7. Add student", self.add_student),
            ("8. Delete student", self.delete_student),
            ("9. Update student", self.update_student),
        ]

        for label, action in menu_options:
            tk.Button(
                menu_frame,
                text=label,
                width=23,
                command=action,
                font=("Segoe UI", 9, "bold"),
                fg=TEXT_COLOR,
                bg=SECONDARY_COLOR,
                activebackground="#B7846D",
                relief="flat",
                anchor="w",
                padx=10,
                cursor="hand2",
            ).pack(fill="x", pady=3, ipady=5)

        output_frame = tk.Frame(
            main_frame,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground=TABLE_BORDER_COLOR,
        )
        output_frame.pack(side="right", fill="both", expand=True)

        search_frame = tk.Frame(output_frame, bg="#FFFFFF")
        search_frame.pack(fill="x", padx=16, pady=(12, 6))

        tk.Label(
            search_frame,
            text="Quick search:",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_COLOR,
            bg="#FFFFFF",
        ).pack(side="left")

        self.search_text = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_text,
            width=32,
            font=("Segoe UI", 10),
        )
        search_entry.pack(side="left", padx=8)
        search_entry.bind("<Return>", lambda event: self.search_students())

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_students,
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg=PRIMARY_RED,
            activebackground=PRIMARY_RED_DARK,
            relief="flat",
            padx=10,
            pady=4,
        ).pack(side="left")

        header_frame = tk.Frame(output_frame, bg="#FFFFFF")
        header_frame.pack(fill="x", padx=16, pady=(6, 8))

        self.output_heading = tk.Label(
            header_frame,
            text="All Student Records",
            font=("Segoe UI", 15, "bold"),
            fg=TEXT_COLOR,
            bg="#FFFFFF",
            anchor="w",
        )
        self.output_heading.pack(side="left", fill="x", expand=True)

        self.output_summary = tk.Label(
            header_frame,
            text="",
            font=("Segoe UI", 9),
            fg=MUTED_TEXT_COLOR,
            bg="#FFFFFF",
            anchor="e",
        )
        self.output_summary.pack(side="right")

        table_frame = tk.Frame(output_frame, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        columns = (
            "name",
            "number",
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

        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure(
            "Student.Treeview",
            background="#FFFFFF",
            foreground=TEXT_COLOR,
            fieldbackground="#FFFFFF",
            rowheight=38,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Student.Treeview.Heading",
            background=SECONDARY_COLOR,
            foreground=TEXT_COLOR,
            font=("Segoe UI", 9, "bold"),
        )

        headings = [
            ("name", "STUDENT NAME", 180),
            ("number", "NUMBER", 90),
            ("coursework", "COURSEWORK", 105),
            ("exam", "EXAM", 75),
            ("total", "TOTAL", 75),
            ("percentage", "PERCENTAGE", 105),
            ("grade", "GRADE", 65),
        ]
        for column, heading, width in headings:
            self.output.heading(column, text=heading)
            self.output.column(column, width=width, minwidth=65, anchor="center")
        self.output.column("name", anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.output.yview,
        )
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_records(
        self,
        records: list[StudentRecord],
        heading: str,
    ) -> None:
        """Display records and calculate a summary for the displayed selection."""
        self.output_heading.config(text=heading)

        for table_item in self.output.get_children():
            self.output.delete(table_item)

        if not records:
            self.output_summary.config(text="0 records")
            return

        for student in records:
            self.output.insert(
                "",
                tk.END,
                values=(
                    student.student_name,
                    student.student_number,
                    f"{student.coursework_total} / 60",
                    f"{student.exam_mark} / 100",
                    f"{student.overall_mark} / 160",
                    f"{student.percentage:.1f}%",
                    student.grade,
                ),
            )

        average_percentage = (
            sum(student.percentage for student in records) / len(records)
        )
        record_word = "record" if len(records) == 1 else "records"
        self.output_summary.config(
            text=(
                f"{len(records)} {record_word}  |  "
                f"Average {average_percentage:.1f}%"
            )
        )

    def view_all_students(self) -> None:
        self.show_records(self.students, "All Student Records")

    def search_students(self) -> None:
        """Search by full or partial name, or by exact student number."""
        search_term = self.search_text.get().strip().lower()
        if not search_term:
            self.view_all_students()
            return

        matching_students = [
            student
            for student in self.students
            if search_term in student.student_name.lower()
            or search_term == str(student.student_number)
        ]
        self.show_records(matching_students, f"Search Results: {search_term}")

    def find_student_by_number(self, dialog_title: str) -> StudentRecord | None:
        student_number_text = simpledialog.askstring(
            dialog_title,
            "Enter a student number or name:",
            parent=self.window,
        )
        if student_number_text is None:
            return None

        search_text = student_number_text.strip().lower()
        matches = [
            student
            for student in self.students
            if search_text in student.student_name.lower()
            or search_text == str(student.student_number)
        ]

        if not matches:
            messagebox.showinfo("Student not found", "No matching student was found.")
            return None
        if len(matches) == 1:
            return matches[0]

        selection = simpledialog.askinteger(
            "Choose a student",
            "More than one student matched. Enter the exact student number:",
            parent=self.window,
        )
        if selection is None:
            return None
        return next(
            (student for student in matches if student.student_number == selection),
            None,
        )

    def find_student(self) -> None:
        student = self.find_student_by_number("Find a student")
        if student is not None:
            self.show_records([student], "Individual Student Record")

    def show_highest(self) -> None:
        if not self.students:
            messagebox.showinfo("No records", "There are no student records.")
            return
        highest = max(self.students, key=lambda student: student.overall_mark)
        self.show_records([highest], "Student with the Highest Total")

    def show_lowest(self) -> None:
        if not self.students:
            messagebox.showinfo("No records", "There are no student records.")
            return
        lowest = min(self.students, key=lambda student: student.overall_mark)
        self.show_records([lowest], "Student with the Lowest Total")

    def sort_ascending(self) -> None:
        sorted_students = sorted(
            self.students,
            key=lambda student: student.overall_mark,
        )
        self.show_records(sorted_students, "Records Sorted: Ascending")

    def sort_descending(self) -> None:
        sorted_students = sorted(
            self.students,
            key=lambda student: student.overall_mark,
            reverse=True,
        )
        self.show_records(sorted_students, "Records Sorted: Descending")

    def ask_for_details(
        self,
        existing_student: StudentRecord | None = None,
    ) -> StudentRecord | None:
        """Ask for, validate, and return a complete student record."""
        initial_number = (
            existing_student.student_number
            if existing_student is not None
            else None
        )
        student_number = simpledialog.askinteger(
            "Student details",
            "Enter a student number from 1000 to 9999:",
            initialvalue=initial_number,
            minvalue=1000,
            maxvalue=9999,
            parent=self.window,
        )
        if student_number is None:
            return None

        for student in self.students:
            if (
                student.student_number == student_number
                and student is not existing_student
            ):
                messagebox.showerror(
                    "Number already used",
                    "Each student must have a unique student number.",
                )
                return None

        initial_name = (
            existing_student.student_name
            if existing_student is not None
            else ""
        )
        student_name = simpledialog.askstring(
            "Student details",
            "Enter the student's name:",
            initialvalue=initial_name,
            parent=self.window,
        )
        if student_name is None:
            return None

        student_name = student_name.strip()
        if not student_name or "," in student_name:
            messagebox.showerror(
                "Invalid name",
                "Enter a name that does not contain a comma.",
            )
            return None

        coursework_marks: list[int] = []
        for mark_number in range(1, 4):
            initial_mark = (
                existing_student.coursework_marks[mark_number - 1]
                if existing_student is not None
                else None
            )
            coursework_mark = simpledialog.askinteger(
                "Student details",
                f"Enter coursework mark {mark_number} (0 to 20):",
                initialvalue=initial_mark,
                minvalue=0,
                maxvalue=20,
                parent=self.window,
            )
            if coursework_mark is None:
                return None
            coursework_marks.append(coursework_mark)

        initial_exam = (
            existing_student.exam_mark
            if existing_student is not None
            else None
        )
        exam_mark = simpledialog.askinteger(
            "Student details",
            "Enter the exam mark (0 to 100):",
            initialvalue=initial_exam,
            minvalue=0,
            maxvalue=100,
            parent=self.window,
        )
        if exam_mark is None:
            return None

        return StudentRecord(
            student_number,
            student_name,
            coursework_marks,
            exam_mark,
        )

    def add_student(self) -> None:
        new_student = self.ask_for_details()
        if new_student is None:
            return

        original_students = self.students.copy()
        self.students.append(new_student)
        if self.save_students():
            self.view_all_students()
            messagebox.showinfo("Student added", "The student record was added.")
        else:
            self.students = original_students

    def delete_student(self) -> None:
        student = self.find_student_by_number("Delete a student")
        if student is None:
            return

        confirmed = messagebox.askyesno(
            "Confirm deletion",
            f"Delete the record for {student.student_name}?",
        )
        if not confirmed:
            return

        original_students = self.students.copy()
        self.students.remove(student)
        if self.save_students():
            self.view_all_students()
            messagebox.showinfo("Student deleted", "The student record was deleted.")
        else:
            self.students = original_students

    def update_student(self) -> None:
        old_student = self.find_student_by_number("Update a student")
        if old_student is None:
            return

        updated_student = self.ask_for_details(old_student)
        if updated_student is None:
            return

        original_students = self.students.copy()
        student_index = self.students.index(old_student)
        self.students[student_index] = updated_student
        if self.save_students():
            self.view_all_students()
            messagebox.showinfo(
                "Student updated",
                "The student record was updated.",
            )
        else:
            self.students = original_students


def main() -> None:
    window = tk.Tk()
    StudentManager(window)
    window.mainloop()


if __name__ == "__main__":
    main()
