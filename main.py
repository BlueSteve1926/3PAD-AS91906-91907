"""
Author: Ryan Fernando
Date 8/05/2026
Purpose: To create a program using complex techniques to help students improve their math skills by creating an interactive quiz-like math game.
Version: 1.0
"""

# ===== Modules imported =====

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import random
import time
import json
from PIL import Image, ImageTk
import winsound
import sympy
from sympy import symbols, diff, simplify, sympify

# ===== Constants created =====

NUM_QUESTIONS = 10

"""
This gets the absolute path of the files' directory, so it opens the files which are used in the program.
It is important so the program can run properly while getting all the relevant files,
regardless of which device it is being run on and where or how the program is run.
"""
base_dir = os.path.dirname(os.path.abspath(__file__))

# ===== Main window =====

# Main class to manage the page switching controls
class App(tk.Tk):
    # Main window
    def __init__(self):
        # Since 'tk.Tk' is the main class' parameter, this tells the program that 'self' is reffered to it in order to set the GUI. This is similar to declaring a 'root' variable as 'tk.Tk()'.
        super().__init__()
        self.title("Flow Computing")
        self.state('zoomed')

        # Get app favicon path
        app_favicon = tk.PhotoImage(file=os.path.join(base_dir, "images", "app_favicon.png"))
        # Load favicon
        self.iconphoto(True, app_favicon)

# Welcome Screen window containing the login, signup, and quit buttons


# Initialises the code when the program starts running, and puts the GUI window into a permanent loop to prevent it from closing.
if __name__ == "__main__":
    app = App()
    app.mainloop()
