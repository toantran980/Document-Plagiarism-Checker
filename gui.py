from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk


import os

def gui():
    #root setup
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.title("Document Scanner and Compression Tool")
    root.geometry('550x400')

    #Global Variables
    Files = []
    totalSize = 0 #Running total of size of all files uploaded
    decompressFilePath = None

    def add_button():
        """ Allow user to select a file and display its path and content """
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
        if file_path:
            # Add file path to the global list
            Files.append(file_path)

            # Enable the text box, insert file path, then disable it again
            box1.configure(state='normal')
            box1.insert(tk.END, file_path + "\n")
            box1.configure(state='disabled')

            # Read and display file contents in the second text box
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                box2.configure(state='normal')
                box2.delete("1.0", tk.END)
                box2.insert(tk.END, content)
                box2.configure(state='disabled')

            # Update total file size
            global totalSize
            totalSize += os.path.getsize(file_path)
            size.config(text=f"Total Size: {totalSize} Bytes")

    def remove_button():
        pass

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

    #row 0, title label
    title = Label(root, text="Document Scanner\n", font=("Consolas", 12))
    title.grid(row=0)
    #title.grid_columnconfigure(1, weight=1)   

    #row 3, "Selected Files" label
    l2 = Label(root, text="Selected Files", font=("Consolas", 10))
    l2.grid(row=3)

    #row 4, scrolled text box 1
    box1 = scrolledtext.ScrolledText(root, wrap = WORD, width = 50, height = 7, font = ("Consolas", 8))
    box1.configure(state = 'disabled')
    box1.grid(row = 4,columnspan=3)

    #row 5, "add file" button
    add = Button(text ="Add File", font=("Consolas", 8), command=add_button)
    add.grid(row=5, column=0)

    #row 5, "remove file" button
    add = Button(text ="Remove File", font=("Consolas", 8), command=remove_button)
    add.grid(row=5,column=1)

    #row 5, "Total Size" label
    size = Label(root, text = "Total Size: -- Bytes", font=("Consolas", 10))
    size.grid(row=5,column=2)

    #row 6, "Duplicate patterns exceeding 32 Characters" label
    l3 = Label(root, text="Duplicate Patterns exceeding 32 Characters", font=("Consolas", 10))
    l3.grid(row=6,columnspan=3)

    #row 7, scrolled text box 2
    box2 = scrolledtext.ScrolledText(root, wrap = WORD, width = 50, height = 5, font = ("Consolas", 8))
    box2.configure(state = 'disabled')
    box2.grid(row = 7,columnspan=3)

    #row 8, graph button
    graph = Button(root, text='Graph Citations', font=("Consolas", 8), width=20, command=graph)
    graph.grid(row=8, column=0)

    #row 8, compression details label (tied to "compress_button" function)
    detail = Label(root, text="Compression details will appear here", font=("Consolas", 8))
    detail.grid(row=8, column=1)

    #row 9, "Decompress a File" button
    decom = Button(root, text='Decompress a File', font=("Consolas", 8), width=20, command=decompress_button)
    decom.grid(row=9, column=0)

    #row 9, "exit" button
    exit_ = Button(root, text='Exit', font=("Consolas", 8), width=10, command=root.destroy)
    exit_.grid(row=9, column=1)

    root.mainloop()

gui()
