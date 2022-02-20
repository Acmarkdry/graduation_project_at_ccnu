# coding=gbk
"""
文件答疑

"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
    QGridLayout,QPlainTextEdit,QVBoxLayout,QFileDialog
from PyQt5.QtCore import pyqtSignal
import urllib
import chardet

path = '../resources/question_and_answer.md'

class question_and_answer_page(QWidget):
    def __init__(self):
        super(question_and_answer_page, self).__init__()
        self.resize(800,600)

        self.setWindowTitle("Question And Answer")
        self.question_textline = QTextEdit(self)

        self.finish_button = QPushButton("Close",self)

        layout = QVBoxLayout()
        layout.addWidget(self.question_textline)
        layout.addWidget(self.finish_button)

        self.setLayout(layout)

        self.init_ui()

        self.finish_button.clicked.connect(self.finish)


    def init_ui(self):
        file = path
        ##print(self.question_textline.toPlainText())

        with open(file,'rb') as f:
            out = f.read().decode('utf-8')
            self.question_textline.setMarkdown(out)

        self.question_textline.setReadOnly(True)

    def finish(self):
        self.destroy()

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = question_and_answer_page()
    demo.show()

    sys.exit(app.exec_())