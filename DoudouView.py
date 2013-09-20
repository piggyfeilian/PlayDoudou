#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from Doudouitem import *
import random,sys

NODOU = 0
RED = 1
PINK = 2
YELLO = 3
ORANGE = 4
BLUE = 5
SKY = 6
GREEN = 7
DARKGREEN = 8
PURPLE = 9
BLACK = 10
#特殊的豆豆
PIGGY = 11
#障碍
BALK = 12

Colors = (None, (255,0,0), (255,192,203),(255,255,0), (255,97,0),(0,0,255),
          (176, 224, 230), (124, 252, 0), (34, 139, 34), (160, 32, 240), (0, 0, 0), PIGGY, BALK)



class DouDouView(QGraphicsView):
    def __init__(self, scene, parent = None):
        super(DouDouView, self).__init__(parent)

        self.setMouseTracking(True)
        self.scene = scene
        self.setScene(self.scene)
        #默认size
        self.douMapSize = (12, 12)
        self.range = 0
        self.doudous = []
#        self.dous = []
        self.score = 0
        self.gameStarted = False
        self.douMap_list = []
        self.animation = None
        self.tmpItem = []
        #空白点列表
        self.availableSpots = []
    #设置打豆豆大小
    def setDouSize(self, size):
        for i in range(size[0]):
            for j in range(size[1]):
                new_douMap = DouMap(j, i, (j + i)%2)
                self.scene.addItem(new_douMap)
                new_douMap.setPos(j, i)
                self.douMap_list.append(new_douMap)
        self.douMapSize = tuple(size)

    #根据难度range随机获取豆豆和障碍
    def getNewRoundDou(self):
        if not self.range:
            #根据级数调整特殊豆豆，空白，障碍的个数
            num_piggy = None
            num_blank = None
            num_balk = 0
        elif self.range == 1:
            num_piggy = None
            num_blank = int(size[0] * size[1] / 12)
            num_balk = 0
        else:
            num_piggy = 8 - self.range
            num_blank = int(size[0] * size[1] / 10) - self.range
            if num_blank < 8:
                num_blank = 8
            num_balk = -2 + self.range
            if num_balk > num_blank:
                num_balk = num_blank
        print "piggy个数：", num_piggy#for test

        rand_start = 0 if num_blank else -1
        rand_end = 10 if num_piggy else 11
        for i in range(self.douMapSize[0]):
            self.doudous.append([])
            for j in range(self.douMapSize[1]):
                new_color = random.randint(rand_start, rand_end)
                if new_color:
                    new_doudou = DouDou(j, i, Colors[new_color])
                    self.scene.addItem(new_doudou)
                    new_doudou.setPos(j, i)
                else:
                    new_doudou = None
                    self.availableSpots.append((j, i))
                self.doudous[i].append(new_doudou)

        if num_piggy and num_piggy > 0:
            for i in range(num_piggy):
                a = random.randint(-1, self.douMapSize[0] - 1)
                b = random.randint(-1, self.douMapSize[1] - 1)
                item = self.doudous[a][b]
                self.scene.removeItem(item)
                self.doudous[a][b] = DouDou(b, a, None)
                self.scene.addItem(self.doudous[a][b])
                self.doudous[a][b].setPos(b, a)

        if num_blank:
            for i in range(num_blank):
                a = random.randint(-1, self.douMapSize[0] - 1)
                b = random.randint(-1, self.douMapSize[1] - 1)
                while self.doudous[a][b].color == None:
                    a = random.randint(-1, self.douMapSize[0] - 1)
                    b = random.randint(-1, self.douMapSize[1] - 1)
                item = self.doudous[a][b]
                self.scene.removeItem(item)
                self.doudous[a][b] = None
                self.availableSpots.append((b, a))

        if num_balk:
            for i in range(num_blank):
                a = random.randint(-1, self.douMapSize[0] - 1)
                b = random.randint(-1, self.douMapSize[1] - 1)
                while not isinstance(self.doudous[a][b], DouDou) or self.doudous[a][b].color == None:
                    a = random.randint(-1, self.douMapSize[0] - 1)
                    b = random.randint(-1, self.douMapSize[1] - 1)
                item = self.doudous[a][b]
                self.scene.removeItem(item)
                self.doudous[a][b] = Balk(b, a)
                self.scene.addItem(self.doudous[a][b])
                self.doudous[a][b].setPos(b, a)
        num = 0
        for i in self.availableSpots:
            if self.checkCorrect((i[1], i[0])):
                num += 1
        #如果一开始太少可以点的地方就处理一下
        if num <= 3:
            pass
            
    #用于继续上次的游戏,文件io在外部实现
    def setDoudou(self, douList, range_, score):
        self.reset()
        self.range = range_
        self.score = score
        self.setDouSize(len(douList), len(douList[0]))
        for i in range(len(douList)):
            self.doudous.append([])
            for j in range(len(douList[0])):
                if douList[i][j]:
                    if douList[i][j] == BALK:
                        new_dou = Balk(j, i)
                    else:
                        new_dou = DouDou(j, i, douList[i][j])
                else:
                    new_dou = None
                    self.availableSpots.append((j, i))
                if new_dou:
                    self.scene.addItem(new_dou)
                    new_dou.setPos(j, i)
                self.doudous[i].append(new_dou)

    #检查是否该位置可以消除
    def checkCorrect(self, cord):
        i, j = cord
        while True:
            i += 1
            if i >= self.douMapSize[0]:
                break
            if isinstance(self.doudous[i][cord[1]], DouDou):
                while True:
                    j += 1
                    if j >= self.douMapSize[1]:
                        break
                    if not self.doudous[cord[0]][j]:
                        continue
                    elif isinstance(self.doudous[cord[0]][j], DouDou):
                         if self.doudous[i][cord[1]] == self.doudous[cord[0]][j]:
                             return True, ((i, cord[1]), (cord[0], j))
                         else:
                             break
                    else:
                        break
                while True:
                    j -= 1
                    if j < 0:
                        break
                    if not self.doudous[cord[0]][j]:
                        continue
                    elif isinstance(self.doudous[cord[0]][j], DouDou):
                         if self.doudous[i][cord[1]] == self.doudous[cord[0]][j]:
                             return True, ((i, cord[1]), (cord[0], j))
                         else:
                             break
                    else:
                        break
        while True:
            i -= 1
            if i < 0:
                break
            if isinstance(self.doudous[i][cord[1]], DouDou):
                while True:
                    j += 1
                    if j >= self.douMapSize[1]:
                        break
                    if not self.doudous[cord[0]][j]:
                        continue
                    elif isinstance(self.doudous[cord[0]][j], DouDou):
                         if self.doudous[i][cord[1]] == self.doudous[cord[0]][j]:
                             return True, ((i, cord[1]), (cord[0], j))
                         else:
                             break
                    else:
                        break
                while True:
                    j -= 1
                    if j < 0:
                        break
                    if not self.doudous[cord[0]][j]:
                        continue
                    elif isinstance(self.doudous[cord[0]][j], DouDou):
                         if self.doudous[i][cord[1]] == self.doudous[cord[0]][j]:
                             return True, ((i, cord[1]), (cord[0], j))
                         else:
                             break
                    else:
                        break
        return False, ()

    #mousepresseventhandler
    def mousePressEvent(self, event):
        print "moused"
        if not self.gameStarted:
            event.ignore()
            return
        self.TerminateAni()
        if event.button() != Qt.LeftButton:
            event.ignore()
            return
        print "yes, mouse press"
        items = self.items(event.pos())
        if not items:
            return
        item = items[0]
        if not (item.corX, item.corY) in self.availableSpots:
            #加入一个点击豆豆的框框
            return
        tmp = self.checkCorrect((item.corY, item.corX))
        print "check correct answer:", tmp[0], tmp[1]#for test
        if tmp[0]:
#            self.animation = 
            #用状态机来做动画还是在这里直接add动画？试试直接的吧，虽然觉得不太好
            self.toDisappear = tmp[1]
            self.animation, tmpItem = self.correctAnimation(tmp[1])
            self.tmpItem.extend(tmpItem)
            self.connect(self.animation, SIGNAL("finished()"), self.TerminateAni)
            self.animation.start()

    def itemsOfAnimation(self, two_dou):
        items = []
        start = min(two_dou[1][0],two_dou[0][0])
        end = max(two_dou[1][0], two_dou[0][0])
        for i in range(start + 1, end):
            new_ind = IndItem(two_dou[0][1], i)
            self.scene.addItem(new_ind)
            new_ind.setPos(new_ind.corX, new_ind.corY)
            new_ind.setOpacity(0)
            items.append(new_ind)
        start = min(two_dou[0][1],two_dou[1][1])
        end = max(two_dou[0][1], two_dou[1][1])
        for i in range(start + 1, end):
            new_ind = IndItem(j, two_dou[1][0])
            self.scene.addItem(new_ind)
            new_ind.setPos(new_ind.corX, new_ind.corY)
            new_ind.setOpacity(0)
            items.append(new_ind)
        new_ind = IndItem(two_dou[0][1], two_dou[1][0])
        self.scene.addItem(new_ind)
        new_ind.setPos(new_ind.corX, new_ind.corY)
        new_ind.setOpacity(0)
        items.append(new_ind)

        return items

    def correctAnimation(self, two_dou):
        ani_group = QParallelAnimationGroup()
        tmp = self.itemsOfAnimation(two_dou)
        for item in tmp:
            anim = QPropertyAnimation(item, "opacity")
            anim.setDuration(500)
            anim.setStartValue(0)
            anim.setKeyValueAt(0.1, 1)
            anim.setKeyValueAt(0.8, 1)
            anim.setEndValue(0)
            ani_group.addAnimation(anim)
        #这里要做一个猪猪被消除就睁开眼睛的动画，在item里加入parent-child关系
   #     anim = Q
        return ani_group, tmp

    def TerminateAni(self):
        sender = self.sender()
        if not self.animation:
            return
        if not isinstance(sender, QAbstractAnimation):
            self.animation.stop()
        self.animation.deleteLater()
        self.animation = None
        for item in self.tmpItem:
            self.scene.removeItem(item)
        self.tmpItem = []
        for tup in self.toDisappear:
            item = self.doudous[tup[0]][tup[1]]
            self.doudous[tup[0]][tup[1]] = None
            self.availableSpots.append((tup[1], tup[0]))
            self.scene.removeItem(item)
        self.toDisappear = []

    def mouseMoveEvent(self, event):
        pass
    #重新排列现有豆豆函数
    def refreshDou(self):
        self.TermianteAni()

    #重置数据，删除所有东东
    def reset(self):
        self.TerminateAni()
        self.score = 0
        self.range = 0
        self.score = 0
        self.availableSpots = []
        self.douMapSize = (12, 12)
        for item in self.doudous:
            self.scene.remove(item)
        self.doudous = []
        for item in self.douMap_list:
            self.scene.remove(item)
        self.douMap_list = []


# for test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    form = DouDouView(scene)
    form.setDouSize((12, 12))
    form.show()
    form.getNewRoundDou()
    form.gameStarted = True
    app.exec_()
