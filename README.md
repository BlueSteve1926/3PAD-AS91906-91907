Flow Computing

----------------------------------------

READ ME

----------------------------------------

Author: Ryan Fernando

Date: 08/05/2026

Version: 9.0

----------------------------------------

Overview

This program was developed using Python (3.14.6). The graphical user interface (GUI) was designed using Tkinter to provide visual interactions. The app is designed to improve students' math skills by having them take timed quizzes covering a range of topics from simple to complex. Students can select a difficulty so they can work on developing their weaker areas while reinforcing their stronger areas to prevent losing touch with them. Students must register their own account in order to save all scores from each quiz. Each quiz has a 5-minute timer to test and improve their working speed, and there are 3 lives, which test their accuracy on the questions. These elements incorporate game-like elements to make learning more engaging for this specific target audience.


Features

- User-friendly GUI interface ensuring there are no issues with visuals and functionality
- A signup page to register an account, and a login page to log into it
- 4 difficulties (Easy, Medium, Hard, Challenge) featuring different mathematical topics
- Displays images which engage with users to create a proper game-like experience
- A leaderboard of each account's highest score, sorted by score, then time remaining. This is categorised by difficulty.
- A page for personal scores of the account logged in where they can view their score history. This is also categorised by difficulty.
- Appropriate feedback given in quiz results
- Input validation and error handling


Requirements

- Python 3.10 or higher
- Tkinter (usually included with Python)
- Pillow (for managing and displaying images)
- Pygame Community Edition (for sound effects)
- SymPy (for the advanced mathematical questions)


How to Run


1. Ensure your Python version is 3.10 or above.

2. Install the following libraries if you have not installed them yet:
	- Pillow
	- Pygame Community Edition
	- SymPy

   Open Command Prompt (CMD) or Terminal and run the following:
	- pip install pillow
	- pip install pygame-ce
	- pip install sympy

   These will work on Windows (Command Prompt), macOS, and Linux (Terminal).

3. Ensure all project files and folders are in the same directory as the program.

4. Run the main program, which is located in the "Program" folder:
main.py


Usage

- An account must be created via the signup page where a valid username and password must be entered. A maximum length of 20 characters can be entered for username, and 32 for password. The program rejects invalid data where some characters or lengths are not allowed to be accepted. These will be handled where the error messages give feedback on what is acceptable for your username and password.
- After signing in or logging in, you can select any difficulty from the lobby screen.
- You have 5 minutes to complete a quiz, and 3 lives to help pay attention to accuracy. Each difficulty level has instructions on what the questions are about and how they should be answered. Spaces between operators are not required to be entered as the program handles that already, allowing you to answer questions more quickly.
- Your score will be saved if you get a score of 1 or above (maximum score is 10 for each quiz). A score of 5 or greater is required to win. Even if you score lower than 5 but at least 1, the results will still be saved even though you lost. Getting no score at all (a score of 0) means you have effectively lost, and results won't be saved.
- You can view all your scores on the "Previous Scores" page, which the button for it is located on the lobby screen. The lobby screen also has a button on the top-left to view the leaderboard, where all the top scores of every registered user are ranked. Both the leaderboard and previous scores are categorised by difficulty - use the combo box to select a difficulty and view its records.
- If you want to log out, the logout button is located at the top-right of the lobby screen. After logging out, you can either log in or sign up, or click the "Quit" button to exit the program.

Note: Since the program's window size is automatically maximised and is designed for 1920x1080 screen sizes, a 1080p screen device is recommended. Otherwise, display settings can be changed in the "Display" section in your device's "Settings" utility by changing the "Scale" and/or "Display resolution" properties. An insufficient screen size can obscure some of the widgets from view, making several of the program's functions and features inaccessible.


Testing

- Input validations ensure proper data entry.
- Message boxes handle empty or invalid inputs with clear messages.
- The leaderboard and personal scores listboxes update and display the data correctly. Each user's score history contains every score from each time they have completed a quiz. This is sorted by date from latest to oldest. The leaderboard ranks each player's highest score from highest to lowest, then by time remaining if there are 2 or more records with the same score. Time remaining is sorted from highest to lowest as well.
- A temporary data list (called a "set") is used to make sure no duplicated questions appear in a quiz. It temporarily stores each question, then runs through and checks whether the next randomly-generated question is identical to any of the others.


Problems/Limitations:
- It may take a moment to start the program and load some assets due to the number of modules and processes they make. This can also depend on your computer's processing speed.
- The window won't be displayed properly on devices with smaller screen sizes (smaller than 1920x1080), resulting in some GUI widgets being hidden from view. Make sure you use a 1080p device to be able to access all widgets in the program. Read the note under the "Usage" section for more information on this limitation and how to overcome it if your device's screen size is unsuitable.

Thanks for reading!
