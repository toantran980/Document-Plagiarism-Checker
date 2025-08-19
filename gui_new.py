from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk
from datetime import datetime
import re
import string

import plagiarism_checker
from sorting_title import mergeSort
from naive import naive_search
from sample_algorithms import generate_huffman_codes

# Import graph-related functions
from graph import build_word_graph, bfs, dfs, visualize_word_graph_with_traversal, count_word_occurrences
import os

from tkinter import messagebox

# Global flag for stopping traversal
stop_traversal = False

def gui():
    # Import Huffman tree visualization
    from sample_algorithms import visualize_huffman_for_text

    def show_huffman_tree1():
        text1_content = text1.get("1.0", tk.END).strip()
        if text1_content:
            visualize_huffman_for_text(text1_content)
        else:
            messagebox.showinfo("Huffman Tree", "No text loaded in Document 1.")

    def show_huffman_tree2():
        text2_content = text2.get("1.0", tk.END).strip()
        if text2_content:
            visualize_huffman_for_text(text2_content)
        else:
            messagebox.showinfo("Huffman Tree", "No text loaded in Document 2.")
    #root setup
    root = tk.Tk()
    root.title("Text Document Input")
    root.geometry('1120x550')

    #Global Variables
    global Files, stop_traversal
    Files = []
    # totalSize = 0 #Running total of size of all files uploaded
    # decompressFilePath = None

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
        """Highlights occurrences of a phrase in a text widget, ensuring whole-word matches."""
        if not phrase:  # Skip if the phrase is empty
            return

        start_index = "1.0"
        while True:
            # Search for the phrase in the text widget
            start_index = text_widget.search(phrase, start_index, stopindex=tk.END)
            if not start_index:
                break

            # Calculate the end index of the match
            end_index = f"{start_index}+{len(phrase)}c"

            # Get the surrounding characters
            prev_char_index = f"{start_index}-1c"
            next_char_index = f"{end_index}+1c"

            prev_char = text_widget.get(prev_char_index, start_index)
            next_char = text_widget.get(end_index, next_char_index)

            # Ensure match is a whole word by checking surrounding characters
            if (prev_char in string.whitespace + string.punctuation or not prev_char) and \
                (next_char in string.whitespace + string.punctuation or not next_char):
                text_widget.tag_add("match", start_index, end_index)
                text_widget.tag_config("match", background="yellow", foreground="black")

            # Move to the next match
            start_index = end_index

    def highlight_text2(text_widget, phrase):
        min_length = 1
        """ Highlights occurrences of a full word in a text widget if it's at least min_length characters long """
        if len(phrase) < min_length:
            return  # Skip highlighting if the phrase is too short

        start_index = "1.0"
        while True:
            # Use regex to find whole-word matches
            match_index = text_widget.search(rf'\b{re.escape(phrase)}\b', start_index, stopindex="end", regexp=True)
            if not match_index:
                break
            end_index = f"{match_index}+{len(phrase)}c"
            text_widget.tag_add("match", match_index, end_index)
            text_widget.tag_config("match", background="yellow", foreground="black")
            start_index = exec

    def find_and_highlight_matches():
        """ Uses imported function to find matches and highlight them """
        text1_content = entry1.get()
        text2_content = entry2.get()

        if not text1_content or not text2_content:
            return

        # Call the imported function from plagiarism_checker.py
        matches, similarity = plagiarism_checker.check_plagiarism(text1_content, text2_content)

        # Highlight matches in both text boxes
        text1.configure(state='normal')
        text2.configure(state='normal')

        text1.tag_remove("match", "1.0", tk.END)
        text2.tag_remove("match", "1.0", tk.END)

        for match in matches:
            highlight_text(text1, str(match))
            highlight_text(text2, str(match))

        text1.configure(state='disabled')
        text2.configure(state='disabled')

        # Display similarity score in a message box
        messagebox.showinfo("Similarity Score", f"Similarity score: {similarity:.2f}%")

        # Display valid start vertices (matched words) in a message box
        if matches:
            valid_vertices = "\n".join([str(word) for word in matches])
            messagebox.showinfo("Valid Start Vertices", f"Valid start vertices for BFS/DFS:\n\n{valid_vertices}")

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

    def clear_all():
        """Clear all text fields and reset the GUI."""
        text1.configure(state='normal')
        text2.configure(state='normal')
        entry1.config(state='normal')
        entry2.config(state='normal')
        entry3.config(state='normal')

        text1.delete("1.0", tk.END)
        text2.delete("1.0", tk.END)
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)
        huffman1.delete("1.0", tk.END)
        huffman2.delete("1.0", tk.END)

        original_size_label1.config(text="Original Size: N/A")
        compressed_size_label1.config(text="Compressed Size: N/A")
        compression_ratio_label1.config(text="Compression Ratio: N/A")
        original_size_label2.config(text="Original Size: N/A")
        compressed_size_label2.config(text="Compressed Size: N/A")
        compression_ratio_label2.config(text="Compression Ratio: N/A")
    
    def stop_traversal_action():
        """Stop the graph traversal."""
        global stop_traversal
        stop_traversal = True
        print("Traversal stopped by user.")
    
    def visualize_graph(traversal_type):
        """Visualize the word graph with BFS or DFS traversal for matched highlighted text."""
        global stop_traversal
        stop_traversal = False  # Reset the stop flag

        # Get the text content from the text widgets
        text1_content = text1.get("1.0", tk.END).strip()
        text2_content = text2.get("1.0", tk.END).strip()

        if not text1_content or not text2_content:
            print("Error: Both text documents must be loaded.")
            return

        # Combine words from both text documents
        words1 = text1_content.split()
        words2 = text2_content.split()
        all_words = words1 + words2
        word_counts = count_word_occurrences(all_words)

        # Get the matched highlighted text
        matched_words = plagiarism_checker.check_plagiarism(entry1.get(), entry2.get())
        if not matched_words:
            print("No matched words found for graph generation.")
            return

        print("Matched Words:", matched_words)

        # Build the word graph using only matched words
        word_graph = build_word_graph(all_words, matched_words)

        # Get the start vertex from the entry box
        start_node = start_vertex_entry.get().strip()
        if not start_node:
            print("Error: Start vertex is empty.")
            return

        if start_node not in word_graph:
            print(f"Error: Start vertex '{start_node}' not found in the graph.")
            return

        # Perform the selected traversal
        if traversal_type == "bfs":
            print("\nPerforming BFS Traversal:")
            traversal_order = bfs(word_graph, start_node)
            print("BFS Traversal Order:", traversal_order)
            visualize_word_graph_with_traversal(word_graph, traversal_order, word_counts, lambda: stop_traversal)
        elif traversal_type == "dfs":
            print("\nPerforming DFS Traversal:")
            traversal_order = dfs(word_graph, start_node)
            print("DFS Traversal Order:", traversal_order)
            visualize_word_graph_with_traversal(word_graph, traversal_order, word_counts, lambda: stop_traversal)
    
    # Function to open a file dialog and return the selected file path
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
            messagebox.showinfo("Sort Files", "No files to sort.")
            return

        mergeSort(Files, key=attribute)  # Sort the global Files list
        print(f"Files sorted by {attribute}:")
        sorted_list = "\n".join([f"{file['title']} (Author: {file['author']}, Date: {file['date']})" for file in Files])
        for file in Files:
            print(file)

        # Show a popup with the sorted file list
        if sorted_list:
            messagebox.showinfo("Sorted Files", f"Files sorted by {attribute}:\n\n{sorted_list}")
        else:
            messagebox.showinfo("Sorted Files", "No files to display.")

    #Everything below this point is to make the actual buttons and boxes and stuff

    highestFrame = tk.Frame(root)
    highestFrame.pack(side = TOP)
    

    leftFrame = tk.Frame(highestFrame, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    leftFrame.pack(fill=tk.X, padx=10, pady=5, side = LEFT)
    rightFrame = tk.Frame(highestFrame, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    rightFrame.pack(fill=tk.X, padx=10, pady=5, side = RIGHT)

    lowestFrame = tk.Frame(root)
    lowestFrame.pack()
    
    left2 = tk.Frame(lowestFrame, padx=10, pady=10)
    left2.pack(side = LEFT)
    right2 = tk.Frame(lowestFrame, padx=10, pady=10)
    right2.pack(side = RIGHT)

    #First Document Selection
    topFrame1 = tk.Frame(leftFrame)
    topFrame1.pack()
    
    tk.Label(topFrame1, text="Select First Text Document:").pack(side = LEFT)
    
    entry1 = tk.Entry(topFrame1, width=50)
    entry1.pack(side = RIGHT)
    btn1 = tk.Button(topFrame1, text="Browse", command=lambda: open_file(entry1, text1))
    btn1.pack(side = RIGHT)

    bottomFrame1 = tk.Frame(leftFrame)
    bottomFrame1.pack()
    text1 = scrolledtext.ScrolledText(bottomFrame1, wrap = WORD, width=80, height = 10, font = ("Consolas", 8))
    text1.pack(fill = BOTH)

    huffmanFrame1 = tk.Frame(leftFrame)
    huffmanFrame1.pack()

    tk.Label(huffmanFrame1, text="Huffman Codes:").pack()
    huffman1 = scrolledtext.ScrolledText(huffmanFrame1, wrap = WORD, width=80, height = 5, font = ("Consolas", 8))
    huffman1.pack()
    show_tree_btn1 = tk.Button(huffmanFrame1, text="Show Huffman Tree", command=show_huffman_tree1)
    show_tree_btn1.pack(pady=2)

    #Second Document Selection
    topFrame2 = tk.Frame(rightFrame)
    topFrame2.pack()

    tk.Label(topFrame2, text="Select Second Text Document:").pack(side = LEFT)
    
    entry2 = tk.Entry(topFrame2, width=50)
    entry2.pack(side = RIGHT)
    btn2 = tk.Button(topFrame2, text="Browse", command=lambda: open_file(entry2, text2))
    btn2.pack(side = RIGHT)

    bottomFrame2 = tk.Frame(rightFrame)
    bottomFrame2.pack()
    text2 = scrolledtext.ScrolledText(bottomFrame2, wrap = WORD, width=80, height = 10, font = ("Consolas", 8))
    text2.pack(fill = BOTH)

    huffmanFrame2 = tk.Frame(rightFrame)
    huffmanFrame2.pack()

    tk.Label(huffmanFrame2, text="Huffman Codes:").pack()
    huffman2 = scrolledtext.ScrolledText(huffmanFrame2, wrap = WORD, width=80, height = 5, font = ("Consolas", 8))
    huffman2.pack()
    show_tree_btn2 = tk.Button(huffmanFrame2, text="Show Huffman Tree", command=show_huffman_tree2)
    show_tree_btn2.pack(pady=2)

    #All the other stuff goes here
    topFrame3 = tk.Frame(left2)
    topFrame3.pack(side = TOP)
    bottomFrame3 = tk.Frame(left2, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    bottomFrame3.pack(fill=tk.X, padx=10, pady=5)

    topFrame4 = tk.Frame(right2)
    topFrame4.pack(side = TOP)
    bottomFrame4 = tk.Frame(right2, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    bottomFrame4.pack(fill=tk.X, padx=10, pady=5)

    # Button to find matches
    match_button = tk.Button(topFrame4, text="Find Matches", font=("Consolas", 10), command=find_and_highlight_matches)
    match_button.pack(side = RIGHT)

    # Dropdown menu for selecting the sorting attribute
    attribute_var = tk.StringVar(root)
    attribute_var.set("author")  # Default value

    # Dropdown menu for selecting the attribute to sort by
    attribute_menu = tk.OptionMenu(topFrame4, attribute_var, "author", "title", "date")
    attribute_menu.pack(side = RIGHT)

    # Button to sort files based on the selected attribute
    sort_button = tk.Button(topFrame4, text="Sort Files", font=("Consolas", 10), command=lambda: sort_files(attribute_var.get()))
    sort_button.pack(side = RIGHT)

    # Button to generate Huffman codes
    huffman_button = tk.Button(topFrame4, text="Generate Huffman Codes", font=("Consolas", 10), command=display_huffman_codes)
    huffman_button.pack(side = RIGHT)

    # Entry widget for start vertex
    tk.Label(topFrame3, text="Start Vertex:").pack(side=tk.LEFT)
    start_vertex_entry = tk.Entry(topFrame3, width=20)
    start_vertex_entry.pack(side=tk.LEFT)

    # Visualize BFS button
    graph_button_bfs = tk.Button(topFrame3, text="Visualize BFS Graph", font=("Consolas", 10), command=lambda: visualize_graph("bfs"))
    graph_button_bfs.pack(side=tk.LEFT)

    # Visualize DFS button
    graph_button_dfs = tk.Button(topFrame3, text="Visualize DFS Graph", font=("Consolas", 10), command=lambda: visualize_graph("dfs"))
    graph_button_dfs.pack(side=tk.LEFT)

    # Stop Traversal button
    stop_button = tk.Button(topFrame3, text="Stop Traversal", font=("Consolas", 10), command=stop_traversal_action)
    stop_button.pack(side=tk.LEFT)

    # Clear All button
    clear_button = tk.Button(bottomFrame4, text="Clear All", font=("Consolas", 10), command=clear_all)
    clear_button.pack(side= RIGHT)

    # Labels for compression stats
    original_size_label1 = tk.Label(bottomFrame3, text="Original Size: N/A")
    original_size_label1.pack()

    compressed_size_label1 = tk.Label(bottomFrame3, text="Compressed Size: N/A")
    compressed_size_label1.pack()

    compression_ratio_label1 = tk.Label(bottomFrame3, text="Compression Ratio: N/A")
    compression_ratio_label1.pack()

    original_size_label2 = tk.Label(bottomFrame3, text="Original Size: N/A")
    original_size_label2.pack()

    compressed_size_label2 = tk.Label(bottomFrame3, text="Compressed Size: N/A")
    compressed_size_label2.pack()

    compression_ratio_label2 = tk.Label(bottomFrame3, text="Compression Ratio: N/A")
    compression_ratio_label2.pack()

    # Box to enter search term
    entry3 = tk.Entry(bottomFrame4, width = 50)
    entry3.pack(side = RIGHT)
    search_button = tk.Button(bottomFrame4, text = "Search", font=("Consolas", 10), command=find_and_highlight_terms)
    search_button.pack(side = RIGHT)
    
    # Run the application
    root.mainloop()

