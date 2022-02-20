"""
用来删除玩家，其中只会输入uid
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QTextEdit, QPushButton, \
                            QGridLayout
from PyQt5.QtCore import pyqtSignal

class delete_player_page(QWidget):
    dialog_signal = pyqtSignal(str)

    def __init__(self,parent = None):
        self.uid:str

        super(delete_player_page, self).__init__(parent)
        self.uid_button = QPushButton('uid',self)
        self.setWindowTitle("Delete Player")

        self.uid_line = QLineEdit(self) ## 设置文本行
        self.finish_button = QPushButton('finish',self)

        self.uid_line.setMaxLength(20) ## 设置最大长度

        ## 获取输入 设置数据限制 设置长度限制

        self.g_layout = QGridLayout()
        self.g_layout.addWidget(self.uid_button,0,0,1,1)
        self.g_layout.addWidget(self.uid_line, 0, 1, 1, 1)
        self.g_layout.addWidget(self.finish_button, 1, 0, 1, 1)
        self.setLayout(self.g_layout)

        self.finish_button.clicked.connect(self.get_text_from_line)

    def get_text_from_line(self,parent = None):
        isok:int
        isok = 0

        if self.uid_line.isModified():
            self.uid = str(self.uid_line.text())
            isok += 1

        if isok == 1:
            self.dialog_signal.emit(self.uid)
            self.destroy() ## 自动关闭了


if  __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = delete_player_page()
    demo.show()

    sys.exit(app.exec_())