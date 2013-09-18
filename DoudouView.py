#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Doudouitem import *




class DouDouView(QGraphicsView):
    def __init__(self, scene, parent = None):
        super(DouDouView, self).__init__(parent)
        
        self.scene = scene
        self.setScene(self.scene)
        #默认size
        self.size = (10, 10)
        self.douMap = []
    def setDoudou(self, douMap):
        for i in range(len(Dou)):
            self.douMap.append([])
            for j in range(len(Dou[i])):
                self.douMap[i].append(Dou[i][j])
                new_douMap = DouBack()#教猪
