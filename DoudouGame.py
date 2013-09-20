#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from DoudouView import *
#用状态机做，分主界面，各关分数展示界面（可以跳转到该关卡玩游戏),游戏界面(以后可以加入对对碰界面)

class DouDouGame(QGraphicsView):
    def __init__(self, scene, parent = None):
        super(DouDouGame, self).__init__(parent)

        self.scene = scene
        #背景
        backWidget = BackWidget()
        self.backWindow = QGraphicsProxyWidget()
        self.backWindow.setWidget(backWidget)
        self.backWindow.setX(0)
        self.backWindow.setY(0)
        self.backWindow.setZValue(0)

        #主界面选择button
        mainWidget = MainWidget()
        self.mainWindow = QGraphicsProxyWidget()
        self.mainWindow.setWidget(mainWidget)
        self.mainWindow.setX(400)
        self.mainWindow.setY(200)
        self.mainWinodw.setZValue(1)

        #展示最高纪录widget
        showWidget = ShowWidget()
        self.showWindow = QGraphicsProxyWidget()
        self.showWindow.setWidget(showWidget)
        self.showWindow.setX(50)
        self.showWindow.setY(0)
        self.showWindow.setZValue(1)

        #回合结束跳出
        compWidget = CompWidget()
        self.compWindow = QGraphicsProxyWidget()
        self.compWindow.setWidget(compWidget)
        self.compWindow.setX(300)
        self.compWindow.setY(200)
        self.compWindow.setZValue(1)

        #游戏界面
        gameWidget = GameWidget()
        self.gameWindow = QGraphicsProxyWidget()
        self.gameWindow.setWidget(gameWidget)
        self.gameWindow.setX(50)
        self.gameWindow.setY(20)
        self.gameWindow.setZValue(0.8)

        self.gameWindow.close()
        self.showWindow.close()
        self.compWindow.close()

        #状态机
        self.stateMachine = QStateMachine(self)
        #可以考虑加入一个介绍或者欢迎state
        self.mainState = QState(self.stateMachine)
        self.showState = QState(self.stateMachine)
        #做一个custom transition根据用户决定来选择下一个state
        self.compState = QState(self.stateMachine)
        self.gameState = QState(self.stateMachine)


        #加transition
        
        self.preState = None

        self.stateDict = {self.mainState:self.mainWindow, self.showState:self.showWindow,
                          self.compState:self.compWindow, self.gameState:self.gameWindow}
        for state in self.stateDict:
            self.connect(state, SIGNAL("enterd()"), self.on_Entered)

        self.stateMachine.setInitialState(self.mainState)
        self.stateMachine.start()
