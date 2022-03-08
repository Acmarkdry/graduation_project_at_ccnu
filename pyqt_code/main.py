import json
import sys

import numpy
import pandas
from PyQt5.QtGui import QIcon,QMouseEvent,QPainterPath,QKeyEvent
from PyQt5.QtCore import QMimeData,pyqtSignal,QRectF,QPointF,QPropertyAnimation,Qt,QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, \
    QFontDialog, QColorDialog,QTableWidget,QTableWidgetItem,QAbstractItemView, \
    QGraphicsScene, QGraphicsView, QGraphicsObject,QDockWidget,QGraphicsLineItem, \
    QGraphicsItemGroup
from Help_page import help_page
from Information import Information
from UserChoice import UserChoice

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
        self.recommand_result = [] # 推荐结果列表
        self.setWindowTitle("Recommand Resources Algorithm")

        #self.resources_bar = self.addToolBar('Resources')
        self.resize(800,1000)
        # 以上为各插件的初始化

        self.dock_window = QDockWidget("User Data",self);

        self.menu_init()
        self.toolbar_init()
        self.status_bar_init()
        self.dock_window_init()
        self.action_init()

    def menu_init(self):
        self.resources_bar = self.addToolBar('Resources')
        self.teacher_bar = self.addToolBar('Teacher')
        self.knowledge_bar = self.addToolBar('knowledge')
        self.help_bar = self.addToolBar('Help')
        self.save_bar = self.addToolBar('Save')
        self.choice_bar = self.addToolBar('Choice')

        self.status_bar = self.statusBar()

        self.resources_action = QAction("Resources",self)
        self.teacher_action = QAction("Teacher",self)
        self.knowledge_action = QAction("knowledge",self)
        self.help_action = QAction("Help",self)
        self.save_action = QAction("Save",self)
        self.choice_action = QAction("Choice",self)

        self.set_center()

    def set_center(self):
        # 将栏目居中
        #self.resize(QApplication.desktop().width() - 150,QApplication.desktop().height() - 150)

        # desktop = QApplication.desktop()
        # d_width = desktop.width()
        # d_height = desktop.height()
        #
        # pos_x = d_width/2 - self.frameGeometry().width()/2
        # pos_y = d_height/2 - self.frameGeometry().height()/2
        #
        # self.move(int(pos_x),int(pos_y))
        self.resize(QApplication.desktop().width() - 2500, QApplication.desktop().height() - 150)

    def toolbar_init(self):
        # 初始化toolbar
        self.resources_bar.addAction(self.resources_action)
        self.teacher_bar.addAction(self.teacher_action)
        self.knowledge_bar.addAction(self.knowledge_action)
        self.help_bar.addAction(self.help_action)
        self.save_bar.addAction(self.save_action)
        self.choice_bar.addAction(self.choice_action)

    def status_bar_init(self):
        self.status_bar.showMessage("Ready to compose")

    def action_init(self):
        # self.add_player_action.setShortcut('Ctrl+A')
        # self.add_player_action.setToolTip("Add a new player")## 设置气泡提示
        # self.add_player_action.setStatusTip("Add a new player[Ctrl+A]") ## 设置状态栏提示
        # self.add_player_action.triggered.connect(self.add_player) ## 设置触发器
        self.resources_action.setShortcut('Ctrl+R')
        self.resources_action.setToolTip("Add Resources")
        self.resources_action.setStatusTip("Add your resources[Ctrl+R]")
        self.resources_action.triggered.connect(self.add_resources)

        self.teacher_action.setShortcut('Ctrl+T')
        self.teacher_action.setToolTip('Add Teacher')
        self.teacher_action.setStatusTip('Add your teacher[Ctrl+T]')
        self.teacher_action.triggered.connect(self.add_teacher)

        self.knowledge_action.setShortcut('Ctrl+K')
        self.knowledge_action.setToolTip('Add knowledge reflection')
        self.knowledge_action.setStatusTip('Add knowledge function[Ctrl+K]')
        self.knowledge_action.triggered.connect(self.add_knowledge)

        self.help_action.setShortcut('Ctrl+H')
        self.help_action.setToolTip('Help you')
        self.help_action.setStatusTip('Help you[Ctrl+H]')
        self.help_action.triggered.connect(self.add_help)

        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('Save some file')
        self.save_action.setStatusTip('Save some file[Ctrl+S]')
        self.save_action.triggered.connect(self.add_save_function)

        self.choice_action.setShortcut("Ctrl+C")
        self.choice_action.setToolTip("Choice Something")
        self.choice_action.setStatusTip("Choice Something[Ctrl+s]")
        self.choice_action.triggered.connect(self.add_choice)

    def add_choice(self):
        self.choice_page = UserChoice()
        self.choice_page.dialog_signal.connect(self.add_choice_deal)

        self.choice_page.show()

    def add_choice_deal(self,Algorithm:str,UserId:int,RecommandNum:int):
        self.Algorithm = Algorithm
        self.UserId = UserId
        self.RecommandNum = RecommandNum

    def add_resources(self):
        # 打开json文件 对应resources文件夹
        file,_ = QFileDialog.getOpenFileName(self,'open File','../','Files(*.json)')

        if file:
            f = open(file,'r')
            content = f.read()
            f.close()

            self.student_resources = json.loads(content)
            self.student_resources_path = file
            self.student_resources_list = [[0 for j in range(10)] for i in range(81)]

            for i in range(1,81):
                for j in range(10):
                    tmp = str(i)
                    self.student_resources_list[i][j] = self.student_resources[tmp][j]

            self.user_data_form.StudnetPageChanged(self.student_resources_list)

        else :
            pass

    def add_teacher(self):
        # 打开csv文件
        file,_ = QFileDialog.getOpenFileName(self,'open File','../','Files(*.csv)')

        if file:
            self.teacher = pandas.read_csv(file)
            self.teacher = numpy.array(self.teacher)
            self.teacher_path = file

            self.teacher_list = [[0 for i in range(self.teacher.shape[1])] for i in range(self.teacher.shape[0])]

            self.student_resources = json.loads(content)

            for i in range(self.teacher.shape[0]):
                for j in range(self.teacher.shape[1]):
                    self.teacher_list[i][j] = self.teacher[i][j]

            self.user_data_form.TeacherPageChanged(self.teacher_list)

        else:
            pass

    def add_knowledge(self):
        # 打开csv文件
        file,_ = QFileDialog.getOpenFileName(self,'Open File','../','Files(*.json)')

        if file:
            f = open(file,'r')
            content = f.read()
            f.close()

            self.knowledge_resources = json.loads(content)

            self.knowledge_path = file

            self.knowledge_resources_list = [[0 for i in range(2)] for i in range(221)]

            for i in range(1,221):
                tmp = str(i)
                self.knowledge_resources_list[i][0] = i;
                self.knowledge_resources_list[i][1] = self.knowledge_resources[tmp]

            self.user_data_form.KnowledgeChanged(self.knowledge_resources_list)

    def add_help(self):
        self.help_page = help_page()
        self.help_page.show()

    def add_save_function(self):
        file_name,_ = QFileDialog.getSaveFileName(
            self,'Save File','../','Files(*csv)'
        )
        if file_name:
            tmp = pandas.DataFrame(data = self.recommand_result)
            tmp.to_csv(file_name, encoding='utf-8', index=False)

        else:
            pass

    def dock_window_init(self):
        self.user_data_form = Information()

        self.dock_window.setAllowedAreas(Qt.AllDockWidgetAreas) # 全部可停靠
        self.dock_window.setFeatures(QDockWidget.DockWidgetMovable)
        self.dock_window.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock_window.setWidget(self.user_data_form)

        print(self.dock_window.minimumSize().width())
        self.dock_window.setFixedWidth(480)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())