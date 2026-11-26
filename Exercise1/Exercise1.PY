"""A 10 question arithmetic quiz with three difficulty levels."""

import random
import tkinter as tk
from tkinter import ttk


QUESTION_COUNT = 10
POINTS_FIRST_ATTEMPT = 10
POINTS_SECOND_ATTEMPT = 5

# Each difficulty maps to the inclusive minimum and maximum used when generating numbers.
DIFFICULTY_RANGES = {
    "Easy": (0, 9),
    "Medium": (10, 99),
    "Hard": (1000, 9999),
}


def randomInt(difficulty):
    """Return a randomly generated number from the selected difficulty level."""
    minimum, maximum = DIFFICULTY_RANGES[difficulty]
    return random.randint(minimum, maximum)


def decideOperation():
    """Randomly choose and return either the addition or subtraction symbol."""
    return random.choice(["+", "-"])


def displayMenu(parent, choose_difficulty):
    """Build the difficulty menu and connect each button to its selection callback."""
    ttk.Label(
        parent,
        text="READY?",
        style="Eyebrow.TLabel",
    ).pack(pady=(8, 2))

    ttk.Label(
        parent,
        text="Choose your difficulty",
        style="Header.TLabel",
    ).pack(pady=(0, 18))

    descriptions = {
        "Easy": "Single-digit numbers",
        "Medium": "Two-digit numbers",
        "Hard": "Four-digit numbers",
    }

    for difficulty, description in descriptions.items():
        ttk.Button(
            parent,
            text=f"{difficulty} ({description})",
            command=lambda d=difficulty: choose_difficulty(d),
            style="Difficulty.TButton",
        ).pack(fill="x", ipady=7, pady=5)


def displayProblem(parent, question_text, answer_callback):
    """Display the current arithmetic question and prepare the answer entry box."""
    question_label = ttk.Label(
        parent,
        text=question_text,
        style="Question.TLabel",
    )
    question_label.pack(pady=(12, 8))

    instruction_label = ttk.Label(
        parent,
        text="Enter your answer below and press Enter to submit.",
        style="Muted.TLabel",
    )
    instruction_label.pack(pady=(8, 8))

    answer_entry = ttk.Entry(
        parent,
        font=("Segoe UI", 14),
        justify="center",
        width=14,
    )
    answer_entry.pack(pady=6)
    answer_entry.bind("<Return>", answer_callback)
    answer_entry.focus_set()

    submit_button = ttk.Button(
        parent,
        text="Submit answer",
        command=lambda: answer_callback(None),
        style="Primary.TButton",
    )
    submit_button.pack(pady=10, ipady=4)

    feedback_label = ttk.Label(parent, style="Feedback.TLabel")
    feedback_label.pack(pady=4)

    return question_label, answer_entry, feedback_label


def isCorrectAnswer(user_answer, correct_answer):
    """Compare the submitted answer with the solution and return whether they match."""
    return user_answer == correct_answer


def displayFinalScore(parent, score, replay_callback):
    """Display the final score and select a grade and message that match the result."""
    if score >= 90:
        grade = "A"
        message = "Excellent job!"
    elif score >= 80:
        grade = "B"
        message = "Good work!"
    elif score >= 70:
        grade = "C"
        message = "You passed!"
    elif score >= 60:
        grade = "D"
        message = "You barely passed!"
    else:
        grade = "F"
        message = "Try again and see if you can improve your score!"

    ttk.Label(
        parent,
        text="Quiz Complete!",
        style="Header.TLabel",
    ).pack(pady=(4, 16))

    ttk.Label(
        parent,
        text=f"Your final score is: {score}/100",
        style="Score.TLabel",
    ).pack(pady=6)

    ttk.Label(
        parent,
        text=f"Your grade is: {grade}",
        style="Score.TLabel",
    ).pack(pady=4)

    ttk.Label(parent, text=message, style="Muted.TLabel").pack(pady=(4, 16))
    ttk.Label(parent, text="Would you like to play again?", style="Replay.TLabel").pack(pady=(4, 8))

    buttons = ttk.Frame(parent)
    buttons.pack()
    ttk.Button(
        buttons,
        text="Yes",
        command=replay_callback,
        style="Primary.TButton",
    ).pack(side="left", padx=6, ipadx=8, ipady=4)
    ttk.Button(
        buttons,
        text="No",
        command=parent.winfo_toplevel().destroy,
        style="Secondary.TButton",
    ).pack(
        side="left",
        padx=6,
        ipadx=8,
        ipady=4,
    )


class MathsQuiz:
    """Manage the quiz interface, question flow, answer checking, and score."""

    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz")
        self.root.geometry("520x440")
        self.root.minsize(460, 380)
        self.root.configure(bg="#EDF7FA")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#EDF7FA")
        self.style.configure("Header.TLabel", font=("Trebuchet MS", 22, "bold"), foreground="#123A55", background="#EDF7FA")
        self.style.configure("Eyebrow.TLabel", font=("Trebuchet MS", 9, "bold"), foreground="#5C7F91", background="#EDF7FA")
        self.style.configure("Question.TLabel", font=("Trebuchet MS", 30, "bold"), foreground="#123A55", background="#EDF7FA")
        self.style.configure("Score.TLabel", font=("Trebuchet MS", 17, "bold"), foreground="#123A55", background="#EDF7FA")
        self.style.configure("Muted.TLabel", font=("Segoe UI", 10), foreground="#5C7F91", background="#EDF7FA")
        self.style.configure("Feedback.TLabel", font=("Segoe UI", 11, "bold"), foreground="#087EA4", background="#EDF7FA")
        self.style.configure("Replay.TLabel", font=("Segoe UI", 11, "bold"), foreground="#123A55", background="#EDF7FA")
        self.style.configure("TLabel", font=("Segoe UI", 11), foreground="#123A55", background="#EDF7FA")
        self.style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#123A55")
        self.style.configure("Difficulty.TButton", font=("Segoe UI", 11, "bold"), foreground="#123A55", background="#FFFFFF")
        self.style.map("Difficulty.TButton", background=[("active", "#D6EEF5")])
        self.style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), foreground="#FFFFFF", background="#087EA4")
        self.style.map("Primary.TButton", background=[("active", "#05657F")])
        self.style.configure("Secondary.TButton", font=("Segoe UI", 11, "bold"), foreground="#123A55", background="#CCE5EC")
        self.style.map("Secondary.TButton", background=[("active", "#B8DAE4")])

        self.main_frame = ttk.Frame(self.root, padding=32)
        self.main_frame.pack(fill="both", expand=True, padx=24, pady=24)

        self.score = 0
        self.current_question = 0
        self.attempt_number = 1
        self.difficulty = None
        self.first_number = 0
        self.second_number = 0
        self.operation = "+"
        self.correct_answer = 0
        self.question_label = None
        self.answer_entry = None
        self.feedback_label = None
        self.status_label = None

        self.show_menu()

    def clear_screen(self):
        """Remove all current widgets from the main frame before changing screens."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_menu(self):
        """Reset the quiz state and display the available difficulty levels."""
        self.clear_screen()
        self.score = 0
        self.current_question = 0
        self.attempt_number = 1
        self.difficulty = None
        displayMenu(self.main_frame, self.choose_difficulty)

    def choose_difficulty(self, difficulty):
        """Start the quiz using the selected difficulty."""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.attempt_number = 1
        self.show_question()

    def show_question(self):
        """Display the current question and its answer controls."""
        self.clear_screen()
        self.new_problem()
        question_text = f"{self.first_number} {self.operation} {self.second_number} = ?"
        (
            self.question_label,
            self.answer_entry,
            self.feedback_label,
        ) = displayProblem(
            self.main_frame,
            question_text,
            self.submit_answer,
        )
        self.update_status()

    def new_problem(self):
        """Generate a new pair of numbers and operation, then calculate the solution."""
        self.first_number = randomInt(self.difficulty)
        self.second_number = randomInt(self.difficulty)
        self.operation = decideOperation()

        if self.operation == "+":
            self.correct_answer = self.first_number + self.second_number
        else:
            self.correct_answer = self.first_number - self.second_number

        self.attempt_number = 1

    def submit_answer(self, event=None):
        """Check the user's answer and move forward after first or second attempts."""
        answer_text = self.answer_entry.get().strip()
        if not answer_text:
            self.feedback_label.config(text="Please enter an answer.")
            return

        try:
            user_answer = int(answer_text)
        except ValueError:
            self.feedback_label.config(text="Please enter a whole number.")
            return

        if isCorrectAnswer(user_answer, self.correct_answer):
            if self.attempt_number == 1:
                self.score += POINTS_FIRST_ATTEMPT
                self.feedback_label.config(text="Correct!")
            else:
                self.score += POINTS_SECOND_ATTEMPT
                self.feedback_label.config(text="Correct!")
            self.next_question()
        elif self.attempt_number == 1:
            self.attempt_number = 2
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus_set()
            self.feedback_label.config(text="Incorrect. Try once more.")
            self.update_status()
        else:
            self.feedback_label.config(
                text=f"Incorrect. The correct answer is {self.correct_answer}.",
            )
            self.next_question()

    def next_question(self):
        """Advance to the next problem or show the final score."""
        self.current_question += 1
        if self.current_question >= QUESTION_COUNT:
            self.show_final_score()
        else:
            self.show_question()

    def update_status(self):
        """Update or create the score and question status label."""
        if self.status_label is not None:
            self.status_label.destroy()

        self.status_label = ttk.Label(
            self.main_frame,
            text=f"Question {self.current_question + 1} of {QUESTION_COUNT} | Score: {self.score}",
        )
        self.status_label.pack(pady=(12, 0))

    def show_final_score(self):
        """Clear the question screen and display the final result."""
        self.clear_screen()
        displayFinalScore(self.main_frame, self.score, self.show_menu)


if __name__ == "__main__":
    root = tk.Tk()
    quiz = MathsQuiz(root)
    root.mainloop()
