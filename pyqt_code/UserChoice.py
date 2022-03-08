"""
进行用户选择
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
    QGridLayout
from PyQt5.QtCore import pyqtSignal
import math

class UserChoice(QWidget):
    dialog_signal = pyqtSignal(str,int,int,int)

    def __init__(self,parent = None):
        self.Algorithm:str
        self.UserId:int
        self.RecommandNum:int
        self.RecommandTeacherNum:int

        super(UserChoice,self).__init__(parent)
        self.setWindowTitle('Choice What You Need')

        self.Algorithm = QPushButton('Algorithm SimAls',self)
        self.UserId = QPushButton('User Id',self)
        self.RecommandNum = QPushButton('Num',self)
        self.RecommandTeacherNum = QPushButton("TeacherNum",self)
        self.Finish = QPushButton('Finish',self)

        self.AlgorithmLine = QLineEdit("SIMALS1",self)
        self.UserIdLine = QLineEdit("1",self)
        self.RecommandNumLine = QLineEdit("10",self)
        self.RecommandTeacherLine = QLineEdit("3",self)

        self.AlgorithmLine.setMaxLength(10)
        self.UserIdLine.setMaxLength(5)
        self.RecommandNumLine.setMaxLength(5)
        self.RecommandTeacherLine.setMaxLength(5)

        self.GLayout = QGridLayout()
        self.GLayout.addWidget(self.Algorithm,0,0,1,1)
        self.GLayout.addWidget(self.AlgorithmLine,0,1,1,1)
        self.GLayout.addWidget(self.UserId,1,0,1,1)
        self.GLayout.addWidget(self.UserIdLine,1,1,1,1)
        self.GLayout.addWidget(self.RecommandNum,2,0,1,1)
        self.GLayout.addWidget(self.RecommandNumLine,2,1,1,1)
        self.GLayout.addWidget(self.RecommandTeacherNum,3,0,1,1)
        self.GLayout.addWidget(self.RecommandTeacherLine,3,1,1,1)

        self.GLayout.addWidget(self.Finish,4,0,1,1)
        self.setLayout(self.GLayout)

        self.Finish.clicked.connect(self.GetText)

    def GetText(self):
        print("hello")
        IsOk = 0
        AlgorithmNum = 0
        UserIdNum = 0
        RecommandNumNum = 0
        RecommandTeacherNumNum = 0

        if self.AlgorithmLine.isModified():
            AlgorithmNum = self.AlgorithmLine.text()
            IsOk += 1

        if self.RecommandNumLine.isModified():
            RecommandNumNum = int(self.RecommandNumLine.text())
            IsOk += 1

        if self.UserIdLine.isModified():
            UserIdNum = int(self.RecommandNumLine.text())
            IsOk += 1

        if self.RecommandTeacherLine.isModified():
            RecommandTeacherNumNum = int(self.RecommandTeacherLine.text())
            IsOk += 1

        if IsOk == 4:
            self.dialog_signal.emit(AlgorithmNum,UserIdNum,RecommandNumNum,RecommandTeacherNumNum)
            self.destroy()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = UserChoice()
    demo.show()

    sys.exit(app.exec_())