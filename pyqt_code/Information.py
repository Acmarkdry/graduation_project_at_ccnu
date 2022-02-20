
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QLineEdit, QDateEdit, \
    QComboBox, QTextEdit, QGridLayout,QTableWidget

class Information(QTabWidget):
    def __init__(self):
        super(Information, self).__init__()
        self.TeacherInformation = QTableWidget()
        self.StudentInformation = QTableWidget()
        self.KnowledgeInformation = QTableWidget()

        self.UserChoice = QWidget()

    def TeacherPageInit(self):
        pass

    def StudentPageInit(self):
        pass

    def