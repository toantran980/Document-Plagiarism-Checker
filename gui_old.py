from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk
from datetime import datetime
import string
import plagiarism_checker
from sorting_title import mergeSort
from naive import naive_search
from algorithms import generate_huffman_codes

import os

def gui():
    #root setup
    root = tk.Tk()
    root.title("Text Document Input")
    root.grid_columnconfigure(0, weight=1)
    root.geometry('1280x720')

    #Global Variables
    global Files
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

            # Add file metadata to the Files list
            file_metadata = {
                "author": os.path.basename(file_path),  # Use file name as author
                "title": os.path.splitext(os.path.basename(file_path))[0],  # File name without extension
                "date": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d"),  # Format date
            }
            Files.append(file_metadata)
            print(f"Added file metadata: {file_metadata}")

    def highlight_text(text_widget, phrase):
        """ Highlights occurrences of a whole word in a text widget without overlapping partial matches """
        start_index = "1.0"
    
        while True:
            start_index = text_widget.search(phrase, start_index, stopindex=tk.END)
            if not start_index:
                break
        
            # Compute indices for checking surrounding characters
            prev_char_index = f"{start_index}-1c"
            next_char_index = f"{start_index}+{len(phrase)}c"
        
            prev_char = text_widget.get(prev_char_index, start_index)
            next_char = text_widget.get(next_char_index, f"{next_char_index}+1c")

            # Ensure match is a whole word by checking surrounding characters
            if (prev_char in string.whitespace + string.punctuation or not prev_char) and \
                (next_char in string.whitespace + string.punctuation or not next_char):
                text_widget.tag_add("match", start_index, next_char_index)
                text_widget.tag_config("match", background="yellow", foreground="black")

            start_index = next_char_index

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

    def find_and_highlight_terms():
        text1_content = entry1.get()
        text2_content = entry2.get()
        term = entry3.get()
        print(term)

        if not text1_content or not text2_content:
            return

        #uses naive search to find terms across both documents
        text1_matches = naive_search(text1_content, term)
        text2_matches = naive_search(text2_content, term)

        if text1_matches and text2_matches != []:
            return
        print(term)
            
        # Highlight matches in both text boxes
        text1.configure(state='normal')
        text2.configure(state='normal')

        text1.tag_remove("match", "1.0", tk.END)
        text2.tag_remove("match", "1.0", tk.END)

        highlight_text(text1, term)
        highlight_text(text2, term)

        text1.configure(state='disabled')
        text2.configure(state='disabled')

    def display_huffman_codes():
        """Generate Huffman codes and update compression statistics separately."""
        text1_content = text1.get("1.0", tk.END).strip()
        text2_content = text2.get("1.0", tk.END).strip()

        if not text1_content or not text2_content:
            return

        # Generate Huffman codes and compression stats
        huffman_codes1, encoded_text1, original_size1, compressed_size1 = generate_huffman_codes(text1_content)
        huffman_codes2, encoded_text2, original_size2, compressed_size2 = generate_huffman_codes(text2_content)

        ratio1 = round((compressed_size1 / original_size1) * 100, 2)
        ratio2 = round((compressed_size2 / original_size2) * 100, 2)

        # Update Huffman code text boxes
        huffman1.delete("1.0", tk.END)
        huffman1.insert(tk.END, f"Huffman Codes:\n{huffman_codes1}")

        huffman2.delete("1.0", tk.END)
        huffman2.insert(tk.END, f"Huffman Codes:\n{huffman_codes2}")

        # Update compression stats labels
        original_size_label1.config(text=f"Original Size: {original_size1} bytes")
        compressed_size_label1.config(text=f"Compressed Size: {compressed_size1} bytes")
        compression_ratio_label1.config(text=f"Compression Ratio: {ratio1}%")

        original_size_label2.config(text=f"Original Size: {original_size2} bytes")
        compressed_size_label2.config(text=f"Compressed Size: {compressed_size2} bytes")
        compression_ratio_label2.config(text=f"Compression Ratio: {ratio2}%")



    def decompress_button():
        pass

    def graph():
        pass

    def openFile():
        filepath = filedialog.askopenfilename()
        return filepath

    def details(file, output_file):
        input_size = os.path.getsize(file)
        output_size = os.path.getsize(output_file)
        ratio = round(((output_size/input_size) * 100), 2)
        detail = Label(root, text = f"Original: {input_size} bytes | Compressed: {output_size} | Ratio: {ratio}%", font=("Consolas", 8))
        detail.grid(row = 2)

    def sort_files(attribute):
        """Sort files by the specified attribute and display the sorted list."""
        global Files
        if not Files:
            print("No files to sort.")
            return

        mergeSort(Files, key=attribute)  # Sort the global Files list
        print(f"Files sorted by {attribute}:")
        for file in Files:
            print(file)

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

    # Box to enter search term
    entry3 = tk.Entry(root, width = 50)
    entry3.grid(row=4,column = 6)
    search_button = tk.Button(root, text = "Search", font=("Consolas", 10), command=find_and_highlight_terms)
    search_button.grid(row = 4, column = 5)

    # Button to find matches
    match_button = tk.Button(root, text="Find Matches", font=("Consolas", 10), command=find_and_highlight_matches)
    match_button.grid(row=4, column=1)

    # Dropdown menu for selecting the sorting attribute
    attribute_var = tk.StringVar(root)
    attribute_var.set("author")  # Default value

    attribute_menu = tk.OptionMenu(root, attribute_var, "author", "title", "date")
    attribute_menu.grid(row=5, column=0)

    # Button to sort files based on the selected attribute
    sort_button = tk.Button(root, text="Sort Files", font=("Consolas", 10), command=lambda: sort_files(attribute_var.get()))
    sort_button.grid(row=5, column=1)

    # Text boxes for huffman codes
    huffman1 = tk.Text(root, height=10, width=30)
    huffman1.grid(row=1, column=3)

    huffman2 = tk.Text(root, height=10, width=30)
    huffman2.grid(row=3, column=3)

    # Labels for compression stats
    original_size_label1 = tk.Label(root, text="Original Size: N/A")
    original_size_label1.grid(row=6, column=0)

    compressed_size_label1 = tk.Label(root, text="Compressed Size: N/A")
    compressed_size_label1.grid(row=6, column=1)

    compression_ratio_label1 = tk.Label(root, text="Compression Ratio: N/A")
    compression_ratio_label1.grid(row=6, column=2)

    original_size_label2 = tk.Label(root, text="Original Size: N/A")
    original_size_label2.grid(row=7, column=0)

    compressed_size_label2 = tk.Label(root, text="Compressed Size: N/A")
    compressed_size_label2.grid(row=7, column=1)

    compression_ratio_label2 = tk.Label(root, text="Compression Ratio: N/A")
    compression_ratio_label2.grid(row=7, column=2)


    # Button to generate Huffman codes
    huffman_button = tk.Button(root, text="Generate Huffman Codes", font=("Consolas", 10), command=display_huffman_codes)
    huffman_button.grid(row=5, column=3)

    # Run the application
    root.mainloop()

#gui()
