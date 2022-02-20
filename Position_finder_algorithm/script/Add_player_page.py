"""
玩家页面输入信息
输入包括：自身uid，x，y，speed，attack，image，speed
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
                            QGridLayout
from PyQt5.QtCore import pyqtSignal
from Vadidator import attack_vadidator,position_vadidator

class add_player_page(QWidget):
    dialog_signal = pyqtSignal(str, float, float, float, float, float)

    def __init__(self,parent = None):

        self.speed:float
        self.uid:str
        self.x:float
        self.y:float
        self.attack_radius:float
        self.image_radius:float

        super(add_player_page, self).__init__(parent)
        self.setWindowTitle("Add Player")

        self.uid_button = QPushButton('uid',self)
        self.x_button = QPushButton('x',self)
        self.y_button = QPushButton('y',self)
        self.attack_button = QPushButton('attack radius',self)
        self.image_button = QPushButton('image radius',self)
        self.speed_button = QPushButton('speed',self)
        self.finish_button = QPushButton('finish',self)

        self.uid_line = QLineEdit(self) ## 设置文本行
        self.x_line = QLineEdit(self)
        self.y_line = QLineEdit(self)
        self.attack_line = QLineEdit(self)
        self.image_line = QLineEdit(self)
        self.speed_line = QLineEdit(self)

        self.uid_line.setMaxLength(20) ## 设置最大长度
        self.x_line.setMaxLength(7)
        self.y_line.setMaxLength(7)
        self.attack_line.setMaxLength(7)
        self.image_line.setMaxLength(7)
        self.speed_line.setMaxLength(7)

        self.x_line.setValidator(position_vadidator()) ## 设置触发器
        self.y_line.setValidator(position_vadidator())
        self.attack_line.setValidator(attack_vadidator())
        self.image_line.setValidator(attack_vadidator())
        self.speed_line.setValidator(attack_vadidator())

        ## 获取输入 设置数据限制 设置长度限制

        self.g_layout = QGridLayout()
        self.g_layout.addWidget(self.uid_button,0,0,1,1)
        self.g_layout.addWidget(self.uid_line, 0, 1, 1, 1)
        self.g_layout.addWidget(self.x_button, 1, 0, 1, 1)
        self.g_layout.addWidget(self.x_line, 1, 1, 1, 1)
        self.g_layout.addWidget(self.y_button, 2, 0, 1, 1)
        self.g_layout.addWidget(self.y_line, 2, 1, 1, 1)
        self.g_layout.addWidget(self.image_button, 3, 0, 1, 1)
        self.g_layout.addWidget(self.image_line, 3, 1, 1, 1)
        self.g_layout.addWidget(self.attack_button, 4, 0, 1, 1)
        self.g_layout.addWidget(self.attack_line, 4, 1, 1, 1)
        self.g_layout.addWidget(self.speed_button, 5, 0, 1, 1)
        self.g_layout.addWidget(self.speed_line, 5, 1, 1, 1)
        self.g_layout.addWidget(self.finish_button, 6, 0, 1, 1)
        self.setLayout(self.g_layout)

        self.finish_button.clicked.connect(self.get_text_from_line)

    def get_text_from_line(self,parent = None):
        isok:int
        isok = 0

        if self.uid_line.isModified():
            self.uid = str(self.uid_line.text())
            isok += 1

        if self.x_line.isModified():
            self.x = float(self.x_line.text())
            isok += 1

        if self.y_line.isModified():
            self.y = float(self.y_line.text())
            isok += 1

        if self.attack_line.isModified():
            self.attack_radius = float(self.attack_line.text())
            isok += 1

        if self.image_line.isModified():
            self.image_radius = float(self.image_line.text())
            isok += 1

        if self.speed_line.isModified():
            self.speed = float(self.speed_line.text())
            isok += 1

        if(self.attack_radius < self.image_radius):
            self.attack_radius = self.image_radius + 1

        if isok == 6:
            self.dialog_signal.emit(self.uid,self.x,self.y,
                                    self.image_radius,self.attack_radius,self.speed)
            self.destroy() ## 自动关闭了


if  __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = add_player_page()
    demo.show()

    sys.exit(app.exec_())