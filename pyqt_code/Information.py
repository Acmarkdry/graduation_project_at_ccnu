
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
        self.UserResult = QWidget()

        self.TeacherPageInit()
        self.StudentPageInit()
        self.KnowledgePageInit()
        self.UserResultPageInit()

        self.addTab(self.TeacherInformation,'Teacher Information')
        self.addTab(self.StudentInformation,'Student Information')
        self.addTab(self.KnowledgeInformation,'Knowledge Information')
        self.addTab(self.UserResult,'Result Information')

    def UserResultPageInit(self):
        pass

    def UserResultPageChange(self,vec:list,ResourcesNum,TeacherNum,UserName:str,AlgorithmName:str):
        """

        :param vec: 推荐资源数组
        :param ResourcesNum: 推荐的资源数量
        :param TeacherNum: 推荐的老师数量
        :param UserName: 用户名称
        :param AlgorithmName：使用的算法名称
        :return:
        """
        NameLabel = QLabel('Name:',self.UserResult)
        AlgorithmLabel = QLabel('Algorithm:',self.UserResult)

        NameLine = QLineEdit(self.UserResult)
        AlgorithmLine = QLineEdit(self.UserResult)

        Glayout = QGridLayout(NameLabel)

        Glayout.addWidget(NameLabel,0,1,1,1)
        Glayout.addWidget(NameLine,0,1,1,1)

        Glayout.addWidget(AlgorithmLabel,1,0,1,1)
        Glayout.addWidget(AlgorithmLine,1,1,1,1)

        ResultLabelList = [0 for i in range(len(vec))]
        ResultLineList = [0 for i in range(len(vec))]
        cnt = 2

        for i in range(0,ResourcesNum):
            ResultList[i] = QLabel(str('Resources') + str(i + 1),self.UserResult)
            ResultLabelList[i] = QLineEdit(self.UserResult)
            Glayout.addWidget(ResultLabelList[i],cnt,0,1,1)
            Glayout.addWidget(ResultLineList[i],cnt,1,1,1)
            cnt += 1

        for i in range(0,TeacherNum):
            ResultList[i + ResourcesNum] = QLabel(str('Resources') + str(i + 1),self.UserResult)
            ResultLabelList[i + ResourcesNum] = QLineEdit(self.UserResult)
            Glayout.addWidget(ResultLabelList[i],cnt,0,1,1)
            Glayout.addWidget(ResultLineList[i],cnt,1,1,1)
            cnt += 1

        self.UserResult.setLayout(Glayout)

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