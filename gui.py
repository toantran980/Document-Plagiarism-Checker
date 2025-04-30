from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk


import os

def gui():
    #root setup
    root = tk.Tk()
    root.title("Text Document Input")
    root.grid_columnconfigure(0, weight=1)
    root.geometry('550x400')

    #Global Variables
    Files = []
    totalSize = 0 #Running total of size of all files uploaded
    decompressFilePath = None

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

    def scan_and_compress():
        pass

    def decompress_button():
        pass

    def graph():
        pass

    def openFile():
        filepath = filedialog.askopenfilename()
        return filepath

    def details(file, output_file):
        input_size = GetFileSize(file)
        output_size = GetFileSize(output_file)
        ratio = round(((output_size/input_size) * 100), 2)
        detail = Label(root, text = f"Original: {input_size} bytes | Compressed: {output_size} | Ratio: {ratio}%", font=("Consolas", 8))
        detail.grid(row = 2)

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

gui()
