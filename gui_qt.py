from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QFileDialog, QMessageBox, QLabel,
    QSplitter, QSizePolicy
)
from PySide6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor
from PySide6.QtCore import Qt
import sys

import plagiarism_checker
from sample_algorithms import generate_huffman_codes, visualize_huffman_for_text


class DocumentScannerMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Scanner (Qt)")
        self.resize(1100, 600)

        font = QFont("Consolas", 10)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)

        # Left panel (Document 1)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.file1_path = QLineEdit()
        self.file1_path.setPlaceholderText("Select first text document...")
        browse1 = QPushButton("Browse")
        browse1.clicked.connect(self.browse_file1)
        hl1 = QHBoxLayout()
        hl1.addWidget(self.file1_path)
        hl1.addWidget(browse1)
        left_layout.addLayout(hl1)

        self.text1 = QTextEdit()
        self.text1.setFont(font)
        self.text1.setReadOnly(False)
        left_layout.addWidget(self.text1)

        # Right panel (Document 2)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.file2_path = QLineEdit()
        self.file2_path.setPlaceholderText("Select second text document...")
        browse2 = QPushButton("Browse")
        browse2.clicked.connect(self.browse_file2)
        hl2 = QHBoxLayout()
        hl2.addWidget(self.file2_path)
        hl2.addWidget(browse2)
        right_layout.addLayout(hl2)

        self.text2 = QTextEdit()
        self.text2.setFont(font)
        right_layout.addWidget(self.text2)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])
        layout.addWidget(splitter)

        # Controls
        controls = QHBoxLayout()

        self.match_btn = QPushButton("Find Matches")
        self.match_btn.clicked.connect(self.find_matches)
        controls.addWidget(self.match_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search term to highlight...")
        controls.addWidget(self.search_input)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_term)
        controls.addWidget(self.search_btn)

        self.huffman_btn = QPushButton("Generate Huffman Codes")
        self.huffman_btn.clicked.connect(self.show_huffman_codes)
        controls.addWidget(self.huffman_btn)

        self.show_tree_btn = QPushButton("Show Huffman Tree (Doc1)")
        self.show_tree_btn.clicked.connect(lambda: self.show_huffman_tree(1))
        controls.addWidget(self.show_tree_btn)

        controls.addStretch()
        layout.addLayout(controls)

        # Compression output
        bottom = QHBoxLayout()
        self.huffman_out = QTextEdit()
        self.huffman_out.setReadOnly(True)
        self.huffman_out.setFixedHeight(120)
        bottom.addWidget(self.huffman_out)
        layout.addLayout(bottom)

    def browse_file1(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Text File", filter="Text files (*.txt)")
        if path:
            self.file1_path.setText(path)
            with open(path, 'r', encoding='utf-8') as f:
                self.text1.setPlainText(f.read())

    def browse_file2(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Text File", filter="Text files (*.txt)")
        if path:
            self.file2_path.setText(path)
            with open(path, 'r', encoding='utf-8') as f:
                self.text2.setPlainText(f.read())

    def find_matches(self):
        f1 = self.file1_path.text().strip()
        f2 = self.file2_path.text().strip()
        if not f1 or not f2:
            QMessageBox.warning(self, "Missing Files", "Please select both text files first.")
            return

        matches, similarity = plagiarism_checker.check_plagiarism(f1, f2)
        QMessageBox.information(self, "Similarity", f"Similarity score: {similarity:.2f}%")

        # Highlight matches in both editors
        self.clear_highlights()
        self.highlight_words(self.text1, matches, QColor('yellow'))
        self.highlight_words(self.text2, matches, QColor('yellow'))

    def search_term(self):
        term = self.search_input.text().strip()
        if not term:
            return
        self.clear_highlights()
        self.highlight_words(self.text1, {term}, QColor('#aaffaa'))
        self.highlight_words(self.text2, {term}, QColor('#aaffaa'))

    def show_huffman_codes(self):
        text1 = self.text1.toPlainText().strip()
        text2 = self.text2.toPlainText().strip()
        if not text1 and not text2:
            QMessageBox.warning(self, "No Text", "Load or paste text into one of the document panes.")
            return

        codes1, enc1, orig1, comp1 = generate_huffman_codes(text1 if text1 else text2)
        # Display codes (keep concise)
        pretty = '\n'.join([f"{repr(k)}: {v}" for k, v in list(codes1.items())[:50]])
        self.huffman_out.setPlainText(f"Huffman Codes (sample):\n{pretty}\nOriginal bytes: {orig1}  Compressed (approx): {comp1}")

    def show_huffman_tree(self, doc_index=1):
        text = self.text1.toPlainText() if doc_index == 1 else self.text2.toPlainText()
        if not text.strip():
            QMessageBox.information(self, "Huffman Tree", "No text available to build Huffman tree.")
            return
        visualize_huffman_for_text(text)

    def clear_highlights(self):
        self.text1.setExtraSelections([])
        self.text2.setExtraSelections([])

    def highlight_words(self, text_edit: QTextEdit, words, color: QColor):
        if not words:
            return
        extra_selections = []
        fmt = QTextCharFormat()
        fmt.setBackground(color)

        for word in words:
            if not word:
                continue
            cursor = text_edit.textCursor()
            # Move to start
            cursor.movePosition(QTextCursor.Start)
            while True:
                found = cursor.find(str(word))
                if not found:
                    break
                sel = QTextEdit.ExtraSelection()
                sel.cursor = cursor.copy()
                sel.format = fmt
                extra_selections.append(sel)

        text_edit.setExtraSelections(extra_selections)


def gui():
    app = QApplication(sys.argv)
    win = DocumentScannerMain()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    gui()
