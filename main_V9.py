"""
Author: Ryan Fernando
Date: 08/05/2026
Purpose: To create a program using complex techniques to help students improve their math skills by creating an interactive quiz-like math game.
Version: 9.0
"""

# ===== Modules imported =====

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import random
import math
import json
from PIL import Image, ImageTk
import pygame
from fractions import Fraction
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

# Initialise pygame assets
pygame.init()
pygame.mixer.init()

# Transformation rule when parsing expressions
transformations = standard_transformations + (implicit_multiplication_application, convert_xor)

# ===== Constants created =====

"""
This gets the absolute path of the files' directory, so it opens the files which are used in the program.
It is important so the program can run properly while getting all the relevant files,
regardless of which device it is being run on and where or how the program is run.
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Maximum and minimum length for each login/signup field.
MIN_ENTRY_LEN_USERNAME = 6
MIN_ENTRY_LEN_PASSWORD = 8
MAX_ENTRY_LEN_USERNAME = 20
MAX_ENTRY_LEN_PASSWORD = 32

# Number of questions for each quiz.
NUM_QUESTIONS = 10

# Total number of lives given.
NUM_LIVES = 3

# Total amount of time given (5 minutes).
TIME_GIVEN = 300

# Game difficultyies
DIFFICULTIES = ["Easy", "Medium", "Hard", "Challenge"]

# Instructions for each difficulty.
DIFFICULTY_INSTRUCTIONS = {
    "Easy": (
        "Welcome to 'Easy Mode'!\n\n"
        "In this difficulty, you will solve equations with squares and square roots. "
        "You'll be dealing with adding and subtracting exponents, as well simplifying equations using product and quotient exponents rules. "
        "For solving square roots, only enter the absolute value (e.g. √64 = 8).\n\n"
        "Use '^' for powers in your answers (e.g. x^2, a^-5)."
    ),
    "Medium": (
        "Welcome to 'Medium Mode'!\n\n"
        "This difficulty deals with adding, subtracting, multiplying, and dividing different fractions. "
        "After solving, make sure you SIMPLIFY each fraction to its simplest form if necessary. "
        "Questions for adding and subtraction contain a mix of identical and different denominators.\n\n"
        "Use '/' for fraction symbols in your answers (e.g. x/y, -g/h, i/-j). Make sure to submit your answers as a fraction (no mixed numbers or decimals)."
    ),
    "Hard": (
        "Welcome to 'Hard Mode'!\n\n"
        "You will being dealing with solving equation to find an unknown, factorising equations, and expanding eqations. "
        "You do not need to focus on simplifying your answers for this difficulty as the idea is to make sure you understand how to tackle these sorts of problems."
    ),
    "Challenge": (
        "Welcome to 'Challenge Mode'!\n\n"
        "This difficulty involves differentiating equations. "
        "The types of equations you will differentiate are quadratic, cubic, and quartic equations. "
        "This difficulty is meant to introduce basic calculus to students taking advanced mathematics courses in high school.\n\n"
        "Use '^' for powers in your answers (e.g. x^2, a^-5)."
    )
}

# The passing score the user much get or higher in order to win.
PASSING_SCORE = 5

# Lives symbols in case the images do not work.
AVALIABLE_LIVE_TEXT = "♥"
UNAVALIABLE_LIVE_TEXT = "♡"

# Variable for the guide on the general gameplay.
GENERAL_GUIDE = """
You will be given a total of 5 minutes to complete the quiz. There are 10 questions to answer altogether. You will be given 3 lives in total, where each wrong answer takes 1 away.

Once you complete the quiz, your score will be stored to your personal record of previous scores. They can be viewed in the 'Previous Scores' page. 

Make sure to answer every question, and make sure you do not run out of time or lives.

A score of 5 or more is required to win. You will still get a score if you lose as long, as you score is at least 1 point.

You may click 'Start' when you're ready. Good luck!
"""

# Maximum amount of characters in the answer entry depending on the selected difficulty.
MAX_ENTRY_LEN_ANSWER = {
    "Easy": 10,
    "Medium": 25,
    "Hard": 35,
    "Challenge": 50
}

# Responses if user answers correctly.
CORRECT_ANSWER_RESPONSES = [
    "Great Job!",
    "Keep It Up!",
    "Welldone!",
    "Awesome!",
    "Incredible!",
    "Fantastic!"
    ]

# Responses if user answers correctly.
INCORRECT_ANSWER_RESPONSES = [
    "Incorrect.",
    "Sorry, incorrect.",
    "Sorry, wrong answer.",
    "Oops!",
    "Yikes!"
]

# Winning messages generated based on the user's total score if they have scored the minimum passing score or higher.
WINNING_MESSAGES = {
    10: "Perfect score! Incredible work!",
    9: "Excellent work!",
    8: "Great job!",
    7: "Well done!",
    6: "Good effort!",
    5: "You passed! Keep practicing!"
}

# Feedback messages for winning screen if user has run out of time or lives.
WINNING_FEEDBACK = {
    "Time": [
        "Time's up, but great effort!",
        "Good job! Try working on improving your speed.",
        "You ran out of time, but great work!"
    ],
    "Lives": [
        "You ran out of lives, but great work!",
        "Well done! Try working on improving accuracy.",
        "Keep practicing, and you'll be able to score higher!\nDon't let mistakes bring you down!"
    ]
}

# Column widths for listboxes.
COLUMN_WIDTHS = {
    "Rank": 5,
    "Username": 25,
    "Date & Time": 25,
    "Score": 8,
    "Time Remaining": 18
}

# Sound effects during the quiz.
SOUND_PATHS = {
    "Easy": {
        "Correct": {
            "Correct_1": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Emaj7.ogg"),
            "Correct_2": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_F#m7.ogg"),
            "Correct_3": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_G#m7.ogg"),
            "Correct_4": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Amaj7.ogg"),
            "Correct_5": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_B7.ogg")
        },

        "Incorrect": {
            "Incorrect_1": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Dissonant_1.ogg"),
            "Incorrect_2": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Dissonant_2.ogg"),
            "Incorrect_3": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Dissonant_3.ogg")
        },

        "Winning_sound": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Win.ogg"),
        "Losing_sound": os.path.join(BASE_DIR, "sounds", "easy_mode", "Vibes_Lose.ogg")
    },

    "Medium": {
        "Correct": {
            "Correct_1": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Amaj7.ogg"),
            "Correct_2": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Bm7.ogg"),
            "Correct_3": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_C#m7.ogg"),
            "Correct_4": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Dmaj7.ogg"),
            "Correct_5": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_E7.ogg")
        },

        "Incorrect": {
            "Incorrect_1": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Dissonant_1.ogg"),
            "Incorrect_2": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Dissonant_2.ogg"),
            "Incorrect_3": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Dissonant_3.ogg")
        },
            
        "Winning_sound": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Win.ogg"),
        "Losing_sound": os.path.join(BASE_DIR, "sounds", "medium_mode", "E-Guitar_Lose.ogg")
        },

    "Hard": {
        "Correct": {
            "Correct_1": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Dmaj7.ogg"),
            "Correct_2": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Em7.ogg"),
            "Correct_3": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_F#m7.ogg"),
            "Correct_4": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Gmaj7.ogg"),
            "Correct_5": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_A7.ogg")
        },

        "Incorrect": {
            "Incorrect_1": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Dissonant_1.ogg"),
            "Incorrect_2": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Dissonant_2.ogg"),
            "Incorrect_3": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Dissonant_3.ogg")
        },
            
        "Winning_sound": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Win.ogg"),
        "Losing_sound": os.path.join(BASE_DIR, "sounds", "hard_mode", "AGP_Lose.ogg")
        },

    "Challenge": {
        "Correct": {
            "Correct_1": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Bmaj7.ogg"),
            "Correct_2": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_C#m7.ogg"),
            "Correct_3": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_D#m7.ogg"),
            "Correct_4": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Emaj7.ogg"),
            "Correct_5": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_F#7.ogg")
        },

        "Incorrect": {
            "Incorrect_1": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Dissonant_1.ogg"),
            "Incorrect_2": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Dissonant_2.ogg"),
            "Incorrect_3": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Dissonant_3.ogg")
        },
            
        "Winning_sound": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Win.ogg"),
        "Losing_sound": os.path.join(BASE_DIR, "sounds", "challenge_mode", "E-Piano_Lose.ogg")
        }
}

# Order of 'Correct' sounds for each difficulty.
SOUNDS_ORDER = {
    "Easy": {
        1: SOUND_PATHS["Easy"]["Correct"]["Correct_1"],
        2: SOUND_PATHS["Easy"]["Correct"]["Correct_5"],
        3: SOUND_PATHS["Easy"]["Correct"]["Correct_4"],
        4: SOUND_PATHS["Easy"]["Correct"]["Correct_3"],
        5: SOUND_PATHS["Easy"]["Correct"]["Correct_1"],
        6: SOUND_PATHS["Easy"]["Correct"]["Correct_5"],
        7: SOUND_PATHS["Easy"]["Correct"]["Correct_2"],
        8: SOUND_PATHS["Easy"]["Correct"]["Correct_4"],
        9: SOUND_PATHS["Easy"]["Correct"]["Correct_5"],
        10: SOUND_PATHS["Easy"]["Correct"]["Correct_1"]
    },

    "Medium": {
        1: SOUND_PATHS["Medium"]["Correct"]["Correct_1"],
        2: SOUND_PATHS["Medium"]["Correct"]["Correct_5"],
        3: SOUND_PATHS["Medium"]["Correct"]["Correct_1"],
        4: SOUND_PATHS["Medium"]["Correct"]["Correct_3"],
        5: SOUND_PATHS["Medium"]["Correct"]["Correct_2"],
        6: SOUND_PATHS["Medium"]["Correct"]["Correct_3"],
        7: SOUND_PATHS["Medium"]["Correct"]["Correct_1"],
        8: SOUND_PATHS["Medium"]["Correct"]["Correct_4"],
        9: SOUND_PATHS["Medium"]["Correct"]["Correct_5"],
        10: SOUND_PATHS["Medium"]["Correct"]["Correct_1"]
    },

    "Hard": {
        1: SOUND_PATHS["Hard"]["Correct"]["Correct_1"],
        2: SOUND_PATHS["Hard"]["Correct"]["Correct_3"],
        3: SOUND_PATHS["Hard"]["Correct"]["Correct_2"],
        4: SOUND_PATHS["Hard"]["Correct"]["Correct_1"],
        5: SOUND_PATHS["Hard"]["Correct"]["Correct_5"],
        6: SOUND_PATHS["Hard"]["Correct"]["Correct_4"],
        7: SOUND_PATHS["Hard"]["Correct"]["Correct_3"],
        8: SOUND_PATHS["Hard"]["Correct"]["Correct_4"],
        9: SOUND_PATHS["Hard"]["Correct"]["Correct_5"],
        10: SOUND_PATHS["Hard"]["Correct"]["Correct_1"]
    },

    "Challenge": {
        1: SOUND_PATHS["Challenge"]["Correct"]["Correct_1"],
        2: SOUND_PATHS["Challenge"]["Correct"]["Correct_5"],
        3: SOUND_PATHS["Challenge"]["Correct"]["Correct_4"],
        4: SOUND_PATHS["Challenge"]["Correct"]["Correct_3"],
        5: SOUND_PATHS["Challenge"]["Correct"]["Correct_1"],
        6: SOUND_PATHS["Challenge"]["Correct"]["Correct_2"],
        7: SOUND_PATHS["Challenge"]["Correct"]["Correct_3"],
        8: SOUND_PATHS["Challenge"]["Correct"]["Correct_4"],
        9: SOUND_PATHS["Challenge"]["Correct"]["Correct_5"],
        10: SOUND_PATHS["Challenge"]["Correct"]["Correct_1"]
    }
}

# Order of sounds for each difficulty

# Motivational messages if user loses and does not score at all.
MOTIVATIONAL_MESSAGES = [
    "Don't worry, it's not too late to practice!",
    "Hey now, this doesn't mean you can't improve!",
    "Keep practicing! You can do this!"
]

# Superscript conversions.
SUPERSCRIPT_CHARACTERS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "−": "⁻"
}

# ==================================================

# ===== Values for styling are stored here =====

# Variables which store colours to prevent reusing hex codes.
DIFFICULTY_COLOURS = {
    "Easy": "#00DA00",
    "Medium": "#F89D1F",
    "Hard": "#FF0000",
    "Challenge": "#9820C5"
}

# ==================================================

# ===== General functions =====

# Superscript conversion function.
def superscript_conv(n):
    # Seperate each character and replace with its superscript counterpart.
    return "".join(SUPERSCRIPT_CHARACTERS[c] for c in str(n))

# Assigns random letter variables for math questions.
def rand_letters(n):
    # Returns a specific amount of unique letters.
    return random.sample("abcdefghijklmnopqrstuvwxyz", n)

# Function to generate linear equations.
def gen_linear_eq(unknown_position):
    # Generate random values.
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    x = random.randint(-25, 25)

    # Choose random operator (addition or subtraction).
    op1 = random.choice(["+", "-"])

    # Calculate 'c'.
    if op1 == "+":
        if unknown_position == "a":
            c = a * x + b
        elif unknown_position == "b":
            c = a + b * x
    else:
        if unknown_position == "a":
            c = a * x - b
        elif unknown_position == "b":
            c = a - b * x

    # Return values.
    return {
        "a": a,
        "b": b,
        "c": c,
        "x": x,
        "x_unknown": rand_letters(1)[0],
        "op1": op1
    }

# Function to generate factorisation questions
def gen_factorisation():
    # Generate a factorised expression first to be expanded and displayed as the question itself.
    factor = random.randint(2, 9)
    coefficient = random.randint(1, 9)
    constant = random.randint(1, 9)
    x_var = rand_letters(1)[0]

    # Choose random operator (addition or subtraction).
    op1 = random.choice(["+", "-"])

    # Create SymPy symbol.
    x_symbol = sp.Symbol(x_var)

    # Create the factorised expression.
    if op1 == "+":
        factorised_expr = sp.Mul(factor, coefficient * x_symbol + constant, evaluate=False)
    else:
        factorised_expr = sp.Mul(factor, coefficient * x_symbol - constant, evaluate=False)

    # Create expanded expression.
    expanded_expr = sp.expand(factorised_expr)

    # Get the simplest factorised expression.
    simplified_factorised_expr = sp.factor(expanded_expr)

    # Return values.
    return {
        "a": expanded_expr.coeff(x_symbol),
        "b": abs(expanded_expr.subs(x_symbol, 0)),
        "x_unknown": x_var,
        "op1": op1,
        "factorised_form": str(simplified_factorised_expr)
    }

# Function to generate expansion questions
def gen_expansion():
    # Generate a factorised expression as the question itself.
    factor = random.randint(2, 9)
    coefficient = random.randint(1, 9)
    constant = random.randint(1, 9)
    x_var = rand_letters(1)[0]

    # Choose random operator (addition or subtraction).
    op1 = random.choice(["+", "-"])

    # Create SymPy symbol.
    x_symbol = sp.Symbol(x_var)

    # Create the factorised expression.
    if op1 == "+":
        factorised_expr = sp.Mul(factor, coefficient * x_symbol + constant, evaluate=False)
    else:
        factorised_expr = sp.Mul(factor, coefficient * x_symbol - constant, evaluate=False)

    # Create expanded expression.
    expanded_expr = sp.expand(factorised_expr)

    # Get the simplest factorised expression.
    simplified_factorised_expr = sp.factor(expanded_expr)

    # Get the coefficient and brackets part and extract them to seperate variables
    a, brackets = simplified_factorised_expr.as_coeff_Mul()

    # Get the terms in the brackets part
    b = brackets.coeff(x_symbol)
    c = abs(brackets.subs(x_symbol, 0))

    # Return values.
    return {
        "a": a,
        "b": b,
        "c": c,
        "x_unknown": x_var,
        "op1": op1,
        "expanded_form": str(expanded_expr)
    }

# Create 'Flow Computing' footer for each page.
def create_footer(parent):
    # Footer frame.
    footer_frame = tk.Frame(parent, background="#FFFFFF", borderwidth=2, relief="solid")
    footer_frame.place(relx=1, rely=1, x=-5, y=-5, anchor="se",)

    # 'Flow Computing' footer.
    footer_label = ttk.Label(footer_frame, text="Flow Computing", font=("Arial", 15), background="#FFFFFF", anchor="center")
    footer_label.pack(ipadx=3, ipady=3)

# Convert time to seconds.
def time_converter(time):
    minutes, seconds = map(int, time.split(":"))
    return minutes * 60 + seconds

# Check if any audio files are missing.
def missing_audio():
    # All missing audio files (if any).
    missing_files = []

    # Another function to check the file paths
    def verify_paths(paths):
        # Check each dictionary item
        for value in paths.values():
            if isinstance(value, dict):
                verify_paths(value)
            else:
                if not os.path.isfile(value):
                    missing_files.append(value)

    verify_paths(SOUND_PATHS)

    # If there are any missing audio files.
    if missing_files:
        # String variable for error message.
        error_message = "Unable to find the following audio files:"

        # Add each missing sound to error message.
        for missing_audio in missing_files:
            error_message += f"\n- {os.path.basename(missing_audio)}"

        # Display error message
        messagebox.showerror("Error!", error_message)

# ==================================================

# ===== Main window =====

# Main class to manage the page switching controls, random-generated questions, and quiz functions.
class App(tk.Tk):
    # Main window.
    def __init__(self):
        """
        Since 'tk.Tk' is the main class' parameter, this tells the program that 'self' is reffered to it in order to set the GUI.
        This is similar to declaring a 'root' variable as 'tk.Tk()'.
        """
        super().__init__()
        self.title("Flow Computing")
        self.state("zoomed")

        # To make sure the app's background image stays correctly scaled and fits in the window properly.
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        # Style variable for ttk widgets.
        self.style = ttk.Style()

        # Set theme for ttk widgets.
        self.style.theme_use("alt")

        # ===== Dictionaries for user accounts (username and pasword) and the scores of all users =====

        # Dictionary for user accounts (username and pasword).
        self.accounts = {}
        # Previous scores of every user.
        self.previous_scores = {}
        # Current user logged in.
        self.current_user = ""

        # Declare file names and paths.
        self.accounts_filename = "accounts_registered.json"
        self.accounts_filepath = os.path.join(BASE_DIR, self.accounts_filename)
        self.previous_scores_filename = "previous_scores.json"
        self.previous_scores_filepath = os.path.join(BASE_DIR, self.previous_scores_filename)

        # Store existing registered accounts to 'accounts' dictionary.
        try:
            with open(self.accounts_filepath, "r", encoding="utf-8") as j:
                self.accounts = json.load(j)
        except:
            self.accounts = {}

        # Store existing previous scores of all accounts to 'previous_scores' dictionary.
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
                    "Question": "{a}² + {b}² =",
                    "Instruction": "Solve the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 12),
                        "b": random.randint(1, 12)
                    },
                    "Answer": lambda a, b: math.pow(a, 2) + math.pow(b, 2)
                },

                "Squares Subtraction": {
                    "Question": "{a}² − {b}² =",
                    "Instruction": "Solve the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 10),
                        "b": random.randint(1, 10)
                    },
                    "Answer": lambda a, b: math.pow(a, 2) - math.pow(b, 2)
                },

                "Square Roots Addition": {
                    "Question": "√{a} + √{b} =",
                    "Instruction": "Solve the following equation:",
                    "Random Values": lambda: {
                        "a": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]),
                        "b": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
                    },
                    "Answer": lambda a, b: math.sqrt(a) + math.sqrt(b)
                },

                "Square Roots Subtraction": {
                    "Question": "√{a} − √{b} =",
                    "Instruction": "Solve the following equation:",
                    "Random Values": lambda: {
                        "a": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]),
                        "b": random.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
                    },
                    "Answer": lambda a, b: math.sqrt(a) - math.sqrt(b)
                },

                "Product Rule": {
                    "Question": "{a}{x_display} × {a}{y_display}",
                    "Superscript Values": ["x", "y"],
                    "Instruction": "Simplify the following equation:",
                    "Random Values": lambda: (
                        lambda letters: {
                        "a": letters[0],
                        "x": random.randint(1, 9),
                        "y": random.randint(1, 9)
                        }
                    )(rand_letters(1)),
                    "Answer": lambda a, x, y: f"{a}^{x + y}"
                },
                
                "Quotient Rule": {
                    "Question": "{a}{x_display} ÷ {a}{y_display}",
                    "Superscript Values": ["x", "y"],
                    "Instruction": "Simplify the following equation:",
                    "Random Values": lambda: (
                        lambda letters: {
                        "a": letters[0],
                        "x": random.randint(1, 9),
                        "y": random.randint(1, 9)
                        }
                    )(rand_letters(1)),
                    "Answer": lambda a, x, y: (
                        "1" if x - y == 0
                        else a if x - y == 1
                        else f"{a}^{x - y}"
                    )
                }
            },
            
            "Medium": {
                "Fraction Addition (Identical Denominators)": {
                    "Question": "{a}/{c} + {b}/{c} =",
                    "Instruction": "Solve and simplify the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9)
                    },
                    "Answer": lambda a, b, c: Fraction(a, c) + Fraction(b, c)
                },

                "Fraction Subtraction (Identical Denominators)": {
                    "Question": "{a}/{c} − {b}/{c} =",
                    "Instruction": "Solve and simplify the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9)
                    },
                    "Answer": lambda a, b, c: Fraction(a, c) - Fraction(b, c)
                },

                "Fraction Addition (Different Denominators)": {
                    "Question": "{a}/{c} + {b}/{d} =",
                    "Instruction": "Solve and simplify the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "d": random.randint(1, 9)
                    },
                    "Answer": lambda a, b, c, d: Fraction(a, c) + Fraction(b, d)
                },

                "Fraction Subtraction (Different Denominators)": {
                    "Question": "{a}/{c} − {b}/{d} =",
                    "Instruction": "Solve and simplify the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "d": random.randint(1, 9)
                    },
                    "Answer": lambda a, b, c, d: Fraction(a, c) - Fraction(b, d)
                },

                "Fraction Multiplication": {
                    "Question": "{a}/{c} × {b}/{d} =",
                    "Instruction": "Solve and simplify the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "d": random.randint(1, 9)
                    },
                    "Answer": lambda a, b, c, d: Fraction(a, c) * Fraction(b, d)
                },

                "Fraction Division": {
                    "Question": "{a}/{c} ÷ {b}/{d} =",
                    "Instruction": "Solve and simplify the following equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "d": random.randint(1, 9)
                    },
                    "Answer": lambda a, b, c, d: Fraction(a, c) / Fraction(b, d)
                }
            },

            "Hard": {
                "Solve the unknown value #1": {
                    "Question": "{a}{x_unknown} {op1_display} {b} = {c}",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1"],
                    "Instruction": "Solve for {x_unknown}:",
                    "Random Values": lambda: gen_linear_eq("a"),
                    "Answer": lambda x, **kwargs: str(x)
                },

                "Solve the unknown value #2": {
                    "Question": "{a} {op1_display} {b}{x_unknown} = {c}",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1"],
                    "Instruction": "Solve for {x_unknown}:",
                    "Random Values": lambda: gen_linear_eq("b"),
                    "Answer": lambda x, **kwargs: str(x)
                },
                
                "Factorisation": {
                    "Question": "{a}{x_unknown} {op1_display} {b}",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1"],
                    "Instruction": "Factorise the following equation:",
                    "Random Values": gen_factorisation,
                    "Answer": lambda factorised_form, **kwargs: factorised_form.replace("*", "")
                },
                
                "Expansion": {
                    "Question": "{a}({b}{x_unknown} {op1_display} {c})",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1"],
                    "Instruction": "Expand the following equation:",
                    "Random Values": gen_expansion,
                    "Answer": lambda expanded_form, **kwargs: expanded_form.replace("*", "")
                }
            },

            "Challenge": {
                "Quadratic Differentiation": {
                    "Question": "{a}{x_unknown}² {op1_display} {b}{x_unknown} {op2_display} {c}",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1", "op2"],
                    "Instruction": "Differentiate the following quadratic equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "x_unknown": rand_letters(1)[0],
                        "op1": random.choice(["+", "-"]),
                        "op2": random.choice(["+", "-"])
                    },
                    "Answer": lambda a, b, c, x_unknown, op1, op2, **kwargs: str(
                        sp.diff(
                            sp.sympify(f"{a}*{x_unknown}**2 {op1} {b}*{x_unknown} {op2} {c}"), sp.Symbol(x_unknown)
                        )
                    ).replace("**", "^").replace("*", "")
                },

                "Cubic Differentiation": {
                    "Question": "{a}{x_unknown}³ {op1_display} {b}{x_unknown}² {op2_display} {c}{x_unknown} {op3_display} {d}",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1", "op2", "op3"],
                    "Instruction": "Differentiate the following cubic equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "d": random.randint(1, 9),
                        "x_unknown": rand_letters(1)[0],
                        "op1": random.choice(["+", "-"]),
                        "op2": random.choice(["+", "-"]),
                        "op3": random.choice(["+", "-"])
                    },
                    "Answer": lambda a, b, c, d, x_unknown, op1, op2, op3, **kwargs: str(
                        sp.diff(
                            sp.sympify(f"{a}*{x_unknown}**3 {op1} {b}*{x_unknown}**2 {op2} {c}*{x_unknown} {op3} {d}"), sp.Symbol(x_unknown)
                        )
                    ).replace("**", "^").replace("*", "")
                },
                
                "Quartic Differentiation": {
                    "Question": "{a}{x_unknown}⁴ {op1_display} {b}{x_unknown}³ {op2_display} {c}{x_unknown}² {op3_display} {d}{x_unknown} {op4_display} {e}",
                    "Display Unknowns": ["x_unknown"],
                    "Display Operators": ["op1", "op2", "op3", "op4"],
                    "Instruction": "Differentiate the following quartic equation:",
                    "Random Values": lambda: {
                        "a": random.randint(1, 9),
                        "b": random.randint(1, 9),
                        "c": random.randint(1, 9),
                        "d": random.randint(1, 9),
                        "e": random.randint(1, 9),
                        "x_unknown": rand_letters(1)[0],
                        "op1": random.choice(["+", "-"]),
                        "op2": random.choice(["+", "-"]),
                        "op3": random.choice(["+", "-"]),
                        "op4": random.choice(["+", "-"])
                    },
                    "Answer": lambda a, b, c, d, e, x_unknown, op1, op2, op3, op4, **kwargs: str(
                        sp.diff(
                            sp.sympify(f"{a}*{x_unknown}**4 {op1} {b}*{x_unknown}**3 {op2} {c}*{x_unknown}**2 {op3} {d}*{x_unknown} {op4} {e}"), sp.Symbol(x_unknown)
                        )
                    ).replace("**", "^").replace("*", "")
                }
            }
        }

        

        # ==================================================

        # ===== Variables for the gameplay =====

        # Selected difficulty.
        self.selected_difficulty = ""

        # Dictionary of generated questions containing the question displayed and the correct answer.
        self.questions = {}

        # Current question (initially set to 'None).
        self.question_number = None

        # User score (out of 10) (initially set to 'None').
        self.total_score = None

        # Number of lives (initially set to 'None').
        self.lives_count = None

        # The time remaining on the countdown timer (initially set to 'None').
        self.time_remaining = None

        # The 'minutes' and 'seconds' components of the time remaining for converting from seconds to minutes and seconds.
        self.minutes = None
        self.seconds = None

        # Boolean variable for whether user has won or not (initially set to 'None').
        self.haswon = None

        # ==================================================

        # ===== Configured ttk styles which will be used across multiple widgets =====

        # Style for 'return back' buttons.
        self.style.configure("ReturnBack.TButton", font=("Cambria", 25), background="#FFFFFF")

        # Style for 'show password' button.
        self.style.configure("ShowPassword.TButton", font=("Arial", 26), background="#FFFFFF")

        # Style for labels requiring borders.
        self.style.configure("OutlinedLabels.TLabel", background="#FFFFFF", borderwidth=2, relief="solid")

        # ==================================================

        # ===== Program images =====

        # Stores all the images which the program can locate without errors.
        self.images = {}

        # The images and their path which the program is meant to locate.
        image_files = {
            "Background Image":{
                "name": "background_image.png",
                "dimensions": (self.width, self.height)
            },

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
            },

            "Easy Mode Image": {
                "name": "vibraphone.png",
                "dimensions": (300, 300)
            },

            "Medium Mode Image": {
                "name": "guitar.png",
                "dimensions": (300, 300)
            },

            "Hard Mode Image": {
                "name": "piano.png",
                "dimensions": (300, 300)
            },

            "Challenge Mode Image": {
                "name": "keyboard.png",
                "dimensions": (300, 300)
            },

            "Game Over Image 1": {
                "name": "ruined_sheet_music.png",
                "dimensions": (300, 300)
            },

            "Game Over Image 2": {
                "name": "ripped_sheet_music.png",
                "dimensions": (300, 300)
            },

            "Game Over Image 3": {
                "name": "broken_music_note.png",
                "dimensions": (300, 300)
            }
        }

        # A list containing the missing images.
        missing_images = []

        # Favicon error message if favicon is missing.
        error_msg_favicon = None

        # Function to display a messagebox of all missing images.
        def img_error_messages(list):
            # Generate error message for missing images.
            if list:
                # String variable for error message.
                error_message = "Unable to display the following images:"

                # Add each missing image to error message.
                for missing_image in list:
                    error_message += f"\n- {missing_image}"

                messagebox.showerror("Error!", error_message)
            
            # Generate error emssages for missing favicon.
            if error_msg_favicon:
                messagebox.showerror("Error!", error_msg_favicon)

        # Validate image whether it exists and can be opened and stored in the image list without issues.
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

        # Get app favicon path and load it to replace the default tkinter favicon.
        try:
            app_favicon = tk.PhotoImage(file=os.path.join(BASE_DIR, "images", "app_favicon.png"))
            self.iconphoto(True, app_favicon)
        except tk.TclError as e:
            error_msg_favicon = f"Program favicon image not found!\n{e}"

        # Frame container for the app's pages.
        page_container = tk.Frame(self)
        page_container.pack(fill="both", expand=True)

        # Adjusts grid position to centre widgets.
        page_container.grid_rowconfigure(0, weight=1)
        page_container.grid_columnconfigure(0, weight=1)

        # Array to store each page.
        self.pages = {}

        # Assigns variables which contain a lambda function for specified entry limit criteria for entry fields.
        self.username_limit = self.register(lambda val: self.entry_limit(val, MAX_ENTRY_LEN_USERNAME))
        self.password_limit = self.register(lambda val: self.entry_limit(val, MAX_ENTRY_LEN_PASSWORD))

        # Create pages and add them to the array defined above.
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
        
        # Disable tab navigation control after creating pages.
        for p in self.pages.values():
            self.disable_tab_focus(p)
        
        # Display welcome screen when program is first executed.
        self.display_page(WelcomeScreen)

        # Wait until program fully loads before displaying error messages if any.
        self.after(50, lambda: img_error_messages(missing_images))

        # Check if there are any missing audio files.
        self.after(100, missing_audio)

    # Disables focus control when user hits 'tab'.
    def disable_tab_focus(self, widget):
        for child in widget.winfo_children():
            child.configure(takefocus=False)

            # Call function with page widget passed.
            self.disable_tab_focus(child)

    # Function to display specified page.
    def display_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

        # If a page as a "refresh" function.
        if hasattr(page, "refresh"):
            page.refresh()

    # Function to display background image.
    def display_background(self, page):
        background_img = tk.Label(page, image=self.images["Background Image"])
        background_img.place(x=0, y=0, relwidth=1, relheight=1)
        background_img.lower()

    # Function to prevent actions for entry fields restricting specific keyboard shortcuts.
    def block_action(self, event=None):
        # Return an unused string value to stop the action from triggering.
        return "break"

    # Function to show and hide password field (replaces characters with dots).
    def password_visibility(self, field, button, visibility):
        if visibility:
            field.configure(show="")

            # Check if button has working image.
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
    
    # Character limit for entry fields.
    def entry_limit(self, value, max_len):
        # Checks if the entry field character length exceeds the maximum length.
        if len(value) > max_len:
            return False
        
        # Returns true to allow user to continue typing in entry field.
        return True
    
    # Generates questions based on difficulty selected.
    def generate_questions(self, difficulty):
        # The dictionary of questions (initially empty).
        quiz_questions = {}

        # Variable to keep track of used questions to prevent duplicates (created as an unordered set of values).
        used_questions = set()

        # The dictionary of existing question types based on difficulty.
        existing_questions = self.question_types[difficulty]

        # Generate 10 random questions.
        for i in range(NUM_QUESTIONS):
            while True:
                # Select random question type.
                question_type = random.choice(list(existing_questions))

                # Get selected question data.
                question_data = existing_questions[question_type]

                # Generate random values for the question.
                rand_values = question_data["Random Values"]()

                # Create a copy of the random values dictionary to one which is intended to display values in a certain format if needed.
                display_values = rand_values.copy() # 'copy()' method used so original values don't get overwritten.

                # Convert display values to superscript as exponents if there are any.
                for v in question_data.get("Superscript Values", []):
                    display_values[f"{v}_display"] = superscript_conv(display_values[v])

                # If any, properly display operator symbols.
                for o in question_data.get("Display Operators", []):
                    display_values[f"{o}_display"] = ("−" if display_values[o] == "-" else display_values[o])

                # Substitute placeholder variables with the random generated values.
                question = question_data["Question"].format(**display_values) # '**display_values' unpacks the substituted values.

                # Break 'while' loop if the question generated is unique.
                if question not in used_questions:
                    used_questions.add(question)
                    break
            
            # Get the question's instructions.
            question_instruction = question_data["Instruction"].format(**rand_values)

            # Calculate the correct answer of the question.
            answer = question_data["Answer"](**rand_values)

            # Check if answer is an integer.
            if isinstance(answer, float) and answer.is_integer():
                answer = int(answer)
            
            # Convert answer to string before storing.
            answer = str(answer)

            # Store question and answer to its question number.
            quiz_questions[i + 1] = {
                "Question": question,
                "Instruction": question_instruction,
                "Answer": answer
            }
        
        # Return function's dictionary variable to be assigned to the universal questions dictionary.
        return quiz_questions
    
    # The function which initialises the variables and assets.
    def gameplay(self):
        # Set question number to '1'.
        self.question_number = 1

        # Set score to '0'.
        self.total_score = 0

        # Set number of lives.
        self.lives_count = NUM_LIVES

        # Set time remaining.
        self.time_remaining = TIME_GIVEN

        # Display quiz screen.
        self.display_page(QuizScreen)

        # Load game assets.
        self.pages[QuizScreen].load_assets()

        # Start timer.
        self.pages[QuizScreen].update_timer()

        # Update question-related widgets.
        self.pages[QuizScreen].update_questions()

    # Checks user's answer.
    def check_answer(self, user_answer):
        # Remove any leading or trailing spaces.
        user_answer = user_answer.lower().strip()

        # Check if user has entered a leading '+' sign.
        if user_answer.startswith("+"):
            user_answer = user_answer[1:] # Slice out the first character.

        # Check if user has entered a leading '+' sign for exponents.
        if "^+" in user_answer:
            user_answer = user_answer.replace("^+", "^")

        # Check if user inputs -0 if the answer is possibly 0.
        if user_answer == "-0":
            user_answer = "0"

        # Check if user input is empty.
        if not user_answer:
            return
        
        # Convert fraction answer to proper formatting if fraction is entered.
        try:
            if "/" in user_answer:
                # Assign temperary variables for numerator and denominator.
                numerator_str, denominator_str = user_answer.split("/")

                # Convert to integers
                numerator_int = int(numerator_str)
                demoninator_int = int(denominator_str)

                # Swap signs if denominator is negative.
                if demoninator_int < 0:
                    numerator_int = -numerator_int
                    demoninator_int = -demoninator_int

                # Store formatted fraction as the answer entered.
                user_answer = f"{numerator_int}/{demoninator_int}"
        except:
            pass

        # Correctly format the user's answer for hard/challenge mode questions using SymPy's parsing procedures.
        if self.selected_difficulty in ["Hard", "Challenge"]:
            try:
                # Remove spaces from user answer and normalise it.
                user_answer_formatted = user_answer.replace("−", "-").replace(" ", "")

                # Convert answer into SymPy expression.
                user_expr = parse_expr(user_answer_formatted, transformations=transformations)

                # Get the correct answer of the question.
                correct_answer = self.questions[self.question_number]["Answer"]

                # Remove spaces from correct answer and normalise it.
                correct_answer_formatted = correct_answer.replace("−", "-").replace(" ", "")

                # Convert correct answer into SymPy expression format.
                correct_expr = parse_expr(correct_answer_formatted, transformations=transformations)

                # Check if both expressions are equal and if user's answer is simplified
                if str(user_expr) == str(correct_expr):
                    user_answer = correct_answer
            except:
                pass

        # If correct.
        if user_answer == self.questions[self.question_number]["Answer"]:
            # Add 1 to total score.
            self.total_score += 1

            # Display feedback to user.
            self.pages[QuizScreen].display_feedback()

            # Play sound effect.
            try:
                sound_path = SOUNDS_ORDER[self.selected_difficulty][self.question_number]
                pygame.mixer.Sound(sound_path).play()
            except:
                pass
        
        # If incorrect.
        else:
            # Update amount of lives displayed.
            self.pages[QuizScreen].remove_life()

            # Display feedback to user.
            self.pages[QuizScreen].display_feedback(incorrectly_answered=True)

            # Generate random number to play a random sound for incorrect answers.
            sound_index = random.randint(1, 3)

            # Play sound effect.
            try:
                sound_path = SOUND_PATHS[self.selected_difficulty]["Incorrect"][f"Incorrect_{sound_index}"]
                pygame.mixer.Sound(sound_path).play()
            except:
                pass

            if self.lives_count > 0:
                # Remove 1 life.
                self.lives_count -= 1

            # Check if lives remaining is 0.
                if self.lives_count == 0:
                    # Change 'lives' label colour.
                    self.pages[QuizScreen].lives_label.configure(foreground="#FF0000")

        # Stop timer when lives reaches 0 or when all questions have been answered to prevent time from influencing quiz results.
        if self.lives_count == 0 or self.question_number == NUM_QUESTIONS:
            # Cancel the timer.
            self.pages[QuizScreen].cancel_timer()

    # Ends the game and decides whether the user has won or not.
    def end_game(self):
        # Checks if all questions have been answered and whether there is any time remaining.
        if self.question_number == NUM_QUESTIONS and self.time_remaining > 0:
            # User has won.
            self.haswon = True

            # Cancel the timer.
            self.pages[QuizScreen].cancel_timer()

        # If user runs out of lives        
        elif self.lives_count == 0:
            # Check if user has scored the minimum passing score or higher.
            if self.total_score >= PASSING_SCORE:
                # User has won.
                self.haswon = True
            else:
                # User has lost.
                self.haswon = False
        
        # If user runs out of time.
        elif self.time_remaining == 0:
            # Check if user has scored the minimum passing score or higher.
            if self.total_score >= PASSING_SCORE:
                # User has won.
                self.haswon = True
            else:
                # User has lost.
                self.haswon = False

            # Cancel the timer.
            self.pages[QuizScreen].cancel_timer()

        # Display results screen.
        self.display_page(ResultsScreen)

        # Display results in results screen.
        self.pages[ResultsScreen].display_results()
        # Set focus on results screen to prevent user from toggling the answer entry using the 'Enter' key.
        self.pages[ResultsScreen].focus_set()

    # The function for containing every function related to the quiz setup and control.
    def start_game(self):
        self.questions = self.generate_questions(self.selected_difficulty)
        self.gameplay()

# ==================================================

# ===== Classes for each page =====
# These are displayed via the main app class.

# Welcome Screen window containing the login, signup, and quit buttons.
class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Create frame for title and subheader.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=30, ipadx=5)

        # Create title label.
        title_label = ttk.Label(title_frame, text="Welcome!", font=("Berlin Sans FB", 75), background="#FFFFFF")
        title_label.pack(pady=(5, 0))

        # Create subheader.
        subheader_text = ttk.Label(title_frame, text="You may log in to your account, or sign up if you don't have one.", font=("Cambria", 25), background="#FFFFFF")
        subheader_text.pack(pady=5)

        # Create frame for login and signup buttons.
        buttons_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        buttons_frame.pack(pady=(275, 0), ipadx=5)

        # Style for login and signup buttons.
        controller.style.configure("Accounts.TButton", font=("Cambria", 30), background="#FFFFFF")

        # Style for quit program button.
        controller.style.configure("Quit.TButton", font=("Cambria", 30), background="#FF0000", foreground="#FFFFFF")
        controller.style.map("Quit.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Create login button.
        login_btn = ttk.Button(buttons_frame, text="Login", style="Accounts.TButton", width=8, command=lambda: controller.display_page(LoginScreen))
        login_btn.pack(pady=5)

        # Create signup button.
        signup_btn = ttk.Button(buttons_frame, text="Sign Up", style="Accounts.TButton", width=8, command=lambda: controller.display_page(SignupScreen))
        signup_btn.pack(pady=5)

        # Create frame for quit button
        quit_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        quit_frame.pack(pady=50, ipadx=5)

        # Create quit program button.
        quit_btn = ttk.Button(quit_frame, text="Quit", style="Quit.TButton", width=8, command=controller.destroy)
        quit_btn.pack(pady=5)

        # Create footer.
        create_footer(self)


# Login screen.
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Create frame for title and subheader.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=50, ipadx=5)

        # Create title label.
        title_label = ttk.Label(title_frame, text="Login", font=("Berlin Sans FB", 50), background="#FFFFFF")
        title_label.pack(pady=(5, 0))

        # Create subheader.
        subheader_text = ttk.Label(title_frame, text="Please enter your correct account details.", font=("Cambria", 25), background="#FFFFFF")
        subheader_text.pack(pady=5)

        # Button to go back to welcome screen.
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(WelcomeScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Login buttons frame.
        login_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        login_frame.pack(pady=(100, 0))

        # Username entry label.
        username_label = ttk.Label(login_frame, text="Username:", font=("Arial", 30))
        username_label.grid(row=0, column=0, padx=(15, 10), pady=(15, 25), sticky="e")

        # Username entry field.
        self.username_entry = ttk.Entry(login_frame, font=("Arial", 30), width=25, validate="key", validatecommand=(controller.username_limit, "%P"))
        self.username_entry.grid(row=0, column=1, padx=(15, 10), pady=(15, 25))

        # Password entry label.
        password_label = ttk.Label(login_frame, text="Password:", font=("Arial", 30))
        password_label.grid(row=1, column=0, padx=(15, 10), pady=(0, 15), sticky="e")

        # Password entry field.
        self.password_entry = ttk.Entry(login_frame, font=("Arial", 30), width=25, show="*", validate="key", validatecommand=(controller.password_limit, "%P"))
        self.password_entry.grid(row=1, column=1, padx=(15, 10), pady=(0, 15))

        # Prevent exporting selected text in password entry.
        self.password_entry.configure(exportselection=False)

        # Prevent user from pasting text in password entry.
        self.password_entry.bind("<<Paste>>", controller.block_action)

        # Prevent user from copying text in password entry.
        self.password_entry.bind("<<Copy>>", controller.block_action)
        # Prevent user from cutting text in password entry.
        self.password_entry.bind("<<Cut>>", controller.block_action)

        # Prevent user from pasting text in password entry using mouse middle-click (for Linux/X11 users).
        self.password_entry.bind("<Button-2>", controller.block_action)

        # Show/hide password button.
        self.show_password_btn = ttk.Button(login_frame, style="ShowPassword.TButton", command=self.showhide_password)
        self.show_password_btn.grid(row=1, column=2, padx=(0, 15), pady=(0, 15))

        # Style for 'Login' button.
        controller.style.configure("Login.TButton", font=("Cambria", 30), background="#00AC00", foreground="#FFFFFF")
        controller.style.map("Login.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Frame for login button.
        login_btn_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        login_btn_frame.pack(pady=50, ipadx=5)

        # Login button.
        login_btn = ttk.Button(login_btn_frame, text="Log In", style="Login.TButton", width=8, command=lambda: self.login_func(controller.accounts))
        login_btn.pack(pady=5)

        # Create footer.
        create_footer(self)

        # Boolean variable for password visibility (initially false).
        self.password_visibility = False
    
    # Reset page so when user returns, the page returns to how it looked like initially.
    def refresh(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.password_visibility = False
        
        # Check if button's images are missing or not.
        if self.controller.images.get("Hide Password") and self.controller.images.get("Show Password"):
            self.show_password_btn.configure(image=self.controller.images["Hide Password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

    # Function to toggle password visibility by checking and changing state of the boolean variable.
    def showhide_password(self):
        # Changes boolean value from 'False' to 'True' and vice versa.
        self.password_visibility = not self.password_visibility

        # Update widget configurations.
        self.controller.password_visibility(self.password_entry, self.show_password_btn, self.password_visibility)
    
    # Validate user's signup details and appends it to the .json of accounts, and then signs user in.
    def login_func(self, accounts_dict):
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        # Validate username.
        if not entered_username: # If entry is blank.
            messagebox.showerror("Invalid Input!", "Username cannot be empty!")
            return
        elif any(char.isspace() for char in entered_username): # If entry contains spaces.
            messagebox.showerror("Invalid Input!", "Username cannot contain spaces (use underscores instead)!")
            return
        elif len(entered_username) < MIN_ENTRY_LEN_USERNAME: # If entry is less than the minimum length required.
            messagebox.showerror("Invalid Input!", "Username must contain 6 or more characters!")
            return
        elif not entered_username.replace("_", "").isalnum(): # If entry contains symbols other than underscores.
            messagebox.showerror("Invalid Input!", "Username cannot contain symbols other than underscores!")
            return
        elif entered_username.lower() not in [accounts.lower() for accounts in accounts_dict]:
            messagebox.showerror("Account Not Found!", "This account does not exist!")
            return
        
        # Validate password.
        if not entered_password: # If entry is blank.
            messagebox.showerror("Invalid Input!", "Password cannot be empty!")
            return
        elif any(char.isspace() for char in entered_password): # If entry contains spaces.
            messagebox.showerror("Invalid Input!", "Password cannot contain spaces!")
            return
        elif len(entered_password) < MIN_ENTRY_LEN_PASSWORD: # If entry is less than the minimum length required.
            messagebox.showerror("Invalid Input!", "Password must contain 8 or more characters!")
            return
        
        # Variable for username but lowercase to prevent case-sensitivity in username entry.
        username_lower = entered_username.lower()

        # Convert all registered accounts' usernames to lowercase for the same reason as the previous comment.
        accounts_lower = {key.lower(): value for key, value, in accounts_dict.items()}

        # Check if username and password matches.
        if accounts_lower[username_lower] != entered_password:
            messagebox.showerror("Incorrect Password!", "The password entered is incorrect!")
            return
        
        # Variable for the original case of the username.
        username_original = next((key for key in accounts_dict if key.lower() == username_lower), None) # Assigns 'None' if there aren't any matches.
        
        # Set 'current_user' variable as the username of the user logged in.
        self.controller.current_user = username_original

        # Display info message.
        messagebox.showinfo("Access Granted!", f"You have successfully logged into your account as {username_original}!")

        # Display lobby screen.
        self.controller.display_page(LobbyScreen)


# Signup screen.
class SignupScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Create frame for title and subheader.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=50, ipadx=5)

        # Create title label.
        title_label = ttk.Label(title_frame, text="Sign Up", font=("Berlin Sans FB", 50), background="#FFFFFF")
        title_label.pack(pady=(5, 0))

        # Create subheader.
        subheader_text = ttk.Label(title_frame, text="Please enter a username and a strong password.", font=("Cambria", 25), background="#FFFFFF")
        subheader_text.pack(pady=5)

        # Button to go back to welcome screen.
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(WelcomeScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Login buttons frame.
        signup_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        signup_frame.pack(pady=(100, 0))

        # Username entry label.
        username_label = ttk.Label(signup_frame, text="Username:", font=("Arial", 30))
        username_label.grid(row=0, column=0, padx=(15, 10), pady=(15, 0), sticky="e")

        # Username entry field.
        self.username_entry = ttk.Entry(signup_frame, font=("Arial", 30), width=25, validate="key", validatecommand=(controller.username_limit, "%P"))
        self.username_entry.grid(row=0, column=1, padx=(15, 10), pady=(15, 0))

        # Password entry label.
        password_label = ttk.Label(signup_frame, text="Password:", font=("Arial", 30))
        password_label.grid(row=1, column=0, padx=(15, 10), pady=15, sticky="e")

        # Password entry field.
        self.password_entry = ttk.Entry(signup_frame, font=("Arial", 30), width=25, show="*", validate="key", validatecommand=(controller.password_limit, "%P"))
        self.password_entry.grid(row=1, column=1, padx=(15, 10), pady=15)

        # Confirm password entry label.
        password_label = ttk.Label(signup_frame, text="Confirm Password:", font=("Arial", 30))
        password_label.grid(row=2, column=0, padx=(15, 10), pady=(0, 15), sticky="e")

        # Confirm password entry field.
        self.confirm_entry = ttk.Entry(signup_frame, font=("Arial", 30), width=25, show="*", validate="key", validatecommand=(controller.password_limit, "%P"))
        self.confirm_entry.grid(row=2, column=1, padx=(15, 10), pady=(0, 15))

        # Prevent exporting selected text in password entries.
        self.password_entry.configure(exportselection=False)
        self.confirm_entry.configure(exportselection=False)

        # Prevent user from pasting text in password entries.
        self.password_entry.bind("<<Paste>>", controller.block_action)
        self.confirm_entry.bind("<<Paste>>", controller.block_action)

        # Prevent user from copying text in password entries.
        self.password_entry.bind("<<Copy>>", controller.block_action)
        self.confirm_entry.bind("<<Copy>>", controller.block_action)

        # Prevent user from cutting text in password entries.
        self.password_entry.bind("<<Cut>>", controller.block_action)
        self.confirm_entry.bind("<<Cut>>", controller.block_action)

        # Prevent user from pasting text in password entries using mouse middle-click (for Linux/X11 users).
        self.password_entry.bind("<Button-2>", controller.block_action)
        self.confirm_entry.bind("<Button-2>", controller.block_action)

        # Show/hide password button.
        self.show_password_btn = ttk.Button(signup_frame, style="ShowPassword.TButton", command=self.showhide_password)
        self.show_password_btn.grid(row=1, column=2, padx=(0, 15), pady=15)

        # Style for 'Signup' button.
        controller.style.configure("Signup.TButton", font=("Cambria", 30), background="#FFFFFF")

        # Frame for signup button.
        signup_btn_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        signup_btn_frame.pack(pady=50, ipadx=5)

        # Signup button.
        signup_btn = ttk.Button(signup_btn_frame, text="Sign Up", style="Signup.TButton", width=8, command=lambda: self.signup_func(controller.accounts, controller.accounts_filepath))
        signup_btn.pack(pady=5)

        # Create footer.
        create_footer(self)

        # Boolean variable for password visibility (initially false).
        self.password_visibility = False
    
    # Reset page so when user returns, the page returns to how it looked like initially.
    def refresh(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)
        self.password_entry.configure(show="*")
        self.confirm_entry.configure(show="*")
        self.password_visibility = False
        
        # Check if button's images are missing or not.
        if self.controller.images.get("Hide Password") and self.controller.images.get("Show Password"):
            self.show_password_btn.configure(image=self.controller.images["Hide Password"])
        else:
            self.show_password_btn.configure(text="Show Password", width=14)

    # Function to toggle password visibility by checking and changing state of the boolean variable.
    def showhide_password(self):
        # Changes boolean value from 'False' to 'True' and vice versa.
        self.password_visibility = not self.password_visibility

        # Update widget configurations.
        self.controller.password_visibility(self.password_entry, self.show_password_btn, self.password_visibility)
        self.controller.password_visibility(self.confirm_entry, self.show_password_btn, self.password_visibility)

    # Validate user's signup details and appends it to the .json of accounts, and then signs user in.
    def signup_func(self, accounts_dict, file):
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()
        confirmed_password = self.confirm_entry.get().strip()

        # Validate username.
        if not entered_username: # If entry is blank.
            messagebox.showerror("Invalid Input!", "Username cannot be empty!")
            return
        elif any(char.isspace() for char in entered_username): # If entry contains spaces.
            messagebox.showerror("Invalid Input!", "Username cannot contain spaces (use underscores instead)!")
            return
        elif len(entered_username) < MIN_ENTRY_LEN_USERNAME: # If entry is less than the minimum length required.
            messagebox.showerror("Invalid Input!", "Username must contain 6 or more characters!")
            return
        elif not entered_username.replace("_", "").isalnum(): # If entry contains symbols other than underscores.
            messagebox.showerror("Invalid Input!", "Username cannot contain symbols other than underscores!")
            return
        
        # Variable for username but lowercase to prevent case-sensitivity in username entry.
        username_lower = entered_username.lower()
        
        # Check if username already exists (not case sensative).
        if username_lower in [accounts.lower() for accounts in accounts_dict]:
            messagebox.showerror("Username Already Taken!", f"{entered_username} has already been taken! Please enter a different username.")
            return
        
        # Validate password.
        if not entered_password: # If entry is blank.
            messagebox.showerror("Invalid Input!", "Password cannot be empty!")
            return
        elif any(char.isspace() for char in entered_password): # If entry contains spaces.
            messagebox.showerror("Invalid Input!", "Password cannot contain spaces!")
            return
        elif len(entered_password) < MIN_ENTRY_LEN_PASSWORD: # If entry is less than the minimum length required.
            messagebox.showerror("Invalid Input!", "Password must contain 8 or more characters!")
            return
        
        # Check if confirmation password field is empty or not.
        if not confirmed_password: # If entry is blank.
            messagebox.showerror("Invalid Input!", "Confirmed password cannot be empty!")
            return
        elif confirmed_password != entered_password: # Check if confirm password exactly matches entered password.
            messagebox.showerror("Error!", "The passwords you entered do not match!")
            return
        
        # Save username and password to .json file.
        try:
            # Add username and password to dictionary.
            accounts_dict[entered_username] = entered_password

            # Write to .json file.
            with open(file, "w", encoding="utf-8") as f:
                # Append sorted dictionary to file.
                json.dump(dict(sorted(accounts_dict.items())), f, indent=4)
        except Exception as e:
            # Display error message.
            messagebox.showerror("Error!", f"Failed to save account details to .json file:\n{e}.")
            # Remove recently added dictionary item.
            del accounts_dict[entered_username]
            return
        
        # Set 'current_user' variable as the username of the user logged in.
        self.controller.current_user = entered_username

        # Display info message.
        messagebox.showinfo("Account Successfully Created!", f"You have successfully registered your account as {entered_username}!")

        # Display lobby screen.
        self.controller.display_page(LobbyScreen)


# Lobby screen containing the difficulty levels, leaderboard button, and button to view user's previous scores.
class LobbyScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Create frame for title and subheader.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=(50, 0), ipadx=5)

        # Create title label.
        title_label = ttk.Label(title_frame, text="Select a Difficulty Level", font=("Berlin Sans FB", 50), background="#FFFFFF")
        title_label.pack(pady=5)

        # Create username label.
        self.username_label = ttk.Label(self, font=("Cambria", 25), background="#FFFFFF", borderwidth=2, relief="solid", padding=(5, 5))
        self.username_label.pack(pady=30)

        # Create frame for difficulty selection buttons.
        buttons_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        buttons_frame.pack(pady=(150, 0))

        # Create logout button.
        logout_btn = ttk.Button(self, text="Log Out", style="ReturnBack.TButton", width=8, command=self.logout_func)
        logout_btn.place(relx=1, rely=0, x=-20, y=20, anchor="ne")

        # ===== All difficulty buttons =====

        # Style for 'Easy' mode button.
        controller.style.configure("Easy.TButton", font=("Cambria", 30), background=DIFFICULTY_COLOURS["Easy"], foreground="#FFFFFF")
        controller.style.map("Easy.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Style for 'Medium' mode button.
        controller.style.configure("Medium.TButton", font=("Cambria", 30), background=DIFFICULTY_COLOURS["Medium"], foreground="#FFFFFF")
        controller.style.map("Medium.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Style for 'Hard' mode button.
        controller.style.configure("Hard.TButton", font=("Cambria", 30), background=DIFFICULTY_COLOURS["Hard"], foreground="#FFFFFF")
        controller.style.map("Hard.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Style for 'Challenge' mode button.
        controller.style.configure("Challenge.TButton", font=("Cambria", 30), background=DIFFICULTY_COLOURS["Challenge"], foreground="#FFFFFF")
        controller.style.map("Challenge.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Easy mode.
        easy_btn = ttk.Button(buttons_frame, text="Easy", style="Easy.TButton", width=10, command=lambda: self.establish_difficulty(DIFFICULTIES[0]))
        easy_btn.pack(padx=5, pady=(5, 20))

        # Medium mode.
        medium_btn = ttk.Button(buttons_frame, text="Medium", style="Medium.TButton", width=10, command=lambda: self.establish_difficulty(DIFFICULTIES[1]))
        medium_btn.pack(padx=5, pady=(0, 20))

        # Hard mode.
        hard_btn = ttk.Button(buttons_frame, text="Hard", style="Hard.TButton", width=10, command=lambda: self.establish_difficulty(DIFFICULTIES[2]))
        hard_btn.pack(padx=5, pady=(0, 20))

        # Challenge mode.
        challenge_btn = ttk.Button(buttons_frame, text="Challenge", style="Challenge.TButton", width=10, command=lambda: self.establish_difficulty(DIFFICULTIES[3]))
        challenge_btn.pack(padx=5, pady=(0, 5))

        # ==================================================

        # Style for 'View Leaderboard' button.
        controller.style.configure("ViewLeaderboard.TButton", font=("Cambria", 25), anchor="center", justify="center", background="#FFFFFF")

        # Create 'View Leaderboard' button.
        leaderboard_btn = ttk.Button(self, text="View\nLeaderboard", style="ViewLeaderboard.TButton", width=12, command=lambda: controller.display_page(LeaderboardScreen))
        leaderboard_btn.place(relx=0, rely=0, x=20, y=20)

        # Style for 'Previous Scores' button.
        controller.style.configure("PreviousScores.TButton", font=("Cambria", 30), anchor="center", justify="center", background="#FFFFFF")

        # Frame for 'Previous Scores' button.
        previous_scores_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        previous_scores_frame.pack(pady=(30, 0), ipadx=5)

        # Create 'Previous Scores' button.
        previous_scores_btn = ttk.Button(previous_scores_frame, text="Previous\nScores", style="PreviousScores.TButton", width=10, command=lambda: controller.display_page(PersonalScoresScreen))
        previous_scores_btn.pack(pady=5)

        # Create footer.
        create_footer(self)
    
    # Reset page so when user returns, the page returns to how it looked like initially.
    def refresh(self):
        self.username_label.configure(text=self.controller.current_user)
    
    # Function for the logging out.
    def logout_func(self):
        # Display 'yes-no' message.
        if messagebox.askyesno("Confirm Log Out", "Are you sure you want to log out?\nMake sure you remember your account password the next you log in!"):
            # Set 'current_user' variable as 'None'.
            self.controller.current_user = None
            # Configure lobby screen username label to an empty string.
            self.username_label.configure(text="")

            # Return to welcome screen
            self.controller.display_page(WelcomeScreen)
    
    # The function to get the selected difficulty based on the difficulty selected via button click. This then takes them to the instructions window with the instructions based on the selected difficulty.
    def establish_difficulty(self, chosen_difficulty):
        # Set selected difficulty.
        self.controller.selected_difficulty = chosen_difficulty

        # Take user to the instructions screen before beginning the quiz.
        self.controller.display_page(InstructionsScreen)

        self.controller.pages[InstructionsScreen].load_instructions()


# Leaderboard page showing the top scores of every registered user ranked by score (then by time remaining if there are identical highest scores).
class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Create frame for title.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=50, ipadx=5)

        # Create title label.
        self.title_label = ttk.Label(title_frame, text="Leaderboard", font=("Berlin Sans FB", 50), background="#FFFFFF")
        self.title_label.pack(pady=5)

        # Create difficulty selection frame for viewing scores based on selected mode in combo box.
        mode_selection_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        mode_selection_frame.pack(pady=(0, 10))

        # Create label for difficulty selection.
        mode_selection_label = ttk.Label(mode_selection_frame, text="Difficulty:", font=("Arial", 20), background="#FFFFFF")
        mode_selection_label.grid(row=0, column=0, padx=5, pady=5)

        # Create combo box to select difficulty mode.
        self.mode_combo_box = ttk.Combobox(
            mode_selection_frame,
            values=DIFFICULTIES,
            state="readonly",
            font=("Arial", 20),
            width=11
        )
        self.mode_combo_box.grid(row=0, column=1, padx=(0, 10), pady=5)

        # Bind combo box to toggle the 'display_scores' function.
        self.mode_combo_box.bind("<<ComboboxSelected>>", self.display_scores)

        # Create frame for listbox.
        main_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid", width=750, height=650)
        main_frame.pack()
        main_frame.pack_propagate(False)

        # Create header frame
        header_frame = tk.Frame(main_frame, background="#008CFF")
        header_frame.pack(fill=tk.X)

        # Create listbox header.
        header = ttk.Label(header_frame, text=self.create_header(), background="#008CFF", foreground="white", font=("Courier New", 14), anchor="w")
        header.pack(fill=tk.X)

        # Scrollbar for the scores list
        self.scrollbar = ttk.Scrollbar(main_frame)

        # Listbox for the scores to be displayed in.
        self.scores_listbox = tk.Listbox(main_frame, yscrollcommand=self.scrollbar.set, font=("Courier New", 14), background="#FFFFFF")

        # Prevent user from being able to interact with records in listbox.
        self.scores_listbox.bind("<Button-1>", self.controller.block_action)

        # Centre label to inform user that they need to select a difficulty, or whether there are no scores in the selected difficulty.
        self.centre_label = ttk.Label(main_frame, font=("Arial", 20), background="#FFFFFF", anchor="center")
        self.centre_label.pack(expand=True)

        # Button to go back to lobby screen.
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(LobbyScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Create footer.
        create_footer(self)

    # Reset page so when user returns, the page returns to how it looked like initially.
    def refresh(self):
        # Set placeholder text for combo box.
        self.mode_combo_box.set("Select Mode")

        # Change centre label text.
        self.centre_label.configure(text="Select a difficulty to display scores.")

        # Display centre label.
        self.centre_label.pack(expand=True)

        # Remove scrollbar.
        self.scrollbar.pack_forget()

        # Clear listbox.
        self.scores_listbox.delete(0, tk.END)

        # Remove listbox.
        self.scores_listbox.pack_forget()

    # Function to create the header text.
    def create_header(self):
        return (
            f"{'Rank':>{COLUMN_WIDTHS['Rank']}} | "
            f"{'Username':<{COLUMN_WIDTHS['Username']}} | "
            f"{'Score':>{COLUMN_WIDTHS['Score']}} | "
            f"{'Time Remaining':>{COLUMN_WIDTHS['Time Remaining']}}"
        )

    # Displays scores of the specified difficulty.
    def display_scores(self, event=None):
        # Get selected difficulty mode.
        selected_mode = self.mode_combo_box.get()

        # Get scores from .json file.
        try:
            with open(self.controller.previous_scores_filepath) as j:
                scores_data = json.load(j)
        except FileNotFoundError:
            self.centre_label.configure(text="Unable to find .json for previous scores.")
            return
        except json.JSONDecodeError:
            self.centre_label.configure(text="Previous scores .json is empty, or file is corrupted.")
            return

        # List for leaderboard
        leaderboard = []

        # Check each user's scores.
        for username, user_scores in scores_data.items():
            # Get scores under the selected difficulty.
            selected_scores = [score for score in user_scores if score["Difficulty"] == selected_mode]

            # Skip users who don't have any scores in this difficulty.
            if not selected_scores:
                continue

            # Get user's best score.
            best_score = max(selected_scores, key=lambda score: (score["Score"], time_converter(score["Time Remaining"])))

            # Add score to leaderboard list.
            leaderboard.append({
                "Username": username,
                "Score": best_score["Score"],
                "Time Remaining": best_score["Time Remaining"]
            })

            # Sort list by score, then by time remaining.
            leaderboard.sort(key=lambda record: (record["Score"], time_converter(record["Time Remaining"])), reverse=True)

        # Clear listbox to display the selected scores.
        self.scores_listbox.delete(0, tk.END)

        # Check if there are any scores in the selected mode.
        if not leaderboard:
            # Change text of centre label.
            self.centre_label.configure(text="No scores in this difficulty.")
            # Display centre label.
            self.centre_label.pack(expand=True)
            # Remove scrollbar.
            self.scrollbar.pack_forget()
            # Remove listbox.
            self.scores_listbox.pack_forget()
        else:
            # Remove centre label.
            self.centre_label.pack_forget()
            # Display scrollbar.
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # Display listbox.
            self.scores_listbox.pack(fill=tk.BOTH, expand=True)

            # Display scores
            for index, record in enumerate(leaderboard):
                # Assign rank to record
                rank = index + 1

                # Extract 'Username', 'Score', and 'Time Remaining' into designated variables.
                username_value = record["Username"]
                score_value = record["Score"]
                time_remaining = record["Time Remaining"]

                # Format column padding.
                display_record = (
                    f"{rank:>{COLUMN_WIDTHS['Rank']}} | "
                    f"{username_value:<{COLUMN_WIDTHS['Username']}} | "
                    f"{score_value:>{COLUMN_WIDTHS['Score']}} | "
                    f"{time_remaining:>{COLUMN_WIDTHS['Time Remaining']}}"
                )

                # Add record to listbox
                self.scores_listbox.insert(tk.END, display_record)
                # Creates an alternating row colour for readability.
                self.scores_listbox.itemconfig(index, {"background": "#FFFFFF" if index % 2 == 0 else "#E0F7FA"})

        # Deselect combo box content and remove focus from it.
        self.mode_combo_box.selection_clear()
        self.focus_set()


# Displays all the user's previous scores (results history).
class PersonalScoresScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Create frame for title.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=(50, 30), ipadx=5)

        # Create title label.
        self.title_label = ttk.Label(title_frame, font=("Berlin Sans FB", 50), background="#FFFFFF", anchor="center", justify="center")
        self.title_label.pack(pady=5)

        # Create difficulty selection frame for viewing scores based on selected mode in combo box.
        mode_selection_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        mode_selection_frame.pack(pady=(0, 10))

        # Create label for difficulty selection.
        mode_selection_label = ttk.Label(mode_selection_frame, text="Difficulty:", font=("Arial", 20), background="#FFFFFF")
        mode_selection_label.grid(row=0, column=0, padx=5, pady=5)

        # Create combo box to select difficulty mode.
        self.mode_combo_box = ttk.Combobox(
            mode_selection_frame,
            values=DIFFICULTIES,
            state="readonly",
            font=("Arial", 20),
            width=11
        )
        self.mode_combo_box.grid(row=0, column=1, padx=(0, 10), pady=5)

        # Bind combo box to toggle the 'display_scores' function.
        self.mode_combo_box.bind("<<ComboboxSelected>>", self.display_scores)

        # Create frame for listbox.
        main_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid", width=673, height=650)
        main_frame.pack()
        main_frame.pack_propagate(False)

        # Create header frame
        header_frame = tk.Frame(main_frame, background="#008CFF")
        header_frame.pack(fill=tk.X)

        # Create listbox header.
        header = ttk.Label(header_frame, text=self.create_header(), background="#008CFF", foreground="white", font=("Courier New", 14), anchor="w")
        header.pack(fill=tk.X, padx=11)

        # Scrollbar for the scores list
        self.scrollbar = ttk.Scrollbar(main_frame)

        # Listbox for the scores to be displayed in.
        self.scores_listbox = tk.Listbox(main_frame, yscrollcommand=self.scrollbar.set, font=("Courier New", 14), background="#FFFFFF")

        # Prevent user from being able to interact with records in listbox.
        self.scores_listbox.bind("<Button-1>", self.controller.block_action)

        # Centre label to inform user that they need to select a difficulty, or whether there are no scores in the selected difficulty.
        self.centre_label = ttk.Label(main_frame, font=("Arial", 20), background="#FFFFFF", anchor="center")
        self.centre_label.pack(expand=True)

        # Button to go back to lobby screen.
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=lambda: controller.display_page(LobbyScreen))
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        # Create footer.
        create_footer(self)

    # Reset page so when user returns, the page returns to how it looked like initially.
    def refresh(self):
        self.title_label.configure(text=f"{self.controller.current_user}'s\nPrevious Scores")

        # Set placeholder text for combo box.
        self.mode_combo_box.set("Select Mode")

        # Change centre label text.
        self.centre_label.configure(text="Select a difficulty to display scores.")

        # Display centre label.
        self.centre_label.pack(expand=True)

        # Remove scrollbar.
        self.scrollbar.pack_forget()

        # Clear listbox.
        self.scores_listbox.delete(0, tk.END)

        # Remove listbox.
        self.scores_listbox.pack_forget()

    # Function to create the header text.
    def create_header(self):
        return (
            f"{'Date & Time':<{COLUMN_WIDTHS['Date & Time']}} | "
            f"{'Score':>{COLUMN_WIDTHS['Score']}} | "
            f"{'Time Remaining':>{COLUMN_WIDTHS['Time Remaining']}}"
        )

    # Displays scores of the specified difficulty.
    def display_scores(self, event=None):
        # Get selected difficulty mode.
        selected_mode = self.mode_combo_box.get()

        # Get scores from .json file.
        try:
            with open(self.controller.previous_scores_filepath) as j:
                scores_data = json.load(j)
        except FileNotFoundError:
                    self.centre_label.configure(text="Unable to find .json for previous scores.")
                    return
        except json.JSONDecodeError:
            self.centre_label.configure(text="Previous scores .json is empty, or file is corrupted.")
            return

        # Get the scores of the current user.
        user_scores = scores_data[self.controller.current_user]

        # Get the scores under the selected difficulty.
        selected_scores = [score for score in user_scores if score["Difficulty"] == selected_mode]

        # Clear listbox to display the selected scores.
        self.scores_listbox.delete(0, tk.END)

        # Check if there are any scores in the selected mode.
        if not selected_scores:
            # Change text of centre label.
            self.centre_label.configure(text="No scores in this difficulty.")
            # Display centre label.
            self.centre_label.pack(expand=True)
            # Remove scrollbar.
            self.scrollbar.pack_forget()
            # Remove listbox.
            self.scores_listbox.pack_forget()
        else:
            # Remove centre label.
            self.centre_label.pack_forget()
            # Display scrollbar.
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # Display listbox.
            self.scores_listbox.pack(fill=tk.BOTH, expand=True)

            # Display scores
            for index, score in enumerate(selected_scores):
                # Extract 'Date & Time', 'Score', and 'Time Remaining' into designated variables.
                dateandtime = score["Date & Time"]
                score_value = score["Score"]
                time_remaining = score["Time Remaining"]

                # Format column padding.
                display_record = (
                    f" {dateandtime:<{COLUMN_WIDTHS['Date & Time']}} | "
                    f"{score_value:>{COLUMN_WIDTHS['Score']}} | "
                    f"{time_remaining:>{COLUMN_WIDTHS['Time Remaining']}}"
                )

                # Add record to listbox
                self.scores_listbox.insert(tk.END, display_record)
                # Creates an alternating row colour for readability.
                self.scores_listbox.itemconfig(index, {"background": "#FFFFFF" if index % 2 == 0 else "#E0F7FA"})

        # Deselect combo box content and remove focus from it.
        self.mode_combo_box.selection_clear()
        self.focus_set()


# Displays the instructions for each difficulty before commencing the game.
class InstructionsScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Create frame for title.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=50, ipadx=5)

        # Create title label.
        title_label = ttk.Label(title_frame, text="How To Play", font=("Berlin Sans FB", 50), background="#FFFFFF")
        title_label.pack(pady=5)

        # Button to go back to lobby screen.
        returnback_btn = ttk.Button(self, text="Back", style="ReturnBack.TButton", width=5, command=self.cancel_game)
        returnback_btn.place(relx=0, rely=0, x=20, y=20)

        #Create frame for main contents.
        main_frame = tk.Frame(self, background="#FFFFFF", width=1000, height=650)
        main_frame.pack()
        main_frame.pack_propagate(False)
        main_frame.grid_propagate(False)
        
        # Configures the alignments for its child widgets.
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Top bar and contents frame.
        topbar = tk.Frame(main_frame, background="#FFFFFF", borderwidth=3, relief="solid")
        topbar.grid(row=0, column=0, sticky="ew")

        # Contents frame.
        contents_frame = tk.Frame(main_frame, background="#FFFFFF", borderwidth=3, relief="solid")
        contents_frame.grid(row=1, column=0, sticky="nsew")

        # Create main frame header (goes in topbar).
        instructions_header = ttk.Label(topbar, text="Instructions", font=("Arial", 25), background="#FFFFFF")
        instructions_header.pack(pady=5)

        # Create instructions text (goes in contents frame).
        self.instructions_text = ttk.Label(contents_frame, font=("Cambria", 15), background="#FFFFFF", wraplength=975, justify="left")
        self.instructions_text.pack(pady=5)

        # Style for 'Start' button.
        controller.style.configure("Start.TButton", font=("Cambria", 30), background="#00CC11", foreground="#FFFFFF")
        controller.style.map("Start.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        # Create 'Start' button.
        start_btn = ttk.Button(self, text="Start", style="Start.TButton", width=6, command=controller.start_game)
        start_btn.pack(pady=(30, 0))

        # Create footer.
        create_footer(self)

    # Loads the intructions based on the difficulty the user has selected.
    def load_instructions(self):
        # Display instructions text based on selected difficulty (if it exists).
        if self.controller.selected_difficulty:
            self.display_instructions(self.controller.selected_difficulty)
    
    # Function to display the instructions text based on the selected difficulty.
    def display_instructions(self, chosen_difficulty):
        # Variable for the instructions text.
        instructions_string = ""

        # Create instructions string data.
        instructions_string = f"{DIFFICULTY_INSTRUCTIONS[chosen_difficulty]}\n\n{GENERAL_GUIDE}"
        
        # Set intructions text to label.
        self.instructions_text.configure(text=instructions_string)
    
    # Function to return to lobby screen if user choses not to play anymore.
    def cancel_game(self):
        # Reset game variables.
        self.selected_difficulty = ""
        self.questions = {}
        self.question_number = None
        self.total_score = None
        self.lives_count = None
        self.haswon = None

        # Take user back to lobby screen.
        self.controller.display_page(LobbyScreen)


# Displays the quiz and loads the random generated questions to the user to answer.
class QuizScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # Variable for the answer entry limit (initially set to 'None').
        self.answer_entry_limit = None

        # Contains the 'ID' (initially set to 'None').
        self.timer_id = None

        # Create frame for title.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=50, ipadx=5)

        # Create title label.
        title_label = ttk.Label(title_frame, text="Gameplay", font=("Berlin Sans FB", 50), background="#FFFFFF")
        title_label.pack(pady=5)

        # Style for 'quit gameplay' button.
        controller.style.configure("QuitGame.TButton", font=("Cambria", 25), background="#FFFFFF")
        controller.style.map("QuitGame.TButton", background=[("pressed", "#ECECEC"), ("active", "#FF0000")], foreground=[("pressed", "#000000"), ("active", "#FFFFFF")])

        # Button to quit current gameplay and go back to lobby screen.
        quitgame_btn = ttk.Button(self, text="Quit", style="QuitGame.TButton", width=5, command=self.quit_game)
        quitgame_btn.place(relx=0, rely=0, x=20, y=20)

        # Label for the 'Confirm quit?' text (displays when cursor hovers over the quit button).
        self.confirm_label = ttk.Label(self, text="Confirm quit? Progress will not be saved!", font=("Cambria", 25), background="#FFFFFF", borderwidth=1, relief="solid", padding=(3, 3))

        # Binds to toggle the confirm label when the user is about to quit the game.
        quitgame_btn.bind("<Enter>", self.cursor_on)
        quitgame_btn.bind("<Leave>", self.cursor_off)

        #Create frame for main contents.
        main_frame = tk.Frame(self, background="#FFFFFF", width=1200, height=650)
        main_frame.pack()
        main_frame.pack_propagate(False)
        main_frame.grid_propagate(False)
        
        # Configures the alignments for its child widgets.
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Top bar and contents frame.
        topbar = tk.Frame(main_frame, background="#FFFFFF", borderwidth=3, relief="solid")
        topbar.grid(row=0, column=0, sticky="ew")

        # Aligns widgets in top bar.
        topbar.grid_columnconfigure(0, minsize=400)
        topbar.grid_columnconfigure(1, weight=1)
        topbar.grid_columnconfigure(2, minsize=400)

        # Contents frame.
        contents_frame = tk.Frame(main_frame, background="#FFFFFF", borderwidth=3, relief="solid")
        contents_frame.grid(row=1, column=0, sticky="nsew")

        # Keep widgets in contents frame horizontally centred.
        contents_frame.grid_columnconfigure(0, weight=1)

        # Create frame for number of lives.
        lives_frame = tk.Frame(topbar, background="#FFFFFF", borderwidth=2, relief="solid")
        lives_frame.grid(row=0, column=0, padx=10, sticky="w")
        lives_frame.grid_propagate(False)

        # Create label for number of lives.
        self.lives_label = ttk.Label(lives_frame, text="Lives:", font=("Arial", 20), background="#FFFFFF")
        self.lives_label.pack(side=tk.LEFT, padx=(0, 5))

        # Create labels for lives graphics.
        self.live1 = ttk.Label(lives_frame, background="#FFFFFF")
        self.live2 = ttk.Label(lives_frame, background="#FFFFFF")
        self.live3 = ttk.Label(lives_frame, background="#FFFFFF")

        self.live1.pack(side=tk.LEFT)
        self.live2.pack(side=tk.LEFT, padx=3)
        self.live3.pack(side=tk.LEFT)

        # Create label for the question number.
        self.question_num = ttk.Label(topbar, font=("Arial", 25), background="#FFFFFF")
        self.question_num.grid(row=0, column=1, pady=5)

        # Frame for widgets on the right in topbar.
        right_widgets = tk.Frame(topbar, background="#FFFFFF")
        right_widgets.grid(row=0, column=2, padx=10, sticky="e")
        right_widgets.grid_propagate(False)

        # Create label for difficulty.
        self.difficulty_label = ttk.Label(right_widgets, font=("Arial", 20), style="OutlinedLabels.TLabel")
        self.difficulty_label.pack(side=tk.LEFT)

        # Create label for score.
        self.score_label = ttk.Label(right_widgets, font=("Arial", 20), style="OutlinedLabels.TLabel")
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Create timer label.
        self.timer_label = ttk.Label(right_widgets, font=("Arial", 20), style="OutlinedLabels.TLabel")
        self.timer_label.pack(side=tk.LEFT)

        # Create question instruction label.
        self.question_instruction = ttk.Label(contents_frame, font=("Cambria", 30), background="#FFFFFF", borderwidth=2, relief="solid", padding=(5, 5))
        self.question_instruction.grid(row=0, column=0, pady=100)

        # Create question label.
        self.question_label = ttk.Label(contents_frame, font=("Cambria", 50), background="#FFFFFF", borderwidth=2, relief="solid", padding=(50, 50))
        self.question_label.grid(row=1, column=0)

        # Create frame for the answering widgets.
        answering_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        answering_frame.pack(pady=(20, 15))

        # Create entry field for user's answer.
        self.answer_entry = ttk.Entry(answering_frame, font=("Arial", 30), width=20)
        self.answer_entry.grid(row=0, column=0, padx=5)

        # Keybind for answer entry button.
        self.answer_entry.bind("<Return>", lambda: self.controller.check_answer(self.answer_entry.get()))

        # Style for 'Submit'/'Next' button.
        controller.style.configure("Submit.TButton", font=("Cambria", 30), background="#00CC11", foreground="#FFFFFF") # 'Submit' button.
        controller.style.map("Submit.TButton", foreground=[("pressed", "#000000"), ("active", "#000000")])

        controller.style.configure("Next.TButton", font=("Cambria", 30), background="#FFFFFF", foreground="#000000") # 'Next' button.

        # Create 'Submit'/'Next' button.
        self.submitnext_btn = ttk.Button(
            answering_frame, text="Submit",
            style="Submit.TButton",
            width=7,
            command=lambda: self.controller.check_answer(self.answer_entry.get()))
        self.submitnext_btn.grid(row=0, column=1, padx=5)

        # Create feedback label.
        self.feedback_label = ttk.Label(self, font=("Cambria", 25), background="#FFFFFF", borderwidth=2, relief="solid", padding=(3, 3))

        # Image of a musical instrument based on selected difficulty.
        self.instrument_image = ttk.Label(self, background="#FFFFFF", borderwidth=2, relief="solid")
        self.instrument_image.place(relx=1, rely=0.5, anchor="e", x=-30)

        # Create footer.
        create_footer(self)

    # Loads initial assets when game starts.
    def load_assets(self):
        # Check if lives' heart images are missing or not.
        if self.controller.images.get("Avaliable Live") and self.controller.images.get("Unavaliable Live"):
            self.live1.configure(image=self.controller.images["Avaliable Live"])
            self.live2.configure(image=self.controller.images["Avaliable Live"])
            self.live3.configure(image=self.controller.images["Avaliable Live"])
        else:
            self.live1.configure(text=AVALIABLE_LIVE_TEXT, font=("Arial", 15))
            self.live2.configure(text=AVALIABLE_LIVE_TEXT, font=("Arial", 15))
            self.live3.configure(text=AVALIABLE_LIVE_TEXT, font=("Arial", 15))

        # Set 'lives' label colour to black.
        self.lives_label.configure(foreground="#000000")
        
        # Set text for the difficulty label.
        self.difficulty_label.configure(text=self.controller.selected_difficulty)

        # Set text for the score label.
        self.score_label.configure(text=f"Score: {self.controller.total_score}/{NUM_QUESTIONS}")

        # Set 'submitnext_btn' to 'submit' button.
        self.submitnext_btn.config(text="Submit", style="Submit.TButton", command=lambda: self.controller.check_answer(self.answer_entry.get()))

        # Make answer entry accessible.
        self.answer_entry.config(state="normal")

        # Clear answer entry field.
        self.answer_entry.delete(0, tk.END)

        # Set max length for answer entry.
        self.answer_entry_limit = self.register(lambda val: self.controller.entry_limit(val, MAX_ENTRY_LEN_ANSWER[self.controller.selected_difficulty]))
        self.answer_entry.configure(validate="key", validatecommand=(self.answer_entry_limit, "%P"))

        # Remove feedback label.
        self.feedback_label.pack_forget()

        # Load image of the musical instrument.
        if self.controller.images.get(f"{self.controller.selected_difficulty} Mode Image"):
            self.instrument_image.configure(text="", image=self.controller.images[f"{self.controller.selected_difficulty} Mode Image"], padding=0)
        else:
            self.instrument_image.configure(text="Unable to display image.", font=("Arial", 20), image="", padding=(3, 3))

        # Keybind for answer entry button.
        self.answer_entry.bind("<Return>", lambda event: self.controller.check_answer(self.answer_entry.get()))

        # Set focus to answer entry.
        self.answer_entry.focus_set()

    # Place 'confirm_label' when mouse cursor hovers over quit button.
    def cursor_on(self, event=None):
        self.confirm_label.place(relx=0, rely=0, x=130, y=22)
    
    # Remove 'confirm_label' when mouse cursor hovers over quit button.
    def cursor_off(self, event=None):
        self.confirm_label.place_forget()

    # Updates question, question instruction, and question number labels with current question.
    def update_questions(self):
        self.question_num.configure(text=f"Question: {self.controller.question_number}/{NUM_QUESTIONS}")
        self.question_instruction.configure(text=self.controller.questions[self.controller.question_number]["Instruction"])
        self.question_label.configure(text=self.controller.questions[self.controller.question_number]["Question"])
    
    # Function generate feedback for each answer.
    def display_feedback(self, incorrectly_answered=False):
        if incorrectly_answered:
            # Generate random number for random feedback message.
            message_index = random.randrange(4)

            # Get correct answer.
            correct_answer = self.controller.questions[self.controller.question_number]["Answer"]
            # Format subtraction symbols (if any).
            correct_answer = correct_answer.replace("-", "−")

            # Display feedback label.
            self.feedback_label.configure(
                text=f"✗ {INCORRECT_ANSWER_RESPONSES[message_index]} The correct answer was {correct_answer}."
                )
            self.feedback_label.pack()
        else:
            # Set text for the score label.
            self.score_label.configure(text=f"Score: {self.controller.total_score}/{NUM_QUESTIONS}")

            # Generate random number for random feedback message.
            message_index = random.randrange(5)

            # Display feedback label.
            self.feedback_label.configure(
                text=f"✓ {CORRECT_ANSWER_RESPONSES[message_index]}"
                )
            self.feedback_label.pack()

        # Make answer entry readonly.
        self.answer_entry.config(state="readonly")

        # Keybind for answer entry button.
        self.answer_entry.bind("<Return>", self.next_question)

        # Change 'submitnext_btn' to 'next' button.
        self.submitnext_btn.config(text="Next", style="Next.TButton", command=self.next_question)
    
    # Function to display the next question on the condition if the user has remaining lives or whether they have answered every question.
    def next_question(self, event=None):
        # Change 'submitnext_btn' to 'submit' button.
        self.submitnext_btn.config(text="Submit", style="Submit.TButton", command=lambda: self.controller.check_answer(self.answer_entry.get()))

        # If user has lost all lives.
        if self.controller.lives_count == 0:
            # End game as the user has lost.
            self.controller.end_game()
            return
        
        # If user has not lost all lives but has not answered every question.
        elif self.controller.question_number < NUM_QUESTIONS:
            # Add '1' to question number.
            self.controller.question_number += 1
        
        # If user has answered all questions and has remaining lives.
        else:
            # End game as the user has won.
            self.controller.end_game()
            return
        
        # Change widget states if program is to display the next question.
        # Make answer entry accessible again.
        self.answer_entry.config(state="normal")

        # Clear answer entry field.
        self.answer_entry.delete(0, tk.END)

        # Remove feedback label.
        self.feedback_label.pack_forget()

        # Keybind for answer entry button.
        self.answer_entry.bind("<Return>", lambda event: self.controller.check_answer(self.answer_entry.get()))

        self.update_questions()

    # Remove life function.
    def remove_life(self):
        # Makes sure the number of lives remaining is above 0.
        if self.controller.lives_count > 0:
            # Which live in the top bar to remove (from the 3rd one).
            live_number = getattr(self, f"live{self.controller.lives_count}")

            # Check if lives' heart images are missing or not.
            if self.controller.images.get("Avaliable Live") and self.controller.images.get("Unavaliable Live"):
                # Replace avaliable life with unavaliable life image.
                live_number.configure(image=self.controller.images["Unavaliable Live"])
            else:
                live_number.configure(text=UNAVALIABLE_LIVE_TEXT)
    
    # Updates countdown timer.
    def update_timer(self):
        # Convert seconds into minutes and seconds.
        self.controller.minutes = self.controller.time_remaining // 60
        self.controller.seconds = self.controller.time_remaining % 60

        # Display time in MM:SS format in timer label.
        self.timer_label.configure(text=f"{self.controller.minutes:02}:{self.controller.seconds:02}")

        # Check if time has reached 10 seconds or below to warn user that time is running out.
        if self.controller.time_remaining <= 30 and self.controller.time_remaining > 10:
            self.timer_label.configure(foreground="#F89D1F")
        
        # Check if time has reached 10 seconds or below to warn user that time is critically running out.
        elif self.controller.time_remaining <= 10:
            self.timer_label.configure(foreground="#FF0000")
        
        # Sets to black if user starts a new game with new countdown duration.
        else:
            self.timer_label.configure(foreground="#000000")
    
        # Continue counting down if there is still time remaining.
        if self.controller.time_remaining > 0:
            self.controller.time_remaining -= 1

            # Run function again after 1 second (1000 milliseconds) and set it as timer ID.
            self.timer_id = self.after(1000, self.update_timer)
        
        else:
            # No more time remaining.
            self.timer_label.configure(text="00:00")

            # End game as the user has lost.
            self.controller.end_game()

    # Function to cancel the timer.
    def cancel_timer(self):
        # Cancel timer.
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)

            # Clear timer ID.
            self.timer_id = None
    
    # Function to quit gameplay.
    def quit_game(self):
        # Cancel the timer.
        self.cancel_timer()

        # Set game variables (except 'haswon') to empty values.
        self.controller.selected_difficulty = ""
        self.controller.questions = {}
        self.controller.question_number = None
        self.controller.total_score = None
        self.controller.lives_count = None
        self.controller.time_remaining = None
        self.controller.minutes = None
        self.controller.seconds = None

        # Go back to lobby screen.
        self.controller.display_page(LobbyScreen)


# This displays the user's score and results after completing the quiz, and then stores it in the data file (.json) containing every user's previous scores.
class ResultsScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Calls the parent class 'tk.Frame' to initialise the page's frame.
        super().__init__(parent)

        controller.display_background(self)

        # Reference for main 'App' method.
        self.controller = controller

        # The time remaining in user's completed quiz (in minutes and seconds) (initially set to 'None').
        self.time_left = None

        # The Date & Time when the user completed a quiz (saved to their quiz score) (initially set to 'None').
        self.dateandtime = None

        # Create frame for title and subheader.
        title_frame = tk.Frame(self, background="#FFFFFF", borderwidth=3, relief="solid")
        title_frame.pack(pady=(50, 30), ipadx=5)

        # Create title label (the message displayed).
        self.title_label = ttk.Label(title_frame, font=("Berlin Sans FB", 50), background="#FFFFFF")
        self.title_label.pack(pady=5)

        # Create subheader.
        self.subheader_text = ttk.Label(title_frame, font=("Cambria", 25), background="#FFFFFF")
        self.subheader_text.pack(pady=5)

        #Create frame for main contents.
        self.main_frame = tk.Frame(self, background="#FFFFFF", width=1000, height=600)
        self.main_frame.pack_propagate(False)
        self.main_frame.grid_propagate(False)
        
        # Configures the alignments for its child widgets.
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Top bar and contents frame.
        topbar = tk.Frame(self.main_frame, background="#FFFFFF", borderwidth=3, relief="solid")
        topbar.grid(row=0, column=0, sticky="ew")

        # Contents frame.
        contents_frame = tk.Frame(self.main_frame, background="#FFFFFF", borderwidth=3, relief="solid")
        contents_frame.grid(row=1, column=0, sticky="nsew")

        # Adjust widths of child frames to fit correctly.
        contents_frame.grid_columnconfigure(0, weight=1)
        contents_frame.grid_columnconfigure(1, weight=1)
        contents_frame.grid_columnconfigure(2, weight=1)

        # Create main frame header (goes in topbar).
        self.mainframe_header = ttk.Label(topbar, font=("Arial", 25), background="#FFFFFF")
        self.mainframe_header.pack(pady=5)

        # Create frame for 'Score'.
        score_frame = tk.Frame(contents_frame, background="#FFFFFF", borderwidth=1, relief="solid", width=250, height=101)
        score_frame.grid(row=0, column=0, sticky="nsew")
        score_frame.grid_propagate(False)

        # Create 'Score' header.
        score_header = ttk.Label(score_frame, text="Score", font=("Arial", 25, "underline"), background="#FFFFFF")
        score_header.pack(pady=5)

        # Create 'Score' label.
        self.score_label = ttk.Label(score_frame, font=("Arial", 25), background="#FFFFFF")
        self.score_label.pack(pady=(0, 5))

        # Create frame for 'Time Remaining'.
        time_frame = tk.Frame(contents_frame, background="#FFFFFF", borderwidth=1, relief="solid", width=250, height=101)
        time_frame.grid(row=0, column=1, sticky="nsew")
        time_frame.grid_propagate(False)

        # Create 'Time Remaining' header.
        time_header = ttk.Label(time_frame, text="Time Remaining", font=("Arial", 25, "underline"), background="#FFFFFF")
        time_header.pack(pady=5)

        # Create 'Time Remaining' label.
        self.time_label = ttk.Label(time_frame, font=("Arial", 25), background="#FFFFFF")
        self.time_label.pack(pady=(0, 5))

        # Create frame for 'Date & Time'.
        datetime_frame = tk.Frame(contents_frame, background="#FFFFFF", borderwidth=1, relief="solid", width=500, height=101)
        datetime_frame.grid(row=0, column=2, sticky="nsew")
        datetime_frame.grid_propagate(False)

        # Create 'Date & Time' header.
        datetime_header = ttk.Label(datetime_frame, text="Date & Time", font=("Arial", 25, "underline"), background="#FFFFFF")
        datetime_header.pack(pady=5)

        # Create 'Date & Time' label.
        self.datetime_label = ttk.Label(datetime_frame, font=("Arial", 25), background="#FFFFFF")
        self.datetime_label.pack(pady=(0, 5))

        # Label for motivational message.
        self.motivational_message = ttk.Label(self, font=("Cambria", 25), background="#FFFFFF", borderwidth=2, relief="solid", padding=(3, 3))

        # Random accompanying image (displayed if user doesn't score any points at all).
        self.accompanying_image = ttk.Label(self, background="#FFFFFF", borderwidth=2, relief="solid")

        # Style for 'Return to Lobby' button.
        controller.style.configure("ReturnToLobby.TButton", font=("Arial", 30), background="#FFFFFF")

        # Create 'Return to Lobby' button.
        self.return_to_lobby_btn = ttk.Button(self, text="Return To Lobby", style="Start.TButton", width=16, command=self.return_to_lobby)
        self.return_to_lobby_btn.pack(pady=(30, 0))

        # Create footer.
        create_footer(self)
    
    # Function to display the results.
    def display_results(self):
        # Temperarily remove the 'Return to Lobby' button.
        self.return_to_lobby_btn.pack_forget()

        # If user has won.
        if self.controller.haswon:
            self.show_winning_screen()

        # If user has lost.
        else:
            self.show_losing_screen()

        # Pack 'Return to Lobby' button.
        self.return_to_lobby_btn.pack(pady=(30, 0))
    
    # Function to display the winning screen.
    def show_winning_screen(self):
        # Update title message.
        self.title_label.configure(text=WINNING_MESSAGES[self.controller.total_score])

        # Update subheader.
        self.subheader_text.configure(text="You won the game!")

        # Display user's score.
        self.show_score()

        # Display motivational message if user has run out of time or lives.
        if self.controller.time_remaining == 0:
            # Generate random number for random motivational message.
            message_index = random.randrange(2)

            self.motivational_message.configure(text=WINNING_FEEDBACK["Time"][message_index])
            self.motivational_message.pack(pady=(10, 0))
        elif self.controller.lives_count == 0:
            # Generate random number for random motivational message.
            message_index = random.randrange(2)

            self.motivational_message.configure(text=WINNING_FEEDBACK["Lives"][message_index])
            self.motivational_message.pack(pady=(10, 0))

        # Play winning sound.
        pygame.mixer.stop() # Stop any previous sounds if they are still playing.
        try:
            sound_path = SOUND_PATHS[self.controller.selected_difficulty]["Winning_sound"]
            pygame.mixer.Sound(sound_path).play()
        except:
            pass
        
        # Save score to .json.
        self.save_results(self.controller.previous_scores, self.controller.previous_scores_filepath)

    # Function to display the losing screen.
    def show_losing_screen(self):
        # Update title message.
        self.title_label.configure(text="Game Over")

        # Displays score regardless unless the user has no score.
        if self.controller.total_score > 0:
            # Display score.
            self.show_score()
        
            # Save score to .json.
            self.save_results(self.controller.previous_scores, self.controller.previous_scores_filepath)
        else:
            # Generate random number for random motivational message.
            message_index = random.randrange(2)

            # Display motivational message.
            self.motivational_message.configure(text=MOTIVATIONAL_MESSAGES[message_index])
            self.motivational_message.pack(pady=(10, 0))

            # Generate random number for random accompanying image.
            image_index = random.randint(1, 3)

            # Display random accompanying image.
            if self.controller.images.get(f"Game Over Image {image_index}"):
                self.accompanying_image.configure(text="", image=self.controller.images[f"Game Over Image {image_index}"], padding=0)
            else:
                self.accompanying_image.configure(text="Unable to display image.", font=("Arial", 20), image="", padding=(3, 3))

            # Pack image.
            self.accompanying_image.pack(pady=75)

        # Display subheader message if user has run out of time or lives.
        if self.controller.time_remaining == 0:
            # Update subheader.
            self.subheader_text.configure(text="You ran out of time!")
        elif self.controller.lives_count == 0:
            # Update subheader.
            self.subheader_text.configure(text="You ran out of lives!")

        # Play losing sound.
        pygame.mixer.stop() # Stop any previous sounds if they are still playing.
        try:
            sound_path = SOUND_PATHS[self.controller.selected_difficulty]["Losing_sound"]
            pygame.mixer.Sound(sound_path).play()
        except:
            pass

    # Function to display the user's score unless they did not score at all.
    def show_score(self):
        # Display main frame.
        self.main_frame.pack()

        # Display main frame header.
        self.mainframe_header.configure(text=f"{self.controller.current_user}'s Score")

        # Display Score.
        self.score_label.configure(text=f"{self.controller.total_score}/{NUM_QUESTIONS}")

        # Get time remaining.
        self.time_left = f"{self.controller.minutes:02}:{self.controller.seconds:02}"
        
        # Display Time (time remaining).
        self.time_label.configure(text=self.time_left)

        # Get Date & Time.
        self.dateandtime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

        # Display Date & Time.
        self.datetime_label.configure(text=self.dateandtime)
    
    # Saves results to .json file containing the previous scores of every registered account (used for the leaderboard and each account's personal previous scores).
    def save_results(self, scores_dict, file):
        # Add results to 'previous_scores' dictionary.
        userscore_record = {
            "Score": self.controller.total_score,
            "Difficulty": self.controller.selected_difficulty,
            "Time Remaining": self.time_left,
            "Date & Time": self.dateandtime
        }

        # Save score to .json file containing every accounts' previous scores.
        try:
            # Prevents duplicating a username in dictionary.
            if self.controller.current_user not in scores_dict:
                # Create an empty list of records dedicated to the current user.
                scores_dict[self.controller.current_user] = []
            
            # Add score to dictionary under the user's username.
            scores_dict[self.controller.current_user].append(userscore_record)

            # Write to .json file.
            with open(file, "w", encoding="utf-8") as f:
                # Append sorted dictionary to file.
                json.dump(dict(sorted(scores_dict.items())), f, indent=4)
        except Exception as e:
            # Display error message.
            messagebox.showerror("Error!", f"Failed to save score record to .json file:\n{e}.")
            # Remove recently added item.
            del scores_dict[self.controller.current_user][-1]

            # Checks if that is the only record under the user's username.
            if not scores_dict[self.controller.current_user]:
                # Delete username in dictionary if there are no records.
                del scores_dict[self.controller.current_user]
            return
    
    # Function to return to lobby screen.
    def return_to_lobby(self):
        # Set game variables to empty values.
        self.controller.selected_difficulty = ""
        self.controller.questions = {}
        self.controller.question_number = None
        self.controller.total_score = None
        self.controller.lives_count = None
        self.controller.time_remaining = None
        self.controller.minutes = None
        self.controller.seconds = None
        self.controller.haswon = None

        # Set variables for time remaining and date and time to empty values.
        self.time_left = None
        self.dateandtime = None

        # Remove (hide) main frame, motivational message widgets, and random accompanying image.
        self.main_frame.pack_forget()
        self.motivational_message.pack_forget()
        self.accompanying_image.pack_forget()

        # Return to lobby screen.
        self.controller.display_page(LobbyScreen)

# ==================================================

# This initialises the code when the program starts running, and puts the GUI window into a permanent loop to prevent it from closing.
if __name__ == "__main__":
    app = App()
    app.mainloop()
