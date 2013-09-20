#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from DoudouView import *
#用状态机做，分主界面，各关分数展示界面（可以跳转到该关卡玩游戏),游戏界面(以后可以加入对对碰界面)

class DouDouGame(QGraphicsView):
    def __init__(self, scene, parent = None):
        super(DouDouGame, self).__init__(parent)

        self.scene = scene



        #状态机
        self.stateMachine = QStateMachine(self)
        self.mainState = QState(self.stateMachine)
        self.showState = QState(self.stateMachine)
        #做一个custom transition根据用户决定来选择下一个state
        self.compState = QState(self.stateMachine)
        self.gameState = QState(self.stateMachine)
