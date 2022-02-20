
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QLineEdit, QDateEdit, \
    QComboBox, QTextEdit, QGridLayout,QTableWidget,QAbstractItemView

from UserChoice import UserChoice

class Information(QTabWidget):
    def __init__(self):
        super(Information, self).__init__()
        self.TeacherInformation = QTableWidget()
        self.StudentInformation = QTableWidget()
        self.KnowledgeInformation = QTableWidget()

    def TeacherPageInit(self):
        self.TeacherInformation.setRowCount(0)
        self.TeacherInformation.setColumnCount(0)

        self.TeacherInformation.setRowHeight(0,30)
        self.TeacherInformation.setColumnWidth(0,80)

        self.TeacherInformation.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def TeacherPageChanged(self,vec:list[list]):
        self.TeacherInformation.setColumnCount(len(vec[0]))

        name = []

        for i in range(1,len(vec[0])):
            name.append(str("Knowledge") + str(i))

        self.TeacherInformation.setHorizontalHeaderLabels(name)

        for i in range(1,len(vec)):
            for j in range(1,len(vec[0])):
                self.TeacherInformation.setItem(i-1,j-1,QTableWidgetItem(str(vec[i][j])))

    def StudentPageInit(self):
        self.StudentInformation.setRowCount(0)
        self.StudentInformation.setColumnCount(0)

        self.StudentInformation.setColumnWidth(0,80)
        self.StudentInformation.setRowHeight(0,30)

        self.StudentInformation.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def StudnetPageChanged(self,vec:dict):
        self.StudentInformation.setColumnCount(9)

        name = []

        for i in range(1,10):
            name.append(str("Resources") + str(i))
        self.StudentInformation.setHorizontalHeaderLabels(name)

        for i in range(1,81):
            for j in range(1,10):
                self.StudentInformation.setItem(i-1,j-1,QTableWidgetItem(str(vec[i][j])))

    def KnowledgePageInit(self):
        self.KnowledgeInformation.setRowCount(0)
        self.KnowledgeInformation.setColumnCount(0)

        self.KnowledgeInformation.setColumnWidth(0,80)
        self.KnowledgeInformation.setRowHeight(0,30)

        self.KnowledgeInformation.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def KnowledgeChanged(self,vec:list):
        self.KnowledgeInformation.setColumnCount(2)

        self.KnowledgeInformation(["Resources","Knowledge"])

        for i in range(len(vec)):
            for j in range(len(vec[0])):
                self.KnowledgeInformation.setItem(i-1,j-1,QTableWidgetItem(str(vec[i][j])))
