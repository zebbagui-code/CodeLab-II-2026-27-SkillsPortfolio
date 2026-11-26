"""A tkinter joke assistant that reads jokes from the supplied text file."""

import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


def load_jokes(filepath):
    """Read valid joke setup and punchline pairs from a text file."""
    jokes = []

    try:
        with filepath.open("r", encoding="utf-8") as joke_file:
            for line in joke_file:
                line = line.strip()

                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    setup = setup.strip() + "?"
                    punchline = punchline.strip()

                    if setup != "?" and punchline:
                        jokes.append((setup, punchline))

    except OSError:
        messagebox.showerror(
            "File error",
            f"Could not find or open the jokes\n{filepath}",
        )

    return jokes

def tell_joke():
    """Chooses a random joke and displays its setup."""
    global current_joke

    if jokes:
        current_joke = random.choice(jokes)
        setup_label.config(text=current_joke[0])
        punchline_label.config(text="")
        punchline_button.config(state="normal")


def show_punchline():
    """Display the punchline for the joke that is currently on screen."""
    if current_joke:
        punchline_label.config(text=current_joke[1])


# Load the jokes and keep track of the joke currently being shown.
jokes_file = (
    Path(__file__).resolve().parent
    / "Assessment 1 - Skills Portfolio"
    / "A1 - Resources"
    / "randomJokes.txt"
)
jokes = load_jokes(jokes_file)
current_joke = None

# Create the main application window.
window = tk.Tk()
window.title("Alexa, Tell Me a Joke")
window.geometry("560x460")
window.minsize(500, 420)
window.configure(bg="#092D3D")

# Add a frame to keep the labels and buttons neatly arranged.
main_frame = tk.Frame(window, padx=28, pady=22, bg="#092D3D")
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

setup_label = tk.Label(
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
setup_label.pack(fill="x", pady=(0, 8))

punchline_label = tk.Label(
    main_frame,
    text="",
    font=("Georgia", 14, "italic"),
    fg="#66D9EF",
    bg="#092D3D",
    wraplength=440,
    justify="center",
)
punchline_label.pack(pady=(8, 12), fill="x")

button_row = tk.Frame(main_frame, bg="#092D3D")
button_row.pack(pady=4)

# Connect each button to the function that handles its action.
tell_button = tk.Button(
    button_row,
    text="TELL A JOKE",
    command=tell_joke,
    width=15,
    font=("Trebuchet MS", 10, "bold"),
    fg="#082D3B",
    bg="#66D9EF",
    activebackground="#9CE8F5",
    activeforeground="#082D3B",
    relief="flat",
    cursor="hand2",
)
tell_button.pack(side="left", padx=5, ipadx=4, ipady=7)

punchline_button = tk.Button(
    button_row,
    text="PUNCHLINE",
    command=show_punchline,
    state="disabled",
    width=15,
    font=("Trebuchet MS", 10, "bold"),
    fg="#FFFFFF",
    bg="#087EA4",
    disabledforeground="#789CAB",
    activebackground="#0796BC",
    relief="flat",
    cursor="hand2",
)
punchline_button.pack(side="left", padx=5, ipadx=4, ipady=7)

bottom_row = tk.Frame(main_frame, bg="#092D3D")
bottom_row.pack(pady=(10, 0))

next_button = tk.Button(
    bottom_row,
    text="NEXT",
    command=tell_joke,
    width=12,
    font=("Trebuchet MS", 9, "bold"),
    fg="#EAFBFF",
    bg="#1F6682",
    activebackground="#2A7D9A",
    relief="flat",
)
next_button.pack(side="left", padx=5, ipady=6)

quit_button = tk.Button(
    bottom_row,
    text="EXIT",
    command=window.destroy,
    width=12,
    font=("Trebuchet MS", 9, "bold"),
    fg="#EAFBFF",
    bg="#1F6682",
    activebackground="#2A7D9A",
    relief="flat",
)
quit_button.pack(side="left", padx=5, ipady=6)

# Disable joke buttons if the file was empty or could not be loaded.
if not jokes:
    tell_button.config(state="disabled")
    next_button.config(state="disabled")
    setup_label.config(text="No jokes are available. Check the jokes file.")

# Keep the window open and respond to button clicks.
window.mainloop()