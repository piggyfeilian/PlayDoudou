#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Doudouitem import *

RED = 0
PINK = 1
YELLO = 2
ORANGE = 3
BLUE = 4
SKY = 5
GREEN = 6
DARKGREEN = 7
PURPLE = 8
BLACK = 9
#特殊的豆豆
PIGGY = 10

Colors = ((255,0,0), (255,192,203),(255,255,0), (255,97,0),(0,0,255),
          (176, 224, 230), (124, 252, 0), (34, 139, 34), (160, 32, 240),(0, 0, 0))



class DouDouView(QGraphicsView):
    def __init__(self, scene, parent = None):
        super(DouDouView, self).__init__(parent)

        self.setMouseTracking(True)
        self.scene = scene
        self.setScene(self.scene)
        #默认size
        self.douMapSize = (10, 10)
        self.range = 0
#        self.douMap = []
    #设置打豆豆大小
    def setDouSize(self, size):
        for i in range(size[0]):
            for j in range(size[1]):
                new_douMap = DouBack(j, i, (j + i)%2)
                self.scene.addItem(new_douMap)
                new_douMap.setPos(j, i)
        self.douMapSize = tuple(size)

    #根据难度range随机获取豆豆
    def getNewRoundDou(self):
        pass

    #用于存档读取上次的豆豆们,文件io在外部实现
    def setDoudou(self, douList):
        pass
    #检查是否该位置可以消除
    def checkCorrect(self, cord):
        pass
    #mousepresseventhandler
    def mousePressEvent(self, event):
        pass
    #indicate mouse moving
    def mouseMoveEvent(self, event):
        pass
    #重新排列现有豆豆函数
    def refreshDou(self):
        pass
