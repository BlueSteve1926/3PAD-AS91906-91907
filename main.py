"""
Date 8/05/2026
Purpose: Flow Computing Maths Game - AS91906
Version: 1.0
Author: Ryan Fernando
"""

# ===== Importing modules =====

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import random
import time
import json
from PIL import Image, ImageTk
import sympy
from sympy import symbols, diff, simplify, sympify

"""
This gets the absolute path of the files' directory, so it opens the files which are used in the program.
It is important so the program can run properly while getting all the relevant files,
regardless of which device it is being run on and where or how the program is run.
"""
base_dir = os.path.dirname(os.path.abspath(__file__))
