#coding=utf-8
"""
主界面
"""
import math
import sys
from PyQt5.QtGui import QIcon,QMouseEvent,QPainterPath,QKeyEvent
from PyQt5.QtCore import QMimeData,pyqtSignal,QRectF,QPointF,QPropertyAnimation,Qt,QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox,\
                            QFontDialog, QColorDialog,QTableWidget,QTableWidgetItem,QAbstractItemView,\
                            QGraphicsScene, QGraphicsView, QGraphicsObject,QDockWidget,QGraphicsLineItem,\
                            QGraphicsItemGroup
import time
import json

from Enemy import enemy,Postion_finder_algorithm
from Add_player_page import add_player_page
from Delete_player_page import delete_player_page
from Update_boss_parameter import update_boss_parameter
from Graphics_item import custom_ellipse,custom_text,custom_scene
from Question_and_answer import question_and_answer_page

class main_window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Position Finder Algorithm")
        self.player_information = Postion_finder_algorithm()
        self.add_page: add_player_page()
        self.player_data_form: QTableWidget()
        self.picture_date: int
        self.dock_window = QDockWidget('player data',self)
        self.graph_scene = custom_scene(self)
        self.graph_view = QGraphicsView(self)

        self.player_circle_list = [] ## 圆的list
        self.player_line_list = []
        self.player_test_list = []

        self.player_animation_circle_list = [] ## 动画的list
        self.player_animation_test_list = []

        self.boss_group = QGraphicsItemGroup()
        self.boss_circle = custom_ellipse(1,1,1,1,1,1,"str")

        self.player_enemy_list = []

        self.boss_isok = 1 ## 判断boss是否已经添加

        self.init_ui()

    def init_ui(self):

        self.add_player_toolbar = self.addToolBar("Add Player")
        self.delete_player_toolbar = self.addToolBar("Delete Player")
        self.update_boss_parameter_toolbar = self.addToolBar("Update Boss")
        self.question_and_answer_toolbar = self.addToolBar("Q&A")
        self.add_boss_file_toolbar = self.addToolBar("Boss File")
        self.add_player_file_toolbar = self.addToolBar('Player File')
        self.save_boss_file_toolbar = self.addToolBar('Save Boss')
        self.save_player_file_toolbar = self.addToolBar('Save Player')

        self.status_bar = self.statusBar()

        self.add_player_action = QAction("Add Player",self)
        self.delete_player_action = QAction("Delete Player",self)
        self.update_boss_parameter_action = QAction("Update boss",self)
        self.question_and_answer_action = QAction("Question And Answer",self)
        self.add_boss_file_action = QAction("Boss File",self)
        self.add_player_file_action = QAction("Player File",self)
        self.save_boss_file_action = QAction("Save Boss",self)
        self.save_player_file_action = QAction("Save Player",self)
        ## 添加状态栏以及工具

        self.set_center() ## 居中显示

        self.toolbar_init()
        self.status_bar_init()
        self.action_init()
        self.player_form_init()
        self.dock_window_init()
        self.graph_scene_init()
        self.graph_view_init()

        self.setCentralWidget(self.graph_view)##表格居中显示

    def set_center(self):
        ## 窗口居中显示
        self.resize(QApplication.desktop().width() - 150,QApplication.desktop().height() - 150) ## 设置大小

        desktop = QApplication.desktop()
        d_width = desktop.width()
        d_height = desktop.height()

        pos_x = d_width/2 - self.frameGeometry().width()/2
        pos_y = d_height/2 - self.frameGeometry().height()/2

        self.move(int(pos_x),int(pos_y))

    def toolbar_init(self):
        self.add_player_toolbar.addAction(self.add_player_action)
        self.delete_player_toolbar.addAction(self.delete_player_action)
        self.update_boss_parameter_toolbar.addAction(self.update_boss_parameter_action)
        self.question_and_answer_toolbar.addAction(self.question_and_answer_action)
        self.add_boss_file_toolbar.addAction(self.add_boss_file_action)
        self.add_player_file_toolbar.addAction(self.add_player_file_action)
        self.save_boss_file_toolbar.addAction(self.save_boss_file_action)
        self.save_player_file_toolbar.addAction(self.save_player_file_action)

    def status_bar_init(self):
        self.status_bar.showMessage("Ready to compose")

    def action_init(self):
        ##self.add_player_action.setIcon() ## 设置动作图标
        self.add_player_action.setShortcut('Ctrl+A')
        self.add_player_action.setToolTip("Add a new player")## 设置气泡提示
        self.add_player_action.setStatusTip("Add a new player[Ctrl+A]") ## 设置状态栏提示
        self.add_player_action.triggered.connect(self.add_player) ## 设置触发器

        ##self.delete_player_action.setIcon()
        self.delete_player_action.setShortcut('Ctrl+D')
        self.delete_player_action.setToolTip('Delete a player')
        self.delete_player_action.setStatusTip("Delete a player[Ctrl+D]")
        self.delete_player_action.triggered.connect(self.delete_player)

        self.update_boss_parameter_action.setShortcut('Ctrl+W')
        self.update_boss_parameter_action.setToolTip('Update Boss parameter')
        self.update_boss_parameter_action.setStatusTip('Update Boss parameter[Ctrl+W]')
        self.update_boss_parameter_action.triggered.connect(self.update_boss_parameter)

        self.question_and_answer_action.setShortcut('Ctrl+Q')
        self.question_and_answer_action.setToolTip('Question And Answer')
        self.question_and_answer_action.setStatusTip('Question And Answer[Ctrl+Q]')
        self.question_and_answer_action.triggered.connect(self.question_and_answer)

        self.add_boss_file_action.setShortcut('Ctrl+1')
        self.add_boss_file_action.setToolTip('Add Boss From File')
        self.add_boss_file_action.setStatusTip('Add Boss From File[Ctrl+1]')
        self.add_boss_file_action.triggered.connect(self.add_boss_file)

        self.add_player_file_action.setShortcut('Ctrl+2')
        self.add_player_file_action.setToolTip('Add Player From File')
        self.add_player_file_action.setStatusTip('Add Player From File[Ctrl+2]')
        self.add_player_file_action.triggered.connect(self.add_player_file)

        self.save_boss_file_action.setShortcut('Ctrl+3')
        self.save_boss_file_action.setToolTip('Save Boss File')
        self.save_boss_file_action.setStatusTip('Save Boss File[Ctrl+3]')
        self.save_boss_file_action.triggered.connect(self.save_boss_file)

        self.save_player_file_action.setShortcut('Ctrl+4')
        self.save_player_file_action.setToolTip('Save Player File')
        self.save_player_file_action.setStatusTip('Save Player File[Ctrl+4]')
        self.save_player_file_action.triggered.connect(self.save_player_file)

    def player_form_init(self):
        """
        初始化表格信息
        :return:
        """
        self.player_data_form = QTableWidget()
        self.player_data_form.setRowCount(0)
        self.player_data_form.setColumnCount(6)

        self.player_data_form.setRowHeight(0,30)
        self.player_data_form.setColumnWidth(0,80)
        self.player_data_form.setColumnWidth(1, 80)
        self.player_data_form.setColumnWidth(2, 80)
        self.player_data_form.setColumnWidth(3, 80)
        self.player_data_form.setColumnWidth(4, 80)
        self.player_data_form.setColumnWidth(5, 80)

        self.player_data_form.setHorizontalHeaderLabels(['uid','x','y','des_x','des_y','dir'])
        self.player_data_form.setEditTriggers(QAbstractItemView.NoEditTriggers)## 设置表格为不可编辑

    def dock_window_init(self):
        """
        停靠窗口初始化
        :return:
        """
        self.dock_window.setAllowedAreas(Qt.AllDockWidgetAreas)## 全部可停靠
        self.dock_window.setFeatures(QDockWidget.DockWidgetMovable)
        self.dock_window.setFeatures(QDockWidget.NoDockWidgetFeatures)## 不可关闭
        self.dock_window.setWidget(self.player_data_form)
        print(self.dock_window.minimumSize().width())
        self.dock_window.setFixedWidth(480)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock_window)

    def graph_scene_init(self):
        """
        绘图场景初始化
        :return:
        """
        self.graph_scene = custom_scene()


    def graph_view_init(self):
        """
        绘图视图初始化
        :return:
        """
        self.graph_view.resize(500,500)
        self.graph_view.setScene(self.graph_scene)

    ## 下面是三个页面的槽函数
    def add_boss_file(self):
        """
        用来处理从json文件中读取boss信息
        :return:
        """
        file,_ = QFileDialog.getOpenFileName(self,'open File','../',
                                             'Files(*.json)')
        if(file):## 保证file是存在的
            f = open(file,'r')
            content = f.read()

            a = json.loads(content)

            self.update_boss_information_deal(a['uid'],a['x'],a['y'],a['image'],a['ask_in_angle'],a['le_angle'],a['ri_angle'])
        else:
            pass

    def add_player_file(self):
        """
        用来处理从json文件读取player信息
        :return:
        """
        file,_ = QFileDialog.getOpenFileName(self,'open File','../','Files(*.json)')

        if(file):
            f = open(file,'r')
            content = f.read()
            players = json.loads(content)

            for i in range(len(players["player"])):
                player = players["player"][i]

                self.add_player_information_deal(player['uid'],player['x'],player['y'],
                                                 player['image_radius'],player['attack_radius'],player['speed'])
        else:
            pass

    def save_boss_file(self):
        """
        用来保存boss信息
        :return:
        todo 如何获取文件名称
        """
        new_boss = self.player_information.boss
        file_name,_ = QFileDialog.getSaveFileName(
            self,'Save File','../','Files(*.json)'
        )

        if(file_name):
            boss_dict = {}
            boss_dict['uid'] = new_boss.uid
            boss_dict['x'] = new_boss.x
            boss_dict['y'] = new_boss.y
            boss_dict['image'] = new_boss.image_radius
            boss_dict['ask_in_angle'] = self.player_information.ask_in_angle
            boss_dict['le_angle'] = self.player_information.le_boss_angle
            boss_dict['ri_angle'] = self.player_information.ri_boss_angle

            b = json.dumps(boss_dict)
            file = open(file_name,'w')
            file.write(b)
            file.close()
        else:
            pass

    def save_player_file(self):
        """
        用来保存玩家信息
        :return:
        """
        file_name,_ = QFileDialog.getSaveFileName(
            self,'Save File','../','Files(*.json)'
        )

        if(file_name):
            player_list = []

            for i in range(len(self.player_enemy_list)):
                player_enemy = self.player_enemy_list[i]
                player_dict = {}
                player_dict['uid'] = player_enemy.uid
                player_dict['x'] = player_enemy.x
                player_dict['y'] = player_enemy.y
                player_dict['image_radius'] = player_enemy.image_radius
                player_dict['attack_radius'] = player_enemy.attack_radius
                player_dict['speed'] = player_enemy.speed
                player_list.append(player_dict)
            players_dict = {}
            players_dict['player'] = player_list
            b = json.dumps(players_dict)
            file = open(file_name,'w')
            file.write(b)
            file.close()
        else:
            pass

    def add_player(self):
        """
        add按钮的槽函数
        :return:
        """
        self.add_page = add_player_page()
        self.add_page.dialog_signal.connect(self.add_player_information_deal)

        self.add_page.show()

    def add_player_information_deal(self,uid:str,x:float,y:float,image_radius:float
                                    ,attack_radius:float,speed:float):
        """
        按下finish后会发生的事情 增加一个玩家
        :return:
        """
        new_player = enemy()

        new_player.uid = uid
        new_player.x = x
        new_player.y = y
        new_player.image_radius = image_radius
        new_player.attack_radius = attack_radius
        new_player.speed = speed

        new_player.destination_x,new_player.destination_y = self.player_information.position_finder(
            x,y,image_radius,attack_radius,speed,uid
        )

        rowcount = self.player_data_form.rowCount()
        
        self.player_data_form.insertRow(rowcount)
        self.player_data_form.setItem(rowcount,0,QTableWidgetItem(uid))
        self.player_data_form.setItem(rowcount,1,QTableWidgetItem(str(round(x,2))))
        self.player_data_form.setItem(rowcount,2,QTableWidgetItem(str(round(y,2))))
        self.player_data_form.setItem(rowcount,3,QTableWidgetItem(str(round(new_player.destination_x,2))))
        self.player_data_form.setItem(rowcount,4,QTableWidgetItem(str(round(new_player.destination_y,2))))
        self.player_data_form.setItem(rowcount,5,QTableWidgetItem(str(round(math.atan2(new_player.destination_y - new_player.y,
                                                       new_player.destination_x - new_player.x),2))))
        ## 添加表格

        new_player_circle = custom_ellipse(new_player.x,new_player.y,new_player.image_radius,
                                           new_player.speed,new_player.destination_x,new_player.destination_y,new_player.uid)
        new_player_test = custom_text(new_player.x,new_player.y,new_player.image_radius,new_player.uid)
        new_player_line = QGraphicsLineItem(new_player_circle.show_x,new_player_circle.show_y,new_player_circle.show_destination_x,new_player_circle.show_destination_y)

        self.player_circle_list.append(new_player_circle)
        self.player_test_list.append(new_player_test)
        self.player_line_list.append(new_player_line)

        self.graph_scene.addItem(new_player_circle)
        self.graph_scene.addItem(new_player_test)
        self.graph_scene.addItem(new_player_line)
        ## 将添加的椭圆，字体，直线放入其中

        move_time = math.sqrt((new_player.x - new_player.destination_x)**2 + (new_player.y - new_player.destination_y)**2)
        move_time = int(move_time*1000)

        if move_time == 0: move_time = 1 ## 特殊处理

        new_player_animation_circle = QPropertyAnimation(new_player_circle,b'pos')
        new_player_animation_circle.setDuration(move_time)
        new_player_animation_circle.setStartValue(QPointF(0,0))
        new_player_animation_circle.setEndValue(QPointF(new_player_circle.show_destination_x - new_player_circle.show_x,
                                                       new_player_circle.show_destination_y - new_player_circle.show_y))
        new_player_animation_circle.setLoopCount(1)

        new_player_animation_test = QPropertyAnimation(new_player_test,b'pos')
        new_player_animation_test.setDuration(move_time)
        new_player_animation_test.setStartValue(QPointF(0,0))
        new_player_animation_test.setEndValue(QPointF(new_player_circle.show_destination_x - new_player_circle.show_x,
                                                       new_player_circle.show_destination_y - new_player_circle.show_y))
        new_player_animation_test.setLoopCount(1)

        new_player_animation_circle.start()
        new_player_animation_test.start()
        ## 添加动画

        self.player_animation_circle_list.append(new_player_animation_circle)
        self.player_animation_test_list.append(new_player_animation_test)

        self.player_enemy_list.append(new_player)
        ## 将椭圆，字体，椭圆动画，字体动画放入其中，方便之后的处理

    def delete_player(self,uid:str):
        """
        删除玩家的槽函数
        :param uid:
        :return:
        """
        self.delete_page = delete_player_page()
        self.delete_page.dialog_signal.connect(self.delete_player_information_deal)
        self.delete_page.show()

    def delete_player_information_deal(self,uid:str):
        delete_row = self.player_information.delete_player_uid(uid)

        if(delete_row < self.player_data_form.rowCount()):
            self.player_data_form.removeRow(delete_row) ## 从表格中删除

        if (delete_row < len(self.player_animation_test_list)):
            self.player_animation_test_list = self.player_animation_test_list[0:delete_row] + self.player_animation_test_list[delete_row + 1:]

        if (delete_row < len(self.player_animation_circle_list)):
            self.player_animation_circle_list = self.player_animation_circle_list[0:delete_row] + self.player_animation_circle_list[delete_row + 1:]

        if (delete_row < len(self.player_line_list)):
            self.graph_scene.removeItem(self.player_line_list[delete_row])
            self.player_line_list = self.player_line_list[0:delete_row] + self.player_line_list[delete_row + 1:]

        if(delete_row < len(self.player_test_list)):
            self.graph_scene.removeItem(self.player_test_list[delete_row])
            self.player_test_list = self.player_test_list[0:delete_row] + self.player_test_list[delete_row + 1:]

        if(delete_row < len(self.player_circle_list)):
            self.graph_scene.removeItem(self.player_circle_list[delete_row])
            self.player_circle_list = self.player_circle_list[0:delete_row] + self.player_circle_list[delete_row + 1:]

        if(delete_row < len(self.player_enemy_list)):
            self.player_enemy_list = self.player_enemy_list[0:delete_row] + self.player_enemy_list[delete_row + 1:]
        ## 删除指定uid的图元 动画已经可以被删除了

    def question_and_answer(self):
        self.question_and_answer_page = question_and_answer_page()
        self.question_and_answer_page.show()

    def question_and_answer_deal(self):
        pass

    def update_boss_parameter(self):
        """
        update的槽函数
        :return:
        """
        self.update_boss_page = update_boss_parameter()
        self.update_boss_page.dialog_signal.connect(self.update_boss_information_deal)
        self.update_boss_page.show()

    def update_boss_information_deal(self,uid:str,x:float,y:float,image_radius:float
                                     ,ask_in_angle:int,le_angle:float,ri_angle:float):
        if ask_in_angle == 0:
            le_angle = 0
            ri_angle = 2*math.pi

        self.boss_isok = 0
        self.graph_scene.removeItem(self.boss_group) ## 控制删除之前的boss

        self.player_information.position_boss_reset(x,y,image_radius,uid,ask_in_angle,le_angle,ri_angle)

        boss_circle = custom_ellipse(x,y,image_radius,1,1,1,uid)

        pos = boss_circle.scenePos()

        print(pos.x(),pos.y())

        boss_test = custom_text(x,y,image_radius,uid)
        delta_x = math.cos(le_angle)
        delta_y = math.sin(le_angle)
        boss_le_line = QGraphicsLineItem(boss_circle.show_x + 10*image_radius*delta_x,
                                         boss_circle.show_y + 10*image_radius*delta_y,
                                         boss_circle.show_x + 20*image_radius*delta_x,
                                         boss_circle.show_y + 20*image_radius*delta_y)

        delta_x = math.cos(ri_angle)
        delta_y = math.sin(ri_angle)
        boss_ri_line = QGraphicsLineItem(boss_circle.show_x + 10*image_radius*delta_x,
                                         boss_circle.show_y + 10*image_radius*delta_y,
                                         boss_circle.show_x + 20*image_radius*delta_x,
                                         boss_circle.show_y + 20*image_radius*delta_y)

        ## todo 画一下弧形，这里可能有一些问题
        self.boss_group = QGraphicsItemGroup()
        self.boss_group.addToGroup(boss_circle)
        self.boss_group.addToGroup(boss_test)
        self.boss_group.addToGroup(boss_le_line)
        self.boss_group.addToGroup(boss_ri_line)
        self.boss_group.setFlags(QGraphicsItemGroup.ItemIsSelectable | QGraphicsItemGroup.ItemIsMovable)

        self.graph_scene.addItem(self.boss_group)
        self.boss_circle = boss_circle

        self.update_all_player_state() ## 更新所有玩家的状态

    def update_all_player_state(self):
        """
        处理更新boss信息时，所有玩家自身信息更新的问题

        当更新boss时我们要做的：
        之前路径重新导向
        动画重新导向
        表格信息更新
        :return:
        """
        for i in range(len(self.player_enemy_list)):
            player_animation_circle = self.player_animation_circle_list[i]
            player_animation_circle:QPropertyAnimation

            player_enemy = self.player_enemy_list[i]
            player_enemy:enemy

            pos = player_animation_circle.currentValue()

            show_x = player_enemy.x*10 + 250 + pos.x()
            show_y = player_enemy.y*10 + 250 + pos.y()

            x = show_x/10 - 25
            y = show_y/10 - 25
            self.player_information.add_obstacle(
                x,
                y,
                player_enemy.image_radius,
                player_enemy.attack_radius,
                player_enemy.speed,
                player_enemy.uid
            )
            ##print(player_enemy.uid,player_enemy.x,player_enemy.y)
            ##print(self.player_enemy_list[i].uid,self.player_enemy_list[i].x,self.player_enemy_list[i].y)

        for i in range(len(self.player_enemy_list)):
            player_animation_circle = self.player_animation_circle_list[i]
            player_animation_circle:QPropertyAnimation

            player_animation_test = self.player_animation_test_list[i]
            player_animation_test: QPropertyAnimation

            player_circle = self.player_circle_list[i]
            player_circle:custom_ellipse

            player_test = self.player_test_list[i]
            player_test:custom_text

            player_line = self.player_line_list[i]
            player_line:QGraphicsLineItem

            player_enemy = self.player_enemy_list[i]
            player_enemy:enemy

            self.graph_scene.removeItem(player_circle)
            self.graph_scene.removeItem(player_line)
            self.graph_scene.removeItem(player_test) ## 删除原来的东西

            pos = player_animation_circle.currentValue()

            show_x = player_enemy.x*10 + 250 + pos.x()
            show_y = player_enemy.y*10 + 250 + pos.y()

            player_enemy.x = show_x/10 - 25
            player_enemy.y = show_y/10 - 25

            ##print("新点的真实坐标为",player_enemy.x,player_enemy.y)

            start = time.time()

            player_enemy.destination_x,player_enemy.destination_y = self.player_information.position_finder(
                    player_enemy.x,
                player_enemy.y,
                player_enemy.image_radius,
                player_enemy.attack_radius,
                player_enemy.speed,
                player_enemy.uid
            ) ## 寻路算法时间复杂度关键点在这里

            end = time.time()
            print("运行时间为:",(end - start)*1000,"ms")

            show_destination_x = player_enemy.destination_x*10 + 250
            show_destination_y = player_enemy.destination_y*10 + 250
            ## 获得终点

            player_circle = custom_ellipse(player_enemy.x,player_enemy.y,player_enemy.image_radius,
                                           player_enemy.speed,player_enemy.destination_x,player_enemy.destination_y,
                                           player_enemy.uid)
            player_test = custom_text(player_enemy.x,player_enemy.y,player_enemy.image_radius,player_enemy.uid)
            ## 圆更新

            player_line = QGraphicsLineItem(show_x, show_y, show_destination_x, show_destination_y)

            self.graph_scene.addItem(player_line)
            self.graph_scene.addItem(player_circle)
            self.graph_scene.addItem(player_test)
            ## 将新的三个东西加入场景中

            move_time = math.sqrt((player_enemy.x - player_enemy.destination_x)**2 +
                                  (player_enemy.y - player_enemy.destination_y)**2)/player_enemy.speed

            move_time = int(move_time*1000)

            if(move_time == 0):move_time = 1

            player_test.setPos(show_x,show_y)
            player_circle.setPos(show_x,show_y)

            player_animation_test = QPropertyAnimation(player_test,b'pos')
            player_animation_test.setDuration(move_time)
            player_animation_test.setStartValue(QPointF(0,0))
            player_animation_test.setEndValue(QPointF(show_destination_x - show_x,
                                                       show_destination_y - show_y))
            player_animation_test.setLoopCount(1)

            player_animation_circle = QPropertyAnimation(player_circle,b'pos')
            player_animation_circle.setDuration(move_time)
            player_animation_circle.setStartValue(QPointF(0,0))
            player_animation_circle.setEndValue(QPointF(show_destination_x - show_x,
                                                       show_destination_y - show_y))
            player_animation_circle.setLoopCount(1)

            player_animation_circle.start()
            player_animation_test.start()
            ## 更新动画

            self.player_line_list[i] = player_line
            self.player_test_list[i] = player_test
            self.player_circle_list[i] = player_circle

            self.player_animation_circle_list[i] = player_animation_circle
            self.player_animation_test_list[i] = player_animation_test
            self.player_enemy_list[i] = player_enemy
            ## 将五个东西进行更新

            self.player_data_form.setItem(i,1,QTableWidgetItem(str(round(player_enemy.x,2))))
            self.player_data_form.setItem(i, 2, QTableWidgetItem(str(round(player_enemy.y,2))))
            self.player_data_form.setItem(i, 3, QTableWidgetItem(str(round(player_enemy.destination_x,2))))
            self.player_data_form.setItem(i, 4, QTableWidgetItem(str(round(player_enemy.destination_y,2))))
            ## 更新表格的信息

        ## pos = animation.currentValue() 获取运动动画的当前信息
        ## x = pos.x()
        ##self.player_data_form.setItem() 更新指定行数的信息

    def mouseDoubleClickEvent(self, a0):
        """
        处理boss信息更新事件 发现不会了，只能在这里通过双击来实现
        坐标处理发现每次通过变换实现
        :param event:
        :return:
        """
        print(self.boss_isok)
        if self.boss_isok == 1:
            return

        new_boss = self.player_information.boss
        pos = self.boss_circle.scenePos()
        new_boss.x = new_boss.x + pos.x()/10
        new_boss.y = new_boss.y + pos.y()/10

        self.graph_scene.removeItem(self.boss_group)

        self.player_information.position_boss_reset(new_boss.x,new_boss.y,
                                                    new_boss.image_radius,new_boss.uid,self.player_information.ask_in_angle,
                                                    self.player_information.le_boss_angle,self.player_information.ri_boss_angle)

        boss_circle = custom_ellipse(new_boss.x, new_boss.y, new_boss.image_radius, 1, 1, 1, new_boss.uid)

        pos = boss_circle.scenePos()

        ##print(pos.x(), pos.y())
        ##print("当前boss所在坐标为",new_boss.x,new_boss.y)

        boss_test = custom_text(new_boss.x, new_boss.y, new_boss.image_radius, new_boss.uid)
        delta_x = math.cos(self.player_information.le_boss_angle)
        delta_y = math.sin(self.player_information.le_boss_angle)
        boss_le_line = QGraphicsLineItem(boss_circle.show_x + 10 * new_boss.image_radius * delta_x,
                                         boss_circle.show_y + 10 * new_boss.image_radius * delta_y,
                                         boss_circle.show_x + 20 * new_boss.image_radius * delta_x,
                                         boss_circle.show_y + 20 * new_boss.image_radius * delta_y)

        delta_x = math.cos(self.player_information.ri_boss_angle)
        delta_y = math.sin(self.player_information.ri_boss_angle)
        boss_ri_line = QGraphicsLineItem(boss_circle.show_x + 10 * new_boss.image_radius * delta_x,
                                         boss_circle.show_y + 10 * new_boss.image_radius * delta_y,
                                         boss_circle.show_x + 20 * new_boss.image_radius * delta_x,
                                         boss_circle.show_y + 20 * new_boss.image_radius * delta_y)

        ## todo 画一下弧形，这里可能有一些问题
        self.boss_group = QGraphicsItemGroup()
        self.boss_group.addToGroup(boss_circle)
        self.boss_group.addToGroup(boss_test)
        self.boss_group.addToGroup(boss_le_line)
        self.boss_group.addToGroup(boss_ri_line)
        self.boss_group.setFlags(QGraphicsItemGroup.ItemIsSelectable | QGraphicsItemGroup.ItemIsMovable)
        self.graph_scene.addItem(self.boss_group)
        self.boss_circle = boss_circle
        self.update_all_player_state()

    def mousePressEvent(self, a0:QMouseEvent):
        new_boss = self.player_information.boss
        pos = self.boss_circle.scenePos()
        _x = new_boss.x + pos.x()/10
        _y = new_boss.y + pos.y()/10
        ##pos = self.graph_view.mapFromScene(pos)
        print_str = str(_x) + " " + str(_y)

        self.status_bar.showMessage(print_str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = main_window()
    demo.show()
    sys.exit(app.exec_())
    ## todo 要求输入时可以实现按下回车自动跳转 不会搞
    ## todo 加上虚线的设置