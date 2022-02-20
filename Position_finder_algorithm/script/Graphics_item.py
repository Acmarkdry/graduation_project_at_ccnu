import sys
import math
from PyQt5.QtCore import QPropertyAnimation,QRectF,QPointF,pyqtSignal,QLine
from PyQt5.QtGui import QColor,QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsObject,\
    QGraphicsItem,QGraphicsEllipseItem,QGraphicsTextItem

class custom_ellipse(QGraphicsObject):
    """
    对于椭圆类的重写
    """
    def __init__(self,_x:float,_y:float,_image_radius:float,speed:float,destination_x:float,
                 destination_y:float,uid:str):
        super(custom_ellipse, self).__init__()
        self.position_x = _x
        self.position_y = _y
        self.show_x = 0.0
        self.show_y = 0.0
        self.image_radius = _image_radius
        self.speed = speed
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.show_destination_x = 0.0
        self.show_destination_y = 0.0
        self.get_show_position()

    def get_show_position(self):
        self.show_x = self.position_x*10 + 250
        self.show_y = self.position_y*10 + 250
        self.show_destination_x = self.destination_x*10 + 250
        self.show_destination_y = self.destination_y*10 + 250

    def boundingRect(self):
        return QRectF(self.show_x - self.image_radius*10,self.show_y - self.image_radius*10
                      ,self.image_radius*10*2,self.image_radius*10*2)

    def paint(self, painter, option, widget = None) -> None:
        painter.drawEllipse(self.boundingRect())

class custom_text(QGraphicsObject):
    """
    对于文本的重写
    """
    def __init__(self,_x:float,_y:float,_image_radius:float,_uid:str):
        super(custom_text, self).__init__()
        self.uid = _uid
        self.position_x = _x
        self.position_y = _y
        self.image_radius = _image_radius
        self.show_x = 0.0
        self.show_y = 0.0
        self.get_show_position()

    def get_show_position(self):
        """
        我们认为他展现出来的是原来的坐标的10倍
        :return:
        """
        self.show_x = self.position_x*10 + 250
        self.show_y = self.position_y*10 + 250

    def boundingRect(self):
        return QRectF(self.show_x,self.show_y
                      ,self.image_radius*20,self.image_radius*20)

    def paint(self, painter, option, widget = None) -> None:
        painter.setPen(QColor(255,255,255))
        painter.drawText(self.boundingRect(),self.uid)

class custom_scene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 一些关于网格背景的设置
        self.grid_size = 20  # 一块网格的大小 （正方形的）
        self.grid_squares = 5  # 网格中正方形的区域个数

        # 一些颜色
        self._color_background = QColor('#aaaaaa')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')
        # 一些画笔
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        # 设置画背景的画笔
        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)

    # override
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # 获取背景矩形的上下左右的长度，分别向上或向下取整数
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        # 从左边和上边开始
        first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        first_top = top - (top % self.grid_size)

        # 分别收集明、暗线
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # 最后把收集的明、暗线分别画出来
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)
