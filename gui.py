from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk
import plagiarism_checker


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

    def highlight_text(text_widget, phrase):
        """ Highlights occurrences of a phrase in a text widget """
        start_index = "1.0"
        while True:
            start_index = text_widget.search(phrase, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(phrase)}c"
            text_widget.tag_add("match", start_index, end_index)
            text_widget.tag_config("match", background="yellow", foreground="black")
            start_index = end_index

    def find_and_highlight_matches():
        """ Uses imported function to find matches and highlight them """
        text1_content = entry1.get()
        text2_content = entry2.get()

        if not text1_content or not text2_content:
            return

        # Call the imported function from text_matcher.py
        matches = plagiarism_checker.check_plagiarism(text1_content, text2_content)

        # Highlight matches in both text boxes
        text1.configure(state='normal')
        text2.configure(state='normal')

        text1.tag_remove("match", "1.0", tk.END)
        text2.tag_remove("match", "1.0", tk.END)

        for match in matches:
            highlight_text(text1, match)
            highlight_text(text2, match)

        text1.configure(state='disabled')
        text2.configure(state='disabled')

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

    # Button to find matches
    match_button = tk.Button(root, text="Find Matches", font=("Consolas", 10), command=find_and_highlight_matches)
    match_button.grid(row=4, column=1)

    # Run the application
    root.mainloop()

gui()
