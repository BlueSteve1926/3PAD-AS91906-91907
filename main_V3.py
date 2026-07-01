"""
Author: Ryan Fernando
Date 8/05/2026
Purpose: To create a program using complex techniques to help students improve their math skills by creating an interactive quiz-like math game.
Version: 3.0
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

"""
This gets the absolute path of the files' directory, so it opens the files which are used in the program.
It is important so the program can run properly while getting all the relevant files,
regardless of which device it is being run on and where or how the program is run.
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NUM_QUESTIONS = 10
NUM_LIVES = 3
TIME_GIVEN = 300 # 5 minutes

# ==================================================

# ===== Values for styling are stored here =====

# Variables which store colours to prevent reusing hex codes
DIFFICULTY_COLOURS = {
    "Easy": "#00FF00",
    "Medium": "#F89D1F",
    "Hard": "#FF0000",
    "Challenge": "#9820C5"
}

# ==================================================

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

        # Style variable for ttk widgets
        self.style = ttk.Style()

        # Set theme for ttk widgets
        self.style.theme_use('alt')

        # ===== Dictionaries for user accounts (username and pasword) and the scores of all users =====

        # Dictionary for user accounts (username and pasword)
        self.accounts = {}
        # Previous scores of every user
        self.previous_scores = {}

        # ==================================================

        # ===== Configured ttk styles which will be used across multiple widgets =====

        # Style for 'Back' buttons
        self.style.configure("Back.TButton", font=("TkDefaultFont", 20), background="#FFFFFF")

        # Style for 'show password' button
        self.style.configure("ShowPassword.TButton", font=("TkDefaultFont", 26), background="#FFFFFF")       

        # ==================================================

        # ===== Program images =====

        # Stores all the images which the program can locate without errors
        self.images = {}

        # The images and their path which the program is meant to locate
        image_files = {
            "hide_password": {
                "name": "hide_password.png",
                "dimensions": (40, 40)
            },
            "show_password": {
                "name": "show_password.png",
                "dimensions": (40, 40)
            }
        }

        # A list containing the missing images
        missing_images = []

        # Favicon error message if favicon is missing
        error_msg_favicon = None

        # Function to display a messagebox of all missing images
        def img_error_messages(list):
            # Generate error message for missing images
            if list:
                # String variable for error message
                error_message = "Unable to display the following images:"

                # Add each missing image to error message
                for missing_image in list:
                    error_message += f"\n- {missing_image}"

                messagebox.showwarning("Warning!", error_message)
            
            # Generate error emssages for missing favicon
            if error_msg_favicon:
                messagebox.showwarning("Warning!", error_msg_favicon)

        # Validate image whether it exists and can be opened and stored in the image list without issues
        for image_name, image_attributes, in image_files.items():
            try:
                file_path = os.path.join(BASE_DIR, "images", image_attributes["name"])

                pil_initialisation = Image.open(file_path)
                pil_initialisation = pil_initialisation.resize(image_attributes["dimensions"])

                self.images[image_name] = ImageTk.PhotoImage(pil_initialisation)
            except FileNotFoundError:
                self.images[image_name] = None
                missing_images.append(image_name)

        # ==================================================

        # Get app favicon path and load it to replace the default tkinter favicon
        try:
            app_favicon = tk.PhotoImage(file=os.path.join(BASE_DIR, "images", "app_favicon.png"))
            self.iconphoto(True, app_favicon)
        except tk.TclError as e:
            error_msg_favicon = f"Program favicon image not found!\n{e}"

        # Frame container for the app's pages
        page_container = tk.Frame(self)
        page_container.pack(fill="both", expand=True)

        # Adjusts grid position to centre widgets
        page_container.grid_rowconfigure(0, weight=1)
        page_container.grid_columnconfigure(0, weight=1)

        # Array to store each page
        self.pages = {}

        # Create pages and add them to the array defined above
        for P in (
            WelcomeScreen,
            LoginScreen,
            SignupScreen,
            LobbyScreen,
            LeaderboardScreen,
            PersonalScoresScreen,
            InstructionsScreen,
            QuizScreen,
            ResultsScreen
            ):
            page = P(page_container, self)
            self.pages[P] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        # Display welcome screen when program is first executed
        self.display_page(WelcomeScreen)

        # Wait until program fully loads before displaying error messages if any
        self.after(50, lambda: img_error_messages(missing_images))

    # Function to display specified page
    def display_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

        # If a page as a "refresh" function
        if hasattr(page, "refresh"):
            page.refresh()

    # Function to show and hide password field (replaces characters with dots)
    def password_visibility(self, field, button, visibility):
        if visibility:
            field.configure(show="")

            # Check if button has working image
            if self.images.get("show_password") and self.images.get("hide_password"):
                button.configure(image=self.images["show_password"])
            else:
                button.configure(text="Hide Password")
        
        else:
            field.configure(show="*")

            if self.images.get("show_password") and self.images.get("hide_password"):
                button.configure(image=self.images["hide_password"])
            else:
                button.configure(text="Show Password")

# ==================================================

# ===== Classes for each page =====
# These are displayed via the main app class

# Welcome Screen window containing the login, signup, and quit buttons
class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Create title label
        title_frame = tk.Frame(self)
        title_frame.pack(pady=10)

        title_label = ttk.Label(title_frame, text="Welcome!", font=("TkDefaultFont", 75))
        title_label.pack()

        # Create subheader
        subheader_text = ttk.Label(title_frame, text="You may login to your account, or sign up if you don't have one.", font=("TkDefaultFont", 25))
        subheader_text.pack(pady=5)

        # Create frame for login and sign up buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(expand=True)

        # Style for login and sign up buttons
        controller.style.configure("Accounts.TButton", font=("TkDefaultFont", 30), background="#FFFFFF")

        # Style for quit program button
        controller.style.configure("Quit.TButton", font=("TkDefaultFont", 30), background="#FF0000", foreground="#FFFFFF")
        controller.style.map("Quit.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Create login button
        login_btn = ttk.Button(buttons_frame, text="Login", style="Accounts.TButton", width="8", command=lambda: controller.display_page(LoginScreen))
        login_btn.pack(pady=10)

        # Create sign up button
        signup_btn = ttk.Button(buttons_frame, text="Sign Up", style="Accounts.TButton", width="8", command=lambda: controller.display_page(SignupScreen))
        signup_btn.pack()

        # Create quit program button
        signup_btn = ttk.Button(buttons_frame, text="Quit", style="Quit.TButton", width="8", command=controller.destroy)
        signup_btn.pack(pady=50)

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)

# Login screen
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Reference for main 'App' method
        self.controller = controller

        # Create title label
        title_frame = tk.Frame(self)
        title_frame.pack(pady=50)

        title_label = ttk.Label(title_frame, text="Login", font=("TkDefaultFont", 50))
        title_label.pack()

        # Create subheader
        subheader_text = ttk.Label(title_frame, text="Please enter your correct account details.", font=("TkDefaultFont", 25))
        subheader_text.pack(pady=5)

        # Button to go back to welcome screen
        returnback_btn = ttk.Button(self, text="Back", style="Back.TButton", width="5", command=lambda: controller.display_page(WelcomeScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Login buttons frame
        login_frame = tk.Frame(self)
        login_frame.pack(pady=(100, 0))

        # Username entry label
        username_label = ttk.Label(login_frame, text="Username:", font=("TkDefaultFont", 30))
        username_label.grid(row=0, column=0, padx=10, pady=25)

        # Username entry field
        self.username_entry = ttk.Entry(login_frame, font=("TkDefaultFont", 30))
        self.username_entry.grid(row=0, column=1, padx=10, pady=25)

        # Password entry label
        password_label = ttk.Label(login_frame, text="Password:", font=("TkDefaultFont", 30))
        password_label.grid(row=1, column=0, padx=10)

        # Password entry field
        self.password_entry = ttk.Entry(login_frame, font=("TkDefaultFont", 30), show="*")
        self.password_entry.grid(row=1, column=1, padx=10)

        # Show/hide password button
        self.show_password_btn = ttk.Button(login_frame, style="ShowPassword.TButton", command=self.showhide_password)

        # Check if button's images are missing or not, otherwise replace with text
        if controller.images.get("hide_password") and controller.images.get("show_password"):
            self.show_password_btn.configure(image=controller.images["hide_password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

        self.show_password_btn.grid(row=1, column=2)

        # Style for 'Login' button
        controller.style.configure("Login.TButton", font=("TkDefaultFont", 30), background="#00AC00", foreground="#FFFFFF")
        controller.style.map("Login.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Login button
        login_btn = ttk.Button(self, text="Login", style="Login.TButton", width=8)
        login_btn.pack(pady=50)

        # Boolean variable for password visibility (initially false)
        self.password_visibility = False
    
    # Reset page so when user returns, the page returns to how it looked like initially
    def refresh(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.password_visibility = False
        
        # Check if button's images are missing or not
        if self.controller.images.get("hide_password") and self.controller.images.get("show_password"):
            self.show_password_btn.configure(image=self.controller.images["hide_password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

    # Function to toggle password visibility by checking and changing state of the boolean variable
    def showhide_password(self):
        # Changes boolean value from 'False' to 'True' and vice versa
        self.password_visibility = not self.password_visibility

        # Update widget configurations
        self.controller.password_visibility(self.password_entry, self.show_password_btn, self.password_visibility)

# Sign up screen
class SignupScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Reference for main 'App' method
        self.controller = controller

        # Create title label
        title_frame = tk.Frame(self)
        title_frame.pack(pady=50)

        title_label = ttk.Label(title_frame, text="Sign Up", font=("TkDefaultFont", 50))
        title_label.pack()

        # Create subheader
        subheader_text = ttk.Label(title_frame, text="Please enter a username and a strong password.", font=("TkDefaultFont", 25))
        subheader_text.pack(pady=5)

        # Button to go back to welcome screen
        returnback_btn = ttk.Button(self, text="Back", style="Back.TButton", width="5", command=lambda: controller.display_page(WelcomeScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Login buttons frame
        signup_frame = tk.Frame(self)
        signup_frame.pack(pady=(100, 0))

        # Username entry label
        username_label = ttk.Label(signup_frame, text="Username:", font=("TkDefaultFont", 30))
        username_label.grid(row=0, column=0, padx=10, pady=25)

        # Username entry field
        self.username_entry = ttk.Entry(signup_frame, font=("TkDefaultFont", 30))
        self.username_entry.grid(row=0, column=1, padx=10, pady=25)

        # Password entry label
        password_label = ttk.Label(signup_frame, text="Password:", font=("TkDefaultFont", 30))
        password_label.grid(row=1, column=0, padx=10)

        # Password entry field
        self.password_entry = ttk.Entry(signup_frame, font=("TkDefaultFont", 30), show="*")
        self.password_entry.grid(row=1, column=1, padx=10)

        # Show/hide password button
        self.show_password_btn = ttk.Button(signup_frame, style="ShowPassword.TButton", command=self.showhide_password)

        # Check if button's images are missing or not, otherwise replace with text
        if controller.images.get("hide_password") and controller.images.get("show_password"):
            self.show_password_btn.configure(image=controller.images["hide_password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

        self.show_password_btn.grid(row=1, column=2)

        # Style for 'Signup' button
        controller.style.configure("Signup.TButton", font=("TkDefaultFont", 30), background="#FFFFFF")

        # Signup button
        signup_btn = ttk.Button(self, text="Sign Up", style="Signup.TButton", width=8)
        signup_btn.pack(pady=50)

        # Boolean variable for password visibility (initially false)
        self.password_visibility = False
    
    # Reset page so when user returns, the page returns to how it looked like initially
    def refresh(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.password_visibility = False
        
        # Check if button's images are missing or not
        if self.controller.images.get("hide_password") and self.controller.images.get("show_password"):
            self.show_password_btn.configure(image=self.controller.images["hide_password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

    # Function to toggle password visibility by checking and changing state of the boolean variable
    def showhide_password(self):
        # Changes boolean value from 'False' to 'True' and vice versa
        self.password_visibility = not self.password_visibility

        # Update widget configurations
        self.controller.password_visibility(self.password_entry, self.show_password_btn, self.password_visibility)

# Lobby screen containing the difficulty levels, leaderboard button, and button to view user's previous scores
class LobbyScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# Leaderboard page showing the top scores of every registered user ranked by score (then by time remaining if there are identical highest scores)
class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# Displays all the user's previous scores (results history)
class PersonalScoresScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# Displays the instructions for each difficulty before commencing the game
class InstructionsScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# Displays the quiz and loads the random generated questions to the user to answer
class QuizScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# This displays the user's score and results after completing the quiz, and then stores it in the data file (.json) containing every user's previous scores.
class ResultsScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

# ==================================================

# ===== Main program functions =====



# ==================================================

# This initialises the code when the program starts running, and puts the GUI window into a permanent loop to prevent it from closing.
if __name__ == "__main__":
    app = App()
    app.mainloop()
