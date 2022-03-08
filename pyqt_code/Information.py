
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QLineEdit, QDateEdit, \
    QComboBox, QTextEdit, QGridLayout,QTableWidget,QAbstractItemView,QTableWidgetItem

from UserChoice import UserChoice

class Information(QTabWidget):
    def __init__(self):
        super(Information, self).__init__()
        self.TeacherInformation = QTableWidget()
        self.StudentInformation = QTableWidget()
        self.KnowledgeInformation = QTableWidget()

        self.TeacherPageInit()
        self.StudentPageInit()
        self.KnowledgePageInit()

        self.addTab(self.TeacherInformation,'Teacher Information')
        self.addTab(self.StudentInformation,'Student Information')
        self.addTab(self.KnowledgeInformation,'Knowledge Information')

    def TeacherPageInit(self):
        self.TeacherInformation.setRowCount(0)
        self.TeacherInformation.setColumnCount(0)

        self.TeacherInformation.setRowHeight(0,30)
        self.TeacherInformation.setColumnWidth(0,80)

        self.TeacherInformation.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def TeacherPageChanged(self,vec:list):
        self.TeacherInformation.setColumnCount(len(vec[0]))
        self.TeacherInformation.setRowCount(len(vec))

        name = []
        row_name = []

        for i in range(1,len(vec[0])):
            name.append(str("Teacher") + str(i))

        for i in range(1,len(vec)):
            row_name.append(str("Student") + str(i))

        self.TeacherInformation.setHorizontalHeaderLabels(name)
        self.TeacherInformation.setVerticalHeaderLabels(row_name)

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
        self.StudentInformation.setRowCount(81)

        name = []
        name_row = []

        for i in range(1,10):
            name.append(str("Resources ") + str(i))
        for i in range(1,81):
            name_row.append(str("Student ") + str(i))

        self.StudentInformation.setHorizontalHeaderLabels(name)
        self.StudentInformation.setVerticalHeaderLabels(name_row)

        for i in range(1,81):
            for j in range(0,9):
                self.StudentInformation.setItem(i-1,j,QTableWidgetItem(str(vec[i][j])))

    def KnowledgePageInit(self):
        self.KnowledgeInformation.setRowCount(0)
        self.KnowledgeInformation.setColumnCount(0)

        self.KnowledgeInformation.setColumnWidth(0,80)
        self.KnowledgeInformation.setRowHeight(0,30)

        self.KnowledgeInformation.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def KnowledgeChanged(self,vec:list):
        self.KnowledgeInformation.setColumnCount(2)
        self.KnowledgeInformation.setRowCount(len(vec))

        name = []
        row_name = []

        name.append("Resources")
        name.append("Knowledge")

        for i in range(1,len(vec)):
            row_name.append(str("Resource ") + str(i))

        self.KnowledgeInformation.setHorizontalHeaderLabels(name)
        self.KnowledgeInformation.setVerticalHeaderLabels(row_name)

        for i in range(1,len(vec)):
            for j in range(len(vec[0])):
                print(i,j)
                self.KnowledgeInformation.setItem(i-1,j,QTableWidgetItem(str(vec[i][j])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Information()
    demo.show()
    sys.exit(app.exec_())