"""
进行用户选择
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
    QGridLayout
from PyQt5.QtCore import pyqtSignal
import math
class UserChoice(QWidget):
    dialog_signal = pyqtSignal(str,int,int)

    def __init__(self,parent = None):
        self.Algorithm:str
        self.UserId:int
        self.RecommandNum:int

        super(UserChoice,self).__init__(parent)
        self.setWindowTitle('Choice What You Need')

        self.Algorithm = QPushButton('Algorithm SimAls',self)
        self.UserId = QPushButton('User Id',self)
        self.RecommandNum = QPushButton('Num',self)
        self.Finish = QPushButton('Finish',self)

        self.AlgorithmLine = QLineEdit(self)
        self.UserIdLine = QLineEdit(self)
        self.RecommandNumLine = QLineEdit(self)

        self.AlgorithmLine.setMaxLength(5)
        self.UserIdLine.setMaxLength(5)
        self.RecommandNumLine.setMaxLength(5)

        self.GLayout = QGridLayout()
        self.GLayout.addWidget(self.Algorithm,0,0,1,1)
        self.GLayout.addWidget(self.AlgorithmLine,0,1,1,1)
        self.GLayout.addWidget(self.UserId,1,0,1,1)
        self.GLayout.addWidget(self.UserIdLine,1,1,1,1)
        self.GLayout.addWidget(self.RecommandNum,2,0,1,1)
        self.GLayout.addWidget(self.RecommandNumLine,2,1,1,1)

        self.GLayout.addWidget(self.Finish,3,0,1,1)
        self.setLayout(self.GLayout)

        self.Finish.clicked.connect(self.GetText)

    def GetText(self):
        IsOk = 0

        if self.AlgorithmLine.isModified():
            self
