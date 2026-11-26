"""Tkinter joke assistant that reads and displays jokes from a text file."""

import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


JOKES_FILE = Path(__file__).resolve().parent / "randomJokes.txt"


def load_jokes(filepath: Path) -> list[tuple[str, str]]:
    """Read valid joke setup and punchline pairs from a text file."""
    jokes: list[tuple[str, str]] = []

    try:
        with filepath.open("r", encoding="utf-8") as joke_file:
            for file_line in joke_file:
                file_line = file_line.strip()

                if "?" not in file_line:
                    continue

                setup, punchline = file_line.split("?", 1)
                setup = setup.strip() + "?"
                punchline = punchline.strip()

                if setup != "?" and punchline:
                    jokes.append((setup, punchline))
    except OSError as file_error:
        messagebox.showerror(
            "File error",
            f"Could not find or open the jokes file:\n{filepath}\n\n{file_error}",
        )

    return jokes


class JokeAssistant:
    """Manage joke selection and the Tkinter interface."""

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.window.title("Alexa, Tell Me a Joke")
        self.window.geometry("560x460")
        self.window.minsize(500, 420)
        self.window.configure(bg="#092D3D")

        self.available_jokes = load_jokes(JOKES_FILE)
        self.current_joke: tuple[str, str] | None = None
        self.create_widgets()

    def create_widgets(self) -> None:
        """Create the title, joke display, and control buttons."""
        main_frame = tk.Frame(
            self.window,
            padx=28,
            pady=22,
            bg="#092D3D",
        )
        main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            main_frame,
            text="ALEXA'S\nLAUGH ROOM",
            font=("Georgia", 24, "bold"),
            fg="#EAFBFF",
            bg="#092D3D",
            justify="center",
        )
        title_label.pack(pady=(2, 12))

        self.setup_label = tk.Label(
            main_frame,
            text="Click the button to get a joke.",
            font=("Trebuchet MS", 15),
            fg="#F7F3FF",
            bg="#164C66",
            relief="flat",
            padx=18,
            pady=16,
            wraplength=440,
            justify="center",
        )
        self.setup_label.pack(fill="x", pady=(0, 8))

        self.punchline_label = tk.Label(
            main_frame,
            text="",
            font=("Georgia", 14, "italic"),
            fg="#66D9EF",
            bg="#092D3D",
            wraplength=440,
            justify="center",
        )
        self.punchline_label.pack(pady=(8, 12), fill="x")

        primary_button_row = tk.Frame(main_frame, bg="#092D3D")
        primary_button_row.pack(pady=4)

        self.tell_button = tk.Button(
            primary_button_row,
            text="Alexa, tell me a joke",
            command=self.tell_joke,
            width=17,
            font=("Trebuchet MS", 10, "bold"),
            fg="#082D3B",
            bg="#66D9EF",
            activebackground="#9CE8F5",
            activeforeground="#082D3B",
            relief="flat",
            cursor="hand2",
        )
        self.tell_button.pack(side="left", padx=5, ipadx=4, ipady=7)

        self.punchline_button = tk.Button(
            primary_button_row,
            text="Show punchline",
            command=self.show_punchline,
            state="disabled",
            width=17,
            font=("Trebuchet MS", 10, "bold"),
            fg="#FFFFFF",
            bg="#087EA4",
            disabledforeground="#789CAB",
            activebackground="#0796BC",
            relief="flat",
            cursor="hand2",
        )
        self.punchline_button.pack(side="left", padx=5, ipadx=4, ipady=7)

        secondary_button_row = tk.Frame(main_frame, bg="#092D3D")
        secondary_button_row.pack(pady=(10, 0))

        tk.Button(
            secondary_button_row,
            text="Next joke",
            command=self.tell_joke,
            width=12,
            font=("Trebuchet MS", 9, "bold"),
            fg="#EAFBFF",
            bg="#1F6682",
            activebackground="#2A7D9A",
            relief="flat",
            cursor="hand2",
        ).pack(side="left", padx=5, ipady=6)

        tk.Button(
            secondary_button_row,
            text="Quit",
            command=self.window.destroy,
            width=12,
            font=("Trebuchet MS", 9, "bold"),
            fg="#EAFBFF",
            bg="#1F6682",
            activebackground="#2A7D9A",
            relief="flat",
            cursor="hand2",
        ).pack(side="left", padx=5, ipady=6)

        if not self.available_jokes:
            self.tell_button.config(state="disabled")
            self.setup_label.config(
                text="No jokes are available. Check the jokes file.",
            )

    def tell_joke(self) -> None:
        """Select a new joke, avoiding the joke currently on screen."""
        if not self.available_jokes:
            return

        unshown_jokes = [
            joke
            for joke in self.available_jokes
            if joke != self.current_joke
        ]
        if not unshown_jokes:
            unshown_jokes = self.available_jokes

        self.current_joke = random.choice(unshown_jokes)
        setup, _ = self.current_joke
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.punchline_button.config(state="normal")

    def show_punchline(self) -> None:
        """Display the punchline for the selected joke."""
        if self.current_joke is not None:
            _, punchline = self.current_joke
            self.punchline_label.config(text=punchline)


def main() -> None:
    window = tk.Tk()
    JokeAssistant(window)
    window.mainloop()


if __name__ == "__main__":
    main()
