#codeing = utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
    QGridLayout,QPlainTextEdit,QVBoxLayout,QFileDialog

path = '/help.md'

class help_page(QWidget):
    def __init__(self):
        super(help_page, self).__init__()
        self.resize(800,600)

        self.setWindowTitle("Help You Know")
        self.help_line = QTextEdit(self)

        self.finish_button = QPushButton("Close",self)

        layout = QVBoxLayout()
        layout.addWidget(self.help_line)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

        self.init_ui()
        self.finish_button.clicked.connect(self.finish)

    def init_ui(self):
        file = path

        with open(file,'rb') as f:
            out = f.read().decode('utf-8')
            self.help_line.setMarkdown(out)

        self.help_line.setReadOnly(True)

    def finish(self):
        self.destroy()