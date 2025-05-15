from tkinter import *
import os
import pprint

# ---------------------------- Data processing ------------------------------- #
texts = [] # List of dictionares "filename": filename, "content": content
folder = "data" # Folder with texts

# Open files and save into texts
for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        path = os.path.join(folder, filename) # Create full file pass
        print(path)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            texts.append({"filename": filename, "content": content})


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("The Most Dangerous Writing App")
window.config(padx=40, pady=40)


window.mainloop()