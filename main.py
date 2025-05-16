import tkinter as tk
from tkinter import messagebox
import os
import time
import random

class DangerousWritingApp:
    def __init__(self, window, folder="data", user_time=5):
        self.window = window
        self.window.title("The Most Dangerous Writing App")
        self.window.config(padx=40, pady=40)
        self.window.geometry("800x800")

        self.user_time = user_time
        self.last_keypress_time = None # Timer doesn't work, waiting start button
        self.folder = folder
        self.texts = self.load_texts()
        # Check empty folder
        if not self.texts:
            messagebox.showerror("Error", f"No text files found in folder '{folder}'")
            window.destroy()
            return

        # Choose random text
        self.random_text = random.choice(self.texts)
        self.text_name = self.random_text["filename"].split(".")[0] # Name of text without .txt

        # Timer label
        self.timer = tk.Label(window, text=f"Timer: {self.user_time} sec", font=("Calibri", 18, "bold"))
        self.timer.pack(fill="x", pady=10)

        # Text name label
        self.text_name = tk.Label(window, text=self.text_name, font=("Calibri", 18, "bold"))
        self.text_name.pack(fill="x", pady=10)

        # User time label
        self.time_label = tk.Label(text="Enter time (sec):", font=("Calibri", 12))
        self.time_label.pack()

        # User time input
        self.user_time_input = tk.Entry(width=20,)
        self.user_time_input.insert(0, "5")
        self.user_time_input.pack(pady=10)

        # Start button
        self.start_button = tk.Button(window, text="Start", width=10, font=("Calibri", 18, "bold"),
                                      bg="#4CAF50",
                                      fg="white",
                                      command=self.start_timer)
        self.start_button.pack(padx=10)

        # Example (non-editable) text field
        self.example_field = tk.Text(window, height=10, wrap="word", font=("Calibri", 14))
        self.example_field.insert("1.0", self.random_text["content"])
        self.example_field.config(state="disabled",
                                  bg="#1e1e1e",  # black bg
                                  fg="#d4d4d4",  # white text
                                  insertbackground="#d4d4d4",
                                  selectbackground="#264f78",
                                  selectforeground="#ffffff"
                                  )
        self.example_field.tag_configure("correct", background="#c8e6c9", foreground="#000000")  # Correct tag color
        self.example_field.tag_configure("wrong", background="#ffcdd2", foreground="#000000")  # Not correct tag color
        self.example_field.pack(fill="x", pady=10)

        # User input field
        self.text_field = tk.Text(window, font=("Calibri", 14), wrap="word")
        self.text_field.config(
                                bg="#1e1e1e",  # black bg
                                fg="#d4d4d4",  # white text
                                insertbackground="#d4d4d4",
                                selectbackground="#264f78",
                                selectforeground="#ffffff",
                                state="disabled"
                                )
        self.text_field.pack(expand=True, fill="both")
        self.text_field.bind("<KeyRelease>", self.on_key) # Call on_key function every time user press button
        self.text_field.focus_set()


    def load_texts(self):
        """
        Load texts from "data" folder
        :return: list of dictionares "texts"
        """
        texts = []
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        for filename in os.listdir(self.folder):
            if filename.endswith(".txt"):
                path = os.path.join(self.folder, filename)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                    texts.append({"filename": filename, "content": content})
        return texts

    def on_key(self, event):
        """
        Check last keypress time.
        Logic for checking correct text input. Green/red backlighting when entering character by character.
        :param event: only for tkinter bind option
        :return: nothing
        """
        if self.last_keypress_time is not None:
            self.last_keypress_time = time.time()

        # User text
        user_text = self.text_field.get("1.0", tk.END).rstrip("\n")
        # Example
        example_text = self.random_text["content"]

        # Clear previous tags
        self.example_field.tag_remove("correct", "1.0", tk.END)
        self.example_field.tag_remove("wrong", "1.0", tk.END)

        for i, char in enumerate(user_text):
            # If the user enters more characters than are in the example, we stop the loop.
            if i >= len(example_text):
                break
            pos_start = f"1.0 + {i} chars"
            pos_end = f"1.0 + {i + 1} chars"

            if char == example_text[i]:
                self.example_field.tag_add("correct", pos_start, pos_end)
            else:
                self.example_field.tag_add("wrong", pos_start, pos_end)

    def start_timer(self):
        """
        Start timer, function for Start Button
        :return: nothing
        """
        try:
            entered_time = int(self.user_time_input.get())
            if entered_time <=0:
                raise ValueError
            self.user_time = entered_time
            self.last_keypress_time = time.time()  # Setup start time
            self.check_idle() # Start main function
            self.start_button.config(state="disabled", bg="grey")  # Disable button after start
            self.user_time_input.config(state="disabled") # Disable entry after start
            self.text_field.config(state="normal") # Enable entry after start
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a positive integer for time.")

    def update_timer(self):
        now = time.time()
        remaining = int(self.user_time - (now - self.last_keypress_time))
        self.timer.config(text=f"Timer: {self.user_time} sec")

        return remaining

    def check_idle(self):
        """
        Main logic, check time from last keypress
        :return: nothing
        """
        # Check timer
        if self.last_keypress_time is None:
            return

        remaining = self.update_timer()
        # If time is over
        if remaining <= 0:
            self.text_field.delete("1.0", tk.END)
            messagebox.showwarning("Oops", "Your time is done!")

            # Restart App
            self.last_keypress_time = None
            self.update_example()
            self.start_button.config(state="normal", bg="#4CAF50")
            self.user_time_input.config(state="normal")
            self.text_field.config(state="disabled")
        else:
            # Continue to check remaining
            self.timer.config(text=f"Timer: {remaining} sec")
            self.window.after(1000, self.check_idle)

    def update_example(self):
        """
        Update example field text
        :return: nothing
        """
        self.random_text = random.choice(self.texts)
        self.example_field.config(state="normal")
        self.example_field.delete("1.0", tk.END)
        self.example_field.insert("1.0", self.random_text["content"])
        self.example_field.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root, user_time=5)
    root.mainloop()