# Main implementation 

import tkinter as tk
from tkinter import filedialog

def open_file(entry_widget, text_widget):
    """ Open a file and display its contents in the text widget """
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, content)

# Create main window
root = tk.Tk()
root.title("Text Document Input")

# First file selection
tk.Label(root, text="Select First Text Document:").grid(row=0, column=0)
entry1 = tk.Entry(root, width=50)
entry1.grid(row=0, column=1)
btn1 = tk.Button(root, text="Browse", command=lambda: open_file(entry1, text1))
btn1.grid(row=0, column=2)

text1 = tk.Text(root, height=10, width=60)
text1.grid(row=1, column=0, columnspan=3)

# Second file selection
tk.Label(root, text="Select Second Text Document:").grid(row=2, column=0)
entry2 = tk.Entry(root, width=50)
entry2.grid(row=2, column=1)
btn2 = tk.Button(root, text="Browse", command=lambda: open_file(entry2, text2))
btn2.grid(row=2, column=2)

text2 = tk.Text(root, height=10, width=60)
text2.grid(row=3, column=0, columnspan=3)

# Run the application
root.mainloop()


import tkinter as tk
from tkinter import filedialog

def open_file(entry_widget, text_widget):
    """ Open a file and display its contents in the text widget """
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, content)

# Create main window
root = tk.Tk()
root.title("Text Document Input")

# First file selection
tk.Label(root, text="Select First Text Document:").grid(row=0, column=0)
entry1 = tk.Entry(root, width=50)
entry1.grid(row=0, column=1)
btn1 = tk.Button(root, text="Browse", command=lambda: open_file(entry1, text1))
btn1.grid(row=0, column=2)

text1 = tk.Text(root, height=10, width=60)
text1.grid(row=1, column=0, columnspan=3)

# Second file selection
tk.Label(root, text="Select Second Text Document:").grid(row=2, column=0)
entry2 = tk.Entry(root, width=50)
entry2.grid(row=2, column=1)
btn2 = tk.Button(root, text="Browse", command=lambda: open_file(entry2, text2))
btn2.grid(row=2, column=2)

text2 = tk.Text(root, height=10, width=60)
text2.grid(row=3, column=0, columnspan=3)

# Run the application
root.mainloop()