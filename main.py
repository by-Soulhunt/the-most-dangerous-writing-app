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

        self.user_time = user_time
        self.last_keypress_time = time.time()
        self.folder = folder
        self.texts = self.load_texts()
        if not self.texts:
            messagebox.showerror("Error", f"No text files found in folder '{folder}'")
            window.destroy()
            return

        self.random_text = random.choice(self.texts)

        # Timer label
        self.timer = tk.Label(root, text=f"Timer: {self.user_time} sec", font=("Arial", 18, "bold"))
        self.timer.pack(fill="x", pady=10)

        # Example (non-editable) text field
        self.example_field = tk.Text(root, height=10, wrap="word", font=("Arial", 14))
        self.example_field.insert("1.0", self.random_text["content"])
        self.example_field.config(state="disabled")
        self.example_field.pack(fill="x", pady=10)

        # User input field
        self.text_field = tk.Text(root, font=("Arial", 14), wrap="word")
        self.text_field.pack(expand=True, fill="both")
        self.text_field.bind("<Key>", self.on_key)
        self.text_field.focus_set()

        # Start timer check
        self.check_idle()

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
        Check last keypress time
        :param event: only for tkinter bind option
        :return: nothing
        """
        self.last_keypress_time = time.time()

    def check_idle(self):
        """
        Main logic, check time from last keypress
        :return: nothing
        """
        now = time.time()
        remaining = int(self.user_time - (now - self.last_keypress_time))
        if remaining <= 0:
            self.text_field.delete("1.0", tk.END)
            messagebox.showwarning("Oops", "Your time is done!")
            # Restart App
            self.last_keypress_time = time.time()
            self.update_example()
            self.timer.config(text=f"Timer: {self.user_time} sec")
            self.window.after(1000, self.check_idle)
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
    app = DangerousWritingApp(root, user_time=10)
    root.mainloop()