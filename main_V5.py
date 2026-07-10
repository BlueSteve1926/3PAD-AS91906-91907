"""
Author: Ryan Fernando
Date 8/05/2026
Purpose: To create a program using complex techniques to help students improve their math skills by creating an interactive quiz-like math game.
Version: 5.0
"""

# ===== Modules imported =====

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import random
import math
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

# Maximum and minimum length for each login/signup field
MIN_ENTRY_LEN_USERNAME = 6
MIN_ENTRY_LEN_PASSWORD = 8
MAX_ENTRY_LEN_USERNAME = 20
MAX_ENTRY_LEN_PASSWORD = 32

# Number of questions for each quiz
NUM_QUESTIONS = 10

# Total number of lives given
NUM_LIVES = 3

# Total amount of time given (5 minutes)
TIME_GIVEN = 300

# Game difficultyies
DIFFICULTIES = ["Easy", "Medium", "Hard", "Challenge"]

# Lives symbols in case the images do not work
AVALIABLE_LIVE_TEXT = "♥"
UNAVALIABLE_LIVE_TEXT = "♡"

# Variable for the guide on the general gameplay
GENERAL_GUIDE = """
You will be given a total of 5 minutes to complete the quiz. There are 10 questions to answer altogether. You will be given 3 lives in total, where each wrong answer takes 1 away.

Once you complete the quiz, your score will be stored to your personal record of previous scores. They can be viewed in the 'Previous Scores' page. 

Make sure to answer every question, and make sure you do not run out of time or lives. You need to score at least 1 point to win.

You may click 'Start' when you're ready. Good luck!
"""

# Responses if user answers correctly
CORRECT_ANSWER_RESPONSES = [
    "Great Job!",
    "Keep It Up!",
    "Welldone!",
    "Awesome!",
    "Incredible!",
    "Fantastic!"
    ]

# Responses if user answers correctly
INCORRECT_ANSWER_RESPONSES = [
    "Incorrect.",
    "Sorry, incorrect.",
    "Sorry, wrong answer.",
    "Oops!",
    "Yikes!"
]

# ==================================================

# ===== Values for styling are stored here =====

# Variables which store colours to prevent reusing hex codes
DIFFICULTY_COLOURS = {
    "Easy": "#00DA00",
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
        # Current user logged in
        self.current_user = ""

        # Declare file names and paths
        self.accounts_filename = "accounts_registered.json"
        self.accounts_filepath = os.path.join(BASE_DIR, self.accounts_filename)
        self.previous_scores_filename = "previous_scores.json"
        self.previous_scores_filepath = os.path.join(BASE_DIR, self.previous_scores_filename)

        # Store existing registered accounts to 'accounts' dictionary
        try:
            with open(self.accounts_filepath, "r", encoding="utf-8") as j:
                self.accounts = json.load(j)
        except:
            self.accounts = {}

        # Store existing previous scores of all accounts to 'previous_scores' dictionary
        try:
            with open(self.previous_scores_filepath, "r", encoding="utf-8") as j:
                self.previous_scores = json.load(j)
        except:
            self.previous_scores = {}
        
        # ==================================================
        
        # ===== The question types for each difficulty =====

        self.question_types = {
            "Easy": {
                "Squares Addition": {
                    "Question": "{a}² + {b}²",
                    "Random Values": lambda: {
                        "a": random.randint(1, 12),
                        "b": random.randint(1, 12)
                    },
                    "Answer": lambda a, b: math.pow(a, 2) + math.pow(b, 2)
                },

                "Squares Subtraction": {
                    "Question": "{a}² − {b}²",
                    "Random Values": lambda: {
                        "a": random.randint(1, 10),
                        "b": random.randint(1, 10)
                    },
                    "Answer": lambda a, b: math.pow(a, 2) - math.pow(b, 2)
                },

                "Square Roots Addition": {
                    "Question": "√{a} + √{b}",
                    "Random Values": lambda: {
                        "a": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]),
                        "b": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
                    },
                    "Answer": lambda a, b: math.sqrt(a) + math.sqrt(b)
                },

                "Square Roots Subtraction": {
                    "Question": "√{a} − √{b}",
                    "Random Values": lambda: {
                        "a": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]),
                        "b": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
                    },
                    "Answer": lambda a, b: math.sqrt(a) - math.sqrt(b)
                }
            }
        }

        # ==================================================

        # ===== Variables for the gameplay =====

        # Selected difficulty
        self.selected_difficulty = ""

        # Dictionary of generated questions containing the question displayed and the correct answer
        self.questions = {}

        # Current question (initially set to 'None)
        self.question_number = None

        # User score (out of 10) (initially set to 'None')
        self.total_score = None

        # Number of lives (initially set to 'None')
        self.lives_count = None

        # The time remaining on the countdown timer (initially set to 'None')
        self.time_remaining = None

        # Boolean variable for whether user has won or not (initially set to 'None')
        self.haswon = None

        # ==================================================

        # ===== Configured ttk styles which will be used across multiple widgets =====

        # Style for 'return back' buttons
        self.style.configure("ReturnBack.TButton", font=("TkDefaultFont", 25), background="#FFFFFF")

        # Style for 'show password' button
        self.style.configure("ShowPassword.TButton", font=("TkDefaultFont", 26), background="#FFFFFF")

        # Style for labels requiring borders
        self.style.configure("OutlinedLabels.TLabel", borderwidth=2, relief="solid")

        # ==================================================

        # ===== Program images =====

        # Stores all the images which the program can locate without errors
        self.images = {}

        # The images and their path which the program is meant to locate
        image_files = {
            "Hide Password": {
                "name": "hide_password.png",
                "dimensions": (40, 40)
            },
            "Show Password": {
                "name": "show_password.png",
                "dimensions": (40, 40)
            },
            "Avaliable Live": {
                "name": "lives_avaliable.png",
                "dimensions": (32, 32)
            },
            "Unavaliable Live": {
                "name": "lives_unavaliable.png",
                "dimensions": (32, 32)
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

        # Assigns variables which contain a lambda function for specified entry limit criteria for entry fields
        self.username_limit = self.register(lambda val: self.entry_limit(val, MAX_ENTRY_LEN_USERNAME))
        self.password_limit = self.register(lambda val: self.entry_limit(val, MAX_ENTRY_LEN_PASSWORD))

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

    # Function to prevent actions for entry fields restricting specific keyboard shortcuts
    def block_action(self, event=None):
        # Return an unused string value to stop the action from triggering
        return "break"

    # Function to show and hide password field (replaces characters with dots)
    def password_visibility(self, field, button, visibility):
        if visibility:
            field.configure(show="")

            # Check if button has working image
            if self.images.get("Show Password") and self.images.get("Hide Password"):
                button.configure(image=self.images["Show Password"])
            else:
                button.configure(text="Hide Password")
        
        else:
            field.configure(show="*")

            if self.images.get("Show Password") and self.images.get("Hide Password"):
                button.configure(image=self.images["Hide Password"])
            else:
                button.configure(text="Show Password")
    
    # Character limit for entry fields
    def entry_limit(self, value, max_len):
        # Checks if the entry field character length exceeds the maximum length
        if len(value) > max_len:
            return False
        
        # Returns true to allow user to continue typing in entry field
        return True
    
    # Generates questions based on difficulty selected
    def generate_questions(self, difficulty):
        # The dictionary of questions (initially empty)
        quiz_questions = {}

        # Variable to keep track of used questions to prevent duplicates (created as an unordered set of values)
        used_questions = set()

        # The dictionary of existing question types based on difficulty
        existing_questions = self.question_types[difficulty]

        # Generate 10 random questions
        for i in range(NUM_QUESTIONS):
            while True:
                # Select random question type
                question_type = random.choice(list(existing_questions))

                # Get selected question data
                question_data = existing_questions[question_type]

                # Generate random values for the question
                rand_values = question_data["Random Values"]()

                # Substitute placeholder variables with the random generated values
                question = question_data["Question"].format(**rand_values) # '**rand_values' unpacks the substituted values

                # Break 'while' loop if the question generated is unique
                if question not in used_questions:
                    used_questions.add(question)
                    break

            # Calculate the correct answer of the question
            answer = question_data["Answer"](**rand_values)

            # Check if answer is an integer
            if isinstance(answer, float) and answer.is_integer():
                answer = int(answer)
            
            # Convert answer to string before storing
            answer = str(answer)

            # Store question and answer to its question number
            quiz_questions[i + 1] = {
                "Question": question,
                "Answer": answer
            }
        
        # Return function's dictionary variable to be assigned to the universal questions dictionary
        return quiz_questions
    
    # The function which initialises the variables and assets
    def gameplay(self):
        # Set question number to '1'
        self.question_number = 1

        # Set score to '0'
        self.total_score = 0

        # Set number of lives
        self.lives_count = NUM_LIVES

        # Set time remaining
        self.time_remaining = TIME_GIVEN

        # Display quiz screen
        self.display_page(QuizScreen)

        # Load game assets
        self.pages[QuizScreen].load_assets()

        # Start timer
        self.pages[QuizScreen].update_timer()

        # Update question-related widgets
        self.pages[QuizScreen].update_questions()

    # Checks user's answer
    def check_answer(self, user_answer):
        # Remove any leading or trailing spaces
        user_answer = user_answer.lower().strip()

        # Check if user input is empty
        if not user_answer:
            return

        # If correct
        if user_answer == self.questions[self.question_number]["Answer"]:
            # Add 1 to total score
            self.total_score += 1

            # Display feedback to user
            self.pages[QuizScreen].display_feedback()
        
        # If incorrect
        else:
            # Update amount of lives displayed
            self.pages[QuizScreen].remove_life()

            # Display feedback to user
            self.pages[QuizScreen].display_feedback(incorrectly_answered=True)

            if self.lives_count > 0:
                # Remove 1 life
                self.lives_count -= 1

        # Stop time when lives reaches 0 to prevent time being the real reason for loss
        if self.lives_count == 0:
            # Cancel the timer
            self.pages[QuizScreen].cancel_timer()

    # Ends the game and decides whether the user has won or not
    def end_game(self):
        # Checks if user's score is above 0 and if all questions have been answered
        if self.total_score > 0 and self.question_number == NUM_QUESTIONS and self.time_remaining != 0:
            # User has won
            self.haswon = True

            # Cancel the timer
            self.pages[QuizScreen].cancel_timer()

            # Display results screen
            self.display_page(ResultsScreen)

        # If user runs out of lives        
        elif self.lives_count == 0:
            # User has lost
            self.haswon = False

            # Display results screen
            self.display_page(ResultsScreen)
        
        # If user runs out of time
        elif self.time_remaining == 0:
            # User has lost
            self.haswon = False

            # Cancel the timer
            self.pages[QuizScreen].cancel_timer()

            # Display results screen
            self.display_page(ResultsScreen)

    # The function for containing every function related to the quiz setup and control
    def start_game(self):
        self.questions = self.generate_questions(self.selected_difficulty)
        self.gameplay()

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
        subheader_text = ttk.Label(title_frame, text="You may log in to your account, or sign up if you don't have one.", font=("TkDefaultFont", 25))
        subheader_text.pack(pady=5)

        # Create frame for login and signup buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(expand=True)

        # Style for login and signup buttons
        controller.style.configure("Accounts.TButton", font=("TkDefaultFont", 30), background="#FFFFFF")

        # Style for quit program button
        controller.style.configure("Quit.TButton", font=("TkDefaultFont", 30), background="#FF0000", foreground="#FFFFFF")
        controller.style.map("Quit.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Create login button
        login_btn = ttk.Button(buttons_frame, text="Login", style="Accounts.TButton", width=8, command=lambda: controller.display_page(LoginScreen))
        login_btn.pack(pady=10)

        # Create signup button
        signup_btn = ttk.Button(buttons_frame, text="Sign Up", style="Accounts.TButton", width=8, command=lambda: controller.display_page(SignupScreen))
        signup_btn.pack()

        # Create quit program button
        signup_btn = ttk.Button(buttons_frame, text="Quit", style="Quit.TButton", width=8, command=controller.destroy)
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
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(WelcomeScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Login buttons frame
        login_frame = tk.Frame(self)
        login_frame.pack(pady=(100, 0))

        # Username entry label
        username_label = ttk.Label(login_frame, text="Username:", font=("TkDefaultFont", 30))
        username_label.grid(row=0, column=0, padx=10, pady=25, sticky="e")

        # Username entry field
        self.username_entry = ttk.Entry(login_frame, font=("TkDefaultFont", 30), width=25, validate="key", validatecommand=(controller.username_limit, "%P"))
        self.username_entry.grid(row=0, column=1, padx=10, pady=25)

        # Password entry label
        password_label = ttk.Label(login_frame, text="Password:", font=("TkDefaultFont", 30))
        password_label.grid(row=1, column=0, padx=10, sticky="e")

        # Password entry field
        self.password_entry = ttk.Entry(login_frame, font=("TkDefaultFont", 30), width=25, show="*", validate="key", validatecommand=(controller.password_limit, "%P"))
        self.password_entry.grid(row=1, column=1, padx=10)

        # Prevent exporting selected text in password entry
        self.password_entry.configure(exportselection=False)

        # Prevent user from pasting text in password entry
        self.password_entry.bind("<<Paste>>", controller.block_action)

        # Prevent user from copying text in password entry
        self.password_entry.bind("<<Copy>>", controller.block_action)
        # Prevent user from cutting text in password entry
        self.password_entry.bind("<<Cut>>", controller.block_action)

        # Prevent user from pasting text in password entry using mouse middle-click (for Linux/X11 users)
        self.password_entry.bind("<Button-2>", controller.block_action)

        # Show/hide password button
        self.show_password_btn = ttk.Button(login_frame, style="ShowPassword.TButton", command=self.showhide_password)
        self.show_password_btn.grid(row=1, column=2)

        # Style for 'Login' button
        controller.style.configure("Login.TButton", font=("TkDefaultFont", 30), background="#00AC00", foreground="#FFFFFF")
        controller.style.map("Login.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Login button
        login_btn = ttk.Button(self, text="Log In", style="Login.TButton", width=8, command=lambda: self.login_func(controller.accounts))
        login_btn.pack(pady=50)

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)

        # Boolean variable for password visibility (initially false)
        self.password_visibility = False
    
    # Reset page so when user returns, the page returns to how it looked like initially
    def refresh(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.password_visibility = False
        
        # Check if button's images are missing or not
        if self.controller.images.get("Hide Password") and self.controller.images.get("Show Password"):
            self.show_password_btn.configure(image=self.controller.images["Hide Password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

    # Function to toggle password visibility by checking and changing state of the boolean variable
    def showhide_password(self):
        # Changes boolean value from 'False' to 'True' and vice versa
        self.password_visibility = not self.password_visibility

        # Update widget configurations
        self.controller.password_visibility(self.password_entry, self.show_password_btn, self.password_visibility)
    
    # Validate user's signup details and appends it to the .json of accounts, and then signs user in
    def login_func(self, accounts_dict):
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        # Validate username
        if not entered_username: # If entry is blank
            messagebox.showerror("Invalid Input!", "Username cannot be empty!")
            return
        elif any(char.isspace() for char in entered_username): # If entry contains spaces
            messagebox.showerror("Invalid Input!", "Username cannot contain spaces (use underscores instead)!")
            return
        elif len(entered_username) < MIN_ENTRY_LEN_USERNAME: # If entry is less than the minimum length required
            messagebox.showerror("Invalid Input!", "Username must contain 6 or more characters!")
            return
        elif not entered_username.replace("_", "").isalnum(): # If entry contains symbols other than underscores
            messagebox.showerror("Invalid Input!", "Username cannot contain symbols other than underscores!")
            return
        
        # Validate password
        if not entered_password: # If entry is blank
            messagebox.showerror("Invalid Input!", "Password cannot be empty!")
            return
        elif any(char.isspace() for char in entered_password): # If entry contains spaces
            messagebox.showerror("Invalid Input!", "Password cannot contain spaces!")
            return
        elif len(entered_password) < MIN_ENTRY_LEN_PASSWORD: # If entry is less than the minimum length required
            messagebox.showerror("Invalid Input!", "Password must contain 8 or more characters!")
            return
        
        # Variable for username but lowercase to prevent case-sensitivity in username entry
        username_lower = entered_username.lower()

        # Convert all registered accounts' usernames to lowercase for the same reason as the previous comment
        accounts_lower = {key.lower(): value for key, value, in accounts_dict.items()}

        # Check if username and password matches
        if not username_lower in [accounts.lower() for accounts in accounts_dict] or accounts_lower[username_lower] != entered_password:
            messagebox.showwarning("Warning!", "Incorrect username or password entered!")
            return
        
        # Variable for the original case of the username
        username_original = next((key for key in accounts_dict if key.lower() == username_lower), None) # Assigns 'None' if there aren't any matches
        
        # Set 'current_user' variable as the username of the user logged in
        self.controller.current_user = username_original

        # Display info message
        messagebox.showinfo("Access Granted!", f"You have successfully logged into your account as {username_original}!")

        # Display lobby screen
        self.controller.display_page(LobbyScreen)


# Signup screen
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
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(WelcomeScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Login buttons frame
        signup_frame = tk.Frame(self)
        signup_frame.pack(pady=(100, 0))

        # Username entry label
        username_label = ttk.Label(signup_frame, text="Username:", font=("TkDefaultFont", 30))
        username_label.grid(row=0, column=0, padx=10, pady=25, sticky="e")

        # Username entry field
        self.username_entry = ttk.Entry(signup_frame, font=("TkDefaultFont", 30), width=25, validate="key", validatecommand=(controller.username_limit, "%P"))
        self.username_entry.grid(row=0, column=1, padx=10, pady=25)

        # Password entry label
        password_label = ttk.Label(signup_frame, text="Password:", font=("TkDefaultFont", 30))
        password_label.grid(row=1, column=0, padx=10, sticky="e")

        # Password entry field
        self.password_entry = ttk.Entry(signup_frame, font=("TkDefaultFont", 30), width=25, show="*", validate="key", validatecommand=(controller.password_limit, "%P"))
        self.password_entry.grid(row=1, column=1, padx=10)

        # Confirm password entry label
        password_label = ttk.Label(signup_frame, text="Confirm Password:", font=("TkDefaultFont", 30))
        password_label.grid(row=2, column=0, padx=10, pady=25, sticky="e")

        # Confirm password entry field
        self.confirm_entry = ttk.Entry(signup_frame, font=("TkDefaultFont", 30), width=25, show="*", validate="key", validatecommand=(controller.password_limit, "%P"))
        self.confirm_entry.grid(row=2, column=1, padx=10, pady=25)

        # Prevent exporting selected text in password entries
        self.password_entry.configure(exportselection=False)
        self.confirm_entry.configure(exportselection=False)

        # Prevent user from pasting text in password entries
        self.password_entry.bind("<<Paste>>", controller.block_action)
        self.confirm_entry.bind("<<Paste>>", controller.block_action)

        # Prevent user from copying text in password entries
        self.password_entry.bind("<<Copy>>", controller.block_action)
        self.confirm_entry.bind("<<Copy>>", controller.block_action)

        # Prevent user from cutting text in password entries
        self.password_entry.bind("<<Cut>>", controller.block_action)
        self.confirm_entry.bind("<<Cut>>", controller.block_action)

        # Prevent user from pasting text in password entries using mouse middle-click (for Linux/X11 users)
        self.password_entry.bind("<Button-2>", controller.block_action)
        self.confirm_entry.bind("<Button-2>", controller.block_action)

        # Show/hide password button
        self.show_password_btn = ttk.Button(signup_frame, style="ShowPassword.TButton", command=self.showhide_password)
        self.show_password_btn.grid(row=1, column=2)

        # Style for 'Signup' button
        controller.style.configure("Signup.TButton", font=("TkDefaultFont", 30), background="#FFFFFF")

        # Signup button
        signup_btn = ttk.Button(self, text="Sign Up", style="Signup.TButton", width=8, command=lambda: self.signup_func(controller.accounts, controller.accounts_filepath))
        signup_btn.pack(pady=50)

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)

        # Boolean variable for password visibility (initially false)
        self.password_visibility = False
    
    # Reset page so when user returns, the page returns to how it looked like initially
    def refresh(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.confirm_entry.configure(show="*")
        self.password_visibility = False
        
        # Check if button's images are missing or not
        if self.controller.images.get("Hide Password") and self.controller.images.get("Show Password"):
            self.show_password_btn.configure(image=self.controller.images["Hide Password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

    # Function to toggle password visibility by checking and changing state of the boolean variable
    def showhide_password(self):
        # Changes boolean value from 'False' to 'True' and vice versa
        self.password_visibility = not self.password_visibility

        # Update widget configurations
        self.controller.password_visibility(self.password_entry, self.show_password_btn, self.password_visibility)
        self.controller.password_visibility(self.confirm_entry, self.show_password_btn, self.password_visibility)

    # Validate user's signup details and appends it to the .json of accounts, and then signs user in
    def signup_func(self, accounts_dict, file):
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()
        confirmed_password = self.confirm_entry.get().strip()

        # Validate username
        if not entered_username: # If entry is blank
            messagebox.showerror("Invalid Input!", "Username cannot be empty!")
            return
        elif any(char.isspace() for char in entered_username): # If entry contains spaces
            messagebox.showerror("Invalid Input!", "Username cannot contain spaces (use underscores instead)!")
            return
        elif len(entered_username) < MIN_ENTRY_LEN_USERNAME: # If entry is less than the minimum length required
            messagebox.showerror("Invalid Input!", "Username must contain 6 or more characters!")
            return
        elif not entered_username.replace("_", "").isalnum(): # If entry contains symbols other than underscores
            messagebox.showerror("Invalid Input!", "Username cannot contain symbols other than underscores!")
            return
        
        # Variable for username but lowercase to prevent case-sensitivity in username entry
        username_lower = entered_username.lower()
        
        # Check if username already exists (not case sensative)
        if username_lower in [accounts.lower() for accounts in accounts_dict]:
            messagebox.showerror("Username Already Taken!", f"{entered_username} has already been taken! Please enter a different username.")
            return
        
        # Validate password
        if not entered_password: # If entry is blank
            messagebox.showerror("Invalid Input!", "Password cannot be empty!")
            return
        elif any(char.isspace() for char in entered_password): # If entry contains spaces
            messagebox.showerror("Invalid Input!", "Password cannot contain spaces!")
            return
        elif len(entered_password) < MIN_ENTRY_LEN_PASSWORD: # If entry is less than the minimum length required
            messagebox.showerror("Invalid Input!", "Password must contain 8 or more characters!")
            return
        
        # Check if confirmation password field is empty or not
        if not confirmed_password: # If entry is blank
            messagebox.showerror("Invalid Input!", "Confirmed password cannot be empty!")
            return
        elif confirmed_password != entered_password: # Check if confirm password exactly matches entered password
            messagebox.showwarning("Warning!", "The passwords you entered do not match!")
            return
        
        # Save username and password to .json file
        try:
            # Add username and password to dictionary
            accounts_dict[entered_username] = entered_password

            # Write to .json file
            with open(file, "w", encoding="utf-8") as f:
                # Append to file
                json.dump(accounts_dict, f, indent=4)
        except Exception as e:
            # Display error message
            messagebox.showerror("Error!", f"Failed to save account details to .json file:\n{e}.")
            # Remove recently added dictionary item
            del accounts_dict[entered_username]
            return
        
        # Set 'current_user' variable as the username of the user logged in
        self.controller.current_user = entered_username

        # Display info message
        messagebox.showinfo("Account Successfully Created!", f"You have successfully registered your account as {entered_username}!")

        # Display lobby screen
        self.controller.display_page(LobbyScreen)


# Lobby screen containing the difficulty levels, leaderboard button, and button to view user's previous scores
class LobbyScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Reference for main 'App' method
        self.controller = controller

        # Create title label
        title_frame = tk.Frame(self)
        title_frame.pack(pady=50)

        title_label = ttk.Label(title_frame, text="Select a Difficulty Level", font=("TkDefaultFont", 50))
        title_label.pack()

        # Create username label
        self.username_label = ttk.Label(title_frame, font=("TkDefaultFont", 25))
        self.username_label.pack(pady=30)

        # Create frame for difficulty selection buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=(125, 0))

        # Create logout button
        logout_btn = ttk.Button(self, text="Log Out", style="ReturnBack.TButton", width=8, command=self.logout_func)
        logout_btn.place(relx=1, rely=0, x=-20, y=20, anchor="ne")

        # ===== All difficulty buttons =====

        # Style for 'Easy' mode button
        controller.style.configure("Easy.TButton", font=("TkDefaultFont", 30), background=DIFFICULTY_COLOURS["Easy"], foreground="#FFFFFF")
        controller.style.map("Easy.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Style for 'Medium' mode button
        controller.style.configure("Medium.TButton", font=("TkDefaultFont", 30), background=DIFFICULTY_COLOURS["Medium"], foreground="#FFFFFF")
        controller.style.map("Medium.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Style for 'Hard' mode button
        controller.style.configure("Hard.TButton", font=("TkDefaultFont", 30), background=DIFFICULTY_COLOURS["Hard"], foreground="#FFFFFF")
        controller.style.map("Hard.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Style for 'Challenge' mode button
        controller.style.configure("Challenge.TButton", font=("TkDefaultFont", 30), background=DIFFICULTY_COLOURS["Challenge"], foreground="#FFFFFF")
        controller.style.map("Challenge.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Easy mode
        easy_btn = ttk.Button(buttons_frame, text="Easy", style="Easy.TButton", width=10, command=lambda: self.establish_difficulty(DIFFICULTIES[0]))
        easy_btn.pack(pady=(0, 20))

        # Medium mode
        medium_btn = ttk.Button(buttons_frame, text="Medium", style="Medium.TButton", width=10)
        medium_btn.pack(pady=(0, 20))

        # Hard mode
        hard_btn = ttk.Button(buttons_frame, text="Hard", style="Hard.TButton", width=10)
        hard_btn.pack(pady=(0, 20))

        # Challenge mode
        challenge_btn = ttk.Button(buttons_frame, text="Challenge", style="Challenge.TButton", width=10)
        challenge_btn.pack()

        # ==================================================

        # Style for 'View Leaderboard' button
        controller.style.configure("ViewLeaderboard.TButton", font=("TkDefaultFont", 25), anchor="center", justify="center", background="#FFFFFF")

        # Create 'View Leaderboard' button
        leaderboard_btn = ttk.Button(self, text="View\nLeaderboard", style="ViewLeaderboard.TButton", width=12, command=lambda: controller.display_page(LeaderboardScreen))
        leaderboard_btn.place(relx=0, rely=0, x=20, y=20)

        # Style for 'Previous Scores' button
        controller.style.configure("PreviousScores.TButton", font=("TkDefaultFont", 30), anchor="center", justify="center", background="#FFFFFF")

        # Create 'Previous Scores' button
        previous_scores_btn = ttk.Button(self, text="Previous\nScores", style="PreviousScores.TButton", width=10, command=lambda: controller.display_page(PersonalScoresScreen))
        previous_scores_btn.pack(pady=(50, 0))

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)
    
    # Reset page so when user returns, the page returns to how it looked like initially
    def refresh(self):
        self.username_label.configure(text=self.controller.current_user)
    
    # Function for the logging out
    def logout_func(self):
        # Display 'yes-no' message
        if messagebox.askyesno("Confirm Log Out", "Are you sure you want to log out?\nMake sure you remember your account password the next you log in!"):
            # Set 'current_user' variable as 'None'
            self.controller.current_user = None
            # Configure lobby screen username label to an empty string
            self.username_label.configure(text="")

            # Return to welcome screen
            self.controller.display_page(WelcomeScreen)
    
    # The function to get the selected difficulty based on the difficulty selected via button click. This then takes them to the instructions window with the instructions based on the selected difficulty.
    def establish_difficulty(self, chosen_difficulty):
        # Set selected difficulty
        self.controller.selected_difficulty = chosen_difficulty

        # Take user to the instructions screen before beginning the quiz
        self.controller.display_page(InstructionsScreen)

        self.controller.pages[InstructionsScreen].load_instructions()


# Leaderboard page showing the top scores of every registered user ranked by score (then by time remaining if there are identical highest scores)
class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Button to go back to lobby screen
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(LobbyScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)


# Displays all the user's previous scores (results history)
class PersonalScoresScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Button to go back to lobby screen
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(LobbyScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)


# Displays the instructions for each difficulty before commencing the game
class InstructionsScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Reference for main 'App' method
        self.controller = controller

        # Create title label
        title_label = ttk.Label(self, text="How To Play", font=("TkDefaultFont", 50))
        title_label.pack(pady=50)

        # Button to go back to lobby screen
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=self.cancel_game)
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        #Create frame for main contents
        main_frame = tk.Frame(self, width=1000, height=650)
        main_frame.pack()
        main_frame.pack_propagate(False)
        main_frame.grid_propagate(False)
        
        # Configures the alignments for its child widgets
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Top bar and contents frame
        topbar = tk.Frame(main_frame, borderwidth=3, relief="solid")
        topbar.grid(row=0, column=0, sticky="ew")

        # Contents frame
        contents_frame = tk.Frame(main_frame, borderwidth=3, relief="solid")
        contents_frame.grid(row=1, column=0, sticky="nsew")

        # Create main frame header (goes in topbar)
        instructions_header = ttk.Label(topbar, text="Instructions", font=("TkDefaultFont", 25))
        instructions_header.pack(pady=5)

        # Create instructions text (goes in contents frame)
        self.instructions_text = ttk.Label(contents_frame, font=("TkDefaultFont", 15), wraplength=975, justify="left")
        self.instructions_text.pack(pady=5)

        # Style for 'Start' button
        controller.style.configure("Start.TButton", font=("TkDefaultFont", 30), background="#00CC11", foreground="#FFFFFF")
        controller.style.map("Start.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Create 'Start' button
        start_btn = ttk.Button(self, text="Start", style="Start.TButton", width=6, command=controller.start_game)
        start_btn.pack(pady=(30, 0))

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)

    # Loads the intructions based on the difficulty the user has selected
    def load_instructions(self):
        # Display instructions text based on selected difficulty (if it exists)
        if self.controller.selected_difficulty:
            self.display_instructions(self.controller.selected_difficulty)
    
    # Function to display the instructions text based on the selected difficulty
    def display_instructions(self, chosen_difficulty):
        # Variable for the instructions text
        instructions_string = ""

        # Create instructions string data
        if chosen_difficulty == DIFFICULTIES[0]:
            instructions_string = f"Welcome to 'Easy Mode'. In this difficulty, you will solve exponents with squares and square roots. You'll be dealing with adding subtracting exponents.\n\n{GENERAL_GUIDE}"
        
        # Set intructions text to label
        self.instructions_text.configure(text=instructions_string)
    
    # Function to return to lobby screen if user choses not to play anymore
    def cancel_game(self):
        # Reset game variables
        self.selected_difficulty = ""
        self.questions = {}
        self.question_number = None
        self.total_score = None
        self.lives_count = None
        self.haswon = None

        # Take user back to lobby screen
        self.controller.display_page(LobbyScreen)


# Displays the quiz and loads the random generated questions to the user to answer
class QuizScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Reference for main 'App' method
        self.controller = controller

        # Contains the 'ID' (initially set to 'None')
        self.timer_id = None

        # Create title label
        title_label = ttk.Label(self, text="Gameplay", font=("TkDefaultFont", 50))
        title_label.pack(pady=50)

        # Style for 'quit gameplay' button
        controller.style.configure("QuitGame.TButton", font=("TkDefaultFont", 25), background="#FFFFFF")
        controller.style.map("QuitGame.TButton", background=[("pressed", "#ECECEC"), ("active", "#FF0000")], foreground=[("pressed", "#000000"), ("active", "#FFFFFF")])

        # Button to quit current gameplay and go back to lobby screen
        quitgame_btn = ttk.Button(self, text="Quit", style="QuitGame.TButton", width=5, command=self.quit_game)
        quitgame_btn.place(relx=0, rely=0, x=20, y=20)

        # Label for the 'Are you sure?' text
        self.confirm_label = ttk.Label(self, text="Confirm quit? Progress will not be saved!", font=("TkDefaultFont", 25))

        # Binds to toggle the confirm label when the user is about to quit the game
        quitgame_btn.bind("<Enter>", self.cursor_on)
        quitgame_btn.bind("<Leave>", self.cursor_off)

        #Create frame for main contents
        main_frame = tk.Frame(self, width=1000, height=650)
        main_frame.pack()
        main_frame.pack_propagate(False)
        main_frame.grid_propagate(False)
        
        # Configures the alignments for its child widgets
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Top bar and contents frame
        topbar = tk.Frame(main_frame, borderwidth=3, relief="solid")
        topbar.grid(row=0, column=0, sticky="ew")

        # Aligns widgets in top bar
        topbar.grid_columnconfigure(0, minsize=300)
        topbar.grid_columnconfigure(1, weight=1)
        topbar.grid_columnconfigure(2, minsize=300)

        # Contents frame
        contents_frame = tk.Frame(main_frame, borderwidth=3, relief="solid")
        contents_frame.grid(row=1, column=0, sticky="nsew")

        # Keep widgets in contents frame horizontally centred
        contents_frame.grid_columnconfigure(0, weight=1)

        # Create frame for number of lives
        lives_frame = tk.Frame(topbar, borderwidth=2, relief="solid")
        lives_frame.grid(row=0, column=0, padx=10, sticky="w")
        lives_frame.grid_propagate(False)

        # Create label for number of lives
        lives_label = ttk.Label(lives_frame, text="Lives:", font=("TkDefaultFont", 20))
        lives_label.pack(side=tk.LEFT, padx=(0, 5))

        # Create labels for lives graphics
        self.live1 = ttk.Label(lives_frame)
        self.live2 = ttk.Label(lives_frame)
        self.live3 = ttk.Label(lives_frame)

        self.live1.pack(side=tk.LEFT)
        self.live2.pack(side=tk.LEFT, padx=3)
        self.live3.pack(side=tk.LEFT)

        # Create label for the question number
        self.question_num = ttk.Label(topbar, font=("TkDefaultFont", 25))
        self.question_num.grid(row=0, column=1, pady=5)

        # Frame for widgets on the right in topbar
        right_widgets = tk.Frame(topbar)
        right_widgets.grid(row=0, column=2, padx=10, sticky="e")
        right_widgets.grid_propagate(False)

        # Create label for difficulty
        self.difficulty_label = ttk.Label(right_widgets, font=("TkDefaultFont", 20), style="OutlinedLabels.TLabel")
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        # Create timer label
        self.timer_label = ttk.Label(right_widgets, font=("TkDefaultFont", 20), style="OutlinedLabels.TLabel")
        self.timer_label.pack(side=tk.LEFT)

        # Create question instruction label
        question_instruction = ttk.Label(contents_frame, text="Solve:", font=("TkDefaultFont", 30))
        question_instruction.grid(row=0, column=0, pady=10)

        # Create question label
        self.question_label = ttk.Label(contents_frame, font=("TkDefaultFont", 25))
        self.question_label.grid(row=1, column=0)

        # Create frame for the answering widgets
        answering_frame = tk.Frame(self)
        answering_frame.pack(pady=(20, 15))

        # Create entry field for user's answer
        self.answer_entry = ttk.Entry(answering_frame, font=("TkDefaultFont", 30), width=20)
        self.answer_entry.grid(row=0, column=0, padx=5)

        # Keybind for answer entry button
        self.answer_entry.bind("<Return>", lambda: self.controller.check_answer(self.answer_entry.get()))

        # Style for 'Submit'/'Next' button
        controller.style.configure("Submit.TButton", font=("TkDefaultFont", 30), background="#00CC11", foreground="#FFFFFF") # 'Submit' button
        controller.style.map("Submit.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        controller.style.configure("Next.TButton", font=("TkDefaultFont", 30), background="#FFFFFF", foreground="#000000") # 'Next' button

        # Create 'Submit'/'Next' button
        self.submitnext_btn = ttk.Button(
            answering_frame, text="Submit",
            style="Submit.TButton",
            width=7,
            command=lambda: self.controller.check_answer(self.answer_entry.get()))
        self.submitnext_btn.grid(row=0, column=1, padx=5)

        # Create feedback label
        self.feedback_label = ttk.Label(self, font=("TkDefaultFont", 25))

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)

    # Loads initial assets when game starts
    def load_assets(self):
        # Check if lives' heart images are missing or not
        if self.controller.images.get("Avaliable Live") and self.controller.images.get("Unavaliable Live"):
            self.live1.configure(image=self.controller.images["Avaliable Live"])
            self.live2.configure(image=self.controller.images["Avaliable Live"])
            self.live3.configure(image=self.controller.images["Avaliable Live"])
        else:
            self.live1.configure(text=AVALIABLE_LIVE_TEXT, font=("TkDefaultFont", 15))
            self.live2.configure(text=AVALIABLE_LIVE_TEXT, font=("TkDefaultFont", 15))
            self.live3.configure(text=AVALIABLE_LIVE_TEXT, font=("TkDefaultFont", 15))
        
        # Set text for the difficulty label
        self.difficulty_label.configure(text=self.controller.selected_difficulty)

        # Set 'submitnext_btn' to 'submit' button
        self.submitnext_btn.config(text="Submit", style="Submit.TButton", command=lambda: self.controller.check_answer(self.answer_entry.get()))

        # Make answer entry accessible
        self.answer_entry.config(state="normal")

        # Clear answer entry field
        self.answer_entry.delete(0, tk.END)

        # Remove feedback label
        self.feedback_label.pack_forget()

        # Keybind for answer entry button
        self.answer_entry.bind("<Return>", lambda event: self.controller.check_answer(self.answer_entry.get()))

    # Place 'confirm_label' when mouse cursor hovers over quit button
    def cursor_on(self, event=None):
        self.confirm_label.place(relx=0, rely=0, x=130, y=24)
    
    # Remove 'confirm_label' when mouse cursor hovers over quit button
    def cursor_off(self, event=None):
        self.confirm_label.place_forget()

    # Updates question, question instruction (will be added later), and question number labels with current question
    def update_questions(self):
        self.question_num.configure(text=f"Question: {self.controller.question_number}/{NUM_QUESTIONS}")
        self.question_label.configure(text=self.controller.questions[self.controller.question_number]["Question"])
    
    # Function generate feedback for each answer
    def display_feedback(self, incorrectly_answered=False):
        if incorrectly_answered:
            # Generate random number for random feedback message
            message_index = random.randrange(4)

            # Display feedback label
            self.feedback_label.configure(
                text=f"{INCORRECT_ANSWER_RESPONSES[message_index]} The correct answer was {self.controller.questions[self.controller.question_number]["Answer"]}."
                )
            self.feedback_label.pack()
        else:
            # Generate random number for random feedback message
            message_index = random.randrange(5)

            # Display feedback label
            self.feedback_label.configure(
                text=f"{CORRECT_ANSWER_RESPONSES[message_index]}"
                )
            self.feedback_label.pack()

        # Make answer entry readonly
        self.answer_entry.config(state="readonly")

        # Keybind for answer entry button
        self.answer_entry.bind("<Return>", self.next_question)

        # Change 'submitnext_btn' to 'next' button
        self.submitnext_btn.config(text="Next", style="Next.TButton", command=self.next_question)
    
    # Function to display the next question on the condition if the user has remaining lives or whether they have answered every question
    def next_question(self, event=None):
        # Change 'submitnext_btn' to 'submit' button
        self.submitnext_btn.config(text="Submit", style="Submit.TButton", command=lambda: self.controller.check_answer(self.answer_entry.get()))

        # If user has lost all lives
        if self.controller.lives_count == 0:
            # End game as the user has lost
            self.controller.end_game()
            return
        
        # If user has not lost all lives but has not answered every question
        elif self.controller.question_number < NUM_QUESTIONS:
            # Add '1' to question number
            self.controller.question_number += 1
        
        # If user has answered all questions and has remaining lives
        else:
            # End game as the user has won
            self.controller.end_game()
            return
        
        # Change widget states if program is to display the next question
        # Make answer entry accessible again
        self.answer_entry.config(state="normal")

        # Clear answer entry field
        self.answer_entry.delete(0, tk.END)

        # Remove feedback label
        self.feedback_label.pack_forget()

        # Keybind for answer entry button
        self.answer_entry.bind("<Return>", lambda event: self.controller.check_answer(self.answer_entry.get()))

        self.update_questions()

    # Remove life function
    def remove_life(self):
        # Makes sure the number of lives remaining is above 0
        if self.controller.lives_count > 0:
            # Which live in the top bar to remove (from the 3rd one)
            live_number = getattr(self, f"live{self.controller.lives_count}")

            # Check if lives' heart images are missing or not
            if self.controller.images.get("Avaliable Live") and self.controller.images.get("Unavaliable Live"):
                # Replace avaliable life with unavaliable life image
                live_number.configure(image=self.controller.images["Unavaliable Live"])
            else:
                live_number.configure(text=UNAVALIABLE_LIVE_TEXT)
    
    # Updates countdown timer
    def update_timer(self):
        # Convert seconds into minutes and seconds
        minutes = self.controller.time_remaining // 60
        seconds = self.controller.time_remaining % 60

        # Display time in MM:SS format in timer label
        self.timer_label.configure(text=f"{minutes:02}:{seconds:02}")

        # Check if time has reached 10 seconds or below to warn user that time is running out
        if self.controller.time_remaining <= 30 and self.controller.time_remaining > 10:
            self.timer_label.configure(foreground="#F89D1F")
        
        # Check if time has reached 10 seconds or below to warn user that time is critically running out
        elif self.controller.time_remaining <= 10:
            self.timer_label.configure(foreground="#FF0000")
        
        # Sets to black if user starts a new game with new countdown duration
        else:
            self.timer_label.configure(foreground="#000000")
    
        # Continue counting down if there is still time remaining
        if self.controller.time_remaining > 0:
            self.controller.time_remaining -= 1

            # Run function again after 1 second (1000 milliseconds) and set it as timer ID
            self.timer_id = self.after(1000, self.update_timer)
        
        else:
            # No more time remaining
            self.timer_label.configure(text="00:00")

            # End game as the user has lost
            self.controller.end_game()

    # Function to cancel the timer
    def cancel_timer(self):
        # Cancel timer
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)

            # Clear timer ID
            self.timer_id = None
    
    # Function to quit gameplay
    def quit_game(self):
        # Cancel the timer
        self.cancel_timer()

        # Set game variables to empty values
        self.controller.selected_difficulty = ""
        self.controller.questions = {}
        self.controller.lives_count = None
        self.controller.time_remaining = None

        # Go back to lobby screen
        self.controller.display_page(LobbyScreen)


# This displays the user's score and results after completing the quiz, and then stores it in the data file (.json) containing every user's previous scores.
class ResultsScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame
        super().__init__(parent)

        # Footer frame
        footer_frame = tk.Frame(self, borderwidth=2, relief="solid")
        footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

        # 'Flow Computing' footer
        footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("TkDefaultFont", 15), background="#FFFFFF", anchor="center")
        footer_label.pack(ipadx=3, ipady=3)

# ==================================================

# This initialises the code when the program starts running, and puts the GUI window into a permanent loop to prevent it from closing.
if __name__ == "__main__":
    app = App()
    app.mainloop()
