import subprocess
import sys
import os
from tkinter import Tk, filedialog, Button, Label, ttk, messagebox
import webbrowser

# Check and install missing dependencies
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing zxcvbn, install if missing
try:
    import zxcvbn
except ImportError:
    install("zxcvbn")
    import zxcvbn

# Function to test password strength
def test_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    return result["score"]

# Function to process the file and display progress
def process_file(file_path, progress_bar, progress_label):
    with open(file_path) as f:
        lines = f.readlines()

    total_lines = len(lines)
    with open("results.txt", "w") as out_file:
        for idx, line in enumerate(lines):
            values = line.strip().split("\t")
            if len(values) >= 2:
                name = values[0]
                password = values[1]
                strength = test_password_strength(password)
                out_file.write(f"Username: {name}\n")
                out_file.write(f"Password: {password}\n")
                out_file.write(f"Strength: {str(strength)}\n\n")
            
            # Update progress bar
            progress = (idx + 1) / total_lines * 100
            progress_bar['value'] = progress
            progress_label.config(text=f"Progress: {int(progress)}%")
            root.update_idletasks()

    messagebox.showinfo("Process Completed", "Password strength test completed!")

# Function to open result file
def open_result_file():
    os.startfile("results.txt")

# Function to open result folder
def open_result_folder():
    folder = os.path.dirname(os.path.abspath("results.txt"))
    webbrowser.open(folder)

# Function to select and process the file
def select_file():
    file_path = filedialog.askopenfilename(title="Select file", filetypes=(("Text files", "*.txt"),))
    if file_path:
        process_file(file_path, progress_bar, progress_label)

# Set up the GUI
root = Tk()
root.title("Password Strength Tester")
root.geometry("497x497")  # Set default window size to 497x497

# Title label
title_label = Label(root, text="Password Strength Testing Tool", font=("Helvetica", 14, "bold"))
title_label.pack(pady=10)

# Select file label and button
label = Label(root, text="Select a file to test password strength", font=("Helvetica", 10))
label.pack(pady=10)

select_file_button = Button(root, text="Select File", command=select_file, width=20)
select_file_button.pack(pady=10)

# Progress bar and progress label
progress_label = Label(root, text="Progress: 0%", font=("Helvetica", 10))
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Buttons to open result file or folder
open_result_button = Button(root, text="Open Result File", command=open_result_file, width=20)
open_result_button.pack(pady=5)

open_folder_button = Button(root, text="Open Result Folder", command=open_result_folder, width=20)
open_folder_button.pack(pady=5)

# Instruction label with detailed explanation
instructions = Label(
    root,
    text="File Format Requirements:\n\n"
         "- The file should be a .txt file.\n"
         "- Each line must contain a username and password separated by a tab.\n\n"
         "Example:\n"
         "username[TAB]password\n"
         "john_doe[TAB]password123\n"
         "jane_smith[TAB]securepassword",
    font=("Helvetica", 9),
    fg="darkblue",
    justify="left",
    wraplength=400
)
instructions.pack(pady=15, side="bottom")

root.mainloop()
