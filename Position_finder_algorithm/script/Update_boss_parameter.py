"""
修改boss参数
其中添加的内容有 boss的uid，自身坐标，自身半径，左右角度
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
                            QGridLayout
from PyQt5.QtCore import pyqtSignal
from Vadidator import attack_vadidator,position_vadidator,angle_vadidator
import math

class update_boss_parameter(QWidget):
    dialog_signal = pyqtSignal(str, float, float, float,int,float,float)

    def __init__(self,parent = None):
        self.uid:str
        self.x:float
        self.y:float
        self.image_radius:float
        self.le_angle:float
        self.ri_angle:float
        self.ask_in_angle = 1

        super(update_boss_parameter, self).__init__(parent)
        self.setWindowTitle("Update Boss Parameter")

        self.uid_button = QPushButton('uid',self)
        self.x_button = QPushButton('x',self)
        self.y_button = QPushButton('y',self)
        self.image_button = QPushButton('image radius',self)
        self.le_angle_button = QPushButton('le angle',self)
        self.ri_angle_button = QPushButton('ri angle',self)
        self.ask_in_angle_button = QPushButton('ask angle',self)
        self.finish_button = QPushButton('finish',self)

        self.uid_line = QLineEdit(self) ## 设置文本行
        self.x_line = QLineEdit(self)
        self.y_line = QLineEdit(self)
        self.image_line = QLineEdit(self)
        self.le_angle_line = QLineEdit(self)
        self.ri_angle_line = QLineEdit(self)
        self.ask_in_angle_line = QLineEdit(self)

        self.uid_line.setMaxLength(20) ## 设置最大长度
        self.x_line.setMaxLength(7)
        self.y_line.setMaxLength(7)
        self.image_line.setMaxLength(7)
        self.le_angle_line.setMaxLength(7)
        self.ri_angle_line.setMaxLength(7)
        self.ask_in_angle_line.setMaxLength(7)

        self.x_line.setValidator(position_vadidator()) ## 设置触发器
        self.y_line.setValidator(position_vadidator())
        self.image_line.setValidator(attack_vadidator())
        self.le_angle_line.setValidator(angle_vadidator())
        self.ri_angle_line.setValidator(angle_vadidator())
        self.ask_in_angle_line.setValidator(attack_vadidator())

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
        self.g_layout.addWidget(self.ask_in_angle_button,4,0,1,1)
        self.g_layout.addWidget(self.ask_in_angle_line,4,1,1,1)

        self.g_layout.addWidget(self.le_angle_button, 5, 0, 1, 1)
        self.g_layout.addWidget(self.le_angle_line, 5, 1, 1, 1)
        self.g_layout.addWidget(self.ri_angle_button, 6, 0, 1, 1)
        self.g_layout.addWidget(self.ri_angle_line, 6, 1, 1, 1)

        self.g_layout.addWidget(self.finish_button, 7, 0, 1, 1)
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

        if self.image_line.isModified():
            self.image_radius = float(self.image_line.text())
            isok += 1

        if self.ask_in_angle_line.isModified():
            self.ask_in_angle = int(self.ask_in_angle_line.text())

        if self.le_angle_line.isModified():
            self.le_angle = float(self.le_angle_line.text())
            isok += 1

        if self.ri_angle_line.isModified():
            self.ri_angle = float(self.ri_angle_line.text())
            isok += 1


        if isok == 7:
            if(self.ask_in_angle != 1 and self.ask_in_angle != 0):
                self.ask_in_angle = 1

            if(self.ask_in_angle == 0):
                self.le_angle = 0
                self.ri_angle = 2*math.pi

            self.dialog_signal.emit(self.uid,self.x,self.y,
                                    self.image_radius,
                                    self.ask_in_angle,
                                    self.le_angle,self.ri_angle)
            self.destroy() ## 自动关闭了

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = update_boss_parameter()
    demo.show()

    sys.exit(app.exec_())