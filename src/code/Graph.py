# _*_coding:utf-8_*_
# author    :tldec_(tanlongs4w@gmail.com)
# date      :2019/12/7 16:52
import numpy as np


class Graph:
    def __init__(self, V, E, W):
        self.V = np.array(V)
        self.Edge = np.array(E)
        self.wEdge = np.array(W)
        self.dList = np.zeros(len(self.V), dtype=np.int32)
        self.degree = 0
        self.init()

    def updateDegree(self):
        self.degree = np.max(self.dList)

    def updateDList(self):
        for v in range(len(self.V)):
            self.dList[v] = np.sum(self.Edge[v, :])

    def init(self):
        self.updateDList()
        self.updateDegree()

    def removeNode(self, n):
        # print("删除邻居:",n)
        self.V[n] = 0
        self.Edge[n, :] = np.zeros(self.Edge.shape[1])
        self.Edge[:, n] = np.zeros(self.Edge.shape[0])
        self.wEdge = self.V * self.wEdge

    def coloring(self, n):
        # print("删除结点",n)
        tmpV = self.V.copy()
        tmpE = self.Edge.copy()
        for i in range(len(tmpV)):
            # print("Edge[n][i]:",tmpE[n][i])
            if tmpE[n][i] == 1:
                self.removeNode(i)
        self.updateDList()
        self.updateDegree()
