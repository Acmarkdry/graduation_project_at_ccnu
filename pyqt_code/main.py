import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, \
    QFontDialog, QColorDialog

class Demo(QMainWindow):
    """
    功能需求
    需要一个 resources导入 teacher 导入 knowledge 导入 一个help导入
    还有一个保存结果

    左边需要三个算法选择 一个用户名称选择 推荐知识个数 推荐老师个数
    右边显示多个页面，分别是导入的resources teacher knowledge 以及最后的推荐结果
    """
    def __init__(self):
        super(Demo, self).__init__()
        self.setWindowTitle("Recommand Resources Algorithm")

        #self.resources_bar = self.addToolBar('Resources')
        self.resize(800,1000)
        # 以上为各插件的初始化

        self.init_ui()

    def menu_init(self):
        self.resources_bar = self.addToolBar('Resources')
        self.teacher_bar = self.addToolBar('Teacher')
        self.knowledge_bar = self.addToolBar('knowledge')
        self.help_bar = self.addToolBar('Help')
        self.save_bar = self.addToolBar('Save')

        self.status_bar = self.statusBar()

        self.resources_action = QAction("Resources",self)
        self.teacher_action = QAction("Teacher",self)
        self.knoledge_action = QAction("knowledge",self)
        self.help_action = QAction("Help",self)
        self.save_action = QAction("Save",self)

        self.set_centrt()

    def set_center(self):
        # 将栏目居中
        pass

    def toolbar_init(self):
        # 初始化toolbar
        pass

    def status_bar_init(self):
        pass

    def action_init(self):
        pass

if __name__ == "__main__":
    pass