# Document Plagiarism Checker

## Overview

A Python-based application for scanning documents, detecting plagiarism, visualizing word relationships, and analyzing file compression. Features include:

- Plagiarism detection using Rabin-Karp, KMP, and Naive algorithms
- GUI for file selection, comparison, and visualization
- Graph analysis (BFS/DFS) of matched words
- Huffman coding for file compression
- Sorting and metadata organization

## Installation

1. Clone the repository:

```sh
  git clone https://github.com/toantran980/Document-Plagiarism-Checker.git
```

2. Make sure you have the following Python packages installed:

- matplotlib
- networkx

## Usage

- Run the GUI:
  ```sh
  python Main.py
  ```
- Use the interface to select files, compare documents, visualize graphs, and view compression stats.

## Modules

- `Main.py`: Launches the GUI
- `gui_new.py`: Main GUI logic and event handling
- `plagiarism_checker.py`: Plagiarism detection algorithms
- `graph.py`: Word graph construction and traversal
- `sorting_title.py`: File sorting by metadata
- `sample_algorithms.py`: Huffman coding and compression
- `naive.py`: Naive string matching

## Features

- **Plagiarism Detection:** Compare documents for matching phrases/words
- **Compression Analysis:** Huffman coding, compression ratio, and stats
- **Graph Visualization:** BFS/DFS traversal of matched words
- **Batch Sorting:** Organize files by author, title, or date
- **User Feedback:** Pop-ups for similarity score, sorted files, and valid graph vertices

## License

This project is licensed under the MIT License.

Copyright 2025  Toan Tran

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
