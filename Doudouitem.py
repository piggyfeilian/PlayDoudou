# -*- coding: UTF-8 -*-
#豆豆item,教猪打豆豆

from PyQt4.QtGui import *
form PyQt4.QtCore import *
import qrc_resource

UNIT_WIDTH = 20
EDGE_WIDTH = 1

def GetPos(x, y):
    return QPointF(x * (UNIT_WIDTH + EDGE_WIDTH), y * (UNIT_WIDTH + EDGE_WIDTH))
class DouBack(QGraphicsObject):
    def __init__(self, x = 0, y = 0,parent = None):
        super(DouBack, self).__init__(parent)
        self.corX = x
        self.corY = y
        self.setPos(GetPos(x,y))
        
    def setPos(self, x, y):
        self.corX = x
        self.corY = y
        self.setPos(GetPos(x,y))

    def boundingRect(self):
        return QRect(0 ,0, UNIT_WIDTH + EDGE_WIDTH, UNIT_WIDTH + EDGE_WIDTH)

class DouDou(DouBack):
    def __init__(self, x, y, color, parent = None):
        super(Doudou, self).__init__(x, y, parent)
        self.color = QColor(*color)

    def paint(self, painter, option, widget = None):
        #暂时用圆代替
        painter.save()
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)
        painter.setBrush(brush)
        painter.drawEllipse(EDGE_WIDTH/2, EDGE_WIDTH / 2, UNIT_WIDTH, UNIT_WIDTH)
        painter.restore()

    def __eq__(self, obj):
        return (self.color == obj.color)

class Balk(DouBack):
    def __init__(self, x, y, parent = None):
        super(Doudou, self).__init__(x, y, parent)
        self.picture = QImage(":balk.png").scaled(UNIT_WIDTH, UNIT_WIDTH)

    def paint(self, painter, option, widget = None):
        #找个图片来
        painter.save()
        painter.setCompositionMode(QPainter.Multiply)
        painter.drawImage(QPointF(EDGE_WIDTH/2, EDGE_WIDTH/2), self.picture)
