"""
Author: Ryan Fernando
Date 8/05/2026
Purpose: To create a program using complex techniques to help students improve their math skills by creating an interactive quiz-like math game.
Version: 2.0
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== Main window =====

# Main class to manage the page switching controls
class App(tk.Tk):
    # Main window
    def __init__(self):
        """
        Since 'tk.Tk' is the main class' parameter, this tells the program that 'self' is reffered to it in order to set the GUI.
        This is similar to declaring a 'root' variable as 'tk.Tk()'.
        """
        super().__init__()
        self.title("Flow Computing")
        self.state('zoomed')

        # Get app favicon path and load it to replace the default tkinter favicon
        app_favicon = tk.PhotoImage(file=os.path.join(BASE_DIR, "images", "app_favicon.png"))
        self.iconphoto(True, app_favicon)

        # Frame container for the app's pages
        page_container = tk.Frame(self)
        page_container.pack(fill="both", expand=True)

        # Array to store each page
        self.pages = {}

        # Create pages and add them to the array defined above
        for P in (WelcomeScreen, LobbyScreen):
            page = P(page_container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        # Display welcome screen when program is first executed
        self.display_page(WelcomeScreen)

    # Function to display specified page
    def display_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

# ===== Classes for each page =====
# These are displayed via the main app class

# Welcome Screen window containing the login, signup, and quit buttons
class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# Lobby screen containing the difficulty levels, leaderboard button, and button to view user's previous scores
class LobbyScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)



# Initialises the code when the program starts running, and puts the GUI window into a permanent loop to prevent it from closing.
if __name__ == "__main__":
    app = App()
    app.mainloop()
