import sys
from PyQt5.QtCore import QPropertyAnimation, QPointF, QRectF, pyqtSignal
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsObject,QLineEdit
from PyQt5.QtGui import QMouseEvent
from Graphics_item import custom_ellipse,custom_text
import time
import Hello_Boost
import json

if __name__ == '__main__':

    test = Hello_Boost.position_finder_algorithm(1,1,1,1,1,1,"boss")
    test.add_obstacle(1,1,0,1,1,2,"1")
    ret_x,ret_y = test.find_position(1,1,0,1,1,1,"1",1,4)
    print(ret_y,ret_x)



